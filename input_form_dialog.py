import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QDialog, QDateEdit, QSpinBox, QSpacerItem, QSizePolicy
from PySide6.QtGui import QFont
from PySide6.QtCore import QDate



class InputFormDialog(QDialog):
    def __init__(self, form_structure, parent=None):
        super().__init__(parent)
        self.form_structure = form_structure
        self.input_widgets = []

        self.initUI()
        self.setWindowTitle("输入窗口")
        self.adjust_window_size()
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

    def initUI(self):
        layout = QVBoxLayout()

        # 设置字体大小
        font = QFont()
        font.setPointSize(12)  # 可以根据需要调整字体大小

        # 根据数据结构创建表单字段
        for field in self.form_structure:
            label = QLabel(field["label"])
            label.setFont(font)  # 设置标签字体
            layout.addWidget(label)

            if field["type"] == "text":
                input_widget = QLineEdit()
                if "default" in field:
                    input_widget.setText(field["default"])
            elif field["type"] == "date":
                input_widget = QDateEdit()
                input_widget.setCalendarPopup(True)  # 显示日历弹窗
                if "default" in field:
                    try:
                        default_date = QDate.fromString(field["default"], "yyyy-MM-dd")
                        input_widget.setDate(default_date)
                    except Exception:
                        input_widget.setDate(QDate.currentDate())
                else:
                    input_widget.setDate(QDate.currentDate())  # 设置默认日期为当前日期
            elif field["type"] == "spinbox":
                input_widget = QSpinBox()
                input_widget.setRange(0, 999)  # 设置年龄范围，可按需调整
                if "default" in field:
                    input_widget.setValue(field["default"])
            else:
                input_widget = QLineEdit()  # 默认使用文本输入框

            input_widget.setFont(font)  # 设置输入框字体
            layout.addWidget(input_widget)
            self.input_widgets.append(input_widget)

            # 添加垂直间隔
            spacer = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
            layout.addItem(spacer)

        # 添加提交按钮
        submit_button = QPushButton("提交")
        submit_button.setFont(font)  # 设置按钮字体
        submit_button.clicked.connect(self.accept)
        layout.addWidget(submit_button)

        self.setLayout(layout)

    def adjust_window_size(self):
        base_width = 300
        base_height = 100  # 基础高度，包含按钮和一些边距
        field_height = 50  # 每个字段的大致高度（标签 + 输入框）
        spacer_height = 10  # 间隔的高度
        total_height = base_height + len(self.form_structure) * (field_height + spacer_height)
        self.setFixedSize(base_width, total_height)

    def get_input_values(self):
        values = []
        for i, widget in enumerate(self.input_widgets):
            field_type = self.form_structure[i]["type"]
            if field_type == "text":
                values.append(widget.text())
            elif field_type == "date":
                values.append(widget.date().toString("yyyy-MM-dd"))
            elif field_type == "spinbox":
                values.append(widget.value())
        return values


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # 设置字体大小
        font = QFont()
        font.setPointSize(12)  # 可以根据需要调整字体大小

        # 添加打开表单对话框的按钮
        open_dialog_button = QPushButton("打开表单")
        open_dialog_button.setFont(font)  # 设置按钮字体
        open_dialog_button.clicked.connect(self.open_form_dialog)
        layout.addWidget(open_dialog_button)

        self.setLayout(layout)
        self.setWindowTitle("主窗口")
        self.show()

    def open_form_dialog(self):
        # 自定义数据结构，用于描述表单字段，添加了默认值
        form_structure = [
            {"label": "姓名", "type": "text", "default": "张三"},
            {"label": "年龄", "type": "spinbox", "default": 20},
            {"label": "邮箱", "type": "text", "default": "example@example.com"},
            {"label": "出生日期", "type": "date", "default": "2000-01-01"}
        ]

        dialog = InputFormDialog(form_structure, self)
        if dialog.exec() == QDialog.Accepted:
            values = dialog.get_input_values()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec())