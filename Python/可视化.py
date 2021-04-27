import matplotlib.pylab as plt
import numpy as np

#解决中文显示问题
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus'] = False

#2019-2020年四大直辖市GDP对比条形图
city = ['北京市', '上海市', '天津市', '重庆市']
GDP_2019 = [35371, 38155, 14104, 23606]
GDP_2020 = [36102, 38700, 14083, 25002]
bar_width = 0.35

# 绘图
plt.bar(np.arange(4), GDP_2019, label = '2019年', color = 'steelblue', alpha = 0.8, width = bar_width)
plt.bar(np.arange(4) + bar_width, GDP_2020, label = '2020年', color = 'indianred', alpha = 0.8, width = bar_width)

# 添加轴标签
plt.xlabel('城市')
plt.ylabel('GDP')
plt.title('2019-2020年四大直辖市GDP对比条形图')

#增加刻度标签
plt.xticks(np.arange(4)+0.15, city)

#设置y轴的刻度范围
plt.ylim([0, 42000])

# 为每个条形图添加数值标签
for x2019, y2019 in enumerate(GDP_2019):
    plt.text(x2019-0.2, y2019+100, '%s' %y2019)
for x2020,y2020 in enumerate(GDP_2020):
    plt.text(x2020+0.2, y2020+100, '%s' %y2020)

#显示图例
plt.legend(loc='upper right')

plt.show()