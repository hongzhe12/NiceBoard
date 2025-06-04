import base64
import json
import os
from pathlib import Path
from typing import Any, Dict, Optional, Union
import yaml


class Config:
    """YAML配置文件管理器，提供简洁的字典式访问接口。

    特性：
    - 支持类似字典的访问方式
    - 自动处理文件读写
    - 支持点标记法访问嵌套键
    - 类型提示和文档齐全

    示例：
    >>> config = Config('settings.yaml')
    >>> config['database.host'] = 'localhost'
    >>> host = config['database.host']
    """

    def __init__(
            self,
            filepath: Union[str, Path],
            default: Optional[Dict[str, Any]] = None,
            auto_save: bool = False,
    ):
        """初始化配置管理器

        :param filepath: 配置文件路径
        :param default: 当文件不存在时的默认配置
        :param auto_save: 修改后是否自动保存
        """
        self._path = Path(filepath)
        self._auto_save = auto_save
        self._data: Dict[str, Any] = {}

        if default is not None and not self._path.exists():
            self._data = default.copy()
            self.save()
        self.load()

    def __getitem__(self, key: str) -> Any:
        """通过点标记法获取配置值"""
        keys = key.split('.')
        value = self._data
        for k in keys:
            if not isinstance(value, dict):
                raise KeyError(f"Invalid key path: {key}")
            value = value[k]
        return value

    def __setitem__(self, key: str, value: Any) -> None:
        """通过点标记法设置配置值"""
        keys = key.split('.')
        current = self._data

        for k in keys[:-1]:
            if k not in current or not isinstance(current[k], dict):
                current[k] = {}
            current = current[k]

        current[keys[-1]] = value

        if self._auto_save:
            self.save()

    def __contains__(self, key: str) -> bool:
        """检查配置键是否存在"""
        try:
            self[key]
            return True
        except KeyError:
            return False

    def get(self, key: str, default: Any = None) -> Any:
        """安全获取配置值，键不存在时返回默认值"""
        try:
            return self[key]
        except KeyError:
            return default

    def load(self) -> None:
        """从文件加载配置"""
        if not self._path.exists():
            return

        with open(self._path, 'r', encoding='utf-8') as f:
            self._data = yaml.safe_load(f) or {}

    def save(self) -> None:
        """保存配置到文件"""
        os.makedirs(self._path.parent, exist_ok=True)
        with open(self._path, 'w', encoding='utf-8') as f:
            yaml.dump(self._data, f, allow_unicode=True, sort_keys=False)

    def to_dict(self) -> Dict[str, Any]:
        """返回配置的字典副本"""
        return self._data.copy()

    def update(self, new_data: Dict[str, Any], save: Optional[bool] = None) -> None:
        """批量更新配置

        :param new_data: 要合并的字典
        :param save: 是否保存，None表示遵循auto_save设置
        """

        def deep_update(target: Dict, update: Dict) -> Dict:
            for k, v in update.items():
                if isinstance(v, dict):
                    target[k] = deep_update(target.get(k, {}), v)
                else:
                    target[k] = v
            return target

        deep_update(self._data, new_data)

        if save or (save is None and self._auto_save):
            self.save()

    def __repr__(self) -> str:
        return f"Config(filepath={str(self._path)!r}, data={self._data})"

    def import_config(self,base64_str) -> bool:
        """导入配置"""
        # 解码Base64字符串
        base64_str = base64.b64decode(base64_str).decode('utf-8')

        self.update(
            json.loads(base64_str)
        )
        self.save()

        return True

    def export_config(self) -> str:
        """导出配置"""
        # 将配置转换为Base64字符串
        # 将字典转换为JSON字符串，再编码为字节
        json_str = json.dumps(self.to_dict())
        byte_data = json_str.encode('utf-8')
        # 将字节数据进行Base64编码，然后解码为字符串
        base64_str = base64.b64encode(byte_data).decode('utf-8')
        return base64_str


appdata_dir = Path(os.getenv('APPDATA')) / '好贴板'
# 初始化配置
config_instance = Config(os.path.join(appdata_dir, 'config.yaml'))
