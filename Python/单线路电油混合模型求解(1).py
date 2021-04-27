"""
    日期：2020/11/30
    实现功能：单线路电油混合模型求解

"""
import math
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from deap import base, tools, creator, algorithms

# 数据文件路径
file_path = 'C:\\Users\\Lenovo\\Desktop\\694线路OD统计\\694线路OD统计(时段5).xlsx'
distance_path = 'C:\\Users\\Lenovo\\Desktop\\694线路早高峰乘客OD情况\\694线路站距信息表.xls'

# 参数设置
paramDict = {}
paramDict['L'] = 32  # 线路的长度，32千米
paramDict['station_amount'] = 21  # 线路站点数量
paramDict['speed'] = 30  # 车辆运行速度,30km/h
paramDict['ust'] = 3  # 每名乘客上车时间，3秒
paramDict['dst'] = 2  # 每名乘客下车时间，2秒
paramDict['pb_1'] = 11.416  # 燃油车的购置成本，11.416元/小时/辆（50万元/辆）
paramDict['pb_2'] = 45.662  # 电动车的购置成本，45.662元/小时/辆（100万元/辆，算上补贴）
paramDict['b_1'] = 2.013  # 燃油车的运营成本，2.013元/km
paramDict['b_2'] = 0.885  # 电动车的运营成本，0.885元/km
paramDict['b_wt'] = 1.206  # 单位候车时间价值成本，1.206元/分种
paramDict['b_in'] = 0.804  # 单位在车时间价值成本，0.804元/分钟
paramDict['b_cn'] = 0.058  # 碳排放量价值成本，0.058元/kg
paramDict['e_1'], paramDict['e_2'] = 1.12, 0  # 单位公里的碳排放，（燃油车，1.12kg/km；电动车，0）
paramDict['e_limit'] = 200  # 人均碳排放量不能大于200g
paramDict['Lc_limit'] = 120  # 电动公交续驶里程的限定值不能大于120公里
paramDict['f_min'] = 3  # 最小发车频率为3辆/小时
paramDict['f_max'] = 3  # 最大发车频率为12辆/小时
paramDict['bit'] = 6  # 发车频率与配置车辆数二进制编码为6位
paramDict['N_max'] = 37  # 最大能提供的车辆数目, 37辆
paramDict['t_charge'] = 4.57  # 运行一次的充电时间，4.57分钟
paramDict['cap_1'], paramDict['cap_2'] = 90, 90  # 燃油车和电动车的容量，（燃油：90，电动：90）
paramDict['r_f'] = 0.8  # 公交车的满载率
paramDict['OD_data'] = pd.read_excel(file_path)
paramDict['total_passenger_amount'] = 887  # 乘客总人数
paramDict['distance_data'] = pd.read_excel(distance_path)
paramDict['gene_length'] = 12  # 个体长度

paramDict['a_e'] = 0.5  # 目标函数企业支出成本权重，0.5
paramDict['a_p'] = 0.5  # 目标函数乘客利益成本权重，0.5

paramDict['delay'] = 60  # 每个站点进出站的平均延误值，60秒
paramDict['penalty'] = 10 ** 10  # 定义一个超大的数作为惩罚值
paramDict['n'] = 4  # 定义时间区段的长度


def genInd(paramDict = paramDict):  # 生成个体

    f_rdm = random.randrange(paramDict['f_min'], paramDict['f_max']+1)
    f_1 = random.randrange(0, f_rdm+1)
    f_2 = f_rdm - f_1
    ind_list = []
    ind_list.extend(list(bin(f_1)[2:].zfill(6)))
    ind_list.extend(list(bin(f_2)[2:].zfill(6)))
    ind = [int(i) for i in ind_list]

    return ind


def decoding_params(ind):  # 解码操作

    """功能：实现发车频率和车辆数的参数的解码"""

    f_1 = ind[0]*(2**5) + ind[1]*(2**4) + ind[2]*(2**3) + ind[3]*(2**2) + ind[4]*(2**1) + ind[5]*(2**0)
    f_2 = ind[6]*(2**5) + ind[7]*(2**4) + ind[8]*(2**3) + ind[9]*(2**2) + ind[10]*(2**1) + ind[11]*(2**0)
    f = f_1 + f_2

    return f_1, f_2, f


def vehicle_operating_time(paramDict, ind):  # 统计车辆运行时间

    """
        实现功能：单线路车辆运行时间的统计
    """
    operating_time = paramDict['distance_data'].iloc[0][paramDict['station_amount']] / paramDict['speed'] * 60
    total_stop_time = 0
    f_1, f_2, f = decoding_params(ind)
    for st in range(0, paramDict['station_amount']):  # 站站停策略下车辆运行时间统计
        up_time = np.round((np.sum(paramDict['OD_data'][st:st+1].values.tolist()) * paramDict['ust'])/60, 2)
        down_time = np.round((np.sum(paramDict['OD_data'][st+1].values.tolist()) * paramDict['dst'])/60, 2)
        stop_time = max(up_time, down_time) / f
        total_stop_time += stop_time
    t_delay = paramDict['station_amount'] * paramDict['delay'] / 60
    T = np.round(operating_time + total_stop_time + t_delay, 2)

    return T


def calculate_configuration_bus(paramDict, ind):  # 统计配置的车辆数目
    """
            实现功能：计算配置的车辆数目
    """

    f_1, f_2, f = decoding_params(ind)
    T = vehicle_operating_time(paramDict, ind)
    n_1, n_2 = math.ceil(T/60*f_1), math.ceil((T+paramDict['t_charge'])/60*f_2)

    return n_1, n_2


def max_passenger_flow(paramDict):  # 统计断面最大客流量
    """
        实现功能：断面最大客流量的统计
    """

    Q_max = 0
    remain_passenger_amount = 0
    for st in range(0, paramDict['station_amount']):
        if st == 0:
            remain_passenger_amount = np.sum(paramDict['OD_data'][st:st+1].values.tolist())
            Q_max = np.sum(paramDict['OD_data'][st:st+1].values.tolist())
        else:
            up_passenger_amount = np.sum(paramDict['OD_data'][st:st+1].values.tolist())
            down_passenger_amount = np.sum(paramDict['OD_data'][st+1].values.tolist())
            Q = remain_passenger_amount + up_passenger_amount - down_passenger_amount
            if Q > Q_max:
                Q_max = Q

    return Q_max


def calculate_total_cost(paramDict, ind):  # 计算总成本
    """
        实现功能：计算总成本
    """
    # 参数的获取
    f_1, f_2, f = decoding_params(ind)
    n_1, n_2 = calculate_configuration_bus(paramDict, ind)

    # 从公交公司的角度，计算成本(购置成本，运行成本)
    z_ownership = paramDict['n'] * (paramDict['pb_1']*n_1 + paramDict['pb_2']*n_2)   # 车辆的购置成本
    z_operation = paramDict['n'] * (paramDict['L']*f_1*paramDict['b_1'] + paramDict['L']*f_2*paramDict['b_2'])  # 公交运营成本
    # 从环境的角度，计算成本(碳排放成本)
    z_carbon = paramDict['n'] * (paramDict['L'] * f_1 * paramDict['e_1'] * paramDict['b_cn'] + paramDict['L'] * f_2 * paramDict['e_2'] * paramDict['b_cn'])
    z_enterprise = z_ownership + z_operation + z_carbon

    # 从乘客的角度，计算成本（等待时间成本，换乘时间成本，在车时间成本）
    q = np.sum(paramDict['OD_data'].values.tolist())
    waiting_time = 0.5 * 60 / f

    # 计算乘客总体的等待时间成本
    z_wait = q * waiting_time * paramDict['b_wt']  # 乘客的等待时间成本

    # 计算乘客总体的在车时间成本（根据OD计算OD出行时间*OD人数）
    total_invehicle_time = 0
    for i in range(0, paramDict['station_amount']):
        for j in range(i+2, paramDict['station_amount'] + 1):
            total_operating_time = paramDict['distance_data'].loc[i][j] / paramDict['speed'] * 60
            total_delay_time = paramDict['delay'] / 60 * (j-i)
            total_stop_time = 0
            for st in range(i, j):  # 计算站点的停留时间，根据站点人数进行估计
                up_time = np.round((np.sum(paramDict['OD_data'][st:st+1].values.tolist()) * paramDict['ust']) / 60, 2)
                down_time = np.round((np.sum(paramDict['OD_data'][st+1].values.tolist()) * paramDict['dst']) / 60, 2)
                stop_time = max(up_time, down_time) / f
                total_stop_time += stop_time
            invehicle_time = total_operating_time + total_delay_time + total_stop_time
            total_invehicle_time += (invehicle_time * paramDict['OD_data'].loc[i][j])
    z_invehicle = total_invehicle_time * paramDict['b_in']
    # print('z_wait:{}, z_transfer:{}, z_invehicle:{}'.format(z_wait, z_transfer, z_invehicle))
    z_passenger = z_wait + z_invehicle

    z_total = np.round(paramDict['a_e'] * z_enterprise + paramDict['a_p'] * z_passenger, 2)
    # print('z_total:{}'.format(z_total))
    return z_total, z_enterprise, z_passenger, z_carbon


def evaluate(ind):  # 定义评价函数

    f_1, f_2, f = decoding_params(ind)
    if f == 0:
        f_rdm = random.randrange(paramDict['f_min'], paramDict['f_max']+1)
        f_1 = random.randrange(0, f_rdm + 1)
        f_2 = f_rdm - f_1
        ind_list = []
        ind_list.extend(list(bin(f_1)[2:].zfill(6)))
        ind_list.extend(list(bin(f_2)[2:].zfill(6)))
        ind = [int(i) for i in ind_list]

    z_total, z_enterprise, z_passenger, z_carbon = calculate_total_cost(paramDict, ind)

    return z_total,  # 注意这个逗号，即使是单变量优化问题，也需要返回tuple


def feasible(ind):  # 施加约束

    f_1, f_2, f = decoding_params(ind)
    fv = 1
    if f == 0:
        fv = 0
        f_rdm = random.randrange(paramDict['f_min'], paramDict['f_max'] + 1)
        f_1 = random.randrange(0, f_rdm + 1)
        f_2 = f_rdm - f_1
        ind_list = []
        ind_list.extend(list(bin(f_1)[2:].zfill(6)))
        ind_list.extend(list(bin(f_2)[2:].zfill(6)))
        ind = [int(i) for i in ind_list]
    n_1, n_2 = calculate_configuration_bus(paramDict, ind)
    Q_MAX = max_passenger_flow(paramDict)

    # 满足发车频率约束
    con1 = (paramDict['f_min'] <= f <= paramDict['f_max'])
    con2 = (fv == 1)

    # 满足车辆数约束
    con3 = ((n_1 + n_2) <= paramDict['N_max'])

    # 满足断面客流量约束
    Q = paramDict['cap_1'] * f_1 * paramDict['r_f'] + paramDict['cap_2'] * f_2 * paramDict['r_f']
    con4 = (Q_MAX <= Q)

    # 满足人均碳排放量约束
    Carbon = paramDict['n'] * (f_1 * paramDict['L'] * paramDict['e_1'] * 1000 + f_2 * paramDict['L'] * paramDict['e_2'] * 1000) / paramDict['total_passenger_amount']
    con5 = (Carbon <= paramDict['e_limit'])

    # # 满足续驶里程约束
    if n_2 == 0:
        Lc = 0
    else:
        Lc = f_2 * paramDict['L'] / n_2
    con6 = (Lc <= paramDict['Lc_limit'])
    print('con1:{},con2:{},con3:{},con4:{},con5:{},con6:{}'.format(con1, con2, con3, con4, con5, con6))
    if con1 and con2 and con3 and con4 and con5 and con6:
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

    ## 遗传算法主程序
    pop, logbook = algorithms.eaMuPlusLambda(pop, toolbox, mu=toolbox.popSize, lambda_=toolbox.popSize,
                                             cxpb=toolbox.cxpb, mutpb=toolbox.mutpb, ngen=toolbox.ngen,
                                             stats=stats, halloffame=hallOfFame, verbose=True)

    bestInd = hallOfFame.items[0]
    bestFit = bestInd.fitness.values
    print('bestInd:{}'.format(bestInd))
    print('总出行费用:{}'.format(bestFit))
    f_1, f_2, f = decoding_params(bestInd)
    print('f_1:{}, f_2:{}, f:{}'.format(f_1, f_2, f))
    T = vehicle_operating_time(paramDict, bestInd)
    print('T:{}'.format(T))
    Q_MAX = max_passenger_flow(paramDict)
    print('Q_MAX:{}'.format(Q_MAX))
    n_1, n_2 = calculate_configuration_bus(paramDict, bestInd)
    print('n_1:{}, n_2:{}'.format(n_1, n_2))
    z_total, z_enterprise, z_passenger, z_carbon = calculate_total_cost(paramDict, bestInd)
    print('z_total:{},z_enterprise:{},z_passenger:{},z_carbon:{}!'.format(z_total, z_enterprise, z_passenger, z_carbon))

    # 画出Minimum Fitness迭代图
    plt.rcParams['font.sans-serif'] = ['simhei']
    minFit = logbook.select('min')
    plt.plot(minFit, color='k', linewidth=1, label='最小适应度值')
    plt.xlabel('迭代次数')
    plt.ylabel('适应度值')
    plt.legend(loc='best')
    plt.show()
    # 画出Average Fitness迭代图
    avgFit = logbook.select('avg')
    plt.plot(avgFit, color='k', linewidth=1, label='平均适应度值')
    plt.xlabel('迭代次数')
    plt.ylabel('适应度值')
    plt.legend(loc='best')
    plt.show()
