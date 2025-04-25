import os
from auto_py_to_exe.packaging import package

# 配置打包选项
pyinstaller_config = {
    "noconfirm": True,
    "filenames": ["app.py"],
    "onefile": True,
    "console": False,
    "icon_file": "icons/favicon.ico",
    "name": "好贴板",
    "clean_build": False,
    "strip": False,
    "noupx": False,
    "disable_windowed_traceback": False,
    "uac_admin": False,
    "uac_uiaccess": False,
    "argv_emulation": False,
    "bootloader_ignore_signals": False,
    "datas": [
        "static;static/",
        "templates;templates/",
        "uploads;uploads/"
    ]
}

if __name__ == "__main__":
    # 执行打包
    package(pyinstaller_config)
    print("打包完成！")