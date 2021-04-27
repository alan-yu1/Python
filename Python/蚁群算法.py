import scipy.io as scio
import pandas as pd
import numpy as np
import math
import random

df = pd.read_csv('D:\\Program Files\\微信\\WeChat Files\\wxid_ihomrptambwl22\\FileStorage\\File\\2021-04\\vip1.csv', header = None)

c = [1, 2, 1, 2, 1, 4, 2, 2]
m = 50 # 蚂蚁数量
n = 9 # 城市数量
D = np.zeros([n,n])
for i in range(n):
    for j in range(n):
        D[i][j] = df[i][j]

Alpha = 1 # 信息素重要程度因子,一般[0,5]
Beta = 5 # 启发函数重要程度因子,一般[0,5]
Rho = 0.5 # 信息素挥发因子，一般[0.2,0.5]
Q = 1000 # 信息素常量，[10,10000]
Eta = np.zeros([n,n]) # 启发函数
for i in range(n):
    for j in range(n):
        Eta[i][j] = 1 / D[i][j] # 启发函数
Tau = np.ones([n,n]) # 信息素矩阵
for i in range(n):
    for j in range(n):
        Tau[i][j] = 20
Table = np.zeros([m,n]) # 路径记录表
iter = 1 # 迭代次数初值
iter_max = 10 # 最大迭代次数
Route_best = np.zeros([iter_max,n]) # 各代最佳路径
Length_best = np.zeros([iter_max,1]) # 各代最佳路径的长度
Length_ave = np.zeros([iter_max,1]) # 各代路径的平均长度

while iter <= iter_max:
    # 随机产生各个蚂蚁的起点城市
    for i in range(m):
        start = np.random.randint(1, n+1)
        Table[i][0] = start
        cap = c[start-1]
    # 构建解空间
    citys_index = [i for i in range(1,n+1)]
    # 逐个蚂蚁路径选择
    for i in range(m):
        # 逐个城市路径选择
        for j in range(1, n):
            tabu = Table[i][:j] # 已访问的城市集合（禁忌表）
            allow = []
            for k in range(n):
                if (citys_index[k] not in tabu) and (c[k] + cap <= 16):
                    allow.append(citys_index[k])
                else:
                    pass
            # 计算城市间转移概率
            P = np.zeros([len(allow)])
            for k in range(len(allow)):
                P[k] = math.pow(Tau[int(tabu[-1])-1][int(allow[k])-1],Alpha) * math.pow(Eta[int(tabu[-1])-1][int(allow[k])-1],Beta)
            Psum = sum(P)
            for k in range(len(P)):
                P[k] = P[k] / Psum
            rand = random.random()
            Psum = 0
            for k in range(len(P)):
                Psum += P[k]
                if rand <= Psum or not str(Psum).isdigit():
                    Table[i][j] = allow[k]
                    if cap > 8:
                        cap = c[k]
                    else:
                        cap += c[k]
                    break
                else:
                    pass
    # 计算各个蚂蚁的路径距离
    Length = np.zeros([m,1])
    for i in range(m):
        Route = Table[i][:]
        cap1 = c[int(Route[0])-1]
        for j in range(n-1):
            if cap1 < 8:
                Length[i] += D[int(Route[j])-1][int(Route[j+1])-1]
                cap1 += c[int(Route[j])-1]
            else:
                cap1 = c[int(Route[j])-1]

    # 计算最短路径距离及平均距离
    if iter == 1:
        for i in range(len(Length)):
            if Length[i] == min(Length):
                min_index = i
                break
        Length_best[0] = min(Length)
        Length_ave[0] = np.mean(Length)
        Route_best[0][:] = Table[min_index][:]
    else:
        min_Length = min(Length)
        for i in range(len(Length)):
            if Length[i] == min(Length):
                min_index = i
                break
        Length_best[iter-1] = min(Length_best[iter-2],min_Length)
        Length_ave[iter-1] = np.mean(Length)
        if Length_best[iter-1] == min_Length:
            Route_best[iter-1][:] = Table[min_index][:]
        else:
            Route_best[iter-1][:] = Route_best[iter-2][:]
        # 更新信息素
        Delta_Tau = np.zeros([n,n])
        # 逐个蚂蚁计算
        for i in range(m):
            # 逐个城市计算
            for j in range(n-2):
                Delta_Tau[int(Table[i][j])-1][int(Table[i][j+1])-1] += Q / Length[i]
            Delta_Tau[int(Table[i][n-1])-1][int(Table[i][0])-1] += Q / Length[i]
        Tau = (1-Rho) * Tau +Delta_Tau
    # 迭代次数加1，清空路径记录表
    iter += 1
    Table = np.zeros([m,n])

Shortest_Length = min(Length_best)
for i in range(len(Length_best)):
    if Length_best[i] == Shortest_Length:
        index = i
        break
Shortest_Route = Route_best[index][:]
print("最短距离：" + str(Shortest_Length))
print("最短路径：" + str(Shortest_Route))