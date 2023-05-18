# -*- coding: utf-8 -*-
"""
puzzle
Created on Sun Nov 20 2022
@author: Hang Zhang,Feng Liu
"""

import numpy as np
from random import randint
import datetime
from copy import deepcopy as dp
from AStar_Search import AStar  # 从外部导入搜索算法文件
import puzzle_tool
# from BrandSearch import BFS  # 从外部导入搜索算法文件
from puzzle_demo_ui import Ui_MainWindow
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QHeaderView, QAbstractItemView, QTableWidgetItem, QMessageBox, QFileDialog, \
    QGraphicsPixmapItem, QGraphicsScene
from PyQt5.QtCore import QTimer, QSize
from PyQt5.QtGui import QBrush, QColor, QPixmap, QImage, QIcon
import sys
from PIL import Image, ImageQt


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Puzzle")
        # 初始化拼图
        self.n = self.spinBox_MapSize.value()  # 拼图阶数
        self.target = np.zeros((self.n, self.n), dtype=int)
        for i in range(self.n):  # [[0,1,2],[3,4,5],[6,7,8]]
            for j in range(self.n):
                self.target[i, j] = i * self.n + j
        self.image = None
        self.image_cropped = [0 for i in range(self.n * self.n)]

        self.time_str = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H%M%S')
        self.path = []
        self.step = 0
        # 标志
        self.generated = False  # 拼图生成标志
        self.loaded = False  # 拼图载入标志
        self.solved = True  # 拼图可解标志
        self.recovered = False  # 拼图可搜索标志
        self.searched = False  # 拼图已完成搜索标志
        self.player_count = 0 # 玩家步数
        self.player_path = [] # 玩家操作列表
        self.puzzle_generated = self.target
        self.i = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.go_one_step)
        self.ongoing = 0  # 结果显示中标志

        self.button_img_ls = []  # 图片按钮列表
        self.icon_ls = []  # 按钮icon列表

        self.tableWidget.horizontalHeader().hide()
        self.tableWidget.verticalHeader().hide()
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.puzzle_load_display()

        # 槽函数
        self.pushButton1_LoadImage.clicked.connect(self.load_image)
        self.pushButton2_RandomMapCreate.clicked.connect(self.random_map_create)
        self.pushButton3_StartSearch.clicked.connect(self.start_search)
        self.pushButton4_ResultShow.clicked.connect(self.result_show)
        self.pushButton_Recovery.clicked.connect(self.recovery)

    # 恢复到最初的状态
    def status_recovery(self):
        self.generated = False  # 拼图生成标志
        self.solved = True  # 拼图可解标志
        self.recovered = False  # 拼图可搜索标志
        self.searched = False  # 拼图已完成搜索标志
        self.player_count = 0
        self.player_path = []
        self.spinBox_MapSize.setDisabled(False)  # spinBox可使用

    # 导入图片函数
    def load_image(self):
        self.status_recovery()
        image_path, _ = QFileDialog.getOpenFileName(self, '选择文件', '', 'Image files(*.jpg  *.png  *.jpeg)')
        if(image_path==""):
            return
        self.image = Image.open(image_path)
        width = self.image.width
        height = self.image.height
        # 如果图片不是正方形，就进行切割，从图片中点扩展
        if width != height:
            length = width if width < height else height  # 取小
            midw, midh = width // 2, height // 2  # 计算中点
            x1, x2, y1, y2 = midw - length // 2, midw + length // 2, midh - length // 2, midh + length // 2  # 计算切割后的点
            self.image = self.image.crop((x1, y1, x2, y2))
        self.image = self.image.resize((300, 300), Image.ANTIALIAS)  # 缩放为合适大小

        # 初始化拼图参数
        self.n = self.spinBox_MapSize.value()
        self.puzzle = np.zeros((self.n, self.n), dtype=int)
        self.target = np.zeros((self.n, self.n), dtype=int)
        for i in range(self.n):  # [[0,1,2],[3,4,5],[6,7,8]]
            for j in range(self.n):
                self.target[i, j] = i * self.n + j
        for i in range(self.n):
            for j in range(self.n):
                self.puzzle[i, j] = i * self.n + j

        # 显示参考图片，分割图片，加载并显示在n×n的格子里
        self.showLabelImage()
        self.split_image()
        self.button_img_ls, self.icon_ls = self.puzzle_load_display()

        # 改变状态
        self.loaded = True
        self.spinBox_MapSize.setDisabled(True)  # 导入图片后，会禁用spinBox，不能选阶数

    # 在Label中显示参考图片
    def showLabelImage(self):
        labelimage = ImageQt.toqpixmap(self.image)
        self.label_img.setPixmap(
            labelimage.scaled(int(self.label_img.width()), int(self.label_img.height())))  # 在label上显示图片
        self.label_img.setScaledContents(True)

    # 初始化按键拼图，返回图片按钮列表和按键icon列表
    def puzzle_load_display(self):
        self.tableWidget.clear()
        self.tableWidget.setRowCount(self.n)
        self.tableWidget.setColumnCount(self.n)
        # 标志
        self.generated = False  # 拼图生成标志
        self.solved = True  # 拼图可解标志
        self.searched = False  # 拼图已完成搜索标志

        if self.image is None:
            return
        button_img_ls = []
        icon_ls = []
        for i in range(self.n):
            for j in range(self.n):
                if self.puzzle[i, j] == 0:
                    newItem = QtWidgets.QPushButton(self)
                    newItem.setObjectName(str(self.n * i + j))#设置按键id
                    newItem.setIconSize(
                        QSize(int(self.tableWidget.columnWidth(i)) - 5, int(self.tableWidget.rowHeight(j))))
                    newItem.clicked.connect(self.player_move)  # 槽函数
                    button_img_ls.append(newItem)
                    self.tableWidget.setCellWidget(i, j, newItem)
                    continue
                newIcon = QIcon()
                newIcon.addPixmap(self.image_cropped[self.puzzle[i, j]])
                icon_ls.append(newIcon)
                newItem = QtWidgets.QPushButton(self)
                newItem.setObjectName(str(self.n * i + j))
                newItem.clicked.connect(self.player_move)
                button_img_ls.append(newItem)
                newItem.setIcon(newIcon)
                newItem.setIconSize(
                    QSize(int(self.tableWidget.columnWidth(i)) - 5, int(self.tableWidget.rowHeight(j)) - 5))
                self.tableWidget.setCellWidget(i, j, newItem)
        return button_img_ls, icon_ls

    # 图片分割函数
    def split_image(self):
        del self.image_cropped
        self.image_cropped = [0 for i in range(self.n * self.n)]
        if self.image is None:
            return
        h = self.image.height
        w = self.image.width
        for i in range(self.n):
            for j in range(self.n):
                x1 = j * (w // self.n)
                x2 = (j + 1) * (w // self.n)
                y1 = i * (h // self.n)
                y2 = (i + 1) * (h // self.n)
                self.image_cropped[i * self.n + j] = ImageQt.toqpixmap(self.image.crop([x1, y1, x2, y2]))

    # 随机拼图生成按钮对应函数
    def random_map_create(self):
        if self.loaded==False:
            QMessageBox.information(self, '提示', '还未导入图片，请点击 导入图片')
        if self.generated == False:
            self.ongoing = 0
            self.n = self.spinBox_MapSize.value()

            '''
            # 随机初始化
            '''
            self.puzzle = random_puzzle_create(self.n)
            self.split_image()
            self.puzzle_generated = dp(self.puzzle)  # 本局生成的puzzle
            self.searched = False
            self.puzzle_display()
        else:
            QMessageBox.information(self, '提示', '此拼图已生成，请继续游戏')

    # 改变按键Icon
    def puzzle_display(self):
        for i in range(self.n):
            for j in range(self.n):
                if self.puzzle[i, j] == 0:
                    table_num = i * self.n + j
                    newItem = self.button_img_ls[table_num]
                    newItem.setIcon(QIcon())  # set空icon
                    self.tableWidget.setCellWidget(i, j, newItem)
                    continue
                puzzle_num = self.puzzle[i, j]
                table_num = i * self.n + j
                newIcon = self.icon_ls[puzzle_num - 1]
                self.button_img_ls[table_num].setIcon(newIcon)

    def player_move(self):
        # 获取0点坐标
        x, y = puzzle_tool.find_zero(self.puzzle)
        # 根据被点击的图片按键id，解析出被点击的坐标
        clicked_num = int(self.sender().objectName())
        clicked_x = clicked_num // self.n
        clicked_y = clicked_num % self.n
        # 获取被点击按键puzzle的值
        clicked_puzzle_num = self.puzzle[clicked_x, clicked_y]
        if (abs(x - clicked_x) + abs(y - clicked_y)) == 1:  # 判断点击的按钮是否邻近为空的按钮
            self.generated = True  # 意味着本局开始
            # 交换被点击puzzle值和0
            self.puzzle[x, y] = clicked_puzzle_num
            self.puzzle[clicked_x, clicked_y] = 0
            self.player_count += 1
            # 添加到玩家操作列表
            self.player_path.append(clicked_num)
        self.puzzle_display()

        #判断是否胜利
        if puzzle_tool.array_equal_ee(self.puzzle, self.target):
            _, _, step = puzzle_search(self.puzzle_generated, self.target) #computer计算出的步数
            QMessageBox.information(self, '提示', "恭喜获胜！共移动{}步。\n computer移动{}步".format(self.player_count, step - 1))
            filename = "puzzle" + self.time_str + ".txt" #文件名：puzzle+打开游戏时的time.txt
            with open(filename, "a") as f:# 追加写
                print("file open success")
                f.write(str(self.puzzle_generated) + "\n")
                f.write("player移动{}步,computer移动{}步\n".format(self.player_count, step -1))
                f.write(str(self.player_path) + "\n")
                if (self.player_count < step - 1): # 如果玩家比computer步数少
                    f.write("**************\n")
            self.status_recovery()

    # 开始搜索按钮对应函数
    def start_search(self):
        print(self.puzzle)
        if self.searched:
            QMessageBox.information(self, '提示', '当前拼图已完成搜索！')
            return
        if self.recovered == False:
            QMessageBox.information(self, '提示', '当前拼图还不能搜索！请点击 复原拼图')
            return
        self.ongoing = 0
        # 目标状态
        self.target = np.zeros((self.n, self.n), dtype=int)
        for i in range(self.n):
            for j in range(self.n):
                self.target[i, j] = i * self.n + j

        self.solved, self.path, self.step = puzzle_search(self.puzzle, self.target)
        self.searched = True
        if self.solved:
            QMessageBox.information(self, '提示', '搜索完成,一共需要进行{}步!'.format(self.step - 1))
        else:
            QMessageBox.information(self, '提示', '此拼图不可解,请更换拼图重新尝试！')

    # 结果显示按钮对应函数
    def result_show(self):
        if not self.searched:
            QMessageBox.information(self, '提示', '当前拼图尚未搜索，请先进行搜索！')
        elif not self.solved:
            QMessageBox.information(self, '提示', '此拼图不可解,请更换拼图重新尝试！')
        else:
            if self.ongoing == 0:
                self.status_recovery()
                self.puzzle_display()
                self.i = 0
                self.ongoing = 1
                self.timer.start(500)

            else:
                QMessageBox.information(self, '提示', '结果已在显示中，请等待本次显示完成方可再次显示')

    # 复原拼图按钮对应函数,恢复到本局生成后的拼图
    def recovery(self):
        self.puzzle = dp(self.puzzle_generated)
        self.player_count = 0
        self.player_path = []
        self.recovered = True  # 拼图可搜索标志
        self.puzzle_display()

    # 单步结果显示
    def go_one_step(self):
        if self.ongoing == 0:
            self.timer.stop()
            return
        '''
        # path: list, path of the black place from start state to target state
        
        last_step = (self.path[self.i][0], self.path[self.i][1])
        new_step = (self.path[self.i+1][0], self.path[self.i+1][1])
        self.puzzle[last_step]=self.puzzle[new_step]
        self.puzzle[new_step]=self.n*self.n-1
        '''
        # puzzle_path_list: list, path of puzzle from start state to target state
        self.puzzle = np.array(self.path[self.i])
        self.puzzle_display()
        self.i += 1
        if self.i == self.step:
            self.ongoing = 0


def random_puzzle_create(n):
    """
    TO DO:
        Write your own random puzzle create function here.
        Please make sure the created puzzle could be solved.
    INPUT:
        n: int, size of the puzzle.
    OUTPUT:
        puzzle: np.array, the puzzle created
    """
    puzzle = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(n):
            puzzle[i, j] = i * n + j
    action_space = ['left', 'right', 'up', 'down']
    for ii in range(n * (n + 1) * (n + 1)):
        r = randint(0, 3)
        puzzle = puzzle_tool.move(puzzle, action_space[r])
    return puzzle


# 自定义搜索算法
def puzzle_search(puzzle, target):
    '''
    TO DO:
        Write your own search function here.
    INPUT:
        puzzle: np.array.
    OUTPUT:
        solved: boolean, whether the puzzle could be solved
        puzzle_path_list: list, path of puzzle from start state to target state
        (path: list, path of the black place from start state to target state)
        step: int, number of steps in your path
    '''

    S0status = inversions(puzzle) % 2
    TargetStatus = inversions(target) % 2
    print(S0status, TargetStatus)
    if S0status == TargetStatus:
        solved = True
        '''
        # 从外部导入搜索方法
        puzzle = puzzle.tolist()
        target = target.tolist()
        # 实例化
        AStar_method = AStar(puzzle, target)
        # 计算搜索路径
        puzzle_path_list = AStar_method.run()
        '''
        '''
        # 宽度优先搜索
        
        bfs = BFS(puzzle)
        puzzle_path_list = bfs.path
        '''

        '''
        # A*搜索
        '''
        astar = AStar(puzzle, target)
        puzzle_path_list = astar.path
        print(puzzle_path_list)
        step = len(puzzle_path_list)
    else:
        solved = False
        puzzle_path_list = [puzzle]
        step = 0

    return solved, puzzle_path_list, step


def inversions(nlist):
    list = []
    for row in nlist:
        for ele in row:
            if ele != 0:
                list.append(ele)
    res = 0
    for i in range(len(list)):
        for j in range(i):
            if list[j] > list[i]:
                res += 1
    return (res)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())
