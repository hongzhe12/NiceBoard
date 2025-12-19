import sys

from PySide6.QtCore import Signal, QObject
from PySide6.QtWidgets import QApplication

from ui.borderless_base_widget import ImagePreviewWidget
from utils.screen_hot import Screenshot


class ScreenshotManager(QObject):
    """
    截图管理器类，专门负责处理截图功能
    """
    screenshot_taken = Signal(object)  # 截图完成信号，传递 QPixmap 对象
    cancelled = Signal()  # 截图取消信号

    def __init__(self, parent=None):
        super().__init__(parent)
        self.preview = None  # 预览窗口
        self.screenshot_window = None  # 截图窗口

    def take_screenshot(self):
        """
        开始截图
        """
        # 如果已有截图窗口，先关闭
        if self.screenshot_window:
            self.screenshot_window.close()
            self.screenshot_window = None

        # 创建新的截图窗口实例
        self.screenshot_window = Screenshot()
        self.screenshot_window.completed.connect(self._on_screenshot_completed)
        self.screenshot_window.showFullScreen()

        # 确保截图窗口获得焦点
        self.screenshot_window.raise_()
        self.screenshot_window.activateWindow()

    def _on_screenshot_completed(self, pixmap):
        """
        内部方法：处理截图完成事件
        """

        # 关闭截图窗口
        if self.screenshot_window:
            self.screenshot_window.close()
            self.screenshot_window = None

        # 发送相应信号
        if pixmap.isNull():
            self.cancelled.emit()
        else:
            # 创建预览窗口
            self.preview = ImagePreviewWidget()
            self.preview.setWindowTitle("图片预览")
            self.preview.resize(800, 600)
            self.preview.toggle_stay_on_top()
            self.preview.set_pixmap(pixmap)

    def cancel_screenshot(self):
        """
        取消当前截图操作
        """
        if self.screenshot_window:
            self.screenshot_window.close()
            self.screenshot_window = None
            self.cancelled.emit()

    def close_preview_and_screenshot(self):
        """
        关闭预览窗口和截图窗口
        """
        # 关闭预览窗口
        if self.preview:
            self.preview.hide()
            # self.preview = None

        # 关闭截图窗口
        if self.screenshot_window:
            self.screenshot_window.hide()
            # self.screenshot_window = None


# 使用示例
def example_usage():
    """
    使用示例
    """

    app = QApplication(sys.argv)
    # 创建截图管理器
    screenshot_manager = ScreenshotManager()
    # 开始截图
    screenshot_manager.take_screenshot()
    sys.exit(app.exec())


if __name__ == "__main__":
    example_usage()
