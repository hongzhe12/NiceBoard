from PySide6.QtCore import QTimer
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import QWidget, QMessageBox, QDialog, QApplication
import keyboard

from utils.auto_start import enable_auto_start, disable_auto_start
from utils.config_set import config_instance
from utils.input_form_dialog import InputFormDialog
from src.models import get_db_path

from ui.ui_settings_window import Ui_SettingsForm


class SettingsWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_SettingsForm()
        self.ui.setupUi(self)

        self.setFixedSize(300, 250)
        self.setWindowTitle("剪贴板历史设置")

        self.viewer = None

        self.ui.history_limit.setValidator(QIntValidator(1, 100000))
        self.ui.save_btn.clicked.connect(self.save_settings)
        self.ui.hotkey_edit.clicked.connect(self.change_hotkey)
        self.ui.history_limit.textChanged.connect(self._on_history_changed)

        # 从配置实例加载设置
        self.ui.hotkey_edit.setText(config_instance.get('hotkey', 'f9'))
        self.ui.history_limit.setText(str(config_instance.get('max_history', 10000)))
        self.ui.auto_start.setChecked(config_instance.get('auto_start', True))

        self.ui.database_btn.clicked.connect(self.database_btn_clicked)

        # 初始化数据库启用状态
        self.ui.enable_db_box.setChecked(config_instance.get('enable', False))
        # 导入按钮
        self.ui.import_btn.clicked.connect(self.import_btn_clicked)
        # 导出按钮
        self.ui.export_btn.clicked.connect(self.export_btn_clicked)

    def import_btn_clicked(self):
        form_structure = [
            {"label": "导入配置", "type": "text", "default": ""},
        ]

        dialog = InputFormDialog(form_structure, self)
        if dialog.exec() == QDialog.Accepted:
            values = dialog.get_input_values()
            data = values[0]
            res = config_instance.import_config(data)
            if res:
                QMessageBox.information(self, "导入成功", "配置已导入")
                return

        return QMessageBox.information(self, "导入提示", "失败！")

    def export_btn_clicked(self):
        data = config_instance.export_config()
        # 复制到剪贴板
        QApplication.clipboard().setText(data)
        QMessageBox.information(self, "导出成功", "配置已复制到剪贴板")

    def database_btn_clicked(self):
        file_path = get_db_path()
        form_structure = [
            {"label": "数据库类型(支持：mysql、postgresql)", "type": "text",
             "default": config_instance.get('db_type', "sqlite")},
            {"label": "数据库名称", "type": "text",
             "default": config_instance.get('db_name', file_path)},
            {"label": "主机地址", "type": "text",
             "default": config_instance.get('host', 'localhost')},
            {"label": "端口号", "type": "text",
             "default": config_instance.get('port', '5432')},
            {"label": "用户名", "type": "text",
             "default": config_instance.get('username', 'root')},
            {"label": "密码", "type": "text",
             "default": config_instance.get('password', '')},
        ]

        dialog = InputFormDialog(form_structure, self)
        if dialog.exec() == QDialog.Accepted:
            values = dialog.get_input_values()
            config_instance.update(
                {
                    'db_type': values[0],
                    'db_name': values[1],
                    'host': values[2],
                    'port': values[3],
                    'username': values[4],
                    'password': values[5],

                }, save=True
            )

            QMessageBox.information(self, "成功", "数据库配置已成功更新")

    def save_settings(self):
        try:
            # 保存数据库启用状态
            config_instance.set('enable', self.ui.enable_db_box.isChecked())

            # 保存最大记录数
            max_history = int(self.ui.history_limit.text())
            if not 1 <= max_history <= 100000:
                QMessageBox.warning(self, "错误", "请输入1-100000之间的整数")
                return
            config_instance.set('max_history', max_history)

            # 保存热键设置
            hotkey = self.ui.hotkey_edit.text().lower()
            config_instance.set('hotkey', hotkey)

            # 保存开机自启设置
            auto_start = self.ui.auto_start.isChecked()
            config_instance.set('auto_start', auto_start)

            # 保存所有配置
            if config_instance.save_config():
                # 处理开机自启的实际设置
                if auto_start:
                    enable_auto_start()
                else:
                    disable_auto_start()

                # 检查热键是否修改
                if hotkey.lower() not in ('f9', 'f9'):
                    QMessageBox.information(self, "提示", "热键修改后，需要重启好贴板！")
                else:
                    QMessageBox.information(self, "成功", "设置已保存！")

                self.hide()
            else:
                QMessageBox.warning(self, "错误", "保存配置失败")

        except ValueError:
            QMessageBox.warning(self, "错误", "请输入有效数字")

    def _on_history_changed(self, text):
        """处理文本变化"""
        print(f"当前输入值: {text}")

    def change_hotkey(self):
        """修改热键（使用 keyboard 库实现全局监听）"""
        self.ui.hotkey_edit.setText("正在等待按键...")
        self.ui.hotkey_edit.setFocus()  # 确保焦点在输入框

        # 清除之前的监听（避免重复）
        if hasattr(self, '_hotkey_listener'):
            keyboard.unhook(self._hotkey_listener)

        # 监听键盘按键
        self._hotkey_listener = keyboard.on_press(self._on_key_press)

        # 设置超时自动取消（可选）
        QTimer.singleShot(5000, self._cancel_hotkey_listening)

    def _on_key_press(self, event):
        """键盘按键回调"""
        # 忽略单独的修饰键（Ctrl/Shift/Alt/Win）
        if event.name in ("ctrl", "shift", "alt", "windows"):
            return

        # 获取组合键
        modifiers = []
        if keyboard.is_pressed("ctrl"):
            modifiers.append("Ctrl")
        if keyboard.is_pressed("shift"):
            modifiers.append("Shift")
        if keyboard.is_pressed("alt"):
            modifiers.append("Alt")
        if keyboard.is_pressed("windows"):
            modifiers.append("Win")

        # 组合键 + 按键
        key_combination = "+".join(modifiers + [event.name.upper()])

        # 更新 UI
        self.ui.hotkey_edit.setText(key_combination)

        # 取消监听
        keyboard.unhook(self._hotkey_listener)
        delattr(self, '_hotkey_listener')

        # 保存热键（可以在这里调用实际的热键注册逻辑）
        self._register_hotkey(key_combination)

        key_combination = "+".join(modifiers + [event.name.upper()])
        self.ui.hotkey_edit.setText(key_combination)  # 确保这行被执行
        print(f"[DEBUG] 新热键: {key_combination}")  # 调试

    def _cancel_hotkey_listening(self):
        """取消热键监听（超时或手动取消）"""
        if hasattr(self, '_hotkey_listener'):
            keyboard.unhook(self._hotkey_listener)
            delattr(self, '_hotkey_listener')
            self.ui.hotkey_edit.setText("未设置")  # 或恢复之前的热键

    def _register_hotkey(self, hotkey):
        """实际注册热键（示例）"""
        print(f"注册热键: {hotkey}")
        # 示例：使用 keyboard 注册热键
        try:
            if hasattr(self, '_current_hotkey'):
                keyboard.remove_hotkey(self._current_hotkey)
            self._current_hotkey = keyboard.add_hotkey(hotkey.lower(), self._on_hotkey_triggered)
        except ValueError as e:
            print(f"热键注册失败: {e}")
            self.ui.hotkey_edit.setText("热键冲突！")

    def _on_hotkey_triggered(self):
        """热键触发时的回调"""
        print("热键被触发！")
        # 在这里执行你的功能，例如显示/隐藏窗口

    def closeEvent(self, event):
        """重写关闭事件（点击X时最小化到托盘）"""
        if self.isVisible():
            self.hide()
            event.ignore()
