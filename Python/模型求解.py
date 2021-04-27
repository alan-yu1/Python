import math
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from deap import base, tools, creator, algorithms

# 参数设置
paramDict = {}
paramDict['L'] = 29  # 线路的长度，29千米
paramDict['station_amount'] = 27  # 线路站点数量
paramDict['speed'] = 20  # 车辆运行速度,20km/h
paramDict['pb_1'] = 15  # 小型车的购置成本，15元/小时/辆（50万元/辆）
paramDict['pb_2'] = 30  # 中型车的购置成本，30元/小时/辆（65万元/辆，算上补贴）
paramDict['pb_3'] = 45  # 大动车的购置成本，45元/小时/辆（100万元/辆，算上补贴）
paramDict['b_1'] = 2  # 公交车辆的运营成本，2元/km
paramDict['b_wt'] = 0.367  # 单位乘客等待时间价值成本，0.367元/分种
paramDict['f_min'] = 5  # 最小发车频率为5辆/小时
paramDict['f_max'] = 10  # 最大发车频率为10辆/小时
paramDict['bit'] = 6  # 发车频率与配置车辆数二进制编码各6位
paramDict['N_max'] = 37  # 最大能提供的车辆数目, 37辆
paramDict['cap_1'], paramDict['cap_2'], paramDict['cap_3'] = 40, 60, 90  # 小、中、大型公交车的容量
paramDict['r_f'] = 0.8  # 公交车的满载率
paramDict['total_passenger_amount'] = 146  # 乘客总人数
paramDict['gene_length'] = 18  # 个体长度  考虑小、中、大三种车型的发车频率
paramDict['a_e'] = 0.5  # 目标函数企业支出成本权重，0.5
paramDict['a_p'] = 0.5  # 目标函数乘客利益成本权重，0.5
paramDict['penalty'] = 10 ** 10  # 定义一个超大的数作为惩罚值
paramDict['n'] = 1  # 定义时间区段的长度



def genInd(paramDict = paramDict):  # 生成个体

    f_rdm = random.randrange(paramDict['f_min'], paramDict['f_max']+1)   # 生成总的发车频率，即小、中、大总的发车频率。
    f_1 = random.randrange(0, f_rdm+1)
    f_2 = random.randrange(0, f_rdm+1-f_1)
    f_3 = f_rdm - f_1 -f_2
    ind_list = []
    ind_list.extend(list(bin(f_1)[2:].zfill(6)))
    ind_list.extend(list(bin(f_2)[2:].zfill(6)))
    ind_list.extend(list(bin(f_3)[2:].zfill(6)))
    ind = [int(i) for i in ind_list]
    return ind


def decoding_params(ind):  # 解码操作 就是将生成的三种类型的发车频率解码

    """功能：实现发车频率和车辆数的参数的解码"""

    f_1 = ind[0]*(2**5) + ind[1]*(2**4) + ind[2]*(2**3) + ind[3]*(2**2) + ind[4]*(2**1) + ind[5]*(2**0)
    f_2 = ind[6]*(2**5) + ind[7]*(2**4) + ind[8]*(2**3) + ind[9]*(2**2) + ind[10]*(2**1) + ind[11]*(2**0)
    f_3 = ind[12]*(2**5) + ind[13]*(2**4) + ind[14]*(2**3) + ind[15]*(2**2) + ind[16]*(2**1) + ind[17]*(2**0)

    f = f_1 + f_2 + f_3

    return f_1, f_2, f_3, f



def vehicle_operating_time(paramDict):  # 统计车辆运行时间

    """
        实现功能：单线路车辆运行时间的统计
    """
    T = np.round(paramDict['L']/paramDict['speed'])

    return T


def calculate_configuration_bus(paramDict, ind):  # 统计配置的车辆数目
    """
            实现功能：计算配置的车辆数目
    """

    f_1, f_2, f_3, f = decoding_params(ind)
    T = vehicle_operating_time(paramDict)
    n_1, n_2, n_3 = math.ceil(T/60*f_1), math.ceil(T/60*f_2), math.ceil(T/60*f_3)

    return n_1, n_2, n_3


def max_passenger_flow(paramDict):  # 统计断面最大客流量
    """
        实现功能：断面最大客流量的统计
    """
    Q_max = 146

    return Q_max



def calculate_total_cost(paramDict, ind):  # 计算总成本
    """
        实现功能：计算总成本
    """
    # 参数的获取
    f_1, f_2, f_3, f = decoding_params(ind)
    n_1, n_2, n_3 = calculate_configuration_bus(paramDict, ind)

    # 从公交公司的角度，计算成本(购置成本，运行成本)
    z_ownership = paramDict['n'] * (paramDict['pb_1']*n_1 + paramDict['pb_2']*n_2 + paramDict['pb_3']*n_3)   # 车辆的购置成本
    z_operation = paramDict['n'] * (paramDict['L']*f_1*paramDict['b_1'] + paramDict['L']*f_2*paramDict['b_1'])  # 公交运营成本
    z_enterprise = z_ownership + z_operation
    # 从乘客的角度，计算成本（等待时间成本）

    waiting_time = 0.5 * 60 / f

    # 计算乘客总体的等待时间成本
    z_wait = paramDict['total_passenger_amount'] * waiting_time * paramDict['b_wt']  # 乘客的等待时间成本

    z_passenger = z_wait

    z_total = np.round(paramDict['a_e'] * z_enterprise + paramDict['a_p'] * z_passenger, 2)   # 成本进行四舍五入
    # print('z_total:{}'.format(z_total))
    return z_total, z_enterprise, z_passenger


def evaluate(ind):  # 定义评价函数   目的是防止生成的总发车频率为0的情况， 如果出现发车频率为零的情况。

    f_1, f_2, f_3, f = decoding_params(ind)
    if f == 0:
        f_rdm = random.randrange(paramDict['f_min'], paramDict['f_max'] + 1)  # 生成总的发车频率，即小、中、大总的发车频率。
        f_1 = random.randrange(0, f_rdm + 1)
        f_2 = random.randrange(0, f_rdm + 1 - f_1)
        f_3 = f_rdm - f_1 - f_2
        ind_list = []
        ind_list.extend(list(bin(f_1)[2:].zfill(6)))
        ind_list.extend(list(bin(f_2)[2:].zfill(6)))
        ind_list.extend(list(bin(f_3)[2:].zfill(6)))
        ind = [int(i) for i in ind_list]

    z_total, z_enterprise, z_passenger = calculate_total_cost(paramDict, ind)

    return z_total,  # 注意这个逗号，即使是单变量优化问题，也需要返回tuple



def feasible(ind):  # 施加约束

    f_1, f_2, f_3, f = decoding_params(ind)
    fv = 1
    if f == 0:
        fv = 0
    f_rdm = random.randrange(paramDict['f_min'], paramDict['f_max'] + 1)  # 生成总的发车频率，即小、中、大总的发车频率。
    f_1 = random.randrange(0, f_rdm + 1)
    f_2 = random.randrange(0, f_rdm + 1 - f_1)
    f_3 = f_rdm - f_1 - f_2
    ind_list = []
    ind_list.extend(list(bin(f_1)[2:].zfill(6)))
    ind_list.extend(list(bin(f_2)[2:].zfill(6)))
    ind_list.extend(list(bin(f_3)[2:].zfill(6)))
    ind = [int(i) for i in ind_list]
    n_1, n_2, n_3 = calculate_configuration_bus(paramDict, ind)
    Q_MAX = max_passenger_flow(paramDict)

    # 满足发车频率约束
    con1 = (paramDict['f_min'] <= f <= paramDict['f_max'])
    con2 = (fv == 1)

    # 满足车辆数约束
    con3 = ((n_1 + n_2 + n_3) <= paramDict['N_max'])

    # 满足断面客流量约束
    Q = paramDict['cap_1'] * f_1 * paramDict['r_f'] + paramDict['cap_2'] * f_2 * paramDict['r_f'] + paramDict['cap_3'] * f_3 * paramDict['r_f']
    con4 = (Q_MAX <= Q)

    print('con1:{},con2:{},con3:{},con4:{}'.format(con1, con2, con3, con4))
    if con1 and con2 and con3 and con4 :
        # print('出现符合全部条件的情况！！！')
        return True
    return False


if __name__ == '__main__':  # 求解主程序

    # 定义问题
    creator.create('FitnessMin', base.Fitness, weights=(-1.0,))  # 单目标，最小化
    creator.create('Individual', list, fitness=creator.FitnessMin)  # 创建Individual类，继承list
    toolbox = base.Toolbox()
    toolbox.register('individual', tools.initIterate, creator.Individual, genInd)
    toolbox.register('population', tools.initRepeat, list, toolbox.individual)
    toolbox.register('evaluate', evaluate)
    toolbox.decorate('evaluate', tools.DeltaPenalty(feasible, 1e10))  # death penalty
    toolbox.register('select', tools.selTournament, tournsize=2)
    toolbox.register('mate', tools.cxUniform, indpb=0.5)  # 注意这里的indpb需要显示给出
    toolbox.register('mutate', tools.mutFlipBit, indpb=0.5)

    toolbox.popSize = 50
    pop = toolbox.population(toolbox.popSize)

    ## 记录迭代数据
    stats = tools.Statistics(key=lambda ind: ind.fitness.values)
    stats.register('min', np.min)
    stats.register('avg', np.mean)
    stats.register('std', np.std)
    hallOfFame = tools.HallOfFame(maxsize=1)

    ## 遗传算法参数
    toolbox.ngen = 20
    toolbox.cxpb = 0.8
    toolbox.mutpb = 0.1