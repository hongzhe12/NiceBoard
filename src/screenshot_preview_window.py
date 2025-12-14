import os
import sys
from datetime import datetime

from PySide6 import QtCore
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import (QPixmap, QIcon, QAction, QPainter, QColor,
                           QBrush, QFont)
from PySide6.QtWidgets import (QApplication, QMainWindow, QSystemTrayIcon,
                               QMenu, QLabel, QVBoxLayout, QWidget, QPushButton,
                               QHBoxLayout, QFileDialog, QMessageBox)

from utils.hotkey_manager import HotkeyManager
from utils.screen_hot import Screenshot


class ScreenshotPreviewWindow(QWidget):
    """截图预览窗口，可以置顶显示"""

    closed = Signal()

    def __init__(self, pixmap, parent=None):
        super().__init__(parent)
        self.pixmap = pixmap
        self.init_ui()
        self.setup_window_properties()

    def init_ui(self):
        """初始化UI"""
        self.setMinimumSize(400, 300)

        # 主布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # 图片标签
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("border: 1px solid #ccc;")
        layout.addWidget(self.image_label, 1)

        # 按钮布局
        button_layout = QHBoxLayout()

        # 保存按钮
        self.save_btn = QPushButton("保存")
        self.save_btn.clicked.connect(self.save_screenshot)
        self.save_btn.setMinimumWidth(80)
        button_layout.addWidget(self.save_btn)

        # 复制按钮
        self.copy_btn = QPushButton("复制到剪贴板")
        self.copy_btn.clicked.connect(self.copy_to_clipboard)
        self.copy_btn.setMinimumWidth(120)
        button_layout.addWidget(self.copy_btn)

        # 重新截图按钮
        self.retake_btn = QPushButton("重新截图")
        self.retake_btn.clicked.connect(self.retake_screenshot)
        self.retake_btn.setMinimumWidth(100)
        button_layout.addWidget(self.retake_btn)

        # 置顶按钮
        self.pin_btn = QPushButton("取消置顶")
        self.pin_btn.clicked.connect(self.toggle_topmost)
        self.pin_btn.setMinimumWidth(80)
        button_layout.addWidget(self.pin_btn)

        # 关闭按钮
        self.close_btn = QPushButton("关闭")
        self.close_btn.clicked.connect(self.close)
        self.close_btn.setMinimumWidth(80)
        button_layout.addWidget(self.close_btn)

        layout.addLayout(button_layout)

        # 显示图片
        self.update_preview()

    def setup_window_properties(self):
        """设置窗口属性"""
        self.setWindowTitle("截图预览")
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_DeleteOnClose)

        # 根据图片大小调整窗口大小
        if not self.pixmap.isNull():
            img_size = self.pixmap.size()
            # 确保窗口不会太大
            max_width = QApplication.primaryScreen().size().width() * 0.8
            max_height = QApplication.primaryScreen().size().height() * 0.8

            width = min(img_size.width() + 40, max_width)
            height = min(img_size.height() + 100, max_height)
            self.resize(int(width), int(height))

        # 居中显示
        screen_geometry = QApplication.primaryScreen().geometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)

    def update_preview(self):
        """更新预览图片"""
        if not self.pixmap.isNull():
            # 调整图片大小以适应标签
            label_size = self.image_label.size()
            if label_size.width() > 0 and label_size.height() > 0:
                scaled_pixmap = self.pixmap.scaled(
                    label_size,
                    QtCore.Qt.KeepAspectRatio,
                    QtCore.Qt.SmoothTransformation
                )
                self.image_label.setPixmap(scaled_pixmap)
                # 注意：这里移除了 toggle_topmost() 的调用
                # self.toggle_topmost()  # 移除这行

    def resizeEvent(self, event):
        """窗口大小改变事件"""
        super().resizeEvent(event)
        self.update_preview()

    def is_window_topmost(self):
        """检查窗口是否置顶"""
        return bool(self.windowFlags() & Qt.WindowStaysOnTopHint)

    def toggle_topmost(self):
        """切换置顶状态"""
        # 移除递归调用，使用一个标志来避免重复调用
        if self.is_window_topmost():
            # 取消置顶
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
            self.pin_btn.setText("置顶")
            # self.is_top = False
        else:
            # 设置为置顶
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
            self.pin_btn.setText("取消置顶")
            # self.is_top = True

        # 使用 QTimer 延迟显示窗口，避免立即触发 resizeEvent
        QtCore.QTimer.singleShot(10, self.show)

    def save_screenshot(self):
        """保存截图到文件"""
        if self.pixmap.isNull():
            QMessageBox.warning(self, "警告", "没有可保存的图片")
            return

        # 生成默认文件名
        default_dir = os.path.expanduser("~/Pictures")
        if not os.path.exists(default_dir):
            default_dir = os.path.expanduser("~/Desktop")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_name = f"screenshot_{timestamp}.png"
        default_path = os.path.join(default_dir, default_name)

        # 打开文件对话框
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "保存截图",
            default_path,
            "图片文件 (*.png *.jpg *.bmp);;所有文件 (*.*)"
        )

        if file_path:
            if self.pixmap.save(file_path):
                QMessageBox.information(self, "保存成功", f"截图已保存到:\n{file_path}")
            else:
                QMessageBox.warning(self, "保存失败", "保存截图失败")

    def copy_to_clipboard(self):
        """复制图片到剪贴板"""
        if not self.pixmap.isNull():
            clipboard = QApplication.clipboard()
            clipboard.setPixmap(self.pixmap)
            # QMessageBox.information(self, "复制成功", "截图已复制到剪贴板")
        else:
            QMessageBox.warning(self, "警告", "没有可复制的图片")

    def retake_screenshot(self):
        """重新截图"""
        self.close()
        if self.parent():
            self.parent().start_screenshot()

    def closeEvent(self, event):
        """关闭事件"""
        self.closed.emit()
        super().closeEvent(event)


class MyMainWindow(QMainWindow):
    def __init__(self, start_hidden=True):
        super().__init__()

        self.start_hidden = start_hidden  # 控制启动时是否隐藏窗口

        # 创建基本UI元素
        self.setWindowTitle("截图工具")
        self.setGeometry(100, 100, 800, 600)

        # 设置窗口图标
        self.setWindowIcon(self.create_default_icon())

        # 添加一个标签用于显示截图预览
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.image_label = QLabel("截图预览区域")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(400, 300)
        self.image_label.setStyleSheet("border: 1px solid #ccc; background-color: #f0f0f0;")
        layout.addWidget(self.image_label)

        # 截图类实例对象
        self.screenshot_window = None

        # 预览窗口引用
        self.preview_window = None

        # 创建系统托盘
        self.create_system_tray()

        # 创建全局热键管理器
        self.hotkey_manager = HotkeyManager()
        self.hotkey_manager.hotkey_pressed.connect(self.start_screenshot)
        self.hotkey_manager.esc_pressed.connect(self.handle_esc_key)
        self.hotkey_manager.start_listen(hotkey='f1')  # 启动全局热键监听

        # 根据参数决定是否显示窗口
        if self.start_hidden:
            # 启动时隐藏窗口
            self.hide()
        else:
            self.show()

    def create_default_icon(self):
        """创建默认图标"""
        icon_pixmap = QPixmap(64, 64)
        icon_pixmap.fill(Qt.transparent)
        painter = QPainter(icon_pixmap)
        painter.setBrush(QBrush(QColor(66, 133, 244)))
        painter.drawRect(0, 0, 64, 64)
        painter.setPen(QColor(255, 255, 255))
        painter.setFont(QFont("Arial", 24))
        painter.drawText(icon_pixmap.rect(), Qt.AlignCenter, "st")
        painter.end()
        return QIcon(icon_pixmap)

    def create_system_tray(self):
        """创建系统托盘"""
        # 创建托盘图标
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.windowIcon())

        # 创建托盘菜单
        tray_menu = QMenu()

        # 显示/隐藏主窗口
        self.toggle_window_action = QAction("显示主窗口", self)
        self.toggle_window_action.triggered.connect(self.toggle_window)
        tray_menu.addAction(self.toggle_window_action)

        # 开始截图
        screenshot_action = QAction("开始截图", self)
        screenshot_action.triggered.connect(self.start_screenshot)
        tray_menu.addAction(screenshot_action)

        # 分隔线
        tray_menu.addSeparator()

        # 退出程序
        quit_action = QAction("退出", self)
        quit_action.triggered.connect(self.quit_application)
        tray_menu.addAction(quit_action)

        # 设置托盘菜单
        self.tray_icon.setContextMenu(tray_menu)

        # 托盘图标点击事件
        self.tray_icon.activated.connect(self.tray_icon_activated)

        # 显示托盘图标
        self.tray_icon.show()

        # 如果启动时隐藏窗口，显示托盘提示
        if self.start_hidden:
            self.tray_icon.showMessage(
                "截图工具",
                "程序已启动并运行在系统托盘中",
                QSystemTrayIcon.Information,
                3000
            )

    def tray_icon_activated(self, reason):
        """托盘图标激活事件"""
        if reason == QSystemTrayIcon.Trigger:  # 左键单击
            self.toggle_window()
        elif reason == QSystemTrayIcon.DoubleClick:  # 双击
            self.toggle_window()

    def toggle_window(self):
        """切换窗口显示/隐藏状态"""
        if self.isVisible():
            self.hide_window()
        else:
            self.show_window()

    def show_window(self):
        """显示主窗口"""
        self.show()
        self.activateWindow()
        self.raise_()
        self.toggle_window_action.setText("隐藏主窗口")

    def hide_window(self):
        """隐藏主窗口到托盘"""
        self.hide()
        self.toggle_window_action.setText("显示主窗口")

    def start_screenshot(self):
        """开始截图"""
        print("开始截图...")

        # 如果已有预览窗口，先关闭
        if self.preview_window:
            self.preview_window.close()
            self.preview_window = None

        # 确保主窗口不是全屏或最大化状态，避免干扰截图
        if self.isVisible():
            self.hide()

        # 创建新的截图窗口实例
        self.screenshot_window = Screenshot()
        self.screenshot_window.completed.connect(self.handle_screenshot_completed)
        self.screenshot_window.showFullScreen()

        # 确保截图窗口获得焦点
        self.screenshot_window.raise_()
        self.screenshot_window.activateWindow()

    def handle_screenshot_completed(self, pixmap):
        """处理截图完成事件"""
        print("截图完成，显示预览...")

        # 关闭截图窗口
        if self.screenshot_window:
            self.screenshot_window.close()
            self.screenshot_window = None

        # 如果图片为空（用户取消了截图），不显示预览
        if pixmap.isNull():
            print("用户取消了截图")
            return

        # 创建并显示预览窗口
        self.show_preview_window(pixmap)

        # 如果主窗口是隐藏的，可以选择是否显示主窗口
        # 这里我们保持主窗口状态不变，只显示预览窗口

    def show_preview_window(self, pixmap):
        """显示预览窗口"""
        # 如果已有预览窗口，先关闭
        if self.preview_window:
            self.preview_window.close()

        # 创建新的预览窗口
        self.preview_window = ScreenshotPreviewWindow(pixmap, self)
        self.preview_window.closed.connect(self.on_preview_closed)
        self.preview_window.show()

    def on_preview_closed(self):
        """预览窗口关闭时的处理"""
        self.preview_window = None

    def update_preview(self, pixmap):
        """更新预览图片"""
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(
                self.image_label.size(),
                QtCore.Qt.KeepAspectRatio,
                QtCore.Qt.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)
            self.image_label.setText("")
        else:
            self.image_label.setText("截图失败")
            self.image_label.setPixmap(QPixmap())

    def handle_esc_key(self):
        """处理ESC键按下事件"""
        print("ESC键被按下")
        # 如果截图窗口存在，关闭它
        if self.screenshot_window:
            self.screenshot_window.close()
            self.screenshot_window = None

        # 显示主窗口
        if not self.isVisible():
            self.show_window()

    def quit_application(self):
        """退出应用程序"""
        self.hotkey_manager.stop_listen()
        self.tray_icon.hide()
        QApplication.quit()

    def keyPressEvent(self, event):
        """按键事件"""
        if event.key() == Qt.Key_Escape:
            print("取消键！")
            self.handle_esc_key()
        elif event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_K:
            print("Ctrl+K 开始截图...")
            self.start_screenshot()

    def closeEvent(self, event):
        """重写关闭事件，实现最小化到托盘"""
        event.ignore()
        self.hide_window()


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("截图工具")

    # 设置应用程序退出时清理资源
    app.aboutToQuit.connect(lambda: print("应用程序退出"))

    window = MyMainWindow(start_hidden=True)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()