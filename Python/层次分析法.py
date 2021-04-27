import numpy as np
import math

RI_dict = {1: 0, 2: 0, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45}


def main(array):
    row = array.shape[0]  # 计算出阶数
    w = np.ones(row)
    for i in range(row):
        for j in range(row):
            w[i] = array[i][j] * w[i]
    print("积为:", w)
    for i in range(row):
        w[i] = math.pow(w[i], 1 / row)
    print('根为：', w)
    W = sum(w)
    for i in range(row):
        w[i] = w[i] / W
    print('归一化后为：', w)
    Lambda = 0
    for i in range(row):
        Lambda1 = 0
        for j in range(row):
            Lambda1 += w[j] * array[i][j]
        Lambda += Lambda1 / (row * w[i])
    print('特征根为：', Lambda)
    CI = (Lambda - row) / (row - 1)
    print('CI：', CI)
    CR = CI / RI_dict[row]
    print('CR:', CR)


if __name__ == '__main__':
    a = np.array([[1, 2, 2, 3, 4],
                  [1 / 2, 1, 1, 2, 3],
                  [1 / 2, 1, 1, 1, 2],
                  [1 / 3, 1 / 2, 1, 1, 3],
                  [1 / 4, 1 / 3, 1 / 2, 1 / 3, 1]])
    # a = main(a)
    a1 = np.array([[1, 1/9, 1/7, 1/4, 1/2, 1/3],
                  [9, 1, 2, 4, 6, 6],
                  [7, 1/2, 1, 2, 4, 4],
                  [4, 1/4, 1/2, 1, 3, 2],
                  [2, 1/6, 1/4, 1/3, 1, 1],
                  [3, 1/6, 1/4, 1/2, 1, 1]])
    # a1 = main(a1)
    a2 = np.array([[1, 2], [1/2, 1]])
    # a2 = main(a2)
    a3 = np.array([[1, 2], [1/2, 1]])
    # a3 = main(a3)
    a4 = np.array([[1, 2, 1 / 4, 1 / 4, 4, 2],
                   [1 / 2, 1, 1 / 6, 1 / 4, 4, 1],
                   [4, 6, 1, 2, 9, 6],
                   [4, 4, 1 / 2, 1, 2, 3],
                   [1 / 4, 1 / 4, 1 / 9, 1 / 2, 1, 2],
                   [1 / 2, 1, 1 / 6, 1 / 3, 1 / 2, 1]])
    # a4 = main(a4)
    b = np.array([[1, 2, 6, 4],
                  [1 / 2, 1, 4, 2],
                  [1 / 6, 1 / 4, 1, 1 / 2],
                  [1 / 4, 1 / 2, 2, 1]])
    # b = main(b)
    b1 = np.array([[1, 2, 1 / 2], [1 / 2, 1, 1 / 3], [2, 3, 1]])
    # b1 = main(b1)
    b3 = np.array([[1, 2], [1 / 2, 1]])
    # b3 = main(b3)
    b4 = np.array([[1, 4], [1 / 4, 1]])
    # b4 = main(b4)
    c = np.array([[1, 1, 2, 3],
                  [1, 1, 2, 1],
                  [1 / 2, 1 / 2, 1, 1 / 2],
                  [1 / 3, 1, 2, 1]])
    c = main(c)
    c2 = np.array([[1, 2, 3, 2],
                   [1 / 2, 1, 2, 1 / 2],
                   [1 / 3, 1 / 2, 1, 1 / 2],
                   [1 / 2, 2, 2, 1]])
    # c2 = main(c2)
    c4 = np.array([[1, 1 / 2, 3, 2],
                   [2, 1, 3, 3],
                   [1 / 3, 1 / 3, 1, 1],
                   [1 / 2, 1 / 3, 1, 1]])
    # c4 = main(c4)














