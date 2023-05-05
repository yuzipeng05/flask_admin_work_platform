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

# x =['苹果', '香蕉', '西瓜']
# y =[3.12, 1.03, 24.19]
# myline(x, y)
