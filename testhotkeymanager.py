import unittest
from unittest.mock import MagicMock, patch
from pynput.keyboard import Key, KeyCode

from hotkey_manager import HotkeyManager


class TestHotkeyManager(unittest.TestCase):
    def setUp(self):
        self.manager = HotkeyManager()
        self.manager.start_listen("ctrl+a")
        self.manager.hotkey_pressed = MagicMock()
        self.manager.threshold = 0.5

    @patch("time.time")
    def test_valid_hotkey(self, mock_time):
        """正常快速组合键应触发"""
        mock_time.side_effect = [1000.0, 1000.3]  # 时间差0.3秒
        self.manager._on_press(Key.ctrl)
        self.manager._on_press(KeyCode.from_char("a"))
        self.manager.hotkey_pressed.emit.assert_called_once()

    @patch("time.time")
    def test_expired_hotkey(self, mock_time):
        """超时组合键不应触发"""
        mock_time.side_effect = [1000.0, 1000.6]  # 时间差0.6秒
        self.manager._on_press(Key.ctrl)
        self.manager._on_press(KeyCode.from_char("a"))
        self.manager.hotkey_pressed.emit.assert_not_called()

    @patch("time.time")
    def test_repeat_press(self, mock_time):
        """重新按下修饰键应重置时间"""
        mock_time.side_effect = [1000.0, 1001.0, 1001.1]  # 释放后重新按压
        # 第一次按下
        self.manager._on_press(Key.ctrl)
        self.manager._on_release(Key.ctrl)
        # 第二次按下
        self.manager._on_press(Key.ctrl)
        self.manager._on_press(KeyCode.from_char("a"))
        self.manager.hotkey_pressed.emit.assert_called_once()

if __name__ == "__main__":
    unittest.main()