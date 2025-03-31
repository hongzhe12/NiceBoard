from PySide6.QtCore import QObject, Signal
from pynput.keyboard import Key, KeyCode, Listener


class HotkeyManager(QObject):
    """改进版全局热键管理，支持按住修饰键再按其他键触发"""

    hotkey_pressed = Signal()

    def __init__(self):
        super().__init__()
        self._listener = None
        self._modifier_keys = set()  # 修饰键(如Ctrl、Alt等)
        self._trigger_key = None  # 触发键(如字母键)
        self._modifiers_pressed = set()

    def start_listen(self, hotkey: str = 'ctrl+]') -> None:
        """启动热键监听"""
        self.stop_listen()  # 确保先停止现有监听

        # 解析热键组合
        self._modifier_keys.clear()
        self._trigger_key = None
        keys = hotkey.split('+')

        for key in keys[:-1]:  # 前面的都是修饰键
            key = key.strip().lower()
            try:
                self._modifier_keys.add(getattr(Key, key))
            except AttributeError:
                if len(key) == 1:
                    self._modifier_keys.add(KeyCode.from_char(key))

        # 最后一个键是触发键
        trigger = keys[-1].strip().lower()
        try:
            self._trigger_key = getattr(Key, trigger)
        except AttributeError:
            if len(trigger) == 1:
                self._trigger_key = KeyCode.from_char(trigger)

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
        self._modifiers_pressed.clear()

    def _on_press(self, key) -> None:
        """处理按键按下事件"""
        if key in self._modifier_keys:
            self._modifiers_pressed.add(key)
        elif key == self._trigger_key and self._modifiers_pressed == self._modifier_keys:
            self.hotkey_pressed.emit()

    def _on_release(self, key) -> None:
        """处理按键释放事件"""
        if key in self._modifiers_pressed:
            self._modifiers_pressed.remove(key)
        elif key == self._trigger_key:
            pass  # 触发键释放不需要特殊处理

    def __del__(self):
        """析构时自动清理"""
        self.stop_listen()