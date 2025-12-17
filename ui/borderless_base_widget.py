from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt, QPoint, QTimer, QSize
from PySide6.QtGui import QPixmap, QImage, QMouseEvent


class ImagePreviewWidget(QWidget):
    """图片预览控件 - 无边框，自适应填充，支持缩放"""

    def __init__(self, parent=None):
        super().__init__(parent)
        # 设置无边框
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setMinimumSize(QSize(50, 50))  # 设置最小尺寸

        # 初始化变量
        self.original_pixmap = None  # 存储原始图像
        self.scale_factor = 1.0  # 缩放因子
        self._drag_position = QPoint()  # 用于窗口拖动的起始位置

        # 延迟调整大小定时器
        self._resize_timer = QTimer()
        self._resize_timer.setInterval(50)  # 50ms延迟
        self._resize_timer.setSingleShot(True)
        self._resize_timer.timeout.connect(self._delayed_resize)

        # 设置布局和样式
        self._setup_ui()

        # 设置背景色为黑色
        self.setStyleSheet("background-color: black;")

    def _setup_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # 图片显示标签
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("border: none;")
        layout.addWidget(self.image_label)

    def set_image(self, image_path):
        """设置图片"""
        # 加载图像
        image = QImage(image_path)
        if not image.isNull():
            self.original_pixmap = QPixmap.fromImage(image)
            self.scale_factor = 1.0  # 重置缩放因子
            self._update_display()
        else:
            self.image_label.setText("无法加载图片")
            self.original_pixmap = None

    def set_image_from_data(self, image_data):
        """从二进制数据设置图片"""
        image = QImage()
        if image.loadFromData(image_data):
            self.original_pixmap = QPixmap.fromImage(image)
            self.scale_factor = 1.0  # 重置缩放因子
            self._update_display()
        else:
            self.image_label.setText("无法加载图片数据")
            self.original_pixmap = None

    def _update_display(self):
        """更新图像显示"""
        if self.original_pixmap:
            # 根据当前缩放因子计算显示大小
            scaled_size = self._calculate_scaled_size()

            # 创建缩放后的图像
            scaled_pixmap = self.original_pixmap.scaled(
                scaled_size,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )

            self.resize(scaled_size.width(), scaled_size.height())

            # 设置到标签
            self.image_label.setPixmap(scaled_pixmap)

    def _calculate_scaled_size(self):
        """计算缩放后的图像大小"""

        if not self.original_pixmap:
            return QSize()

        base_size: QSize = self.original_pixmap.size()  # 原图片大小

        print("98 line")

        if self.scale_factor == 1.0:
            # 适应窗口
            return base_size.scaled(self.size(), Qt.KeepAspectRatio)
        else:
            # 应用缩放因子
            return base_size * self.scale_factor

    def resizeEvent(self, event):
        """窗口大小变化事件"""
        super().resizeEvent(event)

        # 如果当前没有放大（缩放因子为1），则延迟调整图像
        if self.scale_factor == 1.0:
            self._resize_timer.start()

    def _delayed_resize(self):
        """延迟调整图像大小"""
        if self.original_pixmap and self.scale_factor == 1.0:
            self._update_display()

    def wheelEvent(self, event):
        """鼠标滚轮事件 - 缩放图片"""
        if self.original_pixmap:

            original_width = self.original_pixmap.width()
            original_height = self.original_pixmap.height()

            # 根据滚轮方向调整缩放因子
            if event.angleDelta().y() > 0:
                # 放大
                self.scale_factor = min(self.scale_factor * 1.2, 5.0)  # 最大放大5倍
            else:
                # 缩小
                self.scale_factor = max(self.scale_factor * 0.8, 0.1)  # 最小缩小到0.1倍

            # 计算当前显示尺寸
            current_width = int(original_width * self.scale_factor)
            current_height = int(original_height * self.scale_factor)

            # 调试信息：打印缩放因子和当前尺寸
            print(f"缩放因子: {self.scale_factor:.2f}, "
                  f"原始尺寸: ({original_width}x{original_height}), "
                  f"当前尺寸: ({current_width}x{current_height})")

            # 更新显示
            self._update_display()
            self.resize(current_width, current_height)
            event.accept()

    def mousePressEvent(self, event: QMouseEvent):
        """鼠标按下事件 - 记录拖动起始位置"""
        if event.button() == Qt.LeftButton:
            self._drag_position = event.globalPosition().toPoint()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        """鼠标移动事件 - 实现窗口拖动"""
        if event.buttons() == Qt.LeftButton:
            # 计算移动距离
            delta = event.globalPosition().toPoint() - self._drag_position
            # 移动窗口
            self.move(self.pos() + delta)
            # 更新拖动起始位置
            self._drag_position = event.globalPosition().toPoint()
            event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent):
        """鼠标释放事件"""
        if event.button() == Qt.LeftButton:
            event.accept()

    def mouseDoubleClickEvent(self, event):
        """双击事件 - 重置缩放"""
        if event.button() == Qt.LeftButton:
            self.scale_factor = 1.0
            self._update_display()
            event.accept()

    def toggle_stay_on_top(self):
        """切换置顶状态"""
        flags = self.windowFlags()
        if flags & Qt.WindowStaysOnTopHint:
            self.setWindowFlags(flags & ~Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(flags | Qt.WindowStaysOnTopHint)
        self.show()


def main():
    import sys
    import os
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)

    # 创建预览窗口
    preview = ImagePreviewWidget()
    preview.setWindowTitle("图片预览")
    preview.resize(800, 600)
    preview.toggle_stay_on_top()

    # 测试图片路径
    test_image_path = r"C:\Users\Administrator\Pictures\Screenshots\屏幕截图 2025-12-13 230041.png"

    if os.path.exists(test_image_path):
        preview.set_image(test_image_path)
    else:
        # 如果没有图片文件，显示提示
        preview.image_label.setText("未找到测试图片")

    preview.show()

    sys.exit(app.exec())


# 使用示例
if __name__ == "__main__":
    main()
