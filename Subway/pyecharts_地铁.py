#!/usr/bin/env python
# coding: utf-8

# In[4]:


from pyecharts.charts import *
from pyecharts.charts import Geo
from pyecharts import options as opts


# In[8]:


import pandas as pd
path = r"C:\Users\lenovo\Downloads\地铁线路\北京市地铁站数据.xls"
df = pd.read_excel(path)
print(df)


# In[15]:


lines = []
for i in range(len(df)-1):
    line = []
    line.append(df['站点名称'][i])
    line.append(df['站点名称'][i])
    lines.append(line)
print(lines)


# In[17]:


line_style = {
    'normal': {
        'width': 4,  # 设置线宽
        'shadowColor': 'rgba(0, 0, 0, .5)',  # 阴影颜色
        'shadowBlur': 10,  # 阴影大小
        'shadowOffsetY': 10,  # Y轴方向阴影偏移
        'shadowOffsetX': 10,  # x轴方向阴影偏移
        'curve': 0  # 线弯曲程度，1表示不弯曲
    }
}

geo = Geo(
    init_opts=opts.InitOpts(
        theme='light',
        # bg_color='balck',
        width='1200px',
        height='1000px'
    )
)
geo.add_schema(
    maptype="北京",
    center=[116.46, 39.92],
    zoom=3,
    itemstyle_opts=opts.ItemStyleOpts(color="#fff", border_width=1, border_color="#1E90FF"),
    emphasis_label_opts=opts.LabelOpts(is_show=False),
    emphasis_itemstyle_opts=opts.ItemStyleOpts(color="#FFFACD"),
    label_opts=opts.LabelOpts(is_show=True, font_size=16, font_style='italic', color='#1E90FF'),
)

stations = []
for idx, row in df.iterrows():
    geo.add_coordinate(row['站点名称'], row['经度'], row['纬度'])
    stations.append([row['站点名称'], 1])

for line in lines:
    # 线图
    geo.add(
        line,
        # 数据格式（from， to）
        data_pair=line,
        type_='lines',
        label_opts=opts.LabelOpts(is_show=False),
        symbol_size=8,
        symbol='emptyCircle',
        is_polyline=False,
        linestyle_opts=line_style,
        effect_opts={
            'show': False,
            'trailWidth': 1,
            'trailOpacity': 0.3,
            'trailLength': 0.4,
            'symbolSize': 8
        },
    )
geo.set_global_opts(
    legend_opts=opts.LegendOpts(
        is_show=True,
        legend_icon='circle',
        pos_left='left',
        pos_top='center',
        orient='vertical',
        # selected_mode='single'
    ),
)

geo.render_notebook()


# In[19]:


import random
# 虚假数据
province = [
    '广东',
    '湖北',
    '湖南',
    '四川',
    '重庆',
    '黑龙江',
    '浙江',
    '山西',
    '河北',
    '安徽',
    '河南',
    '山东',
    '西藏']
data = [(i, random.randint(50, 150)) for i in province]

geo = (
    Geo()
    .add_schema(maptype="china")
    .add("", data)
)
geo.render_notebook()


# In[ ]:




