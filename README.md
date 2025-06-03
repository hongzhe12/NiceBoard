# NiceBoard：多功能剪贴板管理工具

## 项目简介
NiceBoard 是一款基于 PySide6 和 Flask 开发的跨平台剪贴板管理工具，支持实时记录剪贴板内容、历史搜索、标签管理、多设备同步等功能。通过友好的界面和强大的配置选项，帮助用户高效管理剪贴板数据，提升工作效率。

---

![QQ_1748861813335](https://github.com/user-attachments/assets/3d98e40f-20b6-4958-a8c5-c1ffaca8371c)

![image](https://github.com/user-attachments/assets/6e1618d4-c66f-43d3-aaf7-211e1977dc1a)

![QQ_1748861865697](https://github.com/user-attachments/assets/83fb1914-de56-4261-8da4-3adc6d0585b3)

![QQ_1748861972989](https://github.com/user-attachments/assets/7238fbd5-946b-42bd-a920-bad22a457c5e)


## 核心功能
1. **剪贴板历史管理**
   - 自动记录所有复制内容，支持文本、文件（需通过 Web 端传输）
   - 历史记录按时间线展示，支持双击快速复制
   - 可设置最大记录数（默认 10000 条），自动清理旧记录

2. **高效搜索与标签系统**
   - 支持关键词搜索内容或标签（支持正则表达式）
   - 可为每条记录添加标签，通过标签快速过滤
   - 搜索结果实时高亮显示

3. **热键与系统托盘**
   - 自定义全局热键（默认 `F9`）快速唤起/隐藏界面
   - 系统托盘图标支持右键菜单操作（设置、清空历史、退出等）
   - 窗口置顶功能，支持拖动和圆角毛玻璃效果

4. **多设备同步（通过 Web 端）**
   - 内置 Flask 后端，支持局域网内设备互传文件/文本
   - 生成二维码供手机扫码连接，实现跨设备剪贴板同步
   - Web 管理界面支持数据导出/导入、远程查看历史记录

5. **丰富的配置选项**
   - 启用/禁用远程数据库（支持 PostgreSQL/SQLite）
   - 自定义热键、开机自启、界面样式
   - 导入/导出配置文件，支持 Base64 编码分享


## 技术架构
- **前端**：PySide6 实现原生 GUI，QSS 自定义样式
- **后端**：Flask + SocketIO 实现 Web 服务和实时通信
- **数据库**：SQLAlchemy 支持 SQLite（默认）和 PostgreSQL
- **热键监听**：pynput 实现全局键盘监听
- **文件处理**：openpyxl 解析 Excel，BeautifulSoup 解析书签 HTML


## 目录结构


```bash
NiceBoard/
├── app.py              # 主程序入口（GUI逻辑）
├── backend.py          # Flask后端服务
├── models.py           # 数据库模型与操作
├── hotkey_manager.py   # 热键管理模块
├── settings_window.py  # 设置窗口逻辑
├── resources_rc.py     # Qt资源文件（图标等）
├── templates/          # Flask模板文件（Web界面）
├── ui_clipboard_history.py # 编译后的UI文件
├── config.yaml         # 配置文件（需手动创建）
└── static/             # Web端静态资源
```


## 安装与运行
### 环境依赖
- Python 3.8+
- PySide6 >= 6.8.3
- Flask >= 2.3.2
- pynput, pyexcel, beautifulsoup4, sqlalchemy

### 安装命令
```bash
pip install -r requirements.txt
```

### 启动方式
1. **GUI 程序**  
   ```bash
   python app.py
   ```
   - 首次运行会自动创建配置文件和数据库

2. **Web 后端（多设备同步）**  
   ```bash
   python backend.py
   ```
   - 访问 `http://localhost:5000` 查看管理界面
   - 手机扫码 `http://<主机IP>:5000/clipboard/listen` 二维码可发送内容


## 使用说明
1. **热键操作**  
   - 按 `F9`（可自定义）唤起主窗口
   - 在历史记录列表中按 `Delete` 键删除选中项
   - 双击列表项自动复制内容并隐藏窗口

2. **标签管理**  
   - 右键点击记录 → "设置标签" 输入标签（多个用逗号分隔）
   - 在搜索框输入 `#标签名` 快速过滤该标签的记录

3. **多设备传输**  
   - 确保电脑和手机在同一局域网
   - 电脑端启动 Web 后端后，手机访问二维码页面发送文件/文本
   - 接收的文件会保存在 `uploads/` 目录


## 配置说明
### 基础配置（config.yaml）
```yaml
hotkey: F9           # 全局热键
max_history: 10000   # 最大记录数
auto_start: true     # 开机自启
enable_db: false     # 是否启用远程数据库（默认使用SQLite）
```

### 数据库配置（远程数据库需手动修改）
```python
# models.py 中修改数据库连接
if config_instance.get('enable_db', False):
    db_url = "postgresql://user:password@host:port/db_name"
else:
    db_url = "sqlite:///clipboard_history.db"
```


---

**好贴板，让效率触手可及，管理从未如此简单！**