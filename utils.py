from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, \
    QTextEdit
import json
from pathlib import Path

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




def load_db_config():
    """从配置文件加载数据库配置"""
    # 默认配置（当没有配置文件时使用）
    default_config = {
        'db_name': '',
        'host': '',
        'port': '',
        'username': '',
        'password': '',
        'enable': False,
    }

    # 配置文件路径（~/.clipboard_manager/db_config.json）
    config_path = Path.home() / '.clipboard_manager' / 'db_config.json'

    try:
        if config_path.exists():
            print(f"尝试加载配置文件: {config_path}")
            with open(config_path, 'r', encoding='utf-8') as f:
                loaded_config = json.load(f)
                # 合并加载的配置和默认配置（确保所有字段都存在）
                result = {**default_config, **loaded_config}
                print(f"成功加载配置: {result}")
                return result
        print("配置文件不存在，返回默认配置")
        return default_config  # 配置文件不存在时返回默认配置
    except Exception as e:
        print(f"加载配置出错: {e}")
        return default_config  # 出错时返回默认配置


def save_db_config(config):
    """将数据库配置保存到配置文件"""
    try:
        import json
        import os

        # 确保配置目录存在
        config_dir = os.path.expanduser("~/.clipboard_manager")
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)

        # 配置文件路径
        config_path = os.path.join(config_dir, "db_config.json")

        print(f"尝试保存配置到文件: {config_path}")
        # 写入配置
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=4)
        print("配置保存成功")

    except Exception as e:
        show_message("错误", f"保存配置时出错: {str(e)}", is_error=True)

