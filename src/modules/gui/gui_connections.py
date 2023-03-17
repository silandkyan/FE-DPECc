# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 17:38:27 2023

@author: pschw
"""

# Fragen:
    
# - Control Übersicht: welche Motoren sind mit welchen parametern am laufen?

# Zu beheben:
    
# - Elegantere Lösung für exklusive groupBoxen
# - Die stacked Widgets werden nicht richtig angezeigt obwohl sie im code drin stehen?!
# - bei all leg betrieb: wie viel RPM wird eingestellt?! und wie wirds realisiert?
# - set allowed ranges für die normalen RPM spin Boxen noch anpassen

import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication)
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut
from modules.gui.main_window_ui import Ui_MainWindow


class Window(QMainWindow, Ui_MainWindow):
    '''This custom class inherits from QMainWindow class and the custom 
    Ui_MainWindow class from main_window_ui.py file. That file is created 
    from main_window.ui using the pyuic5 command line program, e.g.:
    pyuic5 -x main_window.ui -o main_window_ui.py
    '''

    
    def __init__(self, parent=None):  
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('FE_DPECc_GUI')
        # setup functions:
        self.setup()
        self.connectSignalsSlots()
        self.show()
        
    def setup(self):
    # because radioButton for all legs is checked by default, 
    # checkBoxes for motorselection are disabled in the setup 
        self.checkB_zbr.setCheckable(False)
        self.checkB_zbc.setCheckable(False)
        self.checkB_zdr.setCheckable(False)
        self.checkB_zdc.setCheckable(False)
    # if a max RPM spinBox changes its value, the maximum of the mastered spinBoxes change accordingly
        # connect if a master RPM spinBox from legs changes 
        self.spinB_zdc_max_RPM.valueChanged.connect(self.RPM_master)
        self.spinB_zdr_max_RPM.valueChanged.connect(self.RPM_master)
        self.spinB_zbc_max_RPM.valueChanged.connect(self.RPM_master)
        self.spinB_zbr_max_RPM.valueChanged.connect(self.RPM_master)
        # connect if a master RPM spinBox from x changes
        self.spinB_x_max_RPM.valueChanged.connect(self.RPM_master)
        # connect if a master RPM spinBox from pr/cr changes
        self.spinB_pr_max_RPM.valueChanged.connect(self.RPM_master)
        # (cr and switch are not mentioned, since they dont have RPM spinBoxes)
        self.save_show_stats(1)
        
        # global RPM_permanent
        # RPM_permanent = self.spinB_RPM_permanent_leg.value()
        # global RPM_when_pushed
        # RPM_when_pushed = self.spinB_RPM_when_pushed_leg.value()
        # global lcd_up
        # lcd_up = self.lcd_pos_up.value()
        # global lcd_down
        # lcd_down = self.lcd_pos_down.value()

        
        
        
    def RPM_master(self):
        
        # max_legs = self.spinB_zdc_max_RPM.value()
        # self.spinB_RPM_permanent.setMaximum(max_legs)
        # self.spinB_RPM_when_pushed_leg.setMaximum(max_legs)
        
        max_x = self.spinB_x_max_RPM.value()
        self.spinB_RPM_permanent_x.setMaximum(max_x)
        self.spinB_RPM_when_pushed_x.setMaximum(max_x)
        self.spinB_RPM_pos_control_x.setMaximum(max_x)
        
        max_pr = self.spinB_pr_max_RPM.value()
        self.spinB_RPM_when_pushed_pr.setMaximum(max_pr)
        self.spinB_RPM_pr_pos_control.setMaximum(max_pr)
        
    
    def connectSignalsSlots(self): 
        
    # connections for enabling group boxes exclusively
    
        # set exclusive for leg tab:
        self.groupB_mselection_leg.clicked.connect(lambda: self.groupB_manager(1)) 
        self.groupB_permanent_leg.clicked.connect(lambda: self.groupB_manager(2))
        self.groupB_when_pushed_leg.clicked.connect(lambda: self.groupB_manager(3))
        self.groupB_key_control_leg.clicked.connect(lambda: self.groupB_manager(4))
        # set exclusive for x direction:
        self.groupB_pos_control_x.clicked.connect(lambda: self.groupB_manager(5))
        self.groupB_permanent_x.clicked.connect(lambda: self.groupB_manager(6))
        self.groupB_when_pushed_x.clicked.connect(lambda: self.groupB_manager(7))
        self.groupB_key_control_x.clicked.connect(lambda: self.groupB_manager(8)) 
        # set exclusive for pr:
        self.groupB_pos_control_pr.clicked.connect(lambda: self.groupB_manager(9))
        self.groupB_when_pushed_pr.clicked.connect(lambda: self.groupB_manager(11))
        self.groupB_key_control_pr.clicked.connect(lambda: self.groupB_manager(12)) 
        # set exclusive for cr:
        self.groupB_pos_control_cr.clicked.connect(lambda: self.groupB_manager(13))
        self.groupB_key_control_cr.clicked.connect(lambda: self.groupB_manager(14)) 
        # set exclusive for switch:
        self.groupB_switch.clicked.connect(lambda: self.groupB_manager(15))
        self.groupB_key_control_switch.clicked.connect(lambda: self.groupB_manager(16))
        
    # checkboxes for individual motors are only be checkable if single motor radioButton is enabled
        # enables checkability for the motor checkBoxes
        self.radioB_single_motor.clicked.connect(self.enable_motorselection)
        # disables checkability and changes values to unchecked 
        self.radioB_all_motors.clicked.connect(self.all_legs_setup)
        
        self.checkB_zbr.toggled.connect(lambda: self.save_show_stats(1))
        self.checkB_zbc.toggled.connect(lambda: self.save_show_stats(2))
        self.checkB_zdc.toggled.connect(lambda: self.save_show_stats(3))
        self.checkB_zdr.toggled.connect(lambda: self.save_show_stats(4))

        
        
        
    # # connections for position control:
        
    #     # connections for the position pushButtons:
    #     self.pushB_pos_A.clicked.connect(lambda: self.position("A"))
    #     self.pushB_pos_B.clicked.connect(lambda: self.position("B"))
    #     self.pushB_pos_C.clicked.connect(lambda: self.position("C"))
    #     self.pushB_pos_D.clicked.connect(lambda: self.position("D"))
        
    #     # connections for the overwrite functions:
    #     self.shortcut_A = QShortcut(QKeySequence('Ctrl+A'), self)
    #     self.shortcut_A.activated.connect(lambda: self.overwrite(1))
    #     self.shortcut_B = QShortcut(QKeySequence('Ctrl+B'), self)
    #     self.shortcut_B.activated.connect(lambda: self.overwrite(2))
    #     self.shortcut_C = QShortcut(QKeySequence('Ctrl+C'), self)
    #     self.shortcut_C.activated.connect(lambda: self.overwrite(3))
    #     self.shortcut_D = QShortcut(QKeySequence('Ctrl+D'), self)
    #     self.shortcut_D.activated.connect(lambda: self.overwrite(4))
    
    # # connections for permanent:
        
    #     self.pushB_stop.clicked.connect(self.stop)
    #     self.pushB_start.clicked.connect(self.permanent)

        
    # # connections for when pushed:
        
    #     self.pushB_forwards.pressed.connect(self.forwards_when_pushed)
    #     self.pushB_backwards.pressed.connect(self.backwards_when_pushed)
        
    # # connections for invert motor direction:
        
    #     #self.pushB_invert_direction.clicked.connect(self.invert)
        
        
        
    # # general functions:
    
    # def forwards(self):
    #     print("running forwards with chosen RPM")                       
    # def backwards(self):
    #     print("running backwards with chosen RPM")
        
    
    

    # functions for setting exclusive groupBoxes:
    
    def groupB_manager(self, gbox):
        if gbox == 1:
            self.groupB_permanent_leg.setChecked(False)
            self.groupB_when_pushed_leg.setChecked(False)
            self.groupB_key_control_leg.setChecked(False)
        if gbox == 2:
            self.groupB_mselection_leg.setChecked(False)
            self.groupB_when_pushed_leg.setChecked(False)
            self.groupB_key_control_leg.setChecked(False)
        if gbox == 3:
            self.groupB_permanent_leg.setChecked(False)
            self.groupB_mselection_leg.setChecked(False)
            self.groupB_key_control_leg.setChecked(False)
        if gbox == 4:
            self.groupB_permanent_leg.setChecked(False)
            self.groupB_when_pushed_leg.setChecked(False)
            self.groupB_mselection_leg.setChecked(False) 
            
        if gbox == 5:
            self.groupB_permanent_x.setChecked(False)
            self.groupB_when_pushed_x.setChecked(False)
            self.groupB_key_control_x.setChecked(False)
        if gbox == 6:
            self.groupB_pos_control_x.setChecked(False)
            self.groupB_when_pushed_x.setChecked(False)
            self.groupB_key_control_x.setChecked(False)
        if gbox == 7:
            self.groupB_pos_control_x.setChecked(False)
            self.groupB_permanent_x.setChecked(False)
            self.groupB_key_control_x.setChecked(False)
        if gbox == 8:
            self.groupB_pos_control_x.setChecked(False)
            self.groupB_permanent_x.setChecked(False)
            self.groupB_when_pushed_x.setChecked(False)
            
        if gbox == 9:
            self.groupB_when_pushed_pr.setChecked(False)
            self.groupB_key_control_pr.setChecked(False)
        if gbox == 11:
            self.groupB_pos_control_pr.setChecked(False)
            self.groupB_key_control_pr.setChecked(False)
        if gbox == 12:
            self.groupB_pos_control_pr.setChecked(False)
            self.groupB_when_pushed_pr.setChecked(False)
            
        if gbox == 13:
            self.groupB_key_control_cr.setChecked(False)
        if gbox == 14:
            self.groupB_pos_control_cr.setChecked(False)
            
        if gbox == 15:
            self.groupB_key_control_switch.setChecked(False)
        if gbox == 16:
            self.groupB_switch.setChecked(False)
            
    # functions for enabling checkability and checked state 
    def enable_motorselection(self):
        self.checkB_zbr.setCheckable(True)
        self.checkB_zbc.setCheckable(True)
        self.checkB_zdr.setCheckable(True)
        self.checkB_zdc.setCheckable(True)
        
    def all_legs_setup(self):
        self.checkB_zbr.setChecked(False)
        self.checkB_zbc.setChecked(False)
        self.checkB_zdr.setChecked(False)
        self.checkB_zdc.setChecked(False)
        self.checkB_zbr.setCheckable(False)
        self.checkB_zbc.setCheckable(False)
        self.checkB_zdr.setCheckable(False)
        self.checkB_zdc.setCheckable(False)
        
    def save_show_stats(self, motor):
        if motor == 1:
            checkB_zbr = self.checkB_zbr.isChecked()
            if checkB_zbr == False:
                global RPM_permanent
                RPM_permanent = self.spinB_RPM_permanent_leg.value()
                global RPM_when_pushed
                RPM_when_pushed = self.spinB_RPM_when_pushed_leg.value()
                global lcd_up
                lcd_up = self.lcd_pos_up.value()
                global lcd_down
                lcd_down = self.lcd_pos_down.value()
            else: 
                self.spinB_RPM_permanent_leg.setValue(RPM_permanent)
                self.spinB_RPM_when_pushed_leg.setValue(RPM_when_pushed)
                self.lcd_pos_up.display(lcd_up)
                self.lcd_pos_down.display(lcd_down)
        if motor == 2:
            checkB_zbc = self.checkB_zbc.isChecked()
            if checkB_zbc == False:
                global RPM_permanent_zbc
                RPM_permanent_zbc = self.spinB_RPM_permanent_leg.value()
                global RPM_when_pushed_zbc
                RPM_when_pushed_zbc = self.spinB_RPM_when_pushed_leg.value()
                global lcd_up_zbc
                lcd_up_zbc = self.lcd_pos_up.value()
                global lcd_down_zbc
                lcd_down_zbc = self.lcd_pos_down.value()
            else: 
                self.spinB_RPM_permanent_leg.setValue(RPM_permanent_zbc)
                self.spinB_RPM_when_pushed_leg.setValue(RPM_when_pushed_zbc)
                self.lcd_pos_up.display(lcd_up_zbc)
                self.lcd_pos_down.display(lcd_down_zbc)
        if motor == 3:
            checkB_zdr = self.checkB_zdr.isChecked()
            if checkB_zdr == False:
                global RPM_permanent_zdr
                RPM_permanent_zdr = self.spinB_RPM_permanent_leg.value()
                global RPM_when_pushed_zdr
                RPM_when_pushed_zdr = self.spinB_RPM_when_pushed_leg.value()
                global lcd_up_zdr
                lcd_up_zdr = self.lcd_pos_up.value()
                global lcd_down_zdr
                lcd_down_zdr = self.lcd_pos_down.value()
            else: 
                self.spinB_RPM_permanent_leg.setValue(RPM_permanent_zdr)
                self.spinB_RPM_when_pushed_leg.setValue(RPM_when_pushed_zdr)
                self.lcd_pos_up.display(lcd_up_zdr)
                self.lcd_pos_down.display(lcd_down_zdr)
        if motor == 4:
            checkB_zdc = self.checkB_zdc.isChecked()
            if checkB_zdc == False:
                global RPM_permanent_zdc
                RPM_permanent_zdc = self.spinB_RPM_permanent_leg.value()
                global RPM_when_pushed_zdc
                RPM_when_pushed_zdc = self.spinB_RPM_when_pushed_leg.value()
                global lcd_up_zdc
                lcd_up_zdc = self.lcd_pos_up.value()
                global lcd_down_zdc
                lcd_down_zdc = self.lcd_pos_down.value()
            else: 
                self.spinB_RPM_permanent_leg.setValue(RPM_permanent_zdc)
                self.spinB_RPM_when_pushed_leg.setValue(RPM_when_pushed_zdc)
                self.lcd_pos_up.display(lcd_up_zdc)
                self.lcd_pos_down.display(lcd_down_zdc)
     
    # functions for position control: 
        
    # def position(self, position):
    #         print("going to position {}".format(position))
            
    # def overwrite(self, pos):
    #     if pos == 1:
    #         self.lcdNumber.display(self.counter)
    #         print("position A overwritten to parameter shown by LCD")
    #         self.label_overwrite_A.setStyleSheet("QLabel {color: red;}")
    #     elif pos == 2:
    #         self.lcdNumber_3.display(self.counter) 
    #         print("position B overwritten to parameter shown by LCD")
    #         self.label_overwrite_B.setStyleSheet("QLabel {color: red;}")
    #         time.sleep(3)
    #     elif pos == 3:
    #         self.lcdNumber_5.display(self.counter)
    #         print("position C overwritten to parameter shown by LCD") 
    #         self.label_overwrite_C.setStyleSheet("QLabel {color: red;}")
    #     elif pos == 4:
    #         self.lcdNumber_7.display(self.counter) 
    #         print("position D overwritten to parameter shown by LCD")
    #         self.label_overwrite_D.setStyleSheet("QLabel {color: red;}")
            
    # # functions for permanent:
        
    # def permanent(self):
    #     self.timer_interval(1/(self.spinB_RPM_permanent.value() * self.spinB_RPM_when_pushed.value()) * 60000)
    #     self.timer.start()
    #     radio_for = self.radioB_forwards.isChecked()
    #     if radio_for == True:
    #         self.timer.timeout.connect(lambda: self.count(1))
    #         print("adjusting to new RMP and direction")
    #         time.sleep(3)
    #         self.forwards()
    #     else: 
    #         self.timer.timeout.connect(lambda: self.count(2))
    #         print("adjusting to new RMP and direction")
    #         time.sleep(3)
    #         self.backwards()

        
    # def stop(self):
    #     self.timer.stop()
    #     print("motor is stopping, ramp down from {} RPM".format(self.spinB_RPM_permanent.value()))
    #     time.sleep(3)
    #     print("motor stopped!")
        
    # # functions for keyboard control:
 
    # def keyPressEvent(self, event: QKeyEvent) -> None: # pass keys to call the functions 
    #     key_pressed = event.key()
    #     key_print = self.groupB_key_control.isChecked() # key_print makes sure, that only steps are made if the key_control groupBox is enabled
    #     if key_print == True:
    #         if key_pressed == Qt.Key_Up:
    #             print("fine step: {} steps done forwards with {} RPM".format(self.spinB_single_steps.value(), self.spinB_RPM_settings.value()))
    #             self.counter += float((self.spinB_single_steps.value()) / self.spinB_steps_per_revo.value())
    #         elif key_pressed == Qt.Key_Down:
    #             print("fine step: {} steps done backwards with {} RPM".format(self.spinB_single_steps.value(), self.spinB_RPM_settings.value()))
    #             self.counter -= float((self.spinB_single_steps.value()) / self.spinB_steps_per_revo.value())
    #         elif key_pressed == Qt.Key_Left:
    #             print("coarse step: {} steps done forwards with {} RPM".format(self.spinB_multi_steps.value(), self.spinB_RPM_settings.value()))
    #             self.counter += float((self.spinB_multi_steps.value()) / self.spinB_steps_per_revo.value())
    #         elif key_pressed == Qt.Key_Right:
    #             print("coarse step: {} steps done backwards with {} RPM".format(self.spinB_multi_steps.value(), self.spinB_RPM_settings.value()))
    #             self.counter -= float((self.spinB_multi_steps.value()) / self.spinB_steps_per_revo.value())
            
                
    # # functions for when pushed:
    
    # # steps_per_min is a variable which claculates the frequence of steps, according to the RPM per revolution (specified on second tab)
    # # and the RPM given in the spin box (factor 60000 is due to scaling from miliseconds to minutes)
    # def forwards_when_pushed(self):  
    #     steps_per_min = 1/(self.spinB_steps_per_revo.value() * self.spinB_RPM_when_pushed.value()) * 60000
    #     self.pushB_forwards.setAutoRepeatInterval(steps_per_min)
    #     print("running forwards with {} RPM".format(self.spinB_RPM_when_pushed.value()))

    # def backwards_when_pushed(self):
    #     steps_per_min = 1/(self.spinB_steps_per_revo.value() * self.spinB_RPM_when_pushed.value()) * 60000
    #     self.pushB_backwards.setAutoRepeatInterval(steps_per_min)
    #     print("running backwards with {} RPM".format(self.spinB_RPM_when_pushed.value()))

        
        
    # function for invert motor direction:
        
        

          
def run_app(): 
    app = 0
    # Initialize GUI control flow management. Requires passing
    # argument vector (sys.argv) or empty list [] as arg; the former allows
    # to pass configuration commands on startup to the program from the
    # command line, if such commands were implemented.
    # If app is already open, use that one, otherwise open new app:
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
    # Create main window (= instance of custom Window Class):
    main_win = Window()
    # Open GUI window on screen:
    main_win.show()
    # Return an instance of a running QApplication = starts event handling
    return app.exec()
            