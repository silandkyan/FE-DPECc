# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(630, 614)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 60, 421, 441))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.label_10 = QtWidgets.QLabel(self.tab)
        self.label_10.setGeometry(QtCore.QRect(10, 70, 121, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.tab)
        self.label_11.setGeometry(QtCore.QRect(10, 170, 121, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self.tab)
        self.label_12.setGeometry(QtCore.QRect(10, 260, 121, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.multirButton = QtWidgets.QPushButton(self.tab)
        self.multirButton.setGeometry(QtCore.QRect(280, 350, 51, 41))
        self.multirButton.setObjectName("multirButton")
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(20, 300, 71, 16))
        self.label.setObjectName("label")
        self.permstopButton = QtWidgets.QPushButton(self.tab)
        self.permstopButton.setGeometry(QtCore.QRect(220, 190, 51, 41))
        self.permstopButton.setObjectName("permstopButton")
        self.singlelButton = QtWidgets.QPushButton(self.tab)
        self.singlelButton.setGeometry(QtCore.QRect(160, 287, 51, 41))
        self.singlelButton.setObjectName("singlelButton")
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setGeometry(QtCore.QRect(20, 360, 71, 16))
        self.label_2.setObjectName("label_2")
        self.multistep_numberBox = QtWidgets.QSpinBox(self.tab)
        self.multistep_numberBox.setGeometry(QtCore.QRect(80, 360, 71, 26))
        self.multistep_numberBox.setMaximum(999)
        self.multistep_numberBox.setObjectName("multistep_numberBox")
        self.singlerButton = QtWidgets.QPushButton(self.tab)
        self.singlerButton.setGeometry(QtCore.QRect(280, 287, 51, 41))
        self.singlerButton.setObjectName("singlerButton")
        self.multilButton = QtWidgets.QPushButton(self.tab)
        self.multilButton.setGeometry(QtCore.QRect(160, 350, 51, 41))
        self.multilButton.setObjectName("multilButton")
        self.permrButton = QtWidgets.QPushButton(self.tab)
        self.permrButton.setGeometry(QtCore.QRect(280, 190, 51, 41))
        self.permrButton.setObjectName("permrButton")
        self.label_9 = QtWidgets.QLabel(self.tab)
        self.label_9.setGeometry(QtCore.QRect(20, 200, 121, 16))
        self.label_9.setObjectName("label_9")
        self.multistopButton = QtWidgets.QPushButton(self.tab)
        self.multistopButton.setGeometry(QtCore.QRect(220, 350, 51, 41))
        self.multistopButton.setObjectName("multistopButton")
        self.permlButton = QtWidgets.QPushButton(self.tab)
        self.permlButton.setGeometry(QtCore.QRect(160, 190, 51, 41))
        self.permlButton.setObjectName("permlButton")
        self.rpmBox = QtWidgets.QSpinBox(self.tab)
        self.rpmBox.setGeometry(QtCore.QRect(60, 15, 71, 31))
        self.rpmBox.setObjectName("rpmBox")
        self.label_3 = QtWidgets.QLabel(self.tab)
        self.label_3.setGeometry(QtCore.QRect(20, 20, 31, 16))
        self.label_3.setObjectName("label_3")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.label_6 = QtWidgets.QLabel(self.tab_2)
        self.label_6.setGeometry(QtCore.QRect(10, 75, 71, 16))
        self.label_6.setObjectName("label_6")
        self.label_8 = QtWidgets.QLabel(self.tab_2)
        self.label_8.setGeometry(QtCore.QRect(10, 135, 71, 16))
        self.label_8.setObjectName("label_8")
        self.label_5 = QtWidgets.QLabel(self.tab_2)
        self.label_5.setGeometry(QtCore.QRect(10, 45, 71, 16))
        self.label_5.setObjectName("label_5")
        self.rpm_minBox = QtWidgets.QSpinBox(self.tab_2)
        self.rpm_minBox.setGeometry(QtCore.QRect(90, 105, 71, 26))
        self.rpm_minBox.setObjectName("rpm_minBox")
        self.rpm_maxBox = QtWidgets.QSpinBox(self.tab_2)
        self.rpm_maxBox.setGeometry(QtCore.QRect(90, 135, 71, 26))
        self.rpm_maxBox.setObjectName("rpm_maxBox")
        self.microstepsBox = QtWidgets.QSpinBox(self.tab_2)
        self.microstepsBox.setGeometry(QtCore.QRect(90, 75, 71, 26))
        self.microstepsBox.setObjectName("microstepsBox")
        self.label_7 = QtWidgets.QLabel(self.tab_2)
        self.label_7.setGeometry(QtCore.QRect(10, 105, 71, 16))
        self.label_7.setObjectName("label_7")
        self.stepsBox = QtWidgets.QSpinBox(self.tab_2)
        self.stepsBox.setGeometry(QtCore.QRect(90, 45, 71, 26))
        self.stepsBox.setObjectName("stepsBox")
        self.label_4 = QtWidgets.QLabel(self.tab_2)
        self.label_4.setGeometry(QtCore.QRect(10, 10, 181, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.tabWidget.addTab(self.tab_2, "")
        self.motor1_radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.motor1_radioButton.setGeometry(QtCore.QRect(100, 10, 104, 21))
        self.motor1_radioButton.setObjectName("motor1_radioButton")
        self.motor3_radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.motor3_radioButton.setGeometry(QtCore.QRect(260, 10, 104, 21))
        self.motor3_radioButton.setObjectName("motor3_radioButton")
        self.motor2_radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.motor2_radioButton.setGeometry(QtCore.QRect(100, 30, 104, 21))
        self.motor2_radioButton.setObjectName("motor2_radioButton")
        self.motor4_radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.motor4_radioButton.setGeometry(QtCore.QRect(260, 30, 104, 21))
        self.motor4_radioButton.setObjectName("motor4_radioButton")
        self.quitButton = QtWidgets.QPushButton(self.centralwidget)
        self.quitButton.setGeometry(QtCore.QRect(340, 510, 61, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.quitButton.setFont(font)
        self.quitButton.setObjectName("quitButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 630, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_10.setText(_translate("MainWindow", "Position Control"))
        self.label_11.setText(_translate("MainWindow", "Permanent"))
        self.label_12.setText(_translate("MainWindow", "Manual Control"))
        self.multirButton.setText(_translate("MainWindow", "right"))
        self.label.setText(_translate("MainWindow", "single step"))
        self.permstopButton.setText(_translate("MainWindow", "stop"))
        self.singlelButton.setText(_translate("MainWindow", "left"))
        self.label_2.setText(_translate("MainWindow", "multi step"))
        self.singlerButton.setText(_translate("MainWindow", "right"))
        self.multilButton.setText(_translate("MainWindow", "left"))
        self.permrButton.setText(_translate("MainWindow", "right"))
        self.label_9.setText(_translate("MainWindow", "permanent rotation"))
        self.multistopButton.setText(_translate("MainWindow", "stop"))
        self.permlButton.setText(_translate("MainWindow", "left"))
        self.label_3.setText(_translate("MainWindow", "RPM"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Motor Control"))
        self.label_6.setText(_translate("MainWindow", "Microsteps"))
        self.label_8.setText(_translate("MainWindow", "max. RPM"))
        self.label_5.setText(_translate("MainWindow", "Steps"))
        self.label_7.setText(_translate("MainWindow", "min. RPM"))
        self.label_4.setText(_translate("MainWindow", "Stepper motor settings"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Motor Settings"))
        self.motor1_radioButton.setText(_translate("MainWindow", "Motor 1"))
        self.motor3_radioButton.setText(_translate("MainWindow", "Motor 3"))
        self.motor2_radioButton.setText(_translate("MainWindow", "Motor 2"))
        self.motor4_radioButton.setText(_translate("MainWindow", "Motor 4"))
        self.quitButton.setText(_translate("MainWindow", "QUIT"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())