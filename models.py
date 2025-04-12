import os
from datetime import datetime
from pathlib import Path

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Index
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


# 获取数据库路径（返回字符串）
def get_db_path():
    """
    获取数据库文件的路径，如果应用数据目录不存在则创建它。
    :return: 数据库文件的完整路径字符串
    """
    appdata_dir = Path(os.getenv('APPDATA')) / '好贴板'
    appdata_dir.mkdir(exist_ok=True)
    return str(appdata_dir / 'clipboard_history.db')


# 获取数据库文件路径
file_path = get_db_path()
# 初始化数据库
Base = declarative_base()
engine = create_engine(f'sqlite:///{file_path}', echo=False)
Session = sessionmaker(bind=engine)


# 在ClipboardItem类中添加tags字段，并为content字段添加索引
class ClipboardItem(Base):
    """剪贴板历史记录模型"""
    __tablename__ = 'clipboard_history'
    id = Column(Integer, primary_key=True)
    content = Column(String(5000))
    timestamp = Column(DateTime, default=datetime.now)
    tags = Column(String(200), default="")

    def __repr__(self):
        return f"<ClipboardItem(content='{self.content[:20]}...')>"


# 为content字段添加索引
idx_clipboard_content = Index('idx_clipboard_content', ClipboardItem.content)


class AppSettings(Base):
    """精简版应用程序设置模型"""
    __tablename__ = 'app_settings'

    id = Column(Integer, primary_key=True)
    hotkey = Column(String(20), default='Alt+X')
    max_history = Column(Integer, default=50)
    auto_start = Column(Boolean, default=False)


def init_settings():
    """
    初始化应用程序的默认设置，如果设置表为空则插入默认设置。
    """
    session = Session()
    try:
        if not session.query(AppSettings).first():
            session.add(AppSettings())
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
    """
    快捷获取当前应用程序的设置。
    :return: AppSettings对象，如果没有则返回None
    """
    session = Session()
    try:
        return session.query(AppSettings).first()
    finally:
        session.close()


def update_settings(**kwargs):
    """
    更新应用程序的设置项。
    :param kwargs: 要更新的设置项和对应的值
    :return: 更新成功返回True，失败返回False
    """
    print(f"更新设置: hotkey={kwargs.get('hotkey')}, max_history={kwargs.get('max_history')}")
    session = Session()
    try:
        settings = session.query(AppSettings).first()
        if settings:
            for key, value in kwargs.items():
                setattr(settings, key, value)
            session.commit()
            return True
        return False
    except Exception as e:
        session.rollback()
        print(f"更新设置失败: {e}")
        return False
    finally:
        session.close()


def auto_clean_history():
    """
    自动清理剪贴板历史记录，保持记录数量不超过最大限制。
    """
    session = Session()
    try:
        settings = session.query(AppSettings).first()
        if not settings:
            return

        # 查询当前记录总数
        total = session.query(ClipboardItem).count()
        if total <= settings.max_history:
            return

        # 计算需要删除的数量
        excess = total - settings.max_history

        # 找出最旧的 `excess` 条记录并删除
        oldest_items = session.query(ClipboardItem) \
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


def find_tags_by_content(content):
    """
    根据剪贴板项的内容查找对应的标签。
    :param content: 剪贴板项的内容
    :return: 找到的剪贴板项的标签，如果未找到则返回空字符串
    """
    session = Session()
    try:
        item = session.query(ClipboardItem).filter(ClipboardItem.content == content).first()
        if item:
            return item.tags
        return ""
    except Exception as e:
        print(f"查找标签失败: {e}")
        return ""
    finally:
        session.close()


def update_tags_for_clipboard_item(content, new_tags):
    """
    更新指定剪贴板项的标签。
    :param content: 剪贴板项的内容
    :param new_tags: 新的标签，可以是单个标签字符串或多个标签用逗号分隔的字符串
    """
    session = Session()
    try:
        item = session.query(ClipboardItem).filter(ClipboardItem.content == content).first()
        if item:
            tag_list = [tag.strip() for tag in new_tags.split(',') if tag.strip()]
            item.tags = ','.join(sorted(tag_list))
            session.commit()
            print(f"成功更新内容为 {content} 的剪贴板项的标签为: {new_tags}")
        else:
            print(f"未找到内容为 {content} 的剪贴板项")
    except Exception as e:
        session.rollback()
        print(f"更新标签失败: {e}")
    finally:
        session.close()


def get_clipboard_history(limit=50):
    """
    从数据库加载剪贴板历史记录。
    :param limit: 要加载的记录数量上限，默认为50
    :return: 剪贴板历史记录列表
    """
    session = Session()
    try:
        items = session.query(ClipboardItem) \
            .order_by(ClipboardItem.timestamp.desc()) \
            .limit(limit) \
            .all()
        return items
    finally:
        session.close()


def add_clipboard_item(text,tags = ""):
    """
    添加新的剪贴板记录，如果记录已存在则不添加。
    :param text: 剪贴板记录的内容
    :return: 添加成功返回True，记录已存在或失败返回False
    """
    session = Session()
    try:
        # 检查是否已存在相同内容
        exists = session.query(ClipboardItem) \
            .filter(ClipboardItem.content == text) \
            .first()
        if not exists:
            # 插入新记录
            new_item = ClipboardItem(content=text,tags = tags)
            session.add(new_item)
            session.commit()
            return True
        return False
    except Exception as e:
        session.rollback()
        print(f"数据库错误: {e}")
        return False
    finally:
        session.close()


def delete_clipboard_item(content):
    """
    删除指定内容的剪贴板记录。
    :param content: 要删除的剪贴板记录的内容
    :return: 删除成功返回True，失败返回False
    """
    session = Session()
    try:
        session.query(ClipboardItem) \
            .filter(ClipboardItem.content == content) \
            .delete(synchronize_session=False)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        print(f"删除失败: {e}")
        return False
    finally:
        session.close()


def clear_all_clipboard_history():
    """
    清空所有剪贴板历史记录。
    :return: 清空成功返回True，失败返回False
    """
    session = Session()
    try:
        session.query(ClipboardItem).delete()
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        print(f"清空失败: {e}")
        return False
    finally:
        session.close()


def filter_clipboard_history(text, limit=50):
    """
    根据搜索文本过滤剪贴板历史记录，优先按标签搜索，其次按内容搜索。
    :param text: 搜索文本
    :param limit: 要返回的记录数量上限，默认为50
    :return: 过滤后的剪贴板历史记录列表
    """
    session = Session()
    try:
        # 优先按标签搜索
        tag_items = session.query(ClipboardItem) \
            .filter(ClipboardItem.tags.contains(text)) \
            .order_by(ClipboardItem.timestamp.desc()) \
            .limit(limit) \
            .all()
        tag_count = len(tag_items)

        if tag_count < limit:
            # 标签匹配数量不足，再按内容搜索补足
            remaining = limit - tag_count
            content_items = session.query(ClipboardItem) \
                .filter(ClipboardItem.content.contains(text)) \
                .filter(~ClipboardItem.id.in_([item.id for item in tag_items])) \
                .order_by(ClipboardItem.timestamp.desc()) \
                .limit(remaining) \
                .all()
            items = tag_items + content_items
        else:
            items = tag_items

        return items
    finally:
        session.close()
