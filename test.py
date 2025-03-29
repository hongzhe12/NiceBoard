import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QListWidgetItem
from PySide6.QtGui import QPixmap, QClipboard
from PySide6.QtCore import Qt


class ClipboardImageHistory(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("剪贴板图片历史记录")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        self.clear_button = QPushButton("清空历史记录")
        self.clear_button.clicked.connect(self.clear_history)
        layout.addWidget(self.clear_button)

        self.setLayout(layout)

        self.clipboard = QApplication.clipboard()
        self.clipboard.changed.connect(self.on_clipboard_change)

    def on_clipboard_change(self, mode):
        if mode == QClipboard.Clipboard:
            mime_data = self.clipboard.mimeData()
            if mime_data.hasImage():
                image = self.clipboard.image()
                pixmap = QPixmap.fromImage(image)
                item = QListWidgetItem()
                scaled_pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio)
                item.setData(Qt.DecorationRole, scaled_pixmap)
                self.list_widget.addItem(item)

    def clear_history(self):
        self.list_widget.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ClipboardImageHistory()
    window.show()
    sys.exit(app.exec())
