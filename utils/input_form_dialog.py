import sys
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel,
                               QLineEdit, QPushButton, QDialog, QDateEdit,
                               QSpinBox, QSpacerItem, QSizePolicy, QComboBox,
                               QTextEdit)
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
        screen_geometry = QApplication.primaryScreen().geometry()
        window_geometry = self.frameGeometry()
        center_point = screen_geometry.center()
        window_geometry.moveCenter(center_point)
        self.move(window_geometry.topLeft())

    def initUI(self):
        layout = QVBoxLayout()

        font = QFont()
        font.setPointSize(12)

        for field in self.form_structure:
            label = QLabel(field["label"])
            label.setFont(font)
            layout.addWidget(label)

            if field["type"] == "text":
                input_widget = QLineEdit()
                if "default" in field:
                    input_widget.setText(field["default"])
            elif field["type"] == "date":
                input_widget = QDateEdit()
                input_widget.setCalendarPopup(True)
                if "default" in field:
                    try:
                        default_date = QDate.fromString(field["default"], "yyyy-MM-dd")
                        input_widget.setDate(default_date)
                    except Exception:
                        input_widget.setDate(QDate.currentDate())
                else:
                    input_widget.setDate(QDate.currentDate())
            elif field["type"] == "spinbox":
                input_widget = QSpinBox()
                input_widget.setRange(0, 999)
                if "default" in field:
                    input_widget.setValue(field["default"])
            elif field["type"] == "combo":
                input_widget = QComboBox()
                if "items" in field:  # 确保有items字段
                    input_widget.addItems(field["items"])
                if "default" in field and field["default"] in field["items"]:
                    index = field["items"].index(field["default"])
                    input_widget.setCurrentIndex(index)
            elif field["type"] == "textarea":  # 新增长文本输入框
                input_widget = QTextEdit()
                if "default" in field:
                    input_widget.setText(field["default"])
                # 设置长文本输入框的最小高度
                input_widget.setMinimumHeight(100)
                # 可选：设置最大高度
                input_widget.setMaximumHeight(200)
            else:
                input_widget = QLineEdit()  # 默认使用文本输入框

            input_widget.setFont(font)  # 设置输入框字体
            layout.addWidget(input_widget)
            self.input_widgets.append(input_widget)

            spacer = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
            layout.addItem(spacer)

        submit_button = QPushButton("提交")

        submit_font = QFont()
        submit_font.setPointSize(10)
        submit_button.setFixedHeight(30)  # 设置按钮高度，确保文字能完全显示
        submit_button.setFont(submit_font)  # 设置按钮字体
        submit_button.clicked.connect(self.accept)
        layout.addWidget(submit_button)
        spacer = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        layout.addItem(spacer)

        self.setLayout(layout)

    def adjust_window_size(self):
        base_width = 400  # 增加宽度以适应长文本输入框
        base_height = 100  # 基础高度，包含按钮和一些边距
        field_height = 50  # 每个字段的大致高度（标签 + 输入框）
        spacer_height = 10  # 间隔的高度

        # 计算总高度，为长文本输入框分配更多空间
        total_height = base_height
        for field in self.form_structure:
            if field["type"] == "textarea":
                total_height += 120  # 长文本输入框的高度
            else:
                total_height += field_height + spacer_height

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
            elif field_type == "combo":
                values.append(widget.currentText())
            elif field_type == "textarea":  # 处理长文本输入
                values.append(widget.toPlainText())
        return values


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        font = QFont()
        font.setPointSize(12)

        open_dialog_button = QPushButton("打开表单")
        open_dialog_button.setFont(font)
        open_dialog_button.clicked.connect(self.open_form_dialog)
        layout.addWidget(open_dialog_button)

        self.setLayout(layout)
        self.setWindowTitle("主窗口")
        self.show()

    def open_form_dialog(self):
        form_structure = [
            {"label": "姓名", "type": "text", "default": "张三"},
            {"label": "年龄", "type": "spinbox", "default": 20},
            {"label": "邮箱", "type": "text", "default": "example@example.com"},
            {"label": "出生日期", "type": "date", "default": "2000-01-01"},
            {"label": "性别", "type": "combo", "items": ["男", "女", "其他"], "default": "男"},
            {"label": "职业", "type": "combo", "items": ["学生", "教师", "工程师", "医生", "其他"]},
            {"label": "个人简介", "type": "textarea", "default": "请输入您的个人简介..."},  # 新增长文本字段
            {"label": "备注", "type": "textarea"}  # 另一个长文本字段示例
        ]

        dialog = InputFormDialog(form_structure, self)
        if dialog.exec() == QDialog.Accepted:
            values = dialog.get_input_values()
            print(values)  # 打印获取的值


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec())