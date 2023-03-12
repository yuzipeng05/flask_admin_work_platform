# 【Python成长之路】基于Flask-admin库，编写个人工作平台代码 -- 进阶版

## 1、基础功能版

之前已经写过Flask_Admin库的基础应用，

[《【Python成长之路】基于Flask-admin库，编写个人工作平台代码详述》]: https://mp.weixin.qq.com/s?__biz=MzI5ODQxNTA0OA==&amp;mid=2247484442&amp;idx=1&amp;sn=3457ea9638c14052ad4b833f0d62374f&amp;chksm=eca762bddbd0ebab6451aece17a9510555300579ebc454e3cfd5d1a3fe218f11ecb2971035d9&amp;token=1497085470&amp;lang=zh_CN#rd

但是在后续工作使用中，发现有新的需求功能需要添加，因此有了此篇的进阶版。

进阶版主要功能如下：

**（1）支持快速查看详情功能**

**（2）支持数据导出功能** 

**（3）支持自定义功能实现**

**（4）支持搜索结果总数显示**

**（5）改进表格展示方式**



## 2、快速查看详情功能

为了快速查看某条数据的所有信息 ，可以在视图实例代码中，可以打开can_view_details形状，如

```python
class WorkAdmin(CustomView):
	XXXX
	# 以下是新增代码
    can_view_details = True

```

效果如下：

在每条数据前面有个小眼睛，点击后即可查看详情。

![image-20230312095153474](https://gitee.com/yzp_2020/drawing-bed/raw/master/202303120951574.png)

![image-20230312095130107](https://gitee.com/yzp_2020/drawing-bed/raw/master/202303120951219.png)

其他常用视图实例开关可参考：

https://www.cnblogs.com/jackadam/p/12133021.html



## 3、数据导出功能

为了实现数据展出功能，有两处代码需要修改。

![image-20230312100639499](https://gitee.com/yzp_2020/drawing-bed/raw/master/202303121006566.png)

**（1）界面添加导出按钮，修改文件为templates\list.html** 

```html
# 以下是新增代码
{% if admin_view.can_create %}
    <div class="btn-menu">
      <a href="{{ url_for('.create_view', url=return_url) }}" class="btn btn-primary pull-right">{{ _gettext('Create') }}</a>
    </div>
{% endif %}

```

**（2）在视图代码中打开 导出开关**

```python
class WorkAdmin(CustomView):
	XXXX
	# 以下是新增代码
    can_export = True
```

最后数据会以csv文件格式进行导出，但是中文会有乱码问题，当前暂未解决。当然，也支持各类条件过滤后的结果导出。

## 4、自定义功能实现

当前框架默认支持的功能只有增删改查等功能，比如界面添加对应数据的后处理，则需要自定义功能开发了。大致效果如下：

![image-20230312102328935](https://gitee.com/yzp_2020/drawing-bed/raw/master/202303121023028.png)

修改代码如下：

```python
class WorkAdmin(CustomView):
	xxxx
	# 以下是新增代码
    from flask_admin.actions import action
    @action('myaction', 'MyAction', '自定义功能的描述')
    def action_approve(self, ids):
        print(ids)
        # 后续即基于id值可以在数据库中拿到完整的数据内容，从而进行数据二次处理
```

目前了解到 ，自定义action只能传id值，其他参数不支持。拿 到id后再到 数据库里进行查询，就可以拿到 完整的数据信息了。

## 5、搜索结果总数显示

由于界面显示是由templates\list.html 定义的，因此当添加搜索结果时，自然需要修改list.html文件

效果如下：

![image-20230312094637455](https://gitee.com/yzp_2020/drawing-bed/raw/master/202303120946569.png)

修改内容如下：

```html
<h2 id="brand">{{ admin_view.name|capitalize }} 列表</h2>
# 以下是新增代码
<h4>{{ _gettext('当前总数为: ') }}{% if count %} {{ count }}{% endif %}</h4>
```

当前可以对h4标签进行添加sytle，从而对显示文字颜色、大小等修改，具体css代码可自行百度。

## 6、优化表格展示方式

当前框架对超过一定长度的单元格内容会自动设置换行，但是如果表格标题太多，比如10+，其中又有多个列是超长文件，就会有滑动条生成。虽然也能查看，但是对用户体验不佳，比如我自己更愿意所有数据在一页内呈现。

![image-20230312102855923](https://gitee.com/yzp_2020/drawing-bed/raw/master/202303121028036.png)

那么为了实现单页内呈现的功能，需要对list.html进行。

主要是对表格内容（model_menu_bar）里对源框架的list.html重定义，设置td标签的最大宽度为100px，并自动换行和英文单词强行切分

```html
{% block model_menu_bar %}
# 以下是新增代码
	<style>
        td {
            max-width:100px;
            word-wrap:break-word;
            word-break:break-all;
        }
	</style>
{% endblock %}
```



