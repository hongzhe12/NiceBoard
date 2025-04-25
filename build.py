import PyInstaller.__main__

PyInstaller.__main__.run([
    "--noconfirm",
    "--onefile",
    "--windowed",
    "--icon=icons/favicon.ico",
    "--name=好贴板",
    "--add-data=static;static",
    "--add-data=templates;templates",
    "--add-data=uploads;uploads",
    "app.py"
])