
import os
import socket
import sys

from PySide6.QtCore import Qt, QEvent, QUrl
from PySide6.QtGui import QCursor, QPainterPath, QRegion, QIcon, QColor, QDesktopServices
from PySide6.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon, QMenu, QStyle, QMessageBox, QListWidgetItem, \
    QDialog

from log.log import log_file
from utils.config_set import config_instance
from utils.hotkey_manager import HotkeyManager
from utils.input_form_dialog import InputFormDialog
from src.models import auto_clean_history
from src.models import get_clipboard_history, add_clipboard_item, delete_clipboard_item, clear_all_clipboard_history, \
    filter_clipboard_history, update_tags_for_clipboard_item, find_tags_by_content

from src.settings_window import SettingsWindow
from ui.ui_clipboard_history import Ui_SimpleClipboardHistory  # 编译后的UI
from resources import resources_rc # 加载资源文件
# 获取当前用户的应用数据目录
from utils.log_display import LogDisplayWindow
from log.log import logging as _log

from PySide6.QtCore import QThread, Signal

from backen.backend import socketio
from backen.backend import app as flask_app
from PySide6.QtCore import QTimer, QRunnable, QThreadPool, QObject



degree = 10


# 搜索工作线程类
class SearchWorker(QRunnable):
    class Signals(QObject):
        result = Signal(list)

    def __init__(self, search_text):
        super().__init__()
        self.signals = self.Signals()
        self.search_text = search_text

    def run(self):
        try:
            results = filter_clipboard_history(self.search_text, use_regex=True, limit=20)
            self.signals.result.emit(results)
        except Exception as e:
            _log.error(f"搜索出错: {e}")
            self.signals.result.emit([])


class BackendThread(QThread):
    # 信号用于通知主线程后台任务已启动
    started_signal = Signal()

    def run(self):
        try:
            # 发出信号，表示后台任务已启动
            self.started_signal.emit()
            socketio.run(
                flask_app,
                host='0.0.0.0',
                port=5000,
                allow_unsafe_werkzeug=True,
                debug=False  # 生产环境关闭调试
            )
        except Exception as e:
            _log.error(f"后端启动失败: {e}")


class ClipboardHistoryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_SimpleClipboardHistory()
        self.ui.setupUi(self)

        self.settings_window = None  # 添加设置窗口引用
        self.tray_icon = None  # 托盘图标
        # 初始化设置
        # self.setWindowTitle("剪贴板历史记录")

        # 双击复制到粘贴板
        self.ui.history_list.itemDoubleClicked.connect(self._copy_to_clipboard)

        # 初始化剪贴板监控
        self.clipboard = QApplication.clipboard()
        self.clipboard.dataChanged.connect(self._on_clipboard_change)

        # 使用配置实例获取设置
        hotkey = config_instance.get('hotkey', 'f9')
        self.__hotkey = hotkey

        # 转换小写
        hotkey = '+'.join([k.strip().lower() for k in hotkey.split('+')])
        # 预处理
        hotkey = hotkey.replace('alt', '<alt>')
        hotkey = hotkey.replace('ctrl', '<ctrl>')

        # 热键设置
        self.hotkey_manager = HotkeyManager()
        self.hotkey_manager.hotkey_pressed.connect(self.toggle_window)
        self.hotkey_manager.esc_pressed.connect(self.hide)
        self.hotkey_manager.start_listen(hotkey=hotkey)

        # 加载历史记录
        self._load_history()

        # 设置圆角遮罩
        self.setMaskCornerRadius(degree)  # 圆角值需与QSS一致

        # 连接搜索框信号
        self.ui.search_box.textChanged.connect(self.filter_history)
        # 拖动相关变量
        self.drag_pos = None

        # 新增删除功能配置
        self.setup_delete_functionality()

        # 添加系统托盘图标
        self.setup_system_tray()

        # 显示启动通知（不需要常驻托盘图标）
        self.show_startup_notification()

        # 后台线程
        self.backend_thread = None

        # 搜索防抖优化（新增这部分）
        self._search_timer = QTimer()
        self._search_timer.setSingleShot(True)
        self._search_timer.setInterval(500)  # 设置300ms防抖间隔
        self._search_timer.timeout.connect(self._perform_search)
        # 线程池优化（修改这部分）
        self._thread_pool = QThreadPool()
        self._thread_pool.setMaxThreadCount(1)  # 限制同时只有一个搜索线程
        self._current_search_text = ""

        # 日志窗口
        self.log_window = None

    def setup_system_tray(self):
        """创建系统托盘图标"""
        self.tray_icon = QSystemTrayIcon(self)

        self.tray_icon.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogContentsView))
        self.tray_icon.setIcon(QIcon(":/icons/clipboard.svg"))
        self.tray_icon.setToolTip("好贴板 plus")
        tray_menu = QMenu()

        # 添加新菜单项
        settings_action = tray_menu.addAction("设置")
        settings_action.triggered.connect(self.show_settings)
        tray_menu.addSeparator()

        # 原有菜单项
        show_action = tray_menu.addAction("显示主窗口")
        show_action.triggered.connect(self.show_normal)

        history_action = tray_menu.addAction("查看剪贴板历史")
        history_action.triggered.connect(self.toggle_window)

        backend_action = tray_menu.addAction("打开后台管理")
        # 连接打开浏览器的信号槽
        backend_action.triggered.connect(self.open_website)

        logs_action = tray_menu.addAction("查看日志")
        # 连接打开浏览器的信号槽
        logs_action.triggered.connect(self.open_log_file)

        tray_menu.addSeparator()
        quit_action = tray_menu.addAction("退出")
        quit_action.triggered.connect(self.quit_application)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.on_tray_activated)
        self.tray_icon.show()

    def open_log_file(self):
        """打开日志文件"""
        try:
            with open(log_file, 'r', encoding='utf-8') as file:
                log_content = file.read()
            # 创建并显示日志显示窗口
            self.log_window = LogDisplayWindow(log_content)
            self.log_window.show()

        except Exception as e:
            error_message = f"无法打开日志文件: {e}"
            self.log_window = LogDisplayWindow(error_message)
            self.log_window.show()

    def open_website(self):
        if self.backend_thread is None or not self.backend_thread.isRunning():
            # 创建并启动后台线程
            self.backend_thread = BackendThread()
            self.backend_thread.start()

        # 获取本机的IPv4地址
        hostname = socket.gethostname()
        ipv4_address = socket.gethostbyname(hostname)

        # 指定要打开的网站 URL
        url = QUrl(f'http://{ipv4_address}:5000')
        # 使用 QDesktopServices 打开浏览器
        QDesktopServices.openUrl(url)

    def on_tray_activated(self, reason):
        """处理托盘图标点击事件（更健壮版）"""
        if reason == QSystemTrayIcon.Trigger:  # 左键单击
            settings_window = getattr(self, 'settings_window', None)  # 安全获取属性
            if settings_window is not None and settings_window.isVisible():
                settings_window.hide()  # 隐藏窗口
            else:
                self.show_settings()  # 显示或创建窗口
                if self.settings_window and self.settings_window.isVisible():
                    self.settings_window.raise_()  # 确保窗口前置
                    self.settings_window.activateWindow()  # 激活窗口

    def show_settings(self):
        """100%能显示的设置窗口方法"""
        # 如果窗口存在但隐藏了
        if self.settings_window and self.settings_window.isHidden():
            self.settings_window.showNormal()
            return

        # 全新创建窗口
        self.settings_window = SettingsWindow()  # 不设置parent

        # 关键设置（必须）
        self.settings_window.setAttribute(Qt.WA_DeleteOnClose)
        self.settings_window.setWindowModality(Qt.ApplicationModal)

        # 窗口位置计算
        screen_geo = QApplication.primaryScreen().availableGeometry()
        x = (screen_geo.width() - self.settings_window.width()) // 2
        y = (screen_geo.height() - self.settings_window.height()) // 2

        # 显示窗口（三步缺一不可）
        self.settings_window.move(x, y)
        self.settings_window.show()
        self.settings_window.activateWindow()

        # 绑定关闭事件
        self.settings_window.destroyed.connect(lambda: setattr(self, 'settings_window', None))

    def show_normal(self):
        """正常显示窗口"""
        self.show()
        self.activateWindow()
        self.setWindowState(self.windowState() & ~Qt.WindowMinimized)

    def quit_application(self):
        """安全退出应用"""
        self.tray_icon.hide()  # 先隐藏托盘图标
        QApplication.quit()

    def setup_delete_functionality(self):
        """初始化删除相关功能"""
        # 右键菜单
        self.ui.history_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.history_list.customContextMenuRequested.connect(self.show_context_menu)

        # 键盘支持
        self.ui.history_list.installEventFilter(self)

        # 删除按钮信号（如果UI中有）
        if hasattr(self.ui, 'btn_delete'):
            self.ui.btn_delete.clicked.connect(self.delete_selected_item)

    def eventFilter(self, source, event):
        """监听键盘事件"""
        if (event.type() == QEvent.KeyPress and
                source is self.ui.history_list and
                event.key() == Qt.Key_Delete):
            self.delete_selected_item()
            return True
        return super().eventFilter(source, event)

    def show_context_menu(self, pos):
        """智能右键菜单"""

        current_text = self.ui.history_list.itemAt(pos).text()
        menu = QMenu()
        actions = {
            "设置标签": lambda: self.set_label(current_text),
            "复制内容": lambda: self.clipboard.setText(current_text),
            "删除": self.delete_selected_item,
            "清空历史": self.clear_all_history

        }

        for text, callback in actions.items():
            action = menu.addAction(text)
            action.triggered.connect(callback)

        menu.exec(self.ui.history_list.mapToGlobal(pos))

    # 设置标签方法
    def set_label(self, text):
        """设置标签"""

        tag = find_tags_by_content(text)
        # 自定义数据结构，用于描述表单字段，添加了默认值
        form_structure = [
            {"label": f"为【{text[:10] + '...' if len(text) > 10 else text}】设置标签", "type": "text", "default": tag}
        ]

        dialog = InputFormDialog(form_structure, self)
        if dialog.exec() == QDialog.Accepted:
            values = dialog.get_input_values()
            label = values[0]
            update_tags_for_clipboard_item(text, label)

    def delete_selected_item(self):
        """安全删除当前选中项"""
        selected = self.ui.history_list.currentItem()
        if selected:
            if delete_clipboard_item(selected.text()):
                self._remove_from_list(selected.text())

    def clear_all_history(self):
        """批量删除确认"""
        if self.confirm_delete("确定清空所有剪贴板历史吗？", dangerous=True):
            if clear_all_clipboard_history():
                self.ui.history_list.clear()

    def _remove_from_list(self, content):
        """同步更新UI列表"""
        for i in range(self.ui.history_list.count()):
            if self.ui.history_list.item(i).text() == content:
                self.ui.history_list.takeItem(i)
                break

    # 以下为工具方法
    def confirm_delete(self, message, dangerous=False):
        """通用确认对话框"""
        box = QMessageBox(self)
        box.setWindowTitle("确认操作")
        box.setIcon(QMessageBox.Warning if dangerous else QMessageBox.Question)
        box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        box.setText(message)
        return box.exec() == QMessageBox.Yes

    def show_error(self, title, message):
        """错误提示"""
        QMessageBox.critical(self, title, message)

    def show_startup_notification(self):
        """增强版通知方法"""
        if not QSystemTrayIcon.isSystemTrayAvailable():
            print("系统不支持托盘通知")  # 调试用
            return

        # 必须调用show()才能发送通知
        self.tray_icon.show()

        self.tray_icon.showMessage(
            "好贴板已启动",
            f"按 {str(self.__hotkey)} 唤出面板",
            QSystemTrayIcon.Information,
            1000
        )

    def mousePressEvent(self, event):
        """鼠标按下时记录位置"""
        if event.button() == Qt.LeftButton:
            # self.drag_pos = event.globalPos()
            # 新版写法
            self.drag_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        """鼠标移动时拖动窗口"""
        if self.drag_pos and event.buttons() & Qt.LeftButton:
            # 获取当前全局坐标（兼容写法）
            current_pos = event.globalPosition().toPoint()
            self.move(self.pos() + current_pos - self.drag_pos)
            self.drag_pos = current_pos

    def mouseReleaseEvent(self, event):
        """鼠标释放时清空位置"""
        self.drag_pos = None

    def filter_history(self, text):
        """优化后的搜索方法（单点防抖优化版）"""
        # 停止之前的计时器（关键防抖步骤）
        # self._search_timer.stop()

        # 如果是空搜索，立即显示全部（不需要防抖）
        if not text.strip():
            # 启动防抖计时器（500ms后执行实际搜索）
            self._search_timer.start()
            self._load_history()
            return

        # 显示加载状态
        self.ui.history_list.clear()
        loading_item = QListWidgetItem("搜索中...")
        loading_item.setForeground(QColor(150, 150, 150))  # 灰色文字提示
        self.ui.history_list.addItem(loading_item)

        # 启动防抖计时器（500ms后执行实际搜索）
        self._search_timer.start()

    def _perform_search(self):
        """实际执行搜索的方法"""
        text = self.ui.search_box.text().strip()

        # 创建搜索工作线程
        worker = SearchWorker(text)
        worker.signals.result.connect(self._update_search_results)
        self._thread_pool.start(worker)

    def _update_search_results(self, items):
        # 再次检查搜索文本是否匹配
        if not hasattr(self, '_current_search_text'):
            return

        self.ui.history_list.clear()

        if not items:
            self.ui.history_list.addItem("无搜索结果")
            return

        for item in items:
            list_item = QListWidgetItem(item.content)
            if item.tags:
                list_item.setToolTip(f"标签：{item.tags}")
            elif len(item.content) < 500:
                list_item.setToolTip(item.content)
            else:
                list_item.setToolTip("内容过长，无法显示")
            self.ui.history_list.addItem(list_item)

    def setMaskCornerRadius(self, radius):
        """ 创建圆角遮罩 """
        path = QPainterPath()
        path.addRoundedRect(self.rect(), radius, radius)
        region = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(region)

    def resizeEvent(self, event):
        """ 窗口大小改变时更新遮罩 """
        self.setMaskCornerRadius(degree)
        super().resizeEvent(event)

    def _load_history(self, limit=50):
        """从数据库加载历史记录"""
        if limit is None:
            # 从配置中获取最大历史记录数
            limit = config_instance.get('max_history', 10)

        self.ui.history_list.clear()
        items = get_clipboard_history(limit)
        self._update_search_results(items)  # 重用相同的更新逻辑

    def _on_clipboard_change(self):
        """剪贴板内容变化时的处理"""
        mime_data = self.clipboard.mimeData()
        if not mime_data.hasText():
            return

        text = mime_data.text().strip()
        if not text:
            return

        if add_clipboard_item(text):
            # 更新UI
            self.ui.history_list.insertItem(0, text)
            # 限制显示数量
            if self.ui.history_list.count() > 50:
                self.ui.history_list.takeItem(50)

    def _copy_to_clipboard(self, item):
        """双击项目：复制到剪贴板 + 自动粘贴到当前输入框 (Windows)"""
        try:
            # 1. 复制选中内容到剪贴板
            selected_text = item.text()
            self.clipboard.setText(selected_text)

            # 2. 自动清理历史记录
            auto_clean_history()

            # 3. 隐藏窗口（先隐藏再粘贴，避免干扰）
            self.hide()

            # 4. 确保剪贴板内容已更新（短暂延迟）
            QTimer.singleShot(100, lambda: self._paste_to_active_window(selected_text))

        except Exception as e:
            _log.error(f"复制粘贴失败: {e}")

    def _paste_to_active_window(self, text):
        """实际执行粘贴操作的辅助方法"""
        try:
            import keyboard
            # 保存当前剪贴板内容（备用恢复）
            original_clipboard = self.clipboard.text()

            # 设置要粘贴的文本
            self.clipboard.setText(text)

            # 模拟Ctrl+V（包含按下和释放两个动作）
            keyboard.press('ctrl')
            keyboard.press_and_release('v')
            keyboard.release('ctrl')

            # 短暂延迟后恢复原剪贴板内容（可选）
            QTimer.singleShot(200, lambda: self.clipboard.setText(original_clipboard))

        except Exception as e:
            _log.error(f"自动粘贴失败: {e}")
            # 如果失败，至少确保文本已在剪贴板中
            self.clipboard.setText(text)

    def _refresh_history_list(self):
        """刷新历史记录列表显示"""
        # 清空当前列表
        self.ui.history_list.clear()

        # 从数据库重新加载记录
        items = get_clipboard_history()
        for item in items:
            list_item = QListWidgetItem(item.content)
            self.ui.history_list.addItem(list_item)

    def toggle_window(self):
        """切换窗口显示状态"""
        _log.info(f"toggle_window 方法被调用")
        if self.isVisible():
            self.hide()
        else:
            self._show_at_cursor()

    def _show_at_cursor(self):
        _log.info(f" _show_at_cursor 方法被调用")
        # 设置窗口属性
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )

        # 计算位置（多屏幕安全）
        cursor_pos = QCursor.pos()
        screen = QApplication.screenAt(cursor_pos).availableGeometry()
        x = min(max(cursor_pos.x(), screen.x()), screen.right() - self.width())
        y = min(max(cursor_pos.y(), screen.y()), screen.bottom() - self.height())

        _log.info(f" 窗口将移动到位置: ({x}, {y})")
        self.move(int(x), int(y))
        self.show()

        # 确保焦点（但不抢输入焦点）
        self.raise_()
        self.setAttribute(Qt.WA_ShowWithoutActivating, True)

    def closeEvent(self, event):
        """重写关闭事件（点击X时最小化到托盘）"""
        if self.settings_window:
            self.settings_window.close()

        if self.tray_icon.isVisible():
            self.hide()
            event.ignore()
        else:
            self.hotkey_manager.stop_listen()
            super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 全局样式
    app.setStyleSheet("""
        QListWidget {
            font-size: 12px;
            padding: 5px;
        }
        QPushButton {
            padding: 8px;
        }
    """)
    app.setApplicationName("好贴板")  # 设置应用程序名称

    window = ClipboardHistoryApp()
    sys.exit(app.exec())
