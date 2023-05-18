# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'puzzle_demo_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, Ui_MainWindow):
        Ui_MainWindow.setObjectName("Ui_MainWindow")
        Ui_MainWindow.resize(743, 380)
        self.tableWidget = QtWidgets.QTableWidget(Ui_MainWindow)
        self.tableWidget.setGeometry(QtCore.QRect(30, 50, 300, 300))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.groupBox = QtWidgets.QGroupBox(Ui_MainWindow)
        self.groupBox.setGeometry(QtCore.QRect(510, 60, 221, 301))
        self.groupBox.setObjectName("groupBox")
        self.groupBox_selectPic = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_selectPic.setGeometry(QtCore.QRect(10, 40, 191, 71))
        self.groupBox_selectPic.setObjectName("groupBox_selectPic")
        self.pushButton1_LoadImage = QtWidgets.QPushButton(self.groupBox_selectPic)
        self.pushButton1_LoadImage.setGeometry(QtCore.QRect(40, 30, 101, 31))
        self.pushButton1_LoadImage.setObjectName("pushButton1_LoadImage")
        self.groupBox_selectJie = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_selectJie.setGeometry(QtCore.QRect(10, 120, 181, 71))
        self.groupBox_selectJie.setObjectName("groupBox_selectJie")
        self.spinBox_MapSize = QtWidgets.QSpinBox(self.groupBox_selectJie)
        self.spinBox_MapSize.setGeometry(QtCore.QRect(40, 40, 91, 21))
        self.spinBox_MapSize.setMinimum(3)
        self.spinBox_MapSize.setObjectName("spinBox_MapSize")
        self.pushButton3_StartSearch = QtWidgets.QPushButton(Ui_MainWindow)
        self.pushButton3_StartSearch.setGeometry(QtCore.QRect(340, 270, 81, 31))
        self.pushButton3_StartSearch.setObjectName("pushButton3_StartSearch")
        self.pushButton4_ResultShow = QtWidgets.QPushButton(Ui_MainWindow)
        self.pushButton4_ResultShow.setGeometry(QtCore.QRect(430, 270, 81, 31))
        self.pushButton4_ResultShow.setObjectName("pushButton4_ResultShow")
        self.pushButton2_RandomMapCreate = QtWidgets.QPushButton(Ui_MainWindow)
        self.pushButton2_RandomMapCreate.setGeometry(QtCore.QRect(340, 230, 81, 31))
        self.pushButton2_RandomMapCreate.setObjectName("pushButton2_RandomMapCreate")
        self.label_img = QtWidgets.QLabel(Ui_MainWindow)
        self.label_img.setGeometry(QtCore.QRect(360, 60, 120, 120))
        self.label_img.setText("")
        self.label_img.setObjectName("label_img")
        self.pushButton_Recovery = QtWidgets.QPushButton(Ui_MainWindow)
        self.pushButton_Recovery.setGeometry(QtCore.QRect(430, 230, 81, 31))
        self.pushButton_Recovery.setObjectName("pushButton_Recovery")

        self.retranslateUi(Ui_MainWindow)
        QtCore.QMetaObject.connectSlotsByName(Ui_MainWindow)

    def retranslateUi(self, Ui_MainWindow):
        _translate = QtCore.QCoreApplication.translate
        Ui_MainWindow.setWindowTitle(_translate("Ui_MainWindow", "Ui_MainWindow"))
        self.groupBox.setTitle(_translate("Ui_MainWindow", "拼图选项"))
        self.groupBox_selectPic.setTitle(_translate("Ui_MainWindow", "选择图片"))
        self.pushButton1_LoadImage.setText(_translate("Ui_MainWindow", "导入图片"))
        self.groupBox_selectJie.setTitle(_translate("Ui_MainWindow", "选择阶数"))
        self.pushButton3_StartSearch.setText(_translate("Ui_MainWindow", "开始搜索"))
        self.pushButton4_ResultShow.setText(_translate("Ui_MainWindow", "显示结果"))
        self.pushButton2_RandomMapCreate.setText(_translate("Ui_MainWindow", "生成拼图"))
        self.pushButton_Recovery.setText(_translate("Ui_MainWindow", "复原拼图"))