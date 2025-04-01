from PySide6.QtWidgets import (
    QApplication, QListWidget, QListWidgetItem, QWidget,
    QHBoxLayout, QLabel, QPushButton, QVBoxLayout
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QSize, Signal
import sys
import resources_rc


class CustomListItemWidget(QWidget):
    """自定义列表项的Widget"""
    # 定义被收藏信号
    is_favorited_signal = Signal(object)

    def __init__(self, text, parent=None):
        super().__init__(parent)

        # 创建水平布局
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 5, 10, 5)

        # 添加标签显示文本
        self.label = QLabel(text)
        # 关键修改：设置自动换行，让QLabel支持多行显示
        self.label.setWordWrap(True)
        # 设置文本对齐方式为左对齐且垂直居中（可选，可按需调整）
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        # 添加收藏按钮
        self.fav_button = QPushButton()
        self.is_favorited = False
        self.update_icon()

        # 将控件添加到布局
        layout.addWidget(self.label)
        layout.addStretch()
        layout.addWidget(self.fav_button)

        self.setLayout(layout)
        self.fav_button.clicked.connect(self.toggle_favorite)

    def update_icon(self):
        """更新图标和样式"""
        icon = QIcon(":/icons/收藏.svg" if self.is_favorited else ":/icons/未收藏.svg")
        self.fav_button.setIcon(icon)
        self.label.setStyleSheet(f"""
            font-size: 14px;
            color: {'#FFA500' if self.is_favorited else 'black'};
            font-weight: {'bold' if self.is_favorited else 'normal'};
        """)

    def toggle_favorite(self):
        """切换收藏状态"""
        self.is_favorited = not self.is_favorited
        self.update_icon()

        # 发送信号
        self.is_favorited_signal.emit(self)

    def update_favorite_status(self):
        """更新收藏UI"""
        if self.is_favorited:
            icon = QIcon(":/icons/收藏.svg")
            self.fav_button.setIcon(icon)
            self.label.setStyleSheet(f"""
                        font-size: 14px;
                        color: {'#FFA500' if self.is_favorited else 'black'};
                        font-weight: {'bold' if self.is_favorited else 'normal'};
                    """)



class CustomListWidget(QListWidget):
    """自定义QListWidget实现"""

    def __init__(self, parent=None):
        super().__init__(parent)


        # self.setStyleSheet("""
        #     QListWidget {
        #         border: 1px solid #ccc;
        #         border-radius: 5px;
        #         padding: 5px;
        #     }
        # """)

    def addItem(self, item):
        """重写addItem方法以避免双重显示"""
        if isinstance(item, str):
            # 处理字符串输入
            list_item = QListWidgetItem()
            super().addItem(list_item)
            self._setup_item(list_item, item)
            return list_item
        else:
            # 处理QListWidgetItem输入
            super().addItem(item)
            if isinstance(item, QListWidgetItem):
                self._setup_item(item, item.text())
            return item

    def insertItem(self, row, item):
        """重写insertItem方法"""
        if isinstance(item, str):
            list_item = QListWidgetItem()
            super().insertItem(row, list_item)
            self._setup_item(list_item, item)
            return list_item
        else:
            super().insertItem(row, item)
            if isinstance(item, QListWidgetItem):
                self._setup_item(item, item.text())
            return item

    def _setup_item(self, item, text):
        """设置自定义widget"""
        item.setSizeHint(QSize(0, 60))
        widget = CustomListItemWidget(text)
        widget.setToolTip(text)
        self.setItemWidget(item, widget)
        # 关键修改：清空原生文本显示，避免双重显示
        item.setText("")

    def get_all_item_widgets(self):
        """获取所有CustomListItemWidget实例"""
        widgets = []
        for i in range(self.count()):
            item = self.item(i)
            if item:  # 确保item存在
                widget = self.itemWidget(item)
                if isinstance(widget, CustomListItemWidget):  # 类型检查
                    widgets.append(widget)
        return widgets



class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("自定义QListWidgetItem示例")
        self.setGeometry(100, 100, 400, 300)

        # 创建主布局
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)

        # 创建自定义列表控件
        self.list_widget = CustomListWidget()

        # 添加按钮用于测试添加item
        self.add_button = QPushButton("添加新项目")
        self.add_button.clicked.connect(self.add_new_item)

        # 将控件添加到布局
        layout.addWidget(self.list_widget)
        layout.addWidget(self.add_button)
        self.setLayout(layout)

        # 初始化一些示例数据
        self.init_sample_data()

    def init_sample_data(self):
        """初始化示例数据"""
        sample_texts = ["项目1", "项目2\n第二行文本", "项目3"]
        for text in sample_texts:
            # 使用标准addItem方法
            self.list_widget.addItem(text)

    def add_new_item(self):
        """添加新项目"""
        count = self.list_widget.count() + 1
        text = f"新项目 {count}"
        # 使用标准addItem方法
        self.list_widget.addItem(text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())