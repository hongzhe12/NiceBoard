import sys
import os
import winreg as reg
from pathlib import Path

# 定义应用名称（推荐方式）
APP_NAME = "好贴板"  # 不需要加.exe后缀

def enable_auto_start():
    """Windows 启用开机自启动"""
    try:
        key = reg.HKEY_CURRENT_USER
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        registry_key = reg.OpenKey(key, key_path, 0, reg.KEY_WRITE)
        reg.SetValueEx(registry_key, APP_NAME, 0, reg.REG_SZ, sys.executable)
        reg.CloseKey(registry_key)
        return True
    except Exception as e:
        print(f"启用自启动失败: {e}")
        return False

def disable_auto_start():
    """Windows 禁用开机自启动"""
    try:
        key = reg.HKEY_CURRENT_USER
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        registry_key = reg.OpenKey(key, key_path, 0, reg.KEY_WRITE)
        reg.DeleteValue(registry_key, APP_NAME)
        reg.CloseKey(registry_key)
        return True
    except WindowsError as e:
        if e.winerror == 2:  # 文件不存在错误（未设置自启动）
            return True
        print(f"禁用自启动失败: {e}")
        return False
    except Exception as e:
        print(f"禁用自启动失败: {e}")
        return False