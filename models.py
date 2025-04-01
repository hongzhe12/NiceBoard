from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import declarative_base # 在 2.0 及以后的版本中，需要从 sqlalchemy.orm 导入
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import atexit


import os
from pathlib import Path
from sqlalchemy import create_engine

# 获取数据库路径（返回字符串）
def get_db_path():
    appdata_dir = Path(os.getenv('APPDATA')) / '好贴板'
    appdata_dir.mkdir(exist_ok=True)
    return str(appdata_dir / 'clipboard_history.db')  # 关键修改：转换为字符串

# 获取数据库文件路径
file_path = get_db_path()

# 初始化数据库
Base = declarative_base()
engine = create_engine(f'sqlite:///{file_path}', echo=False)  # 使用f-string确保路径格式正确
Session = sessionmaker(bind=engine)



class ClipboardItem(Base):
    """剪贴板历史记录模型"""
    __tablename__ = 'clipboard_history'
    id = Column(Integer, primary_key=True)
    content = Column(String(5000))  # 限制内容长度
    timestamp = Column(DateTime, default=datetime.now)
    is_favorite = Column(Boolean, default=False) # 是否收藏

    def __repr__(self):
        return f"<ClipboardItem(content='{self.content[:20]}...')>"


class AppSettings(Base):
    """精简版应用程序设置模型"""
    __tablename__ = 'app_settings'

    id = Column(Integer, primary_key=True)
    hotkey = Column(String(20), default='Alt+X')  # 热键组合
    max_history = Column(Integer, default=50)  # 最大记录数
    auto_start = Column(Boolean, default=False)  # 开机自启


def init_settings():
    """初始化默认设置"""
    session = Session()
    try:
        if not session.query(AppSettings).first():
            session.add(AppSettings())  # 使用所有默认值
            session.commit()
    except Exception as e:
        session.rollback()
        print(f"初始化设置失败: {e}")
    finally:
        session.close()


# 创建表（如果不存在）
Base.metadata.create_all(engine)

# 确保有默认设置
init_settings()


def get_settings():
    """快捷获取当前设置"""
    session = Session()
    try:
        return session.query(AppSettings).first()
    finally:
        session.close()


def update_settings(**kwargs):
    """更新设置项"""
    print(f"更新设置: hotkey={kwargs.get('hotkey')}, max_history={kwargs.get('max_history')}")
    session = Session()
    try:
        settings = session.query(AppSettings).first()
        for key, value in kwargs.items():
            setattr(settings, key, value)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        print(f"更新设置失败: {e}")
        return False
    finally:
        session.close()


def cleanup():
    """程序退出时关闭数据库连接"""
    engine.dispose()


def auto_clean_history():
    """自动清理历史记录，保持不超过最大限制，不删除收藏的记录"""
    session = Session()
    try:
        settings = session.query(AppSettings).first()
        print("最大上限：", settings.max_history)
        if not settings:
            return  # 无设置则不清理

        # 查询当前非收藏记录总数
        total = session.query(ClipboardItem).filter(ClipboardItem.is_favorite == False).count()
        if total <= settings.max_history:
            return  # 未超限，无需清理

        # 计算需要删除的数量
        excess = total - settings.max_history

        # 找出最旧的 `excess` 条非收藏记录并删除
        oldest_items = session.query(ClipboardItem) \
            .filter(ClipboardItem.is_favorite == False) \
            .order_by(ClipboardItem.timestamp.asc()) \
            .limit(excess) \
            .all()

        for item in oldest_items:
            session.delete(item)

        session.commit()
        print(f"自动清理了 {excess} 条旧记录")
    except Exception as e:
        session.rollback()
        print(f"自动清理失败: {e}")
    finally:
        session.close()

atexit.register(cleanup)