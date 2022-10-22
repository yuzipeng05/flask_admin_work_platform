import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor, CKEditorField
import flask_admin as admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import form

# Create application
app = Flask(__name__)

# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = '123456790'

# Create in-memory database
app.config['DATABASE_FILE'] = 'sample_db.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE_FILE']
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)
ckeditor = CKEditor(app)  # 初始化扩展
app.app_context().push()


# Customized admin interface
class CustomView(ModelView):
    list_template = 'list.html'
    create_template = 'create.html'
    edit_template = 'edit.html'


# Models
class Work(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode(64), nullable=False)
    owner = db.Column(db.Unicode(64))
    time = db.Column(db.DateTime, default=datetime.datetime.now())
    priority = db.Column(db.Unicode(64))
    content = db.Column(db.Text)

    def __unicode__(self):
        return self.name


class WorkAdmin(CustomView):
    form_overrides = dict(content=CKEditorField)  # 重写表单字段，将 text 字段设为 CKEditorField
    column_searchable_list = ('title', 'owner', 'content')
    column_filters = ('time', 'priority')
    form_extra_fields = {
        'priority': form.Select2Field('priority', choices=[(0, '高'), (1, '中'), (2, '低')])
    }


# 自定义视图
from flask_admin.base import BaseView, expose
class MyView(BaseView):
    def __init__(self, myurl, name=None, category=None, endpoint=None):
        super(MyView, self).__init__()
        self.myurl = myurl
        self.name = name
        self.category = category
        self.endpoint = endpoint

    @expose('/')
    def index(self):
        return self.render('mylink.html', myurl=self.myurl)


# Flask views
@app.route('/')
def index():
    return '<a href="/admin/">Click me to get to Admin!</a>'


# Create admin with custom base template
admin = admin.Admin(app, 'Example: Layout-BS3', base_template='layout.html', template_mode='bootstrap3')
# Add views
admin.add_view(WorkAdmin(Work, db.session, name='工作待办'))
# 超链接添加（系统自带）
from flask_admin.base import MenuLink
admin.add_link(MenuLink(name='百度', url='https://www.baidu.com/', category='链接'))
# 添加自定义视图
admin.add_view(MyView(myurl='https://flask-admin.readthedocs.io/en/v1.6.0/', name='Flask-Admin官方文档', endpoint='1', category='链接'))
admin.add_view(MyView(myurl='http://www.google.cn/', name='谷歌', endpoint='2', category='链接'))


# 文件管理
from flask_admin.contrib.fileadmin import FileAdmin
path = 'D:\\python_project\\flask-admin\\examples\\custom-layout'
admin.add_view(FileAdmin(path, 'file', name='文件管理'))



if __name__ == '__main__':
    # Start app
    app.run(debug=True)
