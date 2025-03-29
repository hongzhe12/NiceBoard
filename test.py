# 获取当前设置
from models import get_settings

settings = get_settings()

# 访问具体设置项
hotkey = settings.hotkey          # 获取热键组合（默认 'Alt+X'）
max_history = settings.max_history  # 获取最大历史记录数（默认 50）
auto_start = settings.auto_start   # 获取开机自启状态（默认 False）

print(f"当前热键: {hotkey}")
print(f"最大历史记录数: {max_history}")
print(f"开机自启: {'开启' if auto_start else '关闭'}")