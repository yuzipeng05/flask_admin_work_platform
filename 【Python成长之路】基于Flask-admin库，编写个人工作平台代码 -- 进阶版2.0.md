## 一、前言

前面已经做了Flask-admin库的基本介绍和几个库常用功能如何使用，若不了解请移步到以下博客：

1、[《【Python成长之路】基于Flask-admin库，编写个人工作平台代码详述》](https://mp.weixin.qq.com/s?__biz=MzI5ODQxNTA0OA==&mid=2247484442&idx=1&sn=3457ea9638c14052ad4b833f0d62374f&chksm=eca762bddbd0ebab6451aece17a9510555300579ebc454e3cfd5d1a3fe218f11ecb2971035d9&token=1046875879&lang=zh_CN#rd)

2、[《【Python成长之路】基于Flask-admin库，编写个人工作平台代码 -- 进阶版》](https://mp.weixin.qq.com/s?__biz=MzI5ODQxNTA0OA==&mid=2247484471&idx=1&sn=52adf93e6e355d97e72fa769dd0f1663&chksm=eca76290dbd0eb865f19c6864db43ab5fd47c0174a215a003561ec7fd94b2d6e519538c85943&token=1046875879&lang=zh_CN#rd)

此篇文章主要是讲述：

### 1、结合pyecharts库实现图表展示

### 2、结合flask+html+vue，实现后端数据在前端界面展示，以表格为例

### 3、结合flask+html+vue，实现前端界面数据回传后端

其中各功能效果如下图

**1、如何结合pyecharts库实现图表展示**

![image-20230505201234668](https://gitee.com/yzp_2020/drawing-bed/raw/master/202305052012740.png)

![image-20230505201123801](https://gitee.com/yzp_2020/drawing-bed/raw/master/202305052011319.png)



## 二、图表展示

### 1、增加数据库类和视图类

由于这里已经在之前文章讲过了，因此不再复述。直接上代码

```python
# 新增价格数据库类 
class Price(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Unicode(64))
    price = db.Column(db.Float(64))

    def __unicode__(self):
        return self.name

# 新增价格表的视图类
class PriceAdmin(CustomView):
    column_searchable_list = ('price', 'type')
	
    # 添加自定义功能：绘制图表
    from flask_admin.actions import action
    @action('figure', '绘制曲线图',)
    def action_approve(self, ids):
        fruits = []
        prices = []
        for id in ids:
            tmp = query_data_by_id(int(id), table='price', mydb='instance\\sample_db.sqlite')
            fruits.append(tmp[1])
            prices.append(tmp[2])
        # myline为自定义的画图函数，下面重点介绍
        myline(fruits,prices)
        return render_template("line.html")
```

### 2、利用pyecharts库生成图表

首先介绍下 **pyecharts官方指导文档：https://pyecharts.org/#/zh-cn/intro**

本文即使用Line图进行绘制图表，详细代码如下：

```python
from pyecharts.charts import Line
from pyecharts.globals import CurrentConfig
from pyecharts import options as opts
import os

CurrentConfig.ONLINE_HOST = "https://cdn.jsdelivr.net/npm/echarts@latest/dist/"

def myline(x, y):
    line = Line()
    line.add_xaxis(x)
    line.add_yaxis('价格', y)
    line.set_global_opts(title_opts=opts.TitleOpts(title="Line-基本示例", subtitle="价格表"))
    html_path = os.path.join(os.getcwd(), 'templates', 'line.html')
    print(html_path)
    line.render(html_path)
```

这里要解释下 ，为什么需要添加

```
CurrentConfig.ONLINE_HOST = "https://cdn.jsdelivr.net/npm/echarts@latest/dist/"
```

主要原因是如果不加这个配置，通过flask-admin加载line.html时会特别慢，体验效果很不好。因此通过CDN加速改变了网页源代码。

## 三、结合flask+html+vue，将后端数据传到前端

### 1、Vue组件示例网站介绍

在使用vue前，提供一个vue示例官网，从里面可以快速实现常用前端界面组件

**https://element.eleme.cn/#/zh-CN/component/installation**

![](https://gitee.com/yzp_2020/drawing-bed/raw/master/202305052028015.png)

### 2、结合html+vue，实现前端helloworld展示

为了方便使用，直接采用CDN方式进行安装vue

另外，目前可以通过 [unpkg.com/element-ui](https://unpkg.com/element-ui/) 获取到最新版本的资源，在页面上引入 js 和 css 文件即可开始使用。

helloworld.html代码样式如下 ：

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <!-- import CSS -->
  <link rel="stylesheet" href="https://unpkg.com/element-ui/lib/theme-chalk/index.css">
</head>
<body>
  <div id="app">
    <el-button @click="visible = true">Button</el-button>
    <el-dialog :visible.sync="visible" title="Hello world">
      <p>Try Element</p>
    </el-dialog>
  </div>
</body>
  <!-- import Vue before Element -->
  <script src="https://unpkg.com/vue@2/dist/vue.js"></script>
  <!-- import JavaScript -->
  <script src="https://unpkg.com/element-ui/lib/index.js"></script>
  <script>
    new Vue({
      el: '#app',
      data: function() {
        return { visible: false }
      }
    })
  </script>
</html>
```

### 3、编写前端示例代码(表格)

参考https://element.eleme.cn/#/zh-CN/component/table 章节，修改helloworld.html，实现前端表格代码。

主要是将<div id="app">和script中 的内容进行重新编写。

table.html代码如下：

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <!-- import CSS -->
    <link rel="stylesheet" href="https://unpkg.com/element-ui/lib/theme-chalk/index.css">
</head>
<body>
<div id="app">
    <template>
        <el-table
                :data="tableData"
                style="width: 100%">
            <el-table-column
                    prop="date"
                    label="日期"
                    width="180">
            </el-table-column>
            <el-table-column
                    prop="name"
                    label="姓名"
                    width="180">
            </el-table-column>
            <el-table-column
                    prop="address"
                    label="地址">
            </el-table-column>
        </el-table>
    </template>
</div>
</body>
<!-- import Vue before Element -->
<script src="https://unpkg.com/vue@2/dist/vue.js"></script>
<!-- import JavaScript -->
<script src="https://unpkg.com/element-ui/lib/index.js"></script>
<script>
    new Vue({
      el: '#app',
        data() {
        return {
          tableData: [{
            date: '2016-05-02',
            name: '王小虎',
            address: '上海市普陀区金沙江路 1518 弄'
          }]
        }
      }
    })
</script>
</html>
```

效果如下 ：

![image-20230505203918283](https://gitee.com/yzp_2020/drawing-bed/raw/master/202305052039389.png)

### 4、将后端数据传给前端并以表格形式展示

通过分析table.html可以发现，如果想要将后端数据传给前端并展示，关键是将script中的tableData内容进行更换，而这最简单的方式即通过{{ data|safe }}方式进行传递和赋值。

**后端python代码**

下面只是简单介绍如何将后端数据进行传递，实际应用中data应为数据库数据或者其他数据。

```python
    @action('table', '前端表格展示', )
    def action_table(self, ids):
        data = [{
            'date': '2023/05/05',
            'name': '鹏哥',
            'address': 'test123456789'
          }]
        # 将data数据进行入参传给table.html
        return render_template('table.html',data=data)
```

**前端html代码**

```html
# 其他都不变，仅变更tableData数据内容，通过{{ data|safe }}进行赋值
<script>
    new Vue({
      el: '#app',
        data() {
        return {
          tableData: {{ data|safe}}
        }
      }
    })
</script>
```

**效果如下：**

![image-20230505204827718](https://gitee.com/yzp_2020/drawing-bed/raw/master/202305052048818.png)



## 四、结合flask+html+vue，将前端数据传到后端

### 1、结合html+vue，编写前端示例代码(表单)

参考https://element.eleme.cn/#/zh-CN/component/form，实现前端表单展示

form.html代码示例如下

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <!-- import CSS -->
    <link rel="stylesheet" href="https://unpkg.com/element-ui/lib/theme-chalk/index.css">
</head>
<body>
<div id="app">
    <el-form ref="form" :model="form" label-width="80px">
        <el-form-item label="活动名称">
            <el-input v-model="form.name"></el-input>
        </el-form-item>
        <el-form-item label="活动区域">
            <el-select v-model="form.region" placeholder="请选择活动区域">
                <el-option label="区域一" value="shanghai"></el-option>
                <el-option label="区域二" value="beijing"></el-option>
            </el-select>
        </el-form-item>
        <el-form-item label="活动时间">
            <el-col :span="11">
                <el-date-picker type="date" placeholder="选择日期" v-model="form.date1"
                                style="width: 100%;"></el-date-picker>
            </el-col>
            <el-col class="line" :span="2">-</el-col>
            <el-col :span="11">
                <el-time-picker placeholder="选择时间" v-model="form.date2" style="width: 100%;"></el-time-picker>
            </el-col>
        </el-form-item>
        <el-form-item label="即时配送">
            <el-switch v-model="form.delivery"></el-switch>
        </el-form-item>
        <el-form-item label="活动性质">
            <el-checkbox-group v-model="form.type">
                <el-checkbox label="美食/餐厅线上活动" name="type"></el-checkbox>
                <el-checkbox label="地推活动" name="type"></el-checkbox>
                <el-checkbox label="线下主题活动" name="type"></el-checkbox>
                <el-checkbox label="单纯品牌曝光" name="type"></el-checkbox>
            </el-checkbox-group>
        </el-form-item>
        <el-form-item label="特殊资源">
            <el-radio-group v-model="form.resource">
                <el-radio label="线上品牌商赞助"></el-radio>
                <el-radio label="线下场地免费"></el-radio>
            </el-radio-group>
        </el-form-item>
        <el-form-item label="活动形式">
            <el-input type="textarea" v-model="form.desc"></el-input>
        </el-form-item>
        <el-form-item>
            <el-button type="primary" @click="onSubmit">立即创建</el-button>
            <el-button>取消</el-button>
        </el-form-item>
    </el-form>
</div>
</body>
<!-- import Vue before Element -->
<script src="https://unpkg.com/vue@2/dist/vue.js"></script>
<!-- import JavaScript -->
<script src="https://unpkg.com/element-ui/lib/index.js"></script>
<script>
    new Vue({
      el: '#app',
        data() {
      return {
        form: {
          name: '',
          region: '',
          date1: '',
          date2: '',
          delivery: false,
          type: [],
          resource: '',
          desc: ''
        }
      }
    },
    methods: {
      onSubmit() {
        this.$alert('submit!');
      }
    }
    })

</script>
</html>
```

效果如下 ：

![image-20230505210420402](https://gitee.com/yzp_2020/drawing-bed/raw/master/202305052104504.png)

### 2、编写前端axios方法及参数

从form.html代码中可 以爬到，立即创建按钮当前仅会弹窗功能，并未实现将数据往后端传递功能。

因此需要在前面使用axios发起请求。

本来想是参考以下代码实现axios请求，但是测试发现并不生效，并且报错： axios.post is not a function

```
onSubmit() {
	this.axios({
		method: 'post',
		url: '/test',
		data: {'aa':123},
	})
	.then((response) => {
        console.log(response)
	})
	.catch((error) => {
		console.log(error)
	})
},

```

定位发现是缺少安装axios。为了方便使用，继续使用CDN方式，即在script中添加

```
<script src="https://unpkg.com/axios/dist/axios.min.js"></script>
```

最终form.html内容如下：

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <!-- import CSS -->
    <link rel="stylesheet" href="https://unpkg.com/element-ui/lib/theme-chalk/index.css">
</head>
<body>
<div id="app">
    <el-form ref="form" :model="form" label-width="80px">
        <el-form-item label="活动名称" prop="name">
            <el-input v-model="form.name"></el-input>
        </el-form-item>
        <el-form-item label="活动区域" prop="region">
            <el-select v-model="form.region" placeholder="请选择活动区域">
                <el-option label="区域一" value="shanghai"></el-option>
                <el-option label="区域二" value="beijing"></el-option>
            </el-select>
        </el-form-item>
        <el-form-item label="活动时间">
            <el-col :span="11">
                <el-date-picker type="date" placeholder="选择日期" v-model="form.date1"
                                style="width: 100%;"></el-date-picker>
            </el-col>
            <el-col class="line" :span="2">-</el-col>
            <el-col :span="11">
                <el-time-picker placeholder="选择时间" v-model="form.date2" style="width: 100%;"></el-time-picker>
            </el-col>
        </el-form-item>
        <el-form-item label="即时配送" prop="delivery">
            <el-switch v-model="form.delivery"></el-switch>
        </el-form-item>
        <el-form-item label="活动性质" prop="type">
            <el-checkbox-group v-model="form.type">
                <el-checkbox label="美食/餐厅线上活动" name="type"></el-checkbox>
                <el-checkbox label="地推活动" name="type"></el-checkbox>
                <el-checkbox label="线下主题活动" name="type"></el-checkbox>
                <el-checkbox label="单纯品牌曝光" name="type"></el-checkbox>
            </el-checkbox-group>
        </el-form-item>
        <el-form-item label="特殊资源" prop="resource">
            <el-radio-group v-model="form.resource">
                <el-radio label="线上品牌商赞助"></el-radio>
                <el-radio label="线下场地免费"></el-radio>
            </el-radio-group>
        </el-form-item>
        <el-form-item label="活动形式" prop="desc">
            <el-input type="textarea" v-model="form.desc"></el-input>
        </el-form-item>
        <el-form-item>
            <el-button type="primary" @click="onSubmit">立即创建</el-button>
            <el-button @click="resetForm('form')">重置</el-button>
        </el-form-item>
    </el-form>
</div>
</body>
<!-- import Vue before Element -->
<script src="https://unpkg.com/vue@2/dist/vue.js"></script>
<!-- import JavaScript -->
<script src="https://unpkg.com/element-ui/lib/index.js"></script>
<script src="https://unpkg.com/axios/dist/axios.min.js"></script>
<script>
    new Vue({
      el: '#app',
        data() {
      return {
        form: {
          name: '',
          region: '',
          date1: '',
          date2: '',
          delivery: false,
          type: [],
          resource: '',
          desc: ''
        }
      }
    },
    methods: {
      onSubmit() {
        axios({
                method: 'post',
                url: '/test',
                data: {
                'name':this.form.name,
                'region':this.form.region,
                },
            })
            .then((response) => {
                console.log(response)
            })
            .catch((error) => {
                console.log(error)
            })
    },
          resetForm(formName) {
        this.$refs[formName].resetFields();
      }
    }
    })
</script>
</html>
```

这里再补充说明下，回传数据data的内容，即name/region都是form中定义好的。当前仅以name/region参数做演示，所有字段都可以进行传递。

另外，重置功能可 以简单地通过以下代码实现，但是有2个前置条件：

```
this.$refs[formName].resetFields();
```

**1、form组件上必须要有ref**

**2、form-item上必须要有prop属性**

即需要有以下 代码

```html
    <el-form ref="form" :model="form" label-width="80px">
    xxx
    <el-form-item label="活动名称" prop="name">
```

### 3、后端获取数据

**python代码如下**

```
from flask_cors import CORS
from flask import request

app = Flask(__name__)
CORS(app, resources=r'/*')

@app.route('/test', methods=['post', 'get'])
def test():
    if request.method == 'POST':
        print("********** post *************")
        data = request.get_json(silent=True)
        print(data['name'])
        print(data['region'])
    return render_template('form.html')
```

其中，CORS是为了解决跨域问题。

## 五、完整代码获取

github地址如下：





## FAQ

#### 1、报错：jinja2.exceptions.TemplateSyntaxError: unexpected char '\\' at 1100277

![image-20230422144135217](https://gitee.com/yzp_2020/drawing-bed/raw/master/202304221441369.png)

问题定位：通过升级pyecharts版本至最新版本解决；