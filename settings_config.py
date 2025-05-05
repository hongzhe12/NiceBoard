import base64
import json
from pathlib import Path
from typing import Any, Dict, Optional, TypedDict


class ConfigType(TypedDict):
    db_name: str
    host: str
    port: str
    username: str
    password: str
    enable: bool
    max_history: int
    hotkey: str
    auto_start: bool


class MyConfig:
    def __init__(self) -> None:
        # 默认配置
        self._default_config: ConfigType = {
            'db_name': '',
            'host': '',
            'port': '',
            'username': '',
            'password': '',
            'enable': False,
            'max_history': 100000,
            'hotkey': 'f9',
            'auto_start': True
        }

        # 配置文件路径
        self._config_path: Path = Path.home() / '.clipboard_manager' / 'db_config.json'
        self._config: ConfigType = self._load_config()

    def _load_config(self) -> ConfigType:
        """加载配置文件，合并默认配置和文件中的配置"""
        try:
            if not self._config_path.exists():
                print(f"配置文件不存在于 {self._config_path}，使用默认配置")
                return self._default_config.copy()

            print(f"从 {self._config_path} 加载配置文件")
            with open(self._config_path, 'r', encoding='utf-8') as f:
                loaded_config: Dict[str, Any] = json.load(f)

            # 验证并合并配置
            return self._validate_config(loaded_config)

        except json.JSONDecodeError:
            print(f"配置文件 {self._config_path} 格式错误，使用默认配置")
        except Exception as e:
            print(f"加载配置时出错: {str(e)}，使用默认配置")

        return self._default_config.copy()

    def _validate_config(self, config: Dict[str, Any]) -> ConfigType:
        """验证并清理配置"""
        validated_config = self._default_config.copy()

        for key, value in config.items():
            if key in validated_config:
                # 简单的类型检查
                if isinstance(value, type(validated_config[key])):
                    validated_config[key] = value
                else:
                    print(f"配置项 {key} 类型不匹配，使用默认值")

        return validated_config

    def save_config(self) -> bool:
        """保存当前配置到文件"""
        try:
            self._config_path.parent.mkdir(parents=True, exist_ok=True)

            with open(self._config_path, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"保存配置时出错: {str(e)}")
            return False

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """获取配置项"""
        return self._config.get(key, default)

    def set(self, key: str, value: Any) -> bool:
        """设置配置项，返回是否成功"""
        if key not in self._default_config:
            print(f"尝试设置无效的配置项: {key}")
            return False

        self._config[key] = value
        return True

    def get_all(self) -> ConfigType:
        """获取全部配置的副本"""
        return self._config.copy()

    def reload(self) -> None:
        """重新加载配置文件"""
        self._config = self._load_config()

    def import_config(self,base64_str) -> bool:
        """导入配置"""
        # 解码Base64字符串
        base64_str = base64.b64decode(base64_str).decode('utf-8')

        self._config = json.loads(base64_str)
        self.save_config()

        return True

    def export_config(self) -> None:
        """导出配置"""
        # 将配置转换为Base64字符串
        base64_str = base64.b64encode(json.dumps(self._config).encode('utf-8')).decode('utf-8')
        return base64_str


# 全局配置实例
config_instance = MyConfig()

