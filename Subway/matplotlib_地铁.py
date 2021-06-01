#!/usr/bin/env python
# coding: utf-8

# In[3]:


import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd


# In[11]:


path = r"C:\Users\lenovo\Downloads\地铁经纬度.xlsx"
df = pd.read_excel(path)
print(df)


# In[33]:


cnames = ['aliceblue', 'antiquewhite','aqua','aquamarine','azure','beige','bisque','black','blanchedalmond','blue','blueviolet','brown','burlywood','cadetblue','chartreuse','chocolate','coral','cornflowerblue','cornsilk','crimson','cyan','darkblue','darkcyan']


# In[36]:


plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.figure()
plt.figure(figsize=(10,10))
plt.title('地铁线路')
for i in range(0, len(df[20]), 2):
    plt.plot(df[i+1],df[i+2],color = 'black')
plt.show()

