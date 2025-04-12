from flask import Flask, request, flash, redirect, url_for
from flask_admin import Admin, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.model.template import macro
from flask_babel import Babel
from flask_wtf import FlaskForm
from sqlalchemy import inspect, String, Text, or_
from wtforms import FileField

# 导入模型和会话
from models import ClipboardItem, Session, AppSettings, add_clipboard_item
from parsefile import parse_file

# 初始化 Flask 应用
app = Flask(__name__)
app.config['BABEL_DEFAULT_LOCALE'] = 'zh_CN'
app.config['SECRET_KEY'] = 'zaqhDCimU712GfS'

# 禁用 CSRF 验证
app.config['WTF_CSRF_ENABLED'] = False

babel = Babel(app)

# 定义导入表单
class ImportForm(FlaskForm):
    file = FileField('File')

    class Meta:
        csrf = False  # 确保表单本身不启用 CSRF


# 自定义通用视图类
class GenericModelView(ModelView):
    page_size = 5  # 每页显示的记录数
    can_export = True  # 启用导出功能
    can_create = True  # 启用创建功能
    can_edit = True  # 启用编辑功能
    can_search = True  # 启用搜索功能
    can_import = True  # 启用导入功能
    import_types = ['csv', 'xlsx']  # 支持的导入文件类型
    list_template = 'my_list.html'  # 使用自定义模板名称

    def __init__(self, model, session, **kwargs):
        super().__init__(model, session, **kwargs)
        # 动态设置列标签为字段名
        self.column_labels = {
            column.key: column.key.replace('_', ' ').title()
            for column in inspect(model).attrs
        }

        # 动态设置可搜索字段
        self.column_searchable_list = [
            column.key for column in inspect(model).attrs
            if isinstance(column.expression.type, (String, Text))  # 只对字符串字段启用搜索
        ]

        # 设置默认显示列
        self.column_list = [column.key for column in inspect(model).attrs]

    def render(self, template, **kwargs):
        # 添加导入 URL 到上下文
        kwargs['import_url'] = url_for('.import_view')
        return super().render(template, **kwargs)

    def get_query(self):
        search_term = request.args.get('search')
        query = super().get_query()
        if search_term:
            conditions = []
            for field in self.column_searchable_list:
                column = getattr(self.model, field)
                conditions.append(column.ilike(f'%{search_term}%'))
            query = query.filter(or_(*conditions))
        return query

    @expose('/import/', methods=('GET', 'POST'))
    def import_view(self):
        form = ImportForm(request.form)

        if request.method == 'POST' and form.validate():
            file = request.files.get('file')
            data = parse_file(file)
            # 注意：以下代码硬编码了字段名 '内容' 和 '标签'，
            # 对于其他模型，需要根据实际表头字段名进行修改
            for item in data:
                content = item.get('内容')  # 需要按照实际 Excel 表头索引
                tags = item.get('标签')
                # 注意：add_clipboard_item 是特定于 ClipboardItem 模型的插入函数，
                # 对于其他模型，需要编写对应的插入函数
                add_clipboard_item(content, tags)

            if file and self._is_file_allowed(file.filename):
                try:
                    # 文件处理逻辑（可以根据需求扩展）
                    flash('导入成功', 'success')
                    return redirect(url_for('.index_view'))
                except Exception as e:
                    flash(f'导入失败: {str(e)}', 'error')
            else:
                flash('无效的文件类型', 'error')

        return self.render('admin/import.html',
                           form=form,
                           macro=macro)

    def _is_file_allowed(self, filename):
        """检查文件类型是否允许"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.import_types

# 初始化 Flask-Admin
admin = Admin(
    app,
    name='剪贴板历史管理界面',
    template_mode='bootstrap4',  # 使用 Bootstrap 4 主题
    # index_view=AdminIndexView(name='Home')
)

# 添加视图
# 注意：当前导入逻辑是针对 ClipboardItem 模型编写的，
# 对于 AppSettings 模型或其他模型，导入逻辑可能不兼容
# 添加视图并指定中文名称
admin.add_view(GenericModelView(ClipboardItem, Session(), name='剪贴板历史记录', category='数据'))
admin.add_view(GenericModelView(AppSettings, Session(), name='应用设置', category='配置'))

# 首页路由
@app.route('/')
def home():
    return '<a href="/admin/">点击去管理面板</a>'

if __name__ == '__main__':
    app.run(port=5000, debug=True)