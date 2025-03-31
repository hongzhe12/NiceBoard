from PySide6.QtWidgets import QListWidget, QListWidgetItem, QWidget, QHBoxLayout, QLabel, QPushButton, QSizePolicy
from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QIcon


class ClipboardListItemWidget(QWidget):
    """自定义列表项控件，包含文本、收藏和删除按钮"""
    delete_requested = Signal(QListWidgetItem)
    favorite_toggled = Signal(QListWidgetItem, bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self._item = None  # 关联的QListWidgetItem

    def setup_ui(self):
        """初始化UI布局"""
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(5, 2, 5, 2)
        self.layout.setSpacing(5)

        # 文本标签
        self.label = QLabel()
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.label.setWordWrap(True)

        # 收藏按钮
        self.favorite_btn = QPushButton()
        self.favorite_btn.setIcon(QIcon(":/icons/star_outline.svg"))  # 使用资源文件中的图标
        self.favorite_btn.setCheckable(True)
        self.favorite_btn.setFixedSize(24, 24)
        self.favorite_btn.setStyleSheet("QPushButton { border: none; padding: 0; }")

        # 删除按钮
        self.delete_btn = QPushButton()
        self.delete_btn.setIcon(QIcon(":/icons/delete.svg"))
        self.delete_btn.setFixedSize(24, 24)
        self.delete_btn.setStyleSheet("QPushButton { border: none; padding: 0; }")

        # 添加到布局
        self.layout.addWidget(self.label, 1)
        self.layout.addWidget(self.favorite_btn)
        self.layout.addWidget(self.delete_btn)

        # 连接信号
        self.delete_btn.clicked.connect(self._on_delete)
        self.favorite_btn.toggled.connect(self._on_favorite_toggled)

    def set_item(self, item):
        """设置关联的QListWidgetItem"""
        self._item = item

    def set_text(self, text):
        """设置显示文本"""
        self.label.setText(text)

    def set_favorite(self, favorite):
        """设置收藏状态"""
        self.favorite_btn.setChecked(favorite)
        self._update_favorite_icon()

    def _update_favorite_icon(self):
        """更新收藏按钮图标"""
        if self.favorite_btn.isChecked():
            self.favorite_btn.setIcon(QIcon(":/icons/star_filled.svg"))
        else:
            self.favorite_btn.setIcon(QIcon(":/icons/star_outline.svg"))

    def _on_delete(self):
        """删除按钮点击事件"""
        if self._item:
            self.delete_requested.emit(self._item)

    def _on_favorite_toggled(self, checked):
        """收藏状态改变事件"""
        if self._item:
            self.favorite_toggled.emit(self._item, checked)
        self._update_favorite_icon()


class ClipboardListWidget(QListWidget):
    """自定义剪贴板历史列表控件"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        """初始化UI设置"""
        self.setVerticalScrollMode(QListWidget.ScrollPerPixel)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWordWrap(True)
        self.setSpacing(2)

    def add_item(self, text, favorite=False):
        """添加带有自定义控件的项"""
        item = QListWidgetItem()
        item.setSizeHint(QSize(0, 40))  # 设置固定高度

        widget = ClipboardListItemWidget()
        widget.set_item(item)
        widget.set_text(text)
        widget.set_favorite(favorite)

        # 连接信号
        widget.delete_requested.connect(self._on_delete_requested)
        widget.favorite_toggled.connect(self._on_favorite_toggled)

        self.addItem(item)
        self.setItemWidget(item, widget)
        return item

    def _on_delete_requested(self, item):
        """处理删除请求"""
        row = self.row(item)
        if row >= 0:
            self.takeItem(row)

    def _on_favorite_toggled(self, item, favorite):
        """处理收藏状态变化"""
        # 这里可以添加数据库更新逻辑
        print(f"Item favorited: {favorite}, Text: {self.itemWidget(item).label.text()}")
        # 如果是收藏项，可以移动到列表顶部
        if favorite:
            row = self.row(item)
            if row > 0:
                self.takeItem(row)
                self.insertItem(0, item)
                self.setItemWidget(item, self.itemWidget(item))