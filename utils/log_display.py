from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, \
    QTextEdit


def show_message(title, message, is_error=False):
    """显示消息对话框"""
    from PySide6.QtWidgets import QMessageBox

    msg_box = QMessageBox()
    msg_box.setWindowTitle(title)
    msg_box.setText(message)

    if is_error:
        msg_box.setIcon(QMessageBox.Critical)
    else:
        msg_box.setIcon(QMessageBox.Information)

    msg_box.exec()


class LogDisplayWindow(QWidget):
    def __init__(self, log_content):
        super().__init__()
        self.setWindowTitle("日志显示窗口")
        self.setGeometry(200, 200, 600, 400)

        # 关键代码：禁用关闭按钮（×）
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)  # 移除关闭按钮

        layout = QVBoxLayout()

        # 创建一个 QTextEdit 用于显示日志内容
        self.log_text_edit = QTextEdit()
        self.log_text_edit.setReadOnly(True)
        self.log_text_edit.setPlainText(log_content)
        layout.addWidget(self.log_text_edit)

        # 创建一个关闭按钮
        close_button = QPushButton("关闭")
        close_button.clicked.connect(self.hide)
        layout.addWidget(close_button, alignment=Qt.AlignRight)

        self.setLayout(layout)

        # 将窗口移动到屏幕中间
        self.move_to_center()

    def move_to_center(self):
        # 获取屏幕的几何信息
        screen_geometry = QApplication.primaryScreen().geometry()
        # 获取窗口的几何信息
        window_geometry = self.frameGeometry()
        # 计算窗口居中时左上角的坐标
        center_point = screen_geometry.center()
        window_geometry.moveCenter(center_point)
        # 移动窗口到计算好的位置
        self.move(window_geometry.topLeft())

