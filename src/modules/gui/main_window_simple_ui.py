# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window_simple.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(622, 343)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 10, 311, 141))
        self.tabWidget.setObjectName("tabWidget")
        self.single = QtWidgets.QWidget()
        self.single.setObjectName("single")
        self.motor1_radioButton = QtWidgets.QRadioButton(self.single)
        self.motor1_radioButton.setGeometry(QtCore.QRect(220, 20, 104, 21))
        self.motor1_radioButton.setObjectName("motor1_radioButton")
        self.motor2_radioButton = QtWidgets.QRadioButton(self.single)
        self.motor2_radioButton.setGeometry(QtCore.QRect(220, 60, 104, 21))
        self.motor2_radioButton.setObjectName("motor2_radioButton")
        self.s_right = QtWidgets.QPushButton(self.single)
        self.s_right.setGeometry(QtCore.QRect(150, 30, 51, 41))
        self.s_right.setObjectName("s_right")
        self.s_left = QtWidgets.QPushButton(self.single)
        self.s_left.setGeometry(QtCore.QRect(30, 30, 51, 41))
        self.s_left.setObjectName("s_left")
        self.s_stop = QtWidgets.QPushButton(self.single)
        self.s_stop.setGeometry(QtCore.QRect(90, 30, 51, 41))
        self.s_stop.setObjectName("s_stop")
        self.tabWidget.addTab(self.single, "")
        self.multi = QtWidgets.QWidget()
        self.multi.setObjectName("multi")
        self.motor1_checkBox = QtWidgets.QCheckBox(self.multi)
        self.motor1_checkBox.setGeometry(QtCore.QRect(220, 20, 87, 21))
        self.motor1_checkBox.setObjectName("motor1_checkBox")
        self.motor2_checkBox = QtWidgets.QCheckBox(self.multi)
        self.motor2_checkBox.setGeometry(QtCore.QRect(220, 60, 87, 21))
        self.motor2_checkBox.setObjectName("motor2_checkBox")
        self.m_right = QtWidgets.QPushButton(self.multi)
        self.m_right.setGeometry(QtCore.QRect(150, 30, 51, 41))
        self.m_right.setObjectName("m_right")
        self.m_left = QtWidgets.QPushButton(self.multi)
        self.m_left.setGeometry(QtCore.QRect(30, 30, 51, 41))
        self.m_left.setObjectName("m_left")
        self.m_stop = QtWidgets.QPushButton(self.multi)
        self.m_stop.setGeometry(QtCore.QRect(90, 30, 51, 41))
        self.m_stop.setObjectName("m_stop")
        self.tabWidget.addTab(self.multi, "")
        self.settings = QtWidgets.QWidget()
        self.settings.setObjectName("settings")
        self.label_6 = QtWidgets.QLabel(self.settings)
        self.label_6.setGeometry(QtCore.QRect(10, 75, 71, 16))
        self.label_6.setObjectName("label_6")
        self.label_8 = QtWidgets.QLabel(self.settings)
        self.label_8.setGeometry(QtCore.QRect(200, 80, 71, 16))
        self.label_8.setObjectName("label_8")
        self.label_5 = QtWidgets.QLabel(self.settings)
        self.label_5.setGeometry(QtCore.QRect(10, 45, 71, 16))
        self.label_5.setObjectName("label_5")
        self.rpm_minBox = QtWidgets.QSpinBox(self.settings)
        self.rpm_minBox.setGeometry(QtCore.QRect(280, 50, 71, 26))
        self.rpm_minBox.setObjectName("rpm_minBox")
        self.rpm_maxBox = QtWidgets.QSpinBox(self.settings)
        self.rpm_maxBox.setGeometry(QtCore.QRect(280, 80, 71, 26))
        self.rpm_maxBox.setObjectName("rpm_maxBox")
        self.microstepsBox = QtWidgets.QSpinBox(self.settings)
        self.microstepsBox.setGeometry(QtCore.QRect(90, 75, 71, 26))
        self.microstepsBox.setObjectName("microstepsBox")
        self.label_7 = QtWidgets.QLabel(self.settings)
        self.label_7.setGeometry(QtCore.QRect(200, 50, 71, 16))
        self.label_7.setObjectName("label_7")
        self.stepsBox = QtWidgets.QSpinBox(self.settings)
        self.stepsBox.setGeometry(QtCore.QRect(90, 45, 71, 26))
        self.stepsBox.setObjectName("stepsBox")
        self.label_4 = QtWidgets.QLabel(self.settings)
        self.label_4.setGeometry(QtCore.QRect(10, 10, 181, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.tabWidget.addTab(self.settings, "")
        self.quitButton = QtWidgets.QPushButton(self.centralwidget)
        self.quitButton.setGeometry(QtCore.QRect(330, 200, 71, 51))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.quitButton.setFont(font)
        self.quitButton.setObjectName("quitButton")
        self.mode_single = QtWidgets.QRadioButton(self.centralwidget)
        self.mode_single.setGeometry(QtCore.QRect(30, 185, 104, 21))
        self.mode_single.setObjectName("mode_single")
        self.mode_selection = QtWidgets.QButtonGroup(MainWindow)
        self.mode_selection.setObjectName("mode_selection")
        self.mode_selection.addButton(self.mode_single)
        self.mode_multi = QtWidgets.QRadioButton(self.centralwidget)
        self.mode_multi.setGeometry(QtCore.QRect(30, 205, 104, 21))
        self.mode_multi.setObjectName("mode_multi")
        self.mode_selection.addButton(self.mode_multi)
        self.mode_perm = QtWidgets.QRadioButton(self.centralwidget)
        self.mode_perm.setGeometry(QtCore.QRect(30, 225, 104, 21))
        self.mode_perm.setObjectName("mode_perm")
        self.mode_selection.addButton(self.mode_perm)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(160, 185, 71, 16))
        self.label_2.setObjectName("label_2")
        self.multistep_numberBox = QtWidgets.QSpinBox(self.centralwidget)
        self.multistep_numberBox.setGeometry(QtCore.QRect(230, 180, 71, 26))
        self.multistep_numberBox.setMaximum(999)
        self.multistep_numberBox.setObjectName("multistep_numberBox")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(180, 235, 31, 16))
        self.label_3.setObjectName("label_3")
        self.rpmBox = QtWidgets.QSpinBox(self.centralwidget)
        self.rpmBox.setGeometry(QtCore.QRect(230, 230, 71, 31))
        self.rpmBox.setObjectName("rpmBox")
        self.lcd_current_1 = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcd_current_1.setGeometry(QtCore.QRect(330, 60, 64, 23))
        self.lcd_current_1.setObjectName("lcd_current_1")
        self.lcd_current_2 = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcd_current_2.setGeometry(QtCore.QRect(330, 100, 64, 23))
        self.lcd_current_2.setObjectName("lcd_current_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(330, 30, 71, 16))
        self.label.setObjectName("label")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(420, 30, 81, 16))
        self.label_9.setObjectName("label_9")
        self.lcd_stored_2A = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcd_stored_2A.setGeometry(QtCore.QRect(430, 100, 64, 23))
        self.lcd_stored_2A.setObjectName("lcd_stored_2A")
        self.lcd_stored_1A = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcd_stored_1A.setGeometry(QtCore.QRect(430, 60, 64, 23))
        self.lcd_stored_1A.setObjectName("lcd_stored_1A")
        self.goto_buttonA = QtWidgets.QPushButton(self.centralwidget)
        self.goto_buttonA.setGeometry(QtCore.QRect(430, 180, 61, 28))
        self.goto_buttonA.setObjectName("goto_buttonA")
        self.storeButtonA = QtWidgets.QPushButton(self.centralwidget)
        self.storeButtonA.setGeometry(QtCore.QRect(430, 140, 61, 28))
        self.storeButtonA.setObjectName("storeButtonA")
        self.lcd_stored_2B = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcd_stored_2B.setGeometry(QtCore.QRect(530, 100, 64, 23))
        self.lcd_stored_2B.setObjectName("lcd_stored_2B")
        self.lcd_stored_1B = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcd_stored_1B.setGeometry(QtCore.QRect(530, 60, 64, 23))
        self.lcd_stored_1B.setObjectName("lcd_stored_1B")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(520, 30, 81, 16))
        self.label_10.setObjectName("label_10")
        self.storeButtonB = QtWidgets.QPushButton(self.centralwidget)
        self.storeButtonB.setGeometry(QtCore.QRect(530, 140, 61, 28))
        self.storeButtonB.setObjectName("storeButtonB")
        self.goto_buttonB = QtWidgets.QPushButton(self.centralwidget)
        self.goto_buttonB.setGeometry(QtCore.QRect(530, 180, 61, 28))
        self.goto_buttonB.setObjectName("goto_buttonB")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 622, 22))
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
        self.motor1_radioButton.setText(_translate("MainWindow", "Motor 1"))
        self.motor2_radioButton.setText(_translate("MainWindow", "Motor 2"))
        self.s_right.setText(_translate("MainWindow", "right"))
        self.s_left.setText(_translate("MainWindow", "left"))
        self.s_stop.setText(_translate("MainWindow", "stop"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.single), _translate("MainWindow", "single"))
        self.motor1_checkBox.setText(_translate("MainWindow", "Motor 1"))
        self.motor2_checkBox.setText(_translate("MainWindow", "Motor 2"))
        self.m_right.setText(_translate("MainWindow", "right"))
        self.m_left.setText(_translate("MainWindow", "left"))
        self.m_stop.setText(_translate("MainWindow", "stop"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.multi), _translate("MainWindow", "multi"))
        self.label_6.setText(_translate("MainWindow", "Microsteps"))
        self.label_8.setText(_translate("MainWindow", "max. RPM"))
        self.label_5.setText(_translate("MainWindow", "Steps"))
        self.label_7.setText(_translate("MainWindow", "min. RPM"))
        self.label_4.setText(_translate("MainWindow", "Stepper motor settings"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.settings), _translate("MainWindow", "Motor Settings"))
        self.quitButton.setText(_translate("MainWindow", "QUIT"))
        self.mode_single.setText(_translate("MainWindow", "1: single step"))
        self.mode_multi.setText(_translate("MainWindow", "2: multi step"))
        self.mode_perm.setText(_translate("MainWindow", "3: permanent"))
        self.label_2.setText(_translate("MainWindow", "multi step"))
        self.label_3.setText(_translate("MainWindow", "RPM"))
        self.label.setText(_translate("MainWindow", "current pos."))
        self.label_9.setText(_translate("MainWindow", "stored pos. A"))
        self.goto_buttonA.setText(_translate("MainWindow", "GoTo"))
        self.storeButtonA.setText(_translate("MainWindow", "store"))
        self.label_10.setText(_translate("MainWindow", "stored pos. B"))
        self.storeButtonB.setText(_translate("MainWindow", "store"))
        self.goto_buttonB.setText(_translate("MainWindow", "GoTo"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
