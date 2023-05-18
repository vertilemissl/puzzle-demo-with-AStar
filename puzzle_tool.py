# -*- coding: utf-8 -*-
"""
puzzle
Created on Fri Nov 25 2022
@author: Feng Liu
"""
import numpy as np


def find_zero(num):
    """
    得到0点值所在的x坐标和y坐标
    Input :
    - num：整个状态矩阵
    Output :
    - x : 0 元素的x坐标值
    - y : 0 元素的y坐标值
    """
    x, y = np.where(num == 0)
    return x[0], y[0]

def array_equal_ee(element_1, element_2):
    # 如何判断两个状态相等
    n=len(element_1)
    if np.sum(element_1 == element_2) == pow(n, 2):
        return True
    else:
        pass
    return False

def move(num_data, direction):
    """
    得到更新之后的矩阵
    Input :
    - num_data : 整个状态矩阵
    - direction : 0 移动的方向
    """
    n = num_data.shape[0]
    x, y = find_zero(num_data)
    X, Y = x, y
    num = np.copy(num_data)
    if direction == 'left':
        if y == 0:
            return num
        num[x][y] = num[x][y - 1]
        num[x][y - 1] = 0
        return num
    if direction == 'right':
        # 请同学写作向右移动的代码
        if y == n - 1:
            return num
        num[x][y] = num[x][y + 1]
        num[x][y + 1] = 0
        return num

    if direction == 'up':
        # 请同学写作向上移动的代码
        if x == 0:
            return num
        num[x][y] = num[x - 1][y]
        num[x - 1][y] = 0
        return num

    if direction == 'down':
        # 请同学写作向下移动的代码
        if x == n - 1:
            return num
        num[x][y] = num[x + 1][y]
        num[x + 1][y] = 0
        return num
