# NiceBoard：跨平台剪贴板管理与多设备同步工具

## 项目简介
NiceBoard 是一款基于 PySide6 和 Flask 开发的全能型剪贴板管理工具，旨在解决现代办公中剪贴板内容管理效率低下、多设备数据同步困难等问题。通过强大的历史记录管理、智能搜索、标签分类及跨设备传输功能，帮助用户实现剪贴板内容的高效管理与无缝流转。


## 核心功能升级
### 1. **增强型剪贴板管理**
- **无限历史记录**：支持自定义最大记录数（默认10万条），自动清理旧记录，节省存储空间
- **内容去重**：自动检测重复内容，避免冗余记录
- **多格式支持**：除文本外，支持图片、文件（通过 Web 端）的预览与管理

### 2. **智能搜索与标签系统**
- **正则表达式搜索**：支持通过正则表达式进行内容匹配，精准定位目标记录
- **动态标签过滤**：标签支持多级分类，可通过标签快速筛选相关内容
- **搜索防抖优化**：输入延迟500ms触发搜索，减少无效查询

### 3. **多设备同步与 Web 管理**
- **局域网互传**：通过 SocketIO 实现电脑与手机/平板的实时数据同步
- **Web 控制台**：内置 Flask 管理界面，支持远程查看、导出剪贴板数据
- **二维码连接**：手机扫码快速建立连接，支持文件拖拽上传

### 4. **系统集成与扩展**
- **全局热键**：支持复杂组合热键（如 `Ctrl+Shift+X`），可自定义触发动作
- **开机自启**：自动随系统启动，保持剪贴板管理连续性
- **数据库扩展**：支持 SQLite/PostgreSQL/MySQL，满足不同场景存储需求


## 技术架构
- **前端**：PySide6 实现原生 GUI，QSS 自定义样式
- **后端**：Flask + SocketIO 实现 Web 服务和实时通信
- **数据库**：SQLAlchemy 支持 SQLite（默认）和 PostgreSQL
- **热键监听**：pynput 实现全局键盘监听
- **文件处理**：openpyxl 解析 Excel，BeautifulSoup 解析书签 HTML



## 目录结构说明
```
NiceBoard/
├── backen/              # Flask后端模块
│   ├── backend.py       # 核心服务逻辑
│   └── __init__.py      # 模块初始化
├── log/                 # 日志模块
│   ├── log.py           # 日志配置
│   └── __init__.py      # 
├── resources/           # 资源文件
│   ├── resources_rc.py  # Qt资源编译文件（图标等）
│   └── __init__.py      # 
├── src/                 # 核心应用模块
│   ├── app.py           # GUI主程序
│   ├── models.py        # 数据库模型与操作
│   ├── settings_window.py # 设置窗口逻辑
│   └── __init__.py      # 
├── templates/           # Flask模板文件
│   ├── clipboard_list.html # 剪贴板列表界面
│   └── ...              # 其他Web界面模板
├── ui/                  # UI文件
│   ├── clipboard_history.ui # 主界面UI定义
│   └── settings_window.ui # 设置界面UI定义
└── utils/               # 工具模块
    ├── auto_start.py    # 开机自启工具
    ├── config_set.py    # 配置文件管理器
    └── hotkey_manager.py# 热键管理类
```


## 安装与部署
### 环境依赖
- **基础环境**：Python 3.8+，PySide6>=6.8.3，Flask>=2.3.2
- **可选依赖**：
  - PostgreSQL/MySQL 驱动（用于远程数据库）
  - pyexcel, openpyxl（用于Excel导入/导出）
  - beautifulsoup4（用于书签解析）

### 安装命令
```bash
# 克隆项目
git clone https://github.com/your-username/NiceBoard.git
cd NiceBoard

# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Linux/macOS
.\venv\Scripts\activate   # Windows

# 安装依赖
pip install -r requirements.txt
```

### 启动方式
1. **GUI 程序**  
   ```bash
   python src/app.py
   ```
   - 首次运行会在 `%APPDATA%\好贴板` 生成配置文件和数据库

2. **Web 后端（多设备同步）**  
   ```bash
   python backen/backend.py
   ```
   - 访问 `http://localhost:5000` 进入管理界面
   - 手机扫码 `http://<主机IP>:5000/clipboard/listen` 连接

## 截图

![QQ_1748861813335](https://github.com/user-attachments/assets/3d98e40f-20b6-4958-a8c5-c1ffaca8371c)

![image](https://github.com/user-attachments/assets/6e1618d4-c66f-43d3-aaf7-211e1977dc1a)

![QQ_1748861865697](https://github.com/user-attachments/assets/83fb1914-de56-4261-8da4-3adc6d0585b3)

![QQ_1748861972989](https://github.com/user-attachments/assets/7238fbd5-946b-42bd-a920-bad22a457c5e)


## 使用指南
### 1. **基础操作**
- **唤起窗口**：默认热键 `F9`（可在设置中修改）
- **复制内容**：双击列表项自动复制，支持快捷键 `Ctrl+C`
- **删除记录**：选中项按 `Delete` 键或右键菜单删除

### 2. **高级功能**
- **标签管理**：右键点击记录 → "设置标签"，支持逗号分隔多个标签
- **数据导出**：选中记录后点击 "导出选中"，支持 Excel 格式
- **远程同步**：在 Web 端点击 "接收手机文件"，扫码后可传输文本/文件

### 3. **配置调整**
- **热键修改**：进入设置窗口 → "快捷热键"，按提示按下新组合键
- **数据库切换**：勾选 "启用远程数据库"，填写 PostgreSQL/MySQL 连接信息
- **同步历史**：在 Web 端 "设置" 中开启自动同步，数据实时跨设备更新

### 4. **代码片段存储与管理**

- **Gitee Gist 集成**：支持将代码片段一键保存至 Gitee 云端，自动生成可分享链接
- **内容去重机制**：上传前自动比对云端代码片段，相同内容仅更新不重复存储
- **自动识别代码类型**:（.py/.java/.cpp 等），生成带语法高亮的预览
- **跨设备同步**：代码片段与剪贴板历史联动，修改本地内容可自动同步至云端

## 配置示例
### 本地 SQLite 配置（默认）
```python
# utils/config_set.py
{
    "db_type": "sqlite",
    "db_name": "clipboard_history.db",
    "enable": false
}
```

### 远程 PostgreSQL 配置
```python
{
    "db_type": "postgresql",
    "host": "your-postgres-host",
    "port": "5432",
    "username": "postgres",
    "password": "your-password",
    "db_name": "niceboard_db",
    "enable": true
}
```


## 贡献与反馈
- **代码贡献**：欢迎提交 PR，需遵循 PEP8 规范并添加单元测试
- **问题反馈**：通过 GitHub Issues 提交 Bug，格式：`[BUG] 简短描述`
- **联系方式**：邮件联系 <hongzhe2022@163.com>

## 使用指南（新增章节）
1. **保存当前剪贴板为代码片段**：
   - 按 `F9` 唤起主窗口，选中目标剪贴板记录
   - 点击工具栏 "保存至 Gitee" 按钮或右键选择 "保存为代码片段"
   - 在弹出窗口中填写标题、选择语言类型（默认 `.py`）

2. **查看云端代码片段**：
   - 进入设置窗口 →  点击 "代码块授权" 按钮
    
1. **Gitee 令牌配置**：
   - 访问 Gitee 生成个人令牌（需勾选 `gist` 权限）
   - 进入 NiceBoard 设置 → "代码块授权" → 粘贴令牌至 "Access Token" 输入框
---

**文档更新时间**：2025年6月15日
