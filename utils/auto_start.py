import winreg as reg
import sys
import os
from log.log import logging as _log


def enable_auto_start():
    try:
        exe_path = sys.executable
        work_dir = os.path.dirname(exe_path)
        command = f'"{exe_path}" --working-dir "{work_dir}"'

        key = reg.HKEY_CURRENT_USER
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        with reg.OpenKey(key, key_path, 0, reg.KEY_WRITE) as reg_key:
            reg.SetValueEx(reg_key, "好贴板", 0, reg.REG_SZ, command)
        _log.info("开机自启动设置成功")
        return True
    except Exception as e:
        _log.error(f"开机自启动设置失败: {e}")
        return False


def disable_auto_start():
    try:
        key = reg.HKEY_CURRENT_USER
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        with reg.OpenKey(key, key_path, 0, reg.KEY_WRITE) as reg_key:
            reg.DeleteValue(reg_key, "好贴板")
        _log.info("已禁用开机自启动")
        return True
    except WindowsError as e:
        if e.winerror == 2:  # 注册表项不存在
            return True
        _log.error(f"禁用开机自启动失败: {e}")
        return False
    except Exception as e:
        _log.error(f"禁用开机自启动失败: {e}")
        return False