import os
from pathlib import Path
from sqlalchemy import create_engine

# 获取数据库路径（返回字符串）
def get_db_path():
    appdata_dir = Path(os.getenv('APPDATA')) / '好贴板'
    appdata_dir.mkdir(exist_ok=True)
    return str(appdata_dir / 'clipboard_history.db')  # 关键修改：转换为字符串


print(get_db_path())