import numpy as np
import math
import random

# 参数设置 # 修改乘客总人数/断面客流以及时段数：结果根据时段产生（）
paramDict = {}
paramDict['L'] = 29  # 线路的长度，29千米
paramDict['station_amount'] = 27  # 线路站点数量
paramDict['speed'] = 30  # 车辆运行速度,20km/h
paramDict['pb_1'] = 10  # 小型车的购置成本，15元/小时/辆（50万元/辆）
paramDict['pb_2'] = 15  # 中型车的购置成本，30元/小时/辆（65万元/辆，算上补贴）
paramDict['pb_3'] = 20  # 大动车的购置成本，45元/小时/辆（100万元/辆，算上补贴）
paramDict['f_min'] = 3  # 最小发车频率为5辆/小时
paramDict['f_max'] = 20  # 最大发车频率为10辆/小时
paramDict['N_max'] = 20  # 最大能提供的车辆数目
paramDict['cap_1'], paramDict['cap_2'], paramDict['cap_3'] = 40, 60, 90  # 小、中、大型公交车的容量
paramDict['r_f'] = 0.8  # 公交车的满载率
paramDict['r_f1'] = 0.2  # 最低上车数
paramDict['total_passenger_amount'] = 4050  # 乘客总人数     改
paramDict['q_max'] = 654  # 断面客流                          改
paramDict['total_time'] = 60  # 60分钟
paramDict['ant_num'] = 20  # 蚂蚁数量
paramDict['C1'] = 2  # 每公里运营成本
paramDict['n'] = 3  # 时段数                                  改
paramDict['C2'] = 0.367  # 每分钟等待成本
paramDict['Alpha'], paramDict['Bta'] = 0.5, 0.5 # 权重系数

# 定义目标函数
def function(paramDict,result):
    min_operation = paramDict['C1'] * paramDict['L'] * (result[0] + result[1] + result[2]) # 公交运营成本
    min_ownership = paramDict['pb_1'] * result[0] + paramDict['pb_2'] * result[1] + paramDict['pb_3'] * result[2] # 购置成本
    min_enterprise = min_operation + min_ownership
    min_wait = paramDict['C2'] * paramDict['total_passenger_amount'] * paramDict['total_time'] / (result[0] + result[1] + result[2]) / 2 # 乘客等待时间成本
    min_fun = paramDict['Alpha'] * min_enterprise * paramDict['n'] + paramDict['Bta'] * min_wait
    return min_fun

# 定义约束条件
def restraint(paramDict,result):
    con1 = (paramDict['f_min'] <= (result[0] + result[1] + result[2]) <= paramDict['f_max']) # 发车间隔约束
    con2 = ((result[0] + result[1] + result[2]) <= paramDict['N_max']) # 车辆数目约束
    con3 = ((paramDict['cap_1'] * result[0] + paramDict['cap_2'] * result[1] + paramDict['cap_3'] * result[2]) * paramDict['r_f1'] <= paramDict['q_max'] <= (paramDict['cap_1'] * result[0] + paramDict['cap_2'] * result[1] + paramDict['cap_3'] * result[2]) * paramDict['r_f']) # 满载率约束
    if con1 and con2 and con3:
        return True
    else:
        return False

# 构建初始解空间
def ant_init(paramDict):
    for i in range(paramDict['ant_num']):
        start = np.random.randint(0, paramDict['N_max'] + 1)
        Table[i][0] = start
    return Table

# 选择路径
def choice_citys(paramDict,i,Alpha, Beta):
    for j in range(1,3):
        tabu = paramDict['N_max'] - sum(Table[i][:])
        allow = np.arange(tabu + 1)
        P = np.zeros(len(allow))
        for k in range(len(allow)):
            P[k] = math.pow(Tau[j-1][int(Table[i][-1])][int(allow[k])],Alpha) * math.pow(Eta[j-1][int(Table[i][-1])][int(allow[k])],Beta)
        Psum = sum(P)
        for k in range(len(allow)):
            P[k] = P[k] / Psum
        rand = random.random()
        Psum = P[0]
        for k in range(len(P)):
            Psum += P[k]
            if Psum >= rand:
                Table[i][j] = allow[k]
                break
            else:
                pass
    return Table

# 约束限制
def restraint_citys(paramDict):
    for i in range(paramDict['ant_num']):
        result = Table[i][:]
        if restraint(paramDict,result):
            pass
        else:
            Table[i][:] = [1000,1000,1000]
    return Table

# 目标函数计算
def route(paramDict):
    Table = restraint_citys(paramDict)
    Result = np.zeros(paramDict['ant_num'])
    for i in range(paramDict['ant_num']):
        result = Table[i][:]
        Result[i] = function(paramDict,result)
    R_best = min(Result)
    for i in range(paramDict['ant_num']):
        if R_best == Result[i]:
            min_index = i
            break
        else:
            pass
    Route_best = Table[min_index][:]
    return R_best, Route_best, Result

# 启发函数
def eta(paramDict):
    global Eta
    Eta = np.zeros([2,paramDict['N_max']+1,paramDict['N_max']+1])
    for i in range(paramDict['N_max']+1):
        for j in range(paramDict['N_max']+1):
            for k in range(paramDict['N_max']+1):
                if (i == 0 and j == 0 and k == 0) or ((i+j+k) >paramDict['N_max']):
                    Eta[0][i][j] += 0
                    Eta[1][j][k] += 0
                else:
                    result = [i, j, k]
                    R = function(paramDict,result)
                    Eta[0][i][j] += 1 / R
                    Eta[1][j][k] += 1 / R
    return Eta

# 更新信息素
def updata_Tau(paramDict,Result, Q, Rho):
    global Tau
    Delta_Tau = np.zeros([2,paramDict['N_max']+1,paramDict['N_max']+1])
    for k in range(2):
        # 逐个蚂蚁计算
        for i in range(paramDict['ant_num']):
            # 逐个城市计算
            for j in range(2):
                if Table[i][j] == 1000:
                    pass
                else:
                    Delta_Tau[k][int(Table[i][j])][int(Table[i][j+1])] += Q / Result[i]
    Tau = (1-Rho) * Tau + Delta_Tau
    return Tau

def main(paramDict, Alpha, Beta, Rho, Q, iter_max):
    global Tau, Table, Eta
    paramDict = paramDict
    Eta = eta(paramDict)
    Tau = np.ones([2,paramDict['N_max']+1,paramDict['N_max']+1])
    iter = 1 # 迭代次数初值
    Route_best = np.zeros([iter_max,3]) # 各代最佳路径
    R_best = np.zeros([iter_max,1]) # 各代最佳路径的长度
    while iter <= iter_max:
        Table = np.zeros([paramDict['ant_num'], 3]) # 路径记录表
        Table = ant_init(paramDict)
        for i in range(paramDict['ant_num']):
            Table = choice_citys(paramDict, i, Alpha, Beta)
        R_best[iter-1], Route_best[iter-1], Result = route(paramDict)
        Tau = updata_Tau(paramDict, Result, Q, Rho)
        iter += 1
    return R_best, Route_best

if __name__ == "__main__":
    R_best, Route_best = main(paramDict, 1, 5, 0.1, 1, 200)
    print(R_best)
    Shortest_Result = min(R_best)
    for i in range(len(R_best)):
        if R_best[i] == Shortest_Result:
            index = i
            break
    Shortest_Route = Route_best[index][:]
    print("最短距离：" + str(Shortest_Result))
    print("最短路径：" + str(Shortest_Route))
