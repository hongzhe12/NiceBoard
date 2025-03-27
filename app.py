import sys
import keyboard
from threading import Thread
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QObject, Signal, QPoint
from PySide6.QtGui import QCursor
from models import ClipboardItem, Session
from ui_clipboard_history import Ui_SimpleClipboardHistory  # 编译后的UI


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
        self.setWindowTitle("剪贴板历史记录 (SQLAlchemy)")
        self.setFixedSize(400, 500)

        # 信号连接
        self.ui.toggle_btn.clicked.connect(self.hide)
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

    def toggle_window(self):
        """切换窗口显示状态"""
        if self.isVisible():
            self.hide()
        else:
            self._show_at_cursor()

    def _show_at_cursor(self):
        """在鼠标位置显示窗口"""
        cursor_pos = QCursor.pos()
        screen = QApplication.primaryScreen().availableGeometry()

        # 计算窗口位置（防止超出屏幕）
        x = min(max(cursor_pos.x(), screen.left()),
                screen.right() - self.width())
        y = min(max(cursor_pos.y(), screen.top()),
                screen.bottom() - self.height())

        self.move(QPoint(x, y))
        self.show()
        self.activateWindow()
        self.raise_()

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