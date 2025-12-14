import logging
import os
import inspect
from pathlib import Path


class SimpleLogger:
    """简单易用的日志管理类"""

    def __init__(self, name='App', log_file=None, level='INFO'):
        """
        初始化日志器
        :param name: 日志器名称
        :param log_file: 日志文件路径，None表示只输出到控制台
        :param level: 日志级别 DEBUG/INFO/WARNING/ERROR/CRITICAL
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level.upper()))

        # 清除已有的处理器，避免重复
        self.logger.handlers.clear()

        # 创建格式化器
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # 文件处理器（如果指定了日志文件）
        if log_file:
            # 确保日志目录存在
            os.makedirs(os.path.dirname(log_file), exist_ok=True)
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def debug(self, message):
        """记录调试信息"""
        self.logger.debug(message)

    def info(self, message):
        """记录一般信息"""
        self.logger.info(message)

    def warning(self, message):
        """记录警告信息"""
        self.logger.warning(message)

    def error(self, message):
        """记录错误信息"""
        self.logger.error(f"{inspect.currentframe().f_lineno}: {message}")

    def critical(self, message):
        """记录严重错误信息"""
        self.logger.critical(f"{inspect.currentframe().f_lineno}: {message}")

BASE_DIR = Path(__file__).resolve().parent.parent
log_file = os.path.join(BASE_DIR,"logs","app.log")
logger = SimpleLogger('niceboard', log_file, 'DEBUG')