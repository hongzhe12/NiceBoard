import io
import os
from datetime import datetime

import pandas as pd
import qrcode
from bs4 import BeautifulSoup
from flask import Flask, render_template, send_from_directory
from flask import redirect, url_for, flash
from flask import request  # 确保导入了 request
from flask import send_file
from sqlalchemy.orm import sessionmaker
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from models import ClipboardItem, AppSettings, engine, session_scope
import base64

import os
os.environ['FLASK_SOCKETIO_ASYNC_MODE'] = 'threading'  # 强制锁定异步模式
os.environ['EVENTLET_MONKEY_PATCH'] = 'false'         # 禁用 eventlet 猴子补丁

# 初始化Flask应用
app = Flask(__name__)
app.secret_key = "supersecretkey"  # 设置一个密钥用于flash消息
socketio = SocketIO(app, async_mode='threading',engineio_logger=True)  # 使用 threading 模式
# socketio = SocketIO(app)  # 使用 threading 模式

# 创建数据库会话
Session = sessionmaker(bind=engine)
session = Session()


# ------------------------------
# ClipboardItem 功能
# ------------------------------
# 配置文件上传的路径
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'xls', 'xlsx'}



@app.route('/')
def index():
    return redirect(url_for('clipboard_list'))


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/clipboard/listen')
def clipboard_listen():
    # 二维码内容为监听地址（PC端访问）
    qr_url = request.host_url.rstrip('/') + '/clipboard/send'
    qr_img = qrcode.make(qr_url)
    buffer = io.BytesIO()
    qr_img.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    qr_data_uri = f"data:image/png;base64,{qr_base64}"

    return render_template('clipboard_listen.html',qr_data_uri=qr_data_uri)


def is_mobile():
    user_agent = request.user_agent.string.lower()
    mobile_keywords = ['iphone', 'android', 'webos', 'blackberry',
                      'windows phone', 'mobile', 'ipod', 'ipad']
    return any(keyword in user_agent for keyword in mobile_keywords)

@app.route('/clipboard/send', methods=['GET', 'POST'])
def clipboard_send():
    if request.method == 'POST':
        text = request.form.get('text_content', '').strip()
        uploaded_file = request.files.get('file')

        if text:
            socketio.emit('new_content', {'text': text})
        elif uploaded_file and uploaded_file.filename:
            filename = secure_filename(uploaded_file.filename)
            path = os.path.join(UPLOAD_FOLDER, filename)
            uploaded_file.save(path)
            socketio.emit('new_content', {
                'filename': filename,
                'file_url': f'/uploads/{filename}'
            })
        return '已发送'


    return render_template('clipboard_send.html')


# 检查文件扩展名是否允许
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/bookmark/import', methods=['GET', 'POST'])
def bookmark_import():
    """导入浏览器导出的书签 HTML 文件，存入 ClipboardItem"""
    # 检查上传目录
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    if request.method == 'POST':
        file = request.files.get('file')

        if file and file.filename.endswith('.html'):
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            try:
                # 用 BeautifulSoup 解析 HTML
                with open(filepath, 'r', encoding='utf-8') as f:
                    soup = BeautifulSoup(f, 'html.parser')

                links = soup.find_all('a')

                for link in links:
                    href = link.get('href')
                    title = link.get_text()

                    if href:
                        # 这里将 href 存到 content，title 存到 tags
                        new_item = ClipboardItem(
                            content=href,
                            tags=title,
                            timestamp=datetime.now()
                        )
                        session.add(new_item)

                session.commit()
                flash("书签导入成功")

            except Exception as e:
                flash(f"导入失败: {e}")

            return redirect(url_for('clipboard_list'))

        else:
            flash("请上传有效的 HTML 书签文件")
            return redirect(url_for('bookmark_import'))

    return render_template('bookmark_import.html')


@app.route('/clipboard/import', methods=['GET', 'POST'])
def clipboard_import():
    """导入Excel文件中的ClipboardItems"""
    # 检查是否创建了上传文件夹
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    if request.method == 'POST':
        # 获取上传的文件
        file = request.files.get('file')

        if file and allowed_file(file.filename):
            # 保证文件名安全
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            try:
                # 使用pandas读取Excel文件
                df = pd.read_excel(filepath)

                # 假设Excel中有 'content' 和 'tags' 两列
                for _, row in df.iterrows():
                    content = row['content']
                    tags = row['tags'] if 'tags' in row else None

                    # 将数据保存到数据库
                    new_item = ClipboardItem(content=content, tags=tags, timestamp=datetime.now())
                    session.add(new_item)
                session.commit()

                flash("导入成功")
            except Exception as e:
                flash(f"导入失败: {e}")

            return redirect(url_for('clipboard_list'))

        else:
            flash("请上传有效的Excel文件")
            return redirect(url_for('clipboard_import'))

    return render_template('clipboard_import.html')


@app.route('/clipboard/export')
def clipboard_export():
    # 使用 session 查询数据
    session = Session()
    items = session.query(ClipboardItem).all()

    # 构建 DataFrame
    df = pd.DataFrame([{
        'ID': item.id,
        '内容': item.content,
        '标签': item.tags,
        '时间戳': item.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    } for item in items])

    # 写入到内存中的 Excel 文件
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='剪贴板')

    output.seek(0)
    return send_file(
        output,
        as_attachment=True,
        download_name='剪贴板导出.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )


@app.route('/clipboard/list', methods=['GET'])
def clipboard_list():
    """显示所有 ClipboardItem 的列表，带分页"""
    with session_scope() as local_session:
        page = request.args.get('page', 1, type=int)  # 获取当前页码，默认为第一页
        per_page = 10  # 每页显示的项目数量

        total_items = local_session.query(ClipboardItem).count()
        total_pages = (total_items + per_page - 1) // per_page

        items = local_session.query(ClipboardItem).order_by(ClipboardItem.timestamp.desc()) \
            .offset((page - 1) * per_page).limit(per_page).all()

        # 生成简化页码列表
        def get_pagination_range(current, total):
            if total <= 5:
                return list(range(1, total + 1))
            elif current < 4:
                return [1, 2, 3, 4, 5, None, total]
            elif current > total - 3:
                return [1, None] + list(range(total - 4, total + 1))
            else:
                return [1, None] + list(range(current - 2, current + 3)) + [None, total]

        pagination_range = get_pagination_range(page, total_pages)

        return render_template(
            'clipboard_list.html',
            items=items,
            current_page=page,
            total_pages=total_pages,
            per_page=per_page,
            pagination_range=pagination_range
        )


@app.route('/clipboard/create', methods=['GET', 'POST'])
def clipboard_create():
    """创建新的 ClipboardItem"""
    if request.method == 'POST':
        content = request.form.get("content", "").strip()
        tags = request.form.get("tags", "").strip()

        if not content or len(content) > 5000:
            flash("内容不能为空且长度不得超过5000字符")
            return redirect(url_for('clipboard_create'))
        if tags and any(len(tag) > 50 for tag in tags.split(',')):
            flash("每个标签长度不得超过50字符")
            return redirect(url_for('clipboard_create'))

        new_item = ClipboardItem(content=content, tags=tags, timestamp=datetime.now())
        session.add(new_item)
        session.commit()
        flash("创建成功")
        return redirect(url_for('clipboard_list'))

    return render_template('clipboard_create.html')


@app.route('/clipboard/detail/<int:id>', methods=['GET'])
def clipboard_detail(id):
    """查看指定 ClipboardItem 的详情"""
    item = session.query(ClipboardItem).filter_by(id=id).first()
    if not item:
        flash("记录不存在")
        return redirect(url_for('clipboard_list'))
    return render_template('clipboard_detail.html', item=item)


@app.route('/clipboard/update/<int:id>', methods=['GET', 'POST'])
def clipboard_update(id):
    """更新指定 ClipboardItem"""
    item = session.query(ClipboardItem).filter_by(id=id).first()
    if not item:
        flash("记录不存在")
        return redirect(url_for('clipboard_list'))

    if request.method == 'POST':
        content = request.form.get("content", "").strip()
        tags = request.form.get("tags", "").strip()

        if not content or len(content) > 5000:
            flash("内容不能为空且长度不得超过5000字符")
            return redirect(url_for('clipboard_update', id=id))
        if tags and any(len(tag) > 50 for tag in tags.split(',')):
            flash("每个标签长度不得超过50字符")
            return redirect(url_for('clipboard_update', id=id))

        item.content = content
        item.tags = tags
        item.timestamp = datetime.now()
        session.commit()
        flash("更新成功")
        return redirect(url_for('clipboard_list'))

    return render_template('clipboard_update.html', item=item)


@app.route('/clipboard/delete/<int:id>', methods=['POST'])
def clipboard_delete(id):
    """删除指定 ClipboardItem"""
    item = session.query(ClipboardItem).filter_by(id=id).first()
    if not item:
        flash("记录不存在")
        return redirect(url_for('clipboard_list'))

    session.delete(item)
    session.commit()
    flash("删除成功")
    return redirect(url_for('clipboard_list'))


@app.route('/clipboard/search', methods=['GET'])
def clipboard_search():
    query = request.args.get("q", "").strip()  # 获取搜索关键字
    page = request.args.get("page", 1, type=int)  # 当前页码，默认为第一页
    per_page = 10  # 每页显示的项目数量

    # 查询数据库
    if not query:
        results = session.query(ClipboardItem).order_by(ClipboardItem.timestamp.desc())
    else:
        results = session.query(ClipboardItem).filter(
            ClipboardItem.content.contains(query) | ClipboardItem.tags.contains(query)
        ).order_by(ClipboardItem.timestamp.desc())

    total_items = results.count()
    total_pages = (total_items + per_page - 1) // per_page  # 计算总页数

    # 获取当前页的数据
    items = results.offset((page - 1) * per_page).limit(per_page).all()

    # 渲染模板并传递所有必要的变量
    return render_template(
        'clipboard_list.html',
        items=items,
        current_page=page,
        total_pages=total_pages,
        per_page=per_page,
        query=query
    )


# ------------------------------
# AppSettings 功能
# ------------------------------

@app.route('/settings/list', methods=['GET'])
def settings_list():
    """显示所有 AppSettings 的列表"""
    settings = session.query(AppSettings).all()
    return render_template('app_settings_list.html', settings=settings)


@app.route('/settings/create', methods=['GET', 'POST'])
def settings_create():
    """创建新的 AppSettings"""
    if request.method == 'POST':
        key = request.form.get("key", "").strip()
        value = request.form.get("value", "").strip()

        if not key or not value:
            flash("键和值都不能为空")
            return redirect(url_for('settings_create'))

        new_setting = AppSettings(key=key, value=value)
        session.add(new_setting)
        session.commit()
        flash("创建成功")
        return redirect(url_for('settings_list'))

    return render_template('app_settings_create.html')


@app.route('/settings/detail/<int:id>', methods=['GET'])
def settings_detail(id):
    """查看指定 AppSettings 的详情"""
    setting = session.query(AppSettings).filter_by(id=id).first()
    if not setting:
        flash("记录不存在")
        return redirect(url_for('settings_list'))
    return render_template('app_settings_detail.html', setting=setting)


@app.route('/settings/update/<int:id>', methods=['GET', 'POST'])
def settings_update(id):
    """更新指定 AppSettings"""
    setting = session.query(AppSettings).filter_by(id=id).first()
    if not setting:
        flash("记录不存在")
        return redirect(url_for('settings_list'))

    if request.method == 'POST':
        key = request.form.get("key", "").strip()
        value = request.form.get("value", "").strip()

        if not key or not value:
            flash("键和值都不能为空")
            return redirect(url_for('settings_update', id=id))

        setting.key = key
        setting.value = value
        session.commit()
        flash("更新成功")
        return redirect(url_for('settings_list'))

    return render_template('app_settings_update.html', setting=setting)


@app.route('/settings/delete/<int:id>', methods=['POST'])
def settings_delete(id):
    """删除指定 AppSettings"""
    setting = session.query(AppSettings).filter_by(id=id).first()
    if not setting:
        flash("记录不存在")
        return redirect(url_for('settings_list'))

    session.delete(setting)
    session.commit()
    flash("删除成功")
    return redirect(url_for('settings_list'))

@app.route('/clipboard/cleanup')
def clipboard_cleanup():
    """删除所有没有标签的剪贴板记录"""
    try:
        # 找出 tags 为空或全是空白的记录
        items_to_delete = session.query(ClipboardItem).filter(
            (ClipboardItem.tags == None) | (ClipboardItem.tags == "")
        ).all()

        count = len(items_to_delete)

        for item in items_to_delete:
            session.delete(item)

        session.commit()
        flash(f"已清理 {count} 条无标签内容")
    except Exception as e:
        flash(f"清理失败: {e}")

    return redirect(url_for('clipboard_list'))


@app.route('/clipboard/export_selected', methods=['POST'])
def export_selected():
    selected_ids = request.form.getlist('selected_items')
    print("Received selected items:", selected_ids)  # 打印接收到的参数
    session = Session()
    items = session.query(ClipboardItem).filter(ClipboardItem.id.in_(selected_ids)).all()

    df = pd.DataFrame([{
        'ID': item.id,
        '内容': item.content,
        '标签': item.tags,
        '时间戳': item.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    } for item in items])

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='剪贴板')
    output.seek(0)

    return send_file(
        output,
        as_attachment=True,
        download_name='剪贴板选中导出.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

@app.teardown_request
def shutdown_session(exception=None):
    """确保请求结束后关闭会话"""
    if hasattr(app, 'db_session'):
        app.db_session.remove()



if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)


    # app.run(debug=True)
