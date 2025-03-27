import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QListWidget,
                               QVBoxLayout, QWidget, QPushButton)
from PySide6.QtCore import QObject, Signal, QPoint
from PySide6.QtGui import QCursor
import keyboard
from threading import Thread


class HotkeyManager(QObject):
    hotkey_pressed = Signal()

    def __init__(self):
        super().__init__()
        self._running = False

    def start_listen(self, hotkey):
        """启动热键监听线程"""
        if self._running:
            self.stop_listen()

        self._running = True
        Thread(target=self._listen_hotkey, args=(hotkey,), daemon=True).start()

    def stop_listen(self):
        """停止热键监听"""
        self._running = False
        keyboard.unhook_all()

    def _listen_hotkey(self, hotkey):
        """监听热键的线程函数"""
        while self._running:
            keyboard.wait(hotkey)
            if self._running:
                self.hotkey_pressed.emit()


class SimpleClipboardHistory(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("剪贴板历史记录")
        self.setFixedSize(300, 400)  # 固定窗口大小

        # 初始化UI
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        self.history_list = QListWidget()
        layout.addWidget(self.history_list)

        # 添加控制按钮
        self.toggle_btn = QPushButton("隐藏窗口")
        self.toggle_btn.clicked.connect(self.hide)
        layout.addWidget(self.toggle_btn)

        # 初始化剪贴板历史记录
        self.clipboard_history = []

        # 开始监控剪贴板
        self.clipboard = QApplication.clipboard()
        self.clipboard.dataChanged.connect(self.on_clipboard_change)

        # 设置全局热键
        self.hotkey_manager = HotkeyManager()
        self.hotkey_manager.hotkey_pressed.connect(self.show_at_cursor)
        self.setup_global_hotkey()

    def setup_global_hotkey(self):
        """设置全局热键Ctrl+Shift+V"""
        try:
            self.hotkey_manager.start_listen('ctrl+shift+v')
            print("全局热键注册成功：Ctrl+Shift+V")
        except Exception as e:
            print(f"热键注册失败: {e}\n请尝试以管理员身份运行程序")

    def on_clipboard_change(self):
        """剪贴板内容变化时的处理"""
        mime_data = self.clipboard.mimeData()
        if mime_data.hasText():
            text = mime_data.text().strip()
            if text and (not self.clipboard_history or text != self.clipboard_history[0]):
                self.clipboard_history.insert(0, text)
                self.history_list.insertItem(0, text)

                if len(self.clipboard_history) > 50:
                    self.clipboard_history.pop()
                    self.history_list.takeItem(self.history_list.count() - 1)

    def show_at_cursor(self):
        """在鼠标位置显示窗口的左上角"""
        if self.isVisible():
            self.hide()
        else:
            # 获取鼠标当前位置
            cursor_pos = QCursor.pos()
            screen_geometry = QApplication.primaryScreen().availableGeometry()

            # 计算窗口位置（左上角对齐鼠标）
            x = cursor_pos.x()  # 直接对齐鼠标 x 坐标
            y = cursor_pos.y()  # 直接对齐鼠标 y 坐标

            # 确保窗口不会超出屏幕边界
            window_width = self.width()
            window_height = self.height()
            x = max(screen_geometry.left(), min(x, screen_geometry.right() - window_width))
            y = max(screen_geometry.top(), min(y, screen_geometry.bottom() - window_height))

            self.move(QPoint(x, y))
            self.show()
            self.activateWindow()
            self.raise_()

    def closeEvent(self, event):
        """窗口关闭时清理资源"""
        self.hotkey_manager.stop_listen()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    app.setStyleSheet("""
        QPushButton {
            padding: 8px;
            font-size: 12px;
        }
        QListWidget {
            font-size: 13px;
        }
    """)

    window = SimpleClipboardHistory()
    sys.exit(app.exec())