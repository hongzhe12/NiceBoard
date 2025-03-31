from PySide6.QtCore import QObject, Signal
from pynput.keyboard import Key, KeyCode, Listener


class HotkeyManager(QObject):
    """简化版全局热键管理"""

    hotkey_pressed = Signal()

    def __init__(self):
        super().__init__()
        self._listener = None
        self._target_keys = set()
        self._pressed_keys = set()

    def start_listen(self, hotkey: str = 'ctrl+]') -> None:
        """启动热键监听"""
        self.stop_listen()  # 确保先停止现有监听

        # 解析热键组合
        self._target_keys.clear()
        for key in hotkey.split('+'):
            key = key.strip().lower()
            try:
                # 尝试作为特殊键(如ctrl/shift等)
                self._target_keys.add(getattr(Key, key))
            except AttributeError:
                # 作为普通字符键
                if len(key) == 1:
                    self._target_keys.add(KeyCode.from_char(key))

        # 启动监听器
        self._listener = Listener(
            on_press=self._on_press,
            on_release=self._on_release
        )
        self._listener.start()

    def stop_listen(self) -> None:
        """停止热键监听"""
        if self._listener:
            self._listener.stop()
            self._listener = None
        self._pressed_keys.clear()

    def _on_press(self, key) -> None:
        """处理按键按下事件"""
        self._pressed_keys.add(key)
        if self._pressed_keys == self._target_keys:
            self.hotkey_pressed.emit()

    def _on_release(self, key) -> None:
        """处理按键释放事件"""
        if key in self._pressed_keys:
            self._pressed_keys.remove(key)

    def __del__(self):
        """析构时自动清理"""
        self.stop_listen()