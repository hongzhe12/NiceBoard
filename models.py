from PySide6.QtCore import QByteArray, QIODevice, QBuffer
from PySide6.QtWidgets import QApplication
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import atexit

# 初始化数据库
Base = declarative_base()
engine = create_engine('sqlite:///clipboard_history.db', echo=False)
Session = sessionmaker(bind=engine)

class ClipboardItem(Base):
    """剪贴板历史记录模型"""
    __tablename__ = 'clipboard_history'
    id = Column(Integer, primary_key=True)
    content = Column(String(5000))  # 限制内容长度
    timestamp = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<ClipboardItem(content='{self.content[:20]}...')>"

# 创建表（如果不存在）
Base.metadata.create_all(engine)

def cleanup():
    """程序退出时关闭数据库连接"""
    engine.dispose()

atexit.register(cleanup)