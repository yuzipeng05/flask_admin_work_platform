import flask_admin as admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import form
from db_sql.mysqlite import *
from chart.line import *
from flask import render_template
import datetime
from flask_ckeditor import CKEditor, CKEditorField
from flask_admin.base import BaseView, expose
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask import request

# Create application
app = Flask(__name__)
CORS(app, resources=r'/*')

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
    can_view_details = True
    can_export = True
    form_extra_fields = {
        'priority': form.Select2Field('priority', choices=[(0, '高'), (1, '中'), (2, '低')])
    }

    from flask_admin.actions import action
    @action('myaction', 'MyAction', '自定义功能的描述')
    def action_approve(self, ids):
        print(ids)


class Price(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Unicode(64))
    price = db.Column(db.Float(64))

    def __unicode__(self):
        return self.name


class PriceAdmin(CustomView):
    column_searchable_list = ('price', 'type')

    from flask_admin.actions import action
    @action('figure', '绘制曲线图', )
    def action_approve(self, ids):
        fruits = []
        prices = []
        for id in ids:
            tmp = query_data_by_id(int(id), table='price', mydb='instance\\sample_db.sqlite')
            fruits.append(tmp[1])
            prices.append(tmp[2])
        myline(fruits, prices)
        return render_template("line.html")

    @action('table', '前端表格展示', )
    def action_table(self, ids):
        data = [{
            'date': '2023/05/05',
            'name': '鹏哥',
            'address': 'test123456789'
        }]
        return render_template('table.html', data=data)


# 自定义视图
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


@app.route('/test', methods=['post', 'get'])
def test():
    if request.method == 'POST':
        print("********** post *************")
        data = request.get_json(silent=True)
        print(data['name'])
        print(data['region'])
    return render_template('form.html')


# Create admin with custom base template
admin = admin.Admin(app, 'Example: Layout-BS3', base_template='layout.html', template_mode='bootstrap3')
# Add views
admin.add_view(WorkAdmin(Work, db.session, name='工作待办'))
admin.add_view(PriceAdmin(Price, db.session, name='价格表'))
# 超链接添加（系统自带）
from flask_admin.base import MenuLink

admin.add_link(MenuLink(name='百度', url='https://www.baidu.com/', category='链接'))
# 添加自定义视图
admin.add_view(
    MyView(myurl='https://flask-admin.readthedocs.io/en/v1.6.0/', name='Flask-Admin官方文档', endpoint='1', category='链接'))
admin.add_view(MyView(myurl='http://www.google.cn/', name='谷歌', endpoint='2', category='链接'))

# 文件管理
from flask_admin.contrib.fileadmin import FileAdmin

path = 'D:\\'
admin.add_view(FileAdmin(path, 'file', name='文件管理'))

if __name__ == '__main__':
    # Start app
    app.run(debug=True)
