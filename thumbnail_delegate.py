from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QStyledItemDelegate, QStyle, QStyleOptionViewItem

from PySide6.QtWidgets import QStyledItemDelegate, QListWidget
from PySide6.QtCore import QSize

from PySide6.QtWidgets import QStyledItemDelegate
from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QPainter


class ThumbnailDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        # 保存painter状态
        painter.save()

        # 获取对应的QListWidgetItem
        item = self.list_widget.item(index.row())
        if not item:
            painter.restore()
            return

        # 1. 绘制默认项背景（包括选中状态）
        option.text = ""  # 清空文本，我们自己绘制
        option.features |= QStyleOptionViewItem.HasDisplay
        if option.state & QStyle.State_Selected:
            painter.fillRect(option.rect, option.palette.highlight())
        elif option.state & QStyle.State_MouseOver:
            painter.fillRect(option.rect, option.palette.alternateBase())
        else:
            painter.fillRect(option.rect, option.palette.base())

        # 2. 绘制图标（如果是图片项）
        if not item.icon().isNull():
            icon_margin = 10
            text_height = 25

            # 图标区域
            icon_rect = QRect(
                option.rect.left() + icon_margin,
                option.rect.top() + icon_margin,
                option.rect.width() - 2 * icon_margin,
                option.rect.height() - 2 * icon_margin - text_height
            )

            # 保持图标的正常显示（不受选中状态影响）
            icon_painter = QPainter()
            icon_painter.begin(painter.device())
            item.icon().paint(
                icon_painter,
                icon_rect,
                Qt.AlignCenter,
                QIcon.Mode.Normal,
                QIcon.State.On
            )
            icon_painter.end()

        # 3. 绘制文本（带选中状态颜色）
        text_rect = QRect(
            option.rect.left() + 10,
            option.rect.bottom() - 25,
            option.rect.width() - 20,
            20
        )

        text_color = option.palette.highlightedText() if option.state & QStyle.State_Selected else option.palette.text()
        painter.setPen(text_color)
        painter.drawText(
            text_rect,
            Qt.AlignLeft | Qt.TextSingleLine,
            item.text()
        )

        # 4. 绘制焦点框（虚线边框）
        if option.state & QStyle.State_HasFocus:
            focus_rect = option.rect.adjusted(1, 1, -1, -1)
            focus_pen = QPen(option.palette.highlight(), 1, Qt.DashLine)
            painter.setPen(focus_pen)
            painter.drawRect(focus_rect)

        painter.restore()