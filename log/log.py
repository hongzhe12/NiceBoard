# 配置日志记录
import logging
import os

log_dir = os.path.join(os.getenv('APPDATA'), 'haotieban')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'app.log')

# 创建文件处理器并设置编码
file_handler = logging.FileHandler(log_file, encoding='utf-8')
file_handler.setLevel(logging.INFO)

# 创建格式化器并添加到处理器
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# 获取根记录器并添加处理器
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
root_logger.addHandler(file_handler)

if __name__ == "__main__":
    from log.log import logging as _log

    _log.info("测试")
