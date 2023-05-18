# -*- coding: utf-8 -*-
"""
puzzle
Created on Fri Nov 25 2022
@author: Feng Liu
"""

import math

import numpy as np

class AStar:
    def __init__(self, start_data, end_data):
        self.start_data = start_data  # 初始puzzle状态
        self.n = start_data.shape[0]  # puzzle阶数
        self.end_data = end_data  # 目标puzzle状态
        self.hfun = "h2"  # 选取的启发式函数，目前没有太大用处

        # 问题1 如何建模队列结构：puzzle的字符串:(gn,hn,上一个puzzle状态)
        self.open = {str(self.start_data): (0, self.heuristic(self.start_data, self.hfun), self.start_data)}
        # 问题2 如何建模已经访问过的节点集合
        self.closed = []
        # 问题3 如何建模路径
        self.t_s_dict = {}
        # 返回转换过的路径
        self.path = []

        self.action_space = ['left', 'right', 'up', 'down']
        while True:
            value = self.astar_one_step()
            if value == -1:
                print("这个问题没有解")
                break
            elif value == 1:
                print("我求出解来了")
                break
            else:
                pass
        # 求解后生成路径
        self.path_generate()
        print(self.path)

    def find_zero(self, num):
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

    def move(self, num_data, direction):
        """
        得到更新之后的矩阵
        Input :
        - num_data : 整个状态矩阵
        - direction : 0 移动的方向
        """
        x, y = self.find_zero(num_data)
        num = np.copy(num_data)
        if direction == 'left':
            if y == 0:
                return num
            num[x][y] = num[x][y - 1]
            num[x][y - 1] = 0
            return num
        if direction == 'right':
            # 请同学写作向右移动的代码
            if y == self.n - 1:
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
            if x == self.n - 1:
                return num
            num[x][y] = num[x + 1][y]
            num[x + 1][y] = 0
            return num
        return

    def array_equal_ee(self, element_1, element_2):
        # 如何判断两个状态相等
        if np.sum(element_1 == element_2) == pow(self.n, 2):
            return True
        else:
            pass
        return False

    def array_equal_el(self, element_1, list_1):
        # 如何判断某状态是否在闭集
        for i in range(len(list_1)):
            element_2 = list_1[i]
            if self.array_equal_ee(element_1, element_2):
                return True
        return False

    def array_equal_open(self, element_1):
        # 如何判断某状态是否在开集
        return str(element_1) in self.open.keys()

    def get_next(self):
        minH = 1000  # 随便设的一个很大的数
        min_node = None
        for key, value in self.open.items():
            fn = sum(value[:2])
            if fn < minH:
                minH = fn
                min_node = value[2]
        return min_node

    def astar_one_step(self):
        # 请同学们自行补全
        # 如果队列中没有状态，则直接退出；
        if not bool(self.open):
            return -1
        # 获取队列中第一个状态
        node = self.get_next()
        gn = self.open[str(node)][0]
        # 添加到close里
        self.closed.append(node)
        # 从open里删除
        self.open.pop(str(node))
        #判断是否为目标状态
        if self.array_equal_ee(node, self.end_data):
            return 1

        # 扩展这个状态的所有操作
        for action in self.action_space:
            # 对于扩展的每个状态：
            # 检验是否为新的状态
            # 检验是否为终止状态 （返回1）
            new_space = self.move(node, action)
            if self.array_equal_el(new_space, self.closed):  # 如果在close
                pass
            elif self.array_equal_open(new_space):  # 如果在open,更新
                hn_new = self.heuristic(new_space, self.hfun)
                if gn + 1 + hn_new < sum(self.open[str(new_space)][:2]):
                    self.open[str(new_space)] = (gn + 1, hn_new, new_space)
                    self.t_s_dict[str(new_space)] = node
            else:  # 既不在close又不在open，添加到open里
                self.open[str(new_space)] = (gn + 1, self.heuristic(new_space, self.hfun), new_space)
                self.t_s_dict[str(new_space)] =node
        return 0

    # 路径求解
    def path_generate(self):
        # 如何生成整条的路径
        child = self.end_data
        while True:
            self.path.append(child)
            if self.array_equal_ee(child, self.start_data):
                break
            print(self.t_s_dict[str(child)])
            child = self.t_s_dict[str(child)]
        self.path.reverse()

    def heuristic(self, num_data, fun_name):
        # h1不在最终位置的数码个数，没啥用
        if (fun_name == "h1"):
            diff = 0
            for i in range(self.n):
                for j in range(self.n):
                    tmp = i * self.n + j
                    if (tmp != num_data[i, j]):
                        diff += 1
        if (fun_name == "h2"):
            # h2 曼哈顿距离
            distance = 0
            for i in range(self.n):
                for j in range(self.n):
                    tmp = num_data[i, j]
                    pos_i = tmp // self.n
                    pos_j = tmp % self.n
                    tmp_distance = abs(i - pos_i) + abs(j - pos_j)
                    distance += tmp_distance
        return distance
