def load_db_config():
    """从配置文件加载数据库配置"""
    import json
    from pathlib import Path

    # 默认配置（当没有配置文件时使用）
    default_config = {
        'db_name': 'clipboard.db',
        'host': '',
        'port': '',
        'username': '',
        'password': '',
        'enable': False,
    }

    # 配置文件路径（~/.clipboard_manager/db_config.json）
    config_path = Path.home() / '.clipboard_manager' / 'db_config.json'

    try:
        if config_path.exists():
            print(f"尝试加载配置文件: {config_path}")
            with open(config_path, 'r', encoding='utf-8') as f:
                loaded_config = json.load(f)
                # 合并加载的配置和默认配置（确保所有字段都存在）
                result = {**default_config, **loaded_config}
                print(f"成功加载配置: {result}")
                return result
        print("配置文件不存在，返回默认配置")
        return default_config  # 配置文件不存在时返回默认配置
    except Exception as e:
        print(f"加载配置出错: {e}")
        return default_config  # 出错时返回默认配置


def save_db_config(config):
    """将数据库配置保存到配置文件"""
    try:
        import json
        import os

        # 确保配置目录存在
        config_dir = os.path.expanduser("~/.clipboard_manager")
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)

        # 配置文件路径
        config_path = os.path.join(config_dir, "db_config.json")

        print(f"尝试保存配置到文件: {config_path}")
        # 写入配置
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=4)
        print("配置保存成功")

    except Exception as e:
        show_message("错误", f"保存配置时出错: {str(e)}", is_error=True)
