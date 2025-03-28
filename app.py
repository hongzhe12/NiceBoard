import ctypes
import sys
import keyboard
from threading import Thread
from PySide6.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon, QMenu, QStyle
from PySide6.QtCore import QObject, Signal, QPoint, Qt, QTimer
from PySide6.QtGui import QCursor, QPainterPath, QRegion, QIcon
from models import ClipboardItem, Session
from ui_clipboard_history import Ui_SimpleClipboardHistory  # 编译后的UI
import rc_resources

def make_window_immersive(hwnd):
    """通过 WinAPI 设置为系统级面板样式"""
    GWL_EXSTYLE = -20
    WS_EX_TOOLWINDOW = 0x00000080
    WS_EX_NOACTIVATE = 0x08000000

    old_style = ctypes.windll.user32.GetWindowLongA(hwnd, GWL_EXSTYLE)
    new_style = old_style | WS_EX_TOOLWINDOW | WS_EX_NOACTIVATE
    ctypes.windll.user32.SetWindowLongA(hwnd, GWL_EXSTYLE, new_style)

class HotkeyManager(QObject):
    """全局热键管理"""
    hotkey_pressed = Signal()

    def __init__(self):
        super().__init__()
        self._running = False

    def start_listen(self, hotkey='ctrl+shift+v'):
        if self._running:
            self.stop_listen()
        self._running = True
        Thread(target=self._listen_hotkey, args=(hotkey,), daemon=True).start()

    def stop_listen(self):
        self._running = False
        keyboard.unhook_all()

    def _listen_hotkey(self, hotkey):
        while self._running:
            keyboard.wait(hotkey)
            if self._running:
                self.hotkey_pressed.emit()


class ClipboardHistoryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_SimpleClipboardHistory()
        self.ui.setupUi(self)

        # 初始化设置
        self.setWindowTitle("剪贴板历史记录")
        # self.setFixedSize(400, 500)

        # 信号连接
        # self.ui.toggle_btn.clicked.connect(self.hide)
        self.ui.history_list.itemDoubleClicked.connect(self._copy_to_clipboard)

        # 初始化剪贴板监控
        self.clipboard = QApplication.clipboard()
        self.clipboard.dataChanged.connect(self._on_clipboard_change)



        # 热键设置
        self.hotkey_manager = HotkeyManager()
        self.hotkey_manager.hotkey_pressed.connect(self.toggle_window)
        self.hotkey_manager.start_listen()

        # 加载历史记录
        self._load_history()

        # 关键设置：无边框 + 背景透明
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # 设置圆角遮罩
        self.setMaskCornerRadius(12)  # 圆角值需与QSS一致

        # 显示启动通知（不需要常驻托盘图标）
        self.show_startup_notification()

        # 连接搜索框信号
        self.ui.search_box.textChanged.connect(self.filter_history)
        # 拖动相关变量
        self.drag_pos = None

    def show_startup_notification(self):
        """增强版通知方法"""
        if not QSystemTrayIcon.isSystemTrayAvailable():
            print("系统不支持托盘通知")  # 调试用
            return

        tray = QSystemTrayIcon(self)

        # 强制设置可见图标（Windows 11 需要）
        tray.setIcon(QIcon(":/icons/clipboard.svg") if hasattr(self, 'clipboard.svg')
                     else self.style().standardIcon(QStyle.SP_ComputerIcon))

        # 必须调用show()才能发送通知
        tray.show()

        tray.showMessage(
            "剪贴板历史已启动",
            "按 Ctrl+Shift+V 唤出面板",
            QSystemTrayIcon.Information,
            3000
        )

        # 延迟销毁确保通知能弹出
        QTimer.singleShot(4000, tray.deleteLater)

    def mousePressEvent(self, event):
        """鼠标按下时记录位置"""
        if event.button() == Qt.LeftButton:
            # self.drag_pos = event.globalPos()
            # 新版写法
            self.drag_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        """鼠标移动时拖动窗口"""
        if self.drag_pos and event.buttons() & Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.drag_pos)
            # self.drag_pos = event.globalPos()

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
        """根据搜索文本过滤列表"""
        session = Session()
        try:
            self.ui.history_list.clear()
            items = session.query(ClipboardItem) \
                .filter(ClipboardItem.content.contains(text)) \
                .order_by(ClipboardItem.timestamp.desc()) \
                .limit(50) \
                .all()
            for item in items:
                self.ui.history_list.addItem(item.content)
        finally:
            session.close()

    def setMaskCornerRadius(self, radius):
        """ 创建圆角遮罩 """
        path = QPainterPath()
        path.addRoundedRect(self.rect(), radius, radius)
        region = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(region)

    def resizeEvent(self, event):
        """ 窗口大小改变时更新遮罩 """
        self.setMaskCornerRadius(12)
        super().resizeEvent(event)

    def _load_history(self, limit=50):
        """从数据库加载历史记录"""
        self.ui.history_list.clear()
        session = Session()
        try:
            items = session.query(ClipboardItem) \
                .order_by(ClipboardItem.timestamp.desc()) \
                .limit(limit) \
                .all()
            for item in items:
                self.ui.history_list.addItem(item.content)
        finally:
            session.close()

    def _on_clipboard_change(self):
        """剪贴板内容变化时的处理"""
        mime_data = self.clipboard.mimeData()
        if not mime_data.hasText():
            return

        text = mime_data.text().strip()
        if not text:
            return

        session = Session()
        try:
            # 检查是否已存在相同内容
            exists = session.query(ClipboardItem) \
                .filter(ClipboardItem.content == text) \
                .first()
            if not exists:
                # 插入新记录
                new_item = ClipboardItem(content=text)
                session.add(new_item)
                session.commit()
                # 更新UI
                self.ui.history_list.insertItem(0, text)
                # 限制显示数量
                if self.ui.history_list.count() > 50:
                    self.ui.history_list.takeItem(50)
        except Exception as e:
            session.rollback()
            print(f"数据库错误: {e}")
        finally:
            session.close()

    def _copy_to_clipboard(self, item):
        """双击项目复制到剪贴板"""
        self.clipboard.setText(item.text())
        self.hide()

    def toggle_window(self):
        """切换窗口显示状态"""
        if self.isVisible():
            self.hide()
        else:
            self._show_at_cursor()

    # def _show_at_cursor(self):
    #     """在鼠标位置显示窗口"""
    #     cursor_pos = QCursor.pos()
    #     screen = QApplication.primaryScreen().availableGeometry()
    #
    #     # 计算窗口位置（防止超出屏幕）
    #     x = min(max(cursor_pos.x(), screen.left()),
    #             screen.right() - self.width())
    #     y = min(max(cursor_pos.y(), screen.top()),
    #             screen.bottom() - self.height())
    #
    #     self.move(QPoint(x, y))
    #     self.show()
    #     make_window_immersive(int(self.winId()))  # 传入窗口句柄
    #     self.activateWindow()
    #     self.raise_()

    def _show_at_cursor(self):
        # 设置为无边框工具窗口
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint |
            Qt.Tool |
            Qt.FramelessWindowHint
        )

        # 计算位置（多屏幕安全）
        cursor_pos = QCursor.pos()
        screen = QApplication.screenAt(cursor_pos).availableGeometry()
        x = min(max(cursor_pos.x(), screen.x()), screen.right() - self.width())
        y = min(max(cursor_pos.y(), screen.y()), screen.bottom() - self.height())

        self.move(int(x), int(y))
        self.show()

        # 确保焦点（但不抢输入焦点）
        self.raise_()
        self.setAttribute(Qt.WA_ShowWithoutActivating, True)

    def closeEvent(self, event):
        """关闭时清理资源"""
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

    window = ClipboardHistoryApp()
    sys.exit(app.exec())