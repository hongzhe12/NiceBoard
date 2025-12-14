import sys
from PySide6.QtCore import Qt, QRect, Signal
from PySide6.QtGui import QPen, QPainter, QColor, QGuiApplication, QPixmap, QKeyEvent
from PySide6.QtWidgets import QApplication, QWidget


class Screenshot(QWidget):
    # 自定义信号
    completed = Signal(QPixmap)

    def __init__(self):
        super().__init__()

        # 初始化变量
        self.fullScreenImage = None
        self.captureImage = None
        self.isMousePressLeft = False
        self.beginPosition = None
        self.endPosition = None

        self.initWindow()
        self.captureFullScreen()

        # 确保窗口获得焦点
        self.setFocusPolicy(Qt.StrongFocus)

    def initWindow(self):
        """初始化窗口"""
        self.setCursor(Qt.CrossCursor)
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        self.setWindowState(Qt.WindowFullScreen)

        # 设置窗口为透明背景，只显示截图区域
        self.setAttribute(Qt.WA_TranslucentBackground)

    def captureFullScreen(self):
        """捕获全屏"""
        self.fullScreenImage = QGuiApplication.primaryScreen().grabWindow(0)

    def mousePressEvent(self, event):
        """鼠标按下事件"""
        if event.button() == Qt.LeftButton:
            self.beginPosition = event.position().toPoint()
            self.isMousePressLeft = True
            self.endPosition = self.beginPosition
            self.update()

        elif event.button() == Qt.RightButton:
            if self.captureImage is not None:
                self.captureImage = None
                self.update()
            else:
                self.close()

    def mouseMoveEvent(self, event):
        """鼠标移动事件"""
        if self.isMousePressLeft:
            self.endPosition = event.position().toPoint()
            self.update()

    def mouseReleaseEvent(self, event):
        """鼠标释放事件"""
        if event.button() == Qt.LeftButton:
            self.isMousePressLeft = False
            self.endPosition = event.position().toPoint()
            self.update()

    def mouseDoubleClickEvent(self, event):
        """鼠标双击事件"""
        if self.captureImage and not self.captureImage.isNull():
            self.saveImage()
            self.close()

    def paintEvent(self, event):
        """绘制事件"""
        painter = QPainter(self)

        # 绘制背景（半透明黑色遮罩）
        painter.drawPixmap(0, 0, self.fullScreenImage)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 100))

        # 如果正在选择区域，绘制选框
        if self.beginPosition and self.endPosition:
            rect = self.getRectangle(self.beginPosition, self.endPosition)

            if not rect.isEmpty():
                # 绘制选中的区域（正常显示）
                self.captureImage = self.fullScreenImage.copy(rect)
                painter.drawPixmap(rect.topLeft(), self.captureImage)

                # 绘制选框边框
                painter.setPen(QPen(QColor(30, 150, 255), 2))
                painter.drawRect(rect)

                # 在选框右下角显示尺寸
                size_text = f"{rect.width()} × {rect.height()}"
                font = painter.font()
                font.setPointSize(10)
                painter.setFont(font)
                painter.setPen(QColor(255, 255, 255))
                painter.drawText(rect.bottomRight().x() - 100, rect.bottomRight().y() + 20, size_text)

    def getRectangle(self, beginPoint, endPoint):
        """获取矩形选框"""
        # 确保坐标是有效的
        if not beginPoint or not endPoint:
            return QRect()

        rect = QRect(beginPoint, endPoint).normalized()
        return rect

    def saveImage(self):
        """保存图片并发射信号"""
        if self.captureImage and not self.captureImage.isNull():
            self.completed.emit(self.captureImage)
        else:
            # 如果未选择区域，发送空图片
            self.completed.emit(QPixmap())

    def keyPressEvent(self, event: QKeyEvent):
        """按键事件"""
        # ESC 键退出截图
        if event.key() == Qt.Key_Escape:
            self.completed.emit(QPixmap())  # 发送空图片表示取消
            self.close()

        # Enter、Return 或 Space 键确认截图
        elif event.key() in (Qt.Key_Enter, Qt.Key_Return, Qt.Key_Space):
            if self.captureImage and not self.captureImage.isNull():
                self.saveImage()
                self.close()
            else:
                # 如果未选择区域，按回车则截取全屏
                self.captureImage = self.fullScreenImage
                self.saveImage()
                self.close()

    def showEvent(self, event):
        """显示事件"""
        super().showEvent(event)
        self.activateWindow()
        self.raise_()


def main():
    app = QApplication(sys.argv)
    window = Screenshot()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()