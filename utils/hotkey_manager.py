from PySide6.QtCore import QObject, Signal
from pynput.keyboard import Key, KeyCode, Listener


class HotkeyManager(QObject):
    """单按键触发的全局热键管理类"""

    hotkey_pressed = Signal()
    esc_pressed = Signal()  # 新增：Esc键按下信号

    def __init__(self):
        super().__init__()
        self._listener = None
        self._trigger_key = None
        self._esc_enabled = True  # 是否启用Esc键功能

    def start_listen(self, hotkey: str = 'f9',enable_esc: bool = True) -> None:
        """启动热键监听"""
        self.stop_listen()  # 确保先停止现有监听
        self._esc_enabled = enable_esc

        # 解析单按键
        try:
            self._trigger_key = getattr(Key, hotkey)
        except AttributeError:
            if len(hotkey) == 1:
                self._trigger_key = KeyCode.from_char(hotkey)
            else:
                print(f"无效的热键: {hotkey}")
                return

        # 启动监听器
        self._listener = Listener(
            on_press=self._on_press
        )
        self._listener.start()

    def stop_listen(self) -> None:
        """停止热键监听"""
        if self._listener:
            self._listener.stop()
            self._listener = None

    def _on_press(self, key) -> None:
        """处理按键按下事件"""
        if key == self._trigger_key:
            self.hotkey_pressed.emit()

        # Esc键检测（固定功能）
        if self._esc_enabled and key == Key.esc:
            self.esc_pressed.emit()

    def __del__(self):
        """析构时自动清理"""
        self.stop_listen()
