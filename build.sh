#!/bin/bash
# 激活虚拟环境
source .venv/Scripts/activate

# 执行打包
pyinstaller --noconfirm --onefile --windowed \
  --icon "icons/favicon.ico" \
  --name "NiceBoard" \
  --add-data "static;static" \
  --add-data "templates;templates" \
  --add-data "uploads;uploads" \
  --add-data "backen;backen" \
  --add-data "log;log" \
  --add-data "resources;resources" \
  --add-data "src;src" \
  --add-data "ui;ui" \
  --add-data "utils;utils" \
  --hidden-import "engineio.async_drivers.threading" \
  --hidden-import "flask_socketio" \
  --hidden-import "screenshot_preview_window.MyMainWindow" \
  --hidden-import "socketio" \
  src/app.py

# 打包完成提示
echo "打包完成！可执行文件在 dist/NiceBoard.exe"