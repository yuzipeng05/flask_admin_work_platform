## 一、个人工作平台展示



## 二、搭建过程

### 1、运行Flask-admin库样例custom-layout

下载代码：https://github.com/flask-admin/flask-admin.git

选择样例工程：flask-admin\examples\custom-layout

运行成功后效果如下图：

![](E:\俞子鹏\flask-admin学习\问题截图\custom-layout.png)

### 2、修改Home主页内容

Home内容是在templates/admin/index.html中定义的，可按自己效果修改对应，如下

```html
{% extends 'admin/master.html' %}
{% block body %}
{{ super() }}
<div class="row">
    <h1>个人工作事务平台</h1>
    <p class="lead">
        Created by 鹏哥贼优秀
    </p>
    <p>
        记录个人&工作事务，方便管理跟踪。
    </p>
    <a class="btn btn-primary" href="/"><i class="glyphicon glyphicon-chevron-left"></i> Back</a>
</div>
{% endblock body %}
```

解释：

（1）extends 'admin/master.html' 这里可能会疑问，为什么在admin目录下，并没有master.html文件。

这是因为master.html是定义在flask-admin库中，当前只是引用而已。如果你想修改master.html内容，可至如下路径进行修改：python安装目录\site-packages\flask_admin\templates\bootstrap3\admin\master.html

### 3、修改User/Page界面内容

由于原app.py脚本里自带数据库生成命令，执行成功后会在以下路径生成sqlite数据库（custom-layout\instance\sample_db.sqlite）。因此可以直接修改已有数据库表结构即可。

本人使用的数据库工具是：Navicat

#### （1）修改数据表结构

![](E:\俞子鹏\flask-admin学习\问题截图\navicat.png)

使用数据库工具重新设计表结构会比用python代码实现更方便

#### （2）修改数据表对应代码（增加数据库类和增加视图）

修改后的视图功能有：字段必填、字段设置日历图、字段默认值设置、富文本设置、下拉框设置、支持排序、支持类型搜索。对应效果如下图

![](E:\俞子鹏\flask-admin学习\问题截图\工作待办.png)

对应代码如下：

```python
# 增加数据库类
class Work(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode(64), nullable=False)  # 字段必填
    owner = db.Column(db.Unicode(64))
    time = db.Column(db.DateTime, default=datetime.datetime.now())  # 字段设置默认值
    priority = db.Column(db.Unicode(64))
    content = db.Column(db.Text)

    def __unicode__(self):
        return self.name

# 增加视图
class WorkAdmin(CustomView):
    form_overrides = dict(content=CKEditorField)  # 重写表单字段，将 text 字段设为 CKEditorField
    column_searchable_list = ('title', 'owner', 'content')
    column_filters = ('time', 'priority')
    form_extra_fields = {
        'priority': form.Select2Field('priority', choices=[(0, '高'), (1, '中'), (2, '低')])
    }

# Add views
admin.add_view(WorkAdmin(Work, db.session, name='工作待办'))
```

下面分别解释下各自小功能点的实现。

**A、字段必填：关键是在定义字段时添加nullable=False**

```python
title = db.Column(db.Unicode(64), nullable=False)
```

**B、字段设置日历图：将字段类型定义为db.DateTime，系统会自动设置成日历图格式**

```python
time = db.Column(db.DateTime, default=datetime.datetime.now())  # 字段设置默认值
```

<img src="E:\俞子鹏\flask-admin学习\问题截图\日历图.png" style="zoom:38%;" />

**C、设置默认值：关键添加default=XXXX**

> time = db.Column(db.DateTime, default=datetime.datetime.now())  # 字段设置默认值

**D、下拉框设置：在展示视图代码中添加form_extra_fields类。**

```
from flask_admin import form

form_extra_fields = {
'priority': form.Select2Field('priority', choices=[(0, '高'), (1, '中'), (2, '低')])
}
```

**E、富文本框设置**

这里有3处要修改：修改app.py和edit.html 、create.html

（1）在app.py中重定义content字段的类型

> form_overrides = dict(content=CKEditorField)  # 重写表单字段，将 text 字段设为 CKEditorField

（2）在edit.html和create.html的最后添加以下代码

```html
{% block tail %} <!-- 向父模板的 tail 块内追加内容 -->
    {{ super() }}
    {{ ckeditor.load() }} <!-- 加载 CKEditor 的 JavaScript 文件，默认从 CDN 获取 -->
{% endblock %}
```

**F、搜索功能设置**

```python
column_searchable_list = ('title', 'owner', 'content')  # 支持对应字段的精确、模糊匹配搜索
column_filters = ('time', 'priority') # 支持增加过滤器
```

![](E:\俞子鹏\flask-admin学习\问题截图\搜索功能.png)

**G、修改视图名称**

添加视图时默认是用数据库表名，可以通过设置name=xxx来修改视图名称

> admin.add_view(WorkAdmin(Work, db.session, name='工作待办'))

### 4、超链接视图添加

<img src="E:\俞子鹏\flask-admin学习\问题截图\超链接.png" style="zoom:38%;" />

这里使用的是Flask-admin库自带的MenuLink方法，但是MenuLink方法生成的超链接点击后，无法生成新页面进行跳转，而是基于本界面跳转到新url。

```python
from flask_admin.base import MenuLink
admin.add_link(MenuLink(name='百度', url='https://www.baidu.com/', category='链接'))
```

因此，如果是为了实现跳转到新界面的效果，需要自定义视图。详见第5节。

### 5、自定义视图

app.py脚本添加视图定义代码：

```python
from flask_admin.base import BaseView, expose
class MyView(BaseView):
    def __init__(self, url=None, name=None,category=None, endpoint=None):
        super(MyView, self).__init__()
        self.url = url
        self.name = name
        self.category = category
        self.endpoint = endpoint

    @expose('/')
    def index(self):
        return self.render('mylink.html', myurl=self.url)

# 添加自定义视图
admin.add_view(MyView(url='http://www.google.cn/', name='谷歌',endpoint='1'))
```

mylink.html代码如下：

```html
{% extends 'admin/master.html' %}
{% block body %}
<body>
<script LANGUAGE="javascript">
window.open('{{ myurl }}','_blank')
</script>
<p>
    正在前往：{{ myurl }}
</p>
</body>
{% endblock body %}
```

这里补充说明下，MyView类中为什么要继承父类BaseView的url、name、category、endpoint参数

url：这个不用解释，是我要打开的新网页网址

name：为了方便在界面上显示链接名称

category：是为了后续的目录管理，详见第6节

endpoint：是为了管理区分不同子页面，若endpoint='1'，则对应网址是：http://127.0.0.1:5000/admin/1/

### 6、目录管理

<img src="E:\俞子鹏\flask-admin学习\问题截图\目录管理.png" style="zoom:38%;" />

示例代码：

```python
admin.add_link(MenuLink(name='百度', url='https://www.baidu.com/', category='链接'))
# 添加自定义视图
admin.add_view(MyView(myurl='https://flask-admin.readthedocs.io/en/v1.6.0/', name='Flask-Admin官方文档', endpoint='1', category='链接'))
admin.add_view(MyView(myurl='http://www.google.cn/', name='谷歌', endpoint='2', category='链接'))
```

从这里可以看出，当category相同时，flask-admin框架会自动将所有视图进行合并到同一目录下。

如果想要添加子目录，

```python
admin.add_sub_category(name="子目录", parent_name="链接")
```

### 7、文件管理

![](E:\俞子鹏\flask-admin学习\问题截图\文件管理.png)

示例代码：

```python
# 文件管理
from flask_admin.contrib.fileadmin import FileAdmin
path = 'E:\\'
admin.add_view(FileAdmin(path, 'file', name='文件管理'))
```

这里可以自定义path路径，从而实现文件管理

------

## 三、总结

**至此，当前所有功能已经能满足本人平时工作管理的要求了，因此没有再深入flask-admin其他特性。**

**如果你有兴趣可以继续研究使用更多功能，比如用户登录管理、内容导出、与其他数据库配合使用等，网上也有很多相关大神总结可以参考。**



## 四、FAQ

### 1、执行报错 Working outside of application context.

![](E:\俞子鹏\flask-admin学习\问题截图\Working outside of application context.png)

```python
# Create in-memory database
app.config['DATABASE_FILE'] = 'sample_db.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE_FILE']
app.config['SQLALCHEMY_ECHO'] = True

# 新增以下代码
app.app_context().push()
```



### 2、自定义视图定义时报错：Attempted to instantiate admin view MyView without default view

![](E:\俞子鹏\flask-admin学习\问题截图\Attempted to instantiate admin view MyView without default view.png)

```python
# 原代码
from flask_admin.base import BaseView, expose
class MyView(BaseView):
    def __init__(self, name=None, category=None, endpoint=None, url=None):
        super(MyView, self).__init__()
        self.url = url
        self.name = name
        self.category = category
        self.endpoint = endpoint

    @expose('/link')
    def index(self):
        return self.render('mylink.html', myurl=self.url)
```

原先在自定义MyView视图时，是想直接继承父类BaseView，但是在运行时报错说defalut view未实例。后面查看官方指导，发现在使用expose装饰器时，是基于根目录，即

> @expose('/')

当前暂未清楚为什么不能基于/link目录，猜测flask-admin的Http目录是http://127.0.0.1:5000/admin/，如果变成http://127.0.0.1:5000/link则需要自己写个默认视图。





### 3、打开新页面不生效

原先这里是想打开百度网站的，并且{{myurl}}的值也的确是www.baidu.com

```html
{% extends 'admin/master.html' %}
{% block body %}
<body>
<script LANGUAGE="javascript">
window.open({{ myurl }},'_blank')
</script>
<p>
    正在前往：{{ myurl }}
</p>
</body>
{% endblock body %}
```

但实际效果时，并没有弹出新的界面。

最后发现这里代码有误

> window.open({{ myurl }},'_blank')

应该是：

> window.open('{{ myurl }}','_blank')



## 五、参考

1、Flask-admin官方指导：https://flask-admin.readthedocs.io/en/v1.6.0/

2、Flask-admin中文指导：http://flask123.sinaapp.com/article/57/

3、在 Flask-Admin 中集成富文本编辑器 CKEditor：CSDN搜索即可

