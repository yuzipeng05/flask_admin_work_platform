# 【Python成长之路】基于Flask-admin库，编写个人工作平台代码 -- 进阶版

## 1、基础功能版

之前已经写过Flask_Admin库的基础应用，

[《【Python成长之路】基于Flask-admin库，编写个人工作平台代码详述》]: https://mp.weixin.qq.com/s?__biz=MzI5ODQxNTA0OA==&amp;mid=2247484442&amp;idx=1&amp;sn=3457ea9638c14052ad4b833f0d62374f&amp;chksm=eca762bddbd0ebab6451aece17a9510555300579ebc454e3cfd5d1a3fe218f11ecb2971035d9&amp;token=1497085470&amp;lang=zh_CN#rd

但是在后续工作使用中，发现有新的需求功能需要添加，因此有了此篇的进阶版。

进阶版主要功能如下：

**（1）支持快速查看详情功能**

**（2）支持数据导出 功能** 

**（3）支持自定义功能实现**

**（4）支持搜索结果总数显示**

**（5）改进表格展示方式**



2、快速查看详情功能

3、数据导出功能

4、自定义功能实现

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

6、优化表格展示方式