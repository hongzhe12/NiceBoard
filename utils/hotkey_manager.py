from PySide6.QtCore import QObject, Signal
from pynput.keyboard import Key, Listener
from log.log import logging as logger

class GlobalHotkeyManager(QObject):
    """全局热键管理器"""

    # 定义不同的热键信号
    f9_pressed = Signal()
    f10_pressed = Signal()
    esc_pressed = Signal()

    def __init__(self):
        super().__init__()
        self._listener = None
        logger.info("GlobalHotkeyManager 初始化完成")

    def start_listen(self) -> None:
        """启动监听"""
        logger.info("尝试启动热键监听...")
        self.stop_listen()
        try:
            self._listener = Listener(on_press=self._on_press)
            self._listener.start()
            logger.info("热键监听已启动成功")
        except Exception as e:
            logger.info(f"热键监听启动失败: {e}")

    def stop_listen(self) -> None:
        """停止监听"""
        if self._listener:
            logger.info("停止热键监听")
            self._listener.stop()
            self._listener = None

    def _on_press(self, key) -> None:
        """按键处理"""
        logger.info(f"检测到按键: {key}")

        try:
            if key == Key.f9:
                logger.info("F9 被按下，发射信号")
                self.f9_pressed.emit()
            elif key == Key.f10:
                logger.info("F1 被按下，发射信号")
                self.f10_pressed.emit()
            elif key == Key.esc:
                logger.info("ESC 被按下，发射信号")
                self.esc_pressed.emit()
        except Exception as e:
            logger.info(f"处理按键时出错: {e}")

    def __del__(self):
        logger.info("GlobalHotkeyManager 销毁")
        self.stop_listen()


# 创建全局热键管理器
global_hotkey_manager = GlobalHotkeyManager()