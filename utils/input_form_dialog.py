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

        # 设置布局间距
        layout.setSpacing(10)  # 增加间距
        layout.setContentsMargins(15, 15, 15, 15)  # 设置边距

        font = QFont()
        font.setPointSize(10)  # 减小字体大小，从12改为10

        label_font = QFont()
        label_font.setPointSize(10)
        label_font.setBold(True)  # 标签加粗

        for field in self.form_structure:
            label = QLabel(field["label"])
            label.setFont(label_font)
            label.setMinimumHeight(25)  # 设置最小高度
            layout.addWidget(label)

            if field["type"] == "text":
                input_widget = QLineEdit()
                if "default" in field:
                    input_widget.setText(field["default"])
                input_widget.setMinimumHeight(35)  # 增加最小高度
                input_widget.setStyleSheet("padding: 5px;")  # 添加内边距

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
                input_widget.setMinimumHeight(35)
                input_widget.setStyleSheet("padding: 5px;")

            elif field["type"] == "spinbox":
                input_widget = QSpinBox()
                input_widget.setRange(0, 999)
                if "default" in field:
                    input_widget.setValue(field["default"])
                input_widget.setMinimumHeight(35)
                input_widget.setStyleSheet("padding: 5px;")

            elif field["type"] == "combo":
                input_widget = QComboBox()
                if "items" in field:
                    input_widget.addItems(field["items"])
                if "default" in field and field["default"] in field["items"]:
                    index = field["items"].index(field["default"])
                    input_widget.setCurrentIndex(index)
                input_widget.setMinimumHeight(35)
                input_widget.setStyleSheet("""
                    QComboBox {
                        padding: 5px;
                        border: 1px solid #ccc;
                        border-radius: 3px;
                    }
                    QComboBox::drop-down {
                        border: none;
                    }
                """)

            elif field["type"] == "textarea":
                input_widget = QTextEdit()
                if "default" in field:
                    input_widget.setText(field["default"])
                input_widget.setMinimumHeight(120)  # 增加最小高度
                input_widget.setMaximumHeight(200)
                input_widget.setStyleSheet("""
                    QTextEdit {
                        padding: 5px;
                        border: 1px solid #ccc;
                        border-radius: 3px;
                        font-size: 10pt;
                    }
                """)

            else:
                input_widget = QLineEdit()
                input_widget.setMinimumHeight(35)
                input_widget.setStyleSheet("padding: 5px;")

            input_widget.setFont(font)
            layout.addWidget(input_widget)
            self.input_widgets.append(input_widget)

            # 减小间距高度
            spacer = QSpacerItem(20, 8, QSizePolicy.Minimum, QSizePolicy.Fixed)
            layout.addItem(spacer)

        # 添加底部填充
        layout.addStretch(1)

        # 提交按钮
        submit_button = QPushButton("提交")
        submit_button.setMinimumHeight(40)  # 增加按钮高度
        # submit_button.setStyleSheet("""
        #     QPushButton {
        #         background-color: #4CAF50;
        #         color: white;
        #         border: none;
        #         border-radius: 5px;
        #         padding: 10px;
        #         font-size: 12px;
        #         font-weight: bold;
        #     }
        #     QPushButton:hover {
        #         background-color: #45a049;
        #     }
        #     QPushButton:pressed {
        #         background-color: #3d8b40;
        #     }
        # """)
        submit_button.clicked.connect(self.accept)
        layout.addWidget(submit_button)

        self.setLayout(layout)

    def adjust_window_size(self):
        # 动态计算窗口大小
        base_width = 450  # 增加宽度
        field_count = len(self.form_structure)

        # 计算基础高度
        base_height = 120  # 标题栏 + 按钮 + 边距

        # 计算字段高度
        field_heights = 0
        for field in self.form_structure:
            if field["type"] == "textarea":
                field_heights += 140  # 长文本字段更高
            else:
                field_heights += 70  # 普通字段高度

        total_height = base_height + field_heights

        # 限制最大高度
        max_height = QApplication.primaryScreen().size().height() * 0.8
        if total_height > max_height:
            total_height = int(max_height)
            # 如果太高，设置为可滚动
            self.setMinimumSize(base_width, int(max_height * 0.6))
            self.setMaximumSize(base_width, int(max_height))
        else:
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
            elif field_type == "textarea":
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