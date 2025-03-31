import logging
from typing import Optional, Dict
from PySide6.QtCore import QObject, Signal, QMutex
from pynput import keyboard as pynput_keyboard
from pynput.keyboard import Key, KeyCode, Controller, Listener


class HotkeyManager(QObject):
    """使用 pynput 实现的全局热键管理"""

    # 保持原有信号不变
    hotkey_pressed = Signal()

    def __init__(self):
        super().__init__()
        self._hotkey = None
        self._is_running = False
        self._listener = None
        self._current_keys = set()
        self._mutex = QMutex()
        self._hotkey_combinations = {}  # 存储热键组合

    def start_listen(self, hotkey: str = 'ctrl+]') -> None:
        """
        开始监听热键（保持原有接口）
        :param hotkey: 热键组合字符串
        """
        if self._is_running:
            self.stop_listen()

        self._hotkey = hotkey
        self._parse_hotkey(hotkey)

        try:
            self._listener = pynput_keyboard.Listener(
                on_press=self._on_press,
                on_release=self._on_release
            )
            self._listener.start()
            self._is_running = True
            logging.info(f"开始监听热键: {hotkey}")
        except Exception as e:
            logging.error(f"监听热键失败: {str(e)}")
            self._is_running = False

    def stop_listen(self) -> None:
        """停止监听热键（保持原有接口）"""
        if not self._is_running:
            return

        try:
            if self._listener is not None:
                self._listener.stop()
            self._is_running = False
            self._listener = None
            self._current_keys.clear()
            logging.info(f"停止监听热键: {self._hotkey}")
        except Exception as e:
            logging.error(f"停止监听热键失败: {str(e)}")

    def _parse_hotkey(self, hotkey_str: str) -> None:
        """解析热键字符串为 pynput 可识别的组合"""
        self._hotkey_combinations.clear()
        keys = hotkey_str.split('+')

        for key in keys:
            key = key.strip().lower()
            try:
                # 尝试转换为特殊键
                special_key = getattr(Key, key)
                self._hotkey_combinations[special_key] = False
            except AttributeError:
                # 普通字符键
                char_key = KeyCode.from_char(key) if len(key) == 1 else None
                if char_key:
                    self._hotkey_combinations[char_key] = False
                else:
                    logging.warning(f"无法识别的热键部分: {key}")

    def _on_press(self, key) -> None:
        """按键按下事件处理"""
        self._mutex.lock()
        try:
            self._current_keys.add(key)
            if self._check_hotkey():
                self.hotkey_pressed.emit()
        finally:
            self._mutex.unlock()

    def _on_release(self, key) -> None:
        """按键释放事件处理"""
        self._mutex.lock()
        try:
            if key in self._current_keys:
                self._current_keys.remove(key)
        finally:
            self._mutex.unlock()

    def _check_hotkey(self) -> bool:
        """检查当前按键组合是否匹配热键"""
        if not self._is_running:
            return False

        # 检查按键数量是否匹配
        if len(self._current_keys) != len(self._hotkey_combinations):
            return False

        # 检查每个键是否都按下
        for key in self._hotkey_combinations:
            if key not in self._current_keys:
                return False

        return True

    @property
    def is_running(self) -> bool:
        """获取当前监听状态（保持兼容）"""
        return self._is_running

    @property
    def current_hotkey(self) -> Optional[str]:
        """获取当前设置的热键（保持兼容）"""
        return self._hotkey if self._is_running else None

    def __del__(self):
        """析构时自动停止监听"""
        self.stop_listen()