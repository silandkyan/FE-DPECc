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
# - die RPM müssten für jeden motor einzeln gepseichert werden aber wenn mehrere Motoren ausgewählt sind
# welche RPM sollen die Motoren dann annehmen?

# als nächstes:
    
# - exklusiv Rechte für die Key control groupBoxen 
# - einstellen, dass sich jedes mal, wenn sich die spin Box Werte für die RPM ändern, mit dem Motor connected
# wird und ihm die Änderung mitgeteilt wird 

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
        self.check()
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
    
        
        
    def check(self):
    # function is called whenever motors should do something to make sure the selected motors
    # are running in specified mode
    # when there is a radioButton group only one of them ahs to be checked since exclusive is enabled
        # check for direction in permanent mode for legs
        global check_forwards_leg
        check_forwards_leg = self.radioB_forwards_leg.isChecked()
        # check for all or single motors selected in legs 
        global check_all
        check_all = self.radioB_all_motors.isChecked()
        # check for the checkBoxes for the individual motors
        global check_zbr 
        check_zbr = self.checkB_zbr.isChecked()
        global check_zbc
        check_zbc = self.checkB_zbc.isChecked()
        global check_zdr
        check_zdr = self.checkB_zdr.isChecked()
        global check_zdc
        check_zdc = self.checkB_zdc.isChecked()
        # check if key control is enabled for legs
        global check_groupB_key_leg
        check_groupB_key_leg = self.groupB_key_control_leg.isChecked()
        
        # check for direction in permanent mode for x
        global check_forwards_x
        check_forwards_x = self.radioB_forwards_x.isChecked()
        # check if key control is enabled for x
        global check_groupB_key_x
        check_groupB_key_x = self.groupB_key_control_x.isChecked()
        
        # check if key control is enabled for pr
        global check_groupB_key_pr
        check_groupB_key_pr = self.groupB_key_control_pr.isChecked()
        # check if key control is enabled for cr
        global check_groupB_key_cr
        check_groupB_key_cr = self.groupB_key_control_cr.isChecked()
        
        # check if key control is enabled for switch
        global check_groupB_key_switch
        check_groupB_key_switch = self.groupB_key_control_switch.isChecked()

        
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
        
    # positional pushButtons
        self.pushB_pos_up.clicked.connect(lambda: self.go_to(1))
        self.pushB_pos_down.clicked.connect(lambda: self.go_to(2))
    

        # self.checkB_zbr.toggled.connect(lambda: self.save_show_stats(1))
        # self.checkB_zbc.toggled.connect(lambda: self.save_show_stats(2))
        # self.checkB_zdr.toggled.connect(lambda: self.save_show_stats(3))
        # self.checkB_zdc.toggled.connect(lambda: self.save_show_stats(4))

        # connections for the overwrite functions:
        self.shortcut_A = QShortcut(QKeySequence('Ctrl+U'), self)
        self.shortcut_A.activated.connect(lambda: self.overwrite(1))
        self.shortcut_B = QShortcut(QKeySequence('Ctrl+D'), self)
        self.shortcut_B.activated.connect(lambda: self.overwrite(2))
        self.shortcut_A = QShortcut(QKeySequence('Ctrl+A'), self)
        self.shortcut_A.activated.connect(lambda: self.overwrite(3))
        self.shortcut_B = QShortcut(QKeySequence('Ctrl+B'), self)
        self.shortcut_B.activated.connect(lambda: self.overwrite(4))
        # self.shortcut_C = QShortcut(QKeySequence('Ctrl+X'), self)
        # self.shortcut_C.activated.connect(lambda: self.overwrite(5))
        # self.shortcut_D = QShortcut(QKeySequence('Ctrl+Y'), self)
        # self.shortcut_D.activated.connect(lambda: self.overwrite(6))
    
    # connections for permanent: 
        # connections für permanent legs
        self.pushB_stop_leg.clicked.connect(lambda: self.stop(1))
        self.pushB_start_leg.clicked.connect(lambda: self.permanent(1))
        # connections für permanent x
        self.pushB_stop_x.clicked.connect(lambda: self.stop(2))
        self.pushB_start_x.clicked.connect(lambda: self.permanent(2))

        
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
        # unchecking the chekBoxes of the individual motor selection
        self.checkB_zbr.setChecked(False)
        self.checkB_zbc.setChecked(False)
        self.checkB_zdr.setChecked(False)
        self.checkB_zdc.setChecked(False)
        # setting checkBoxes uncheckable 
        self.checkB_zbr.setCheckable(False)
        self.checkB_zbc.setCheckable(False)
        self.checkB_zdr.setCheckable(False)
        self.checkB_zdc.setCheckable(False)
        
        
    def save_show_stats(self, motor):
        pass
        
    def go_to(self, direction):
        if direction == 1:
            check_all = self.radioB_all_motors.isChecked()
            if check_all == True:
                self.all_motors(1)
            else: 
                self.single_motors(1)
        else:
            check_all = self.radioB_all_motors.isChecked()
            if check_all == True:
                self.all_motors(2)
            else: 
                self.single_motors(2)
                
    def all_motors(self, direction):
        if direction == 1:
            # motors go to saved position shown on upper LCD
            print("ZBC/ZDC/ZBR/ZCR are heading all the way up: {}mm".format(self.lcd_pos_up.value()))
        else:
            # motors go to saved position shown on lower LCD
            print("ZBC/ZDC/ZBR/ZCR are heading all the way down: {}mm".format(self.lcd_pos_down.value()))
            
    def single_motors(self, direction):
        if direction == 1:
            # selected motors go to saved position shown by LCD
            if check_zbr == True:
                print("ZBR going all the way up {}mm".format(self.lcd_pos_up.value()))
            if check_zbc == True:
                print("ZBC going all the way up {}mm".format(self.lcd_pos_up.value()))
            if check_zdr == True:
                print("ZDR going all the way up {}mm".format(self.lcd_pos_up.value()))
            if check_zdc == True:
                print("ZDC going all the way up {}mm".format(self.lcd_pos_up.value()))
        else:
            if check_zbr == True:
                print("ZBR going all the way down {}mm".format(self.lcd_pos_down.value()))
            if check_zbc == True:
                print("ZBC going all the way down {}mm".format(self.lcd_pos_down.value()))
            if check_zdr == True:
                print("ZDR going all the way down {}mm".format(self.lcd_pos_down.value()))
            if check_zdc == True:
                print("ZDC going all the way down {}mm".format(self.lcd_pos_down.value()))
            
        
        
    
            
            
            
    # functions for position control: 
        
    # def position(self, position):
    #         print("going to position {}".format(position))
            
    def overwrite(self, pos):
        if pos == 1:
            print("position up overwritten to new parameter shown by LCD")
            self.label_overwrite_up.setStyleSheet("QLabel {color: red;}")
        elif pos == 2:
            print("position down overwritten to parameter shown by LCD")
            self.label_overwrite_down.setStyleSheet("QLabel {color: red;}")
        elif pos == 3:
            print("position A overwritten to new parameter shown by LCD")
            self.label_overwrite_A.setStyleSheet("QLabel {color: red;}")
        elif pos == 4:
            print("position B overwritten to parameter shown by LCD")
            self.label_overwrite_B.setStyleSheet("QLabel {color: red;}")
        # elif pos == 5:
        #     print("position X overwritten to parameter shown by LCD") 
        #     self.label_overwrite_X.setStyleSheet("QLabel {color: red;}")
        # elif pos == 6:
        #     print("position Y overwritten to parameter shown by LCD")
        #     self.label_overwrite_Y.setStyleSheet("QLabel {color: red;}")
            
    # functions for permanent:
    def permanent(self, function):
        # function legs 
        if function == 1:
        # run all motors on specified RPM
            # update which mode is active: single or all motors
            self.check()
            if check_all == True:
                if check_forwards_leg == True:
                    print("all leg motors are running forwards on {} RPM".format(self.spinB_RPM_permanent_leg.value()))
                else:
                    print("all leg motors are running backwards on {} RPM".format(self.spinB_RPM_permanent_leg.value()))
            # check which motor is selected
            else:
                if check_zbr == True:
                    if check_forwards_leg == True:
                        print("ZBR is running forwards on {} RPM".format(self.spinB_RPM_permanent_leg.value()))
                    else:
                        print("ZBR is running backwards on {} RPM".format(self.spinB_RPM_permanent_leg.value()))
                if check_zbc == True:
                    if check_forwards_leg == True:
                        print("ZBC is running forwards on {} RPM".format(self.spinB_RPM_permanent_leg.value()))
                    else: 
                        print("ZBC is running backwards on {} RPM".format(self.spinB_RPM_permanent_leg.value()))
                if check_zdr == True:
                    if check_forwards_leg == True:
                        print("ZDR is running forwards on {} RPM".format(self.spinB_RPM_permanent_leg.value()))
                    else:
                        print("ZDR is running backwards on {} RPM".format(self.spinB_RPM_permanent_leg.value()))
                if check_zdc == True:
                    if check_forwards_leg == True:
                        print("ZDC is running forwards on {} RPM".format(self.spinB_RPM_permanent_leg.value()))
                    else: 
                        print("ZDC is running backwards on {} RPM".format(self.spinB_RPM_permanent_leg.value()))
        else:
            if check_forwards_x == True:
                print("X is running forwards on {} RPM".format(self.spinB_RPM_permanent_x.value()))
            else: 
                print("X is running backwards on {} RPM".format(self.spinB_RPM_permanent_x.value()))
            
    def stop(self, function):
        if function == 1:
            # stop all motors: doesn't matter if only one or two are selected 
            print("all leg motors stopped!")
        else:
            # stop the x motor
            print("motor for x movement stopped!")
        




    # functions for keyboard control:
 
    def keyPressEvent(self, event: QKeyEvent) -> None: # pass keys to call the functions 
        key_pressed = event.key()
        self.check() #  makes sure, that only steps are made if the key_control groupBox is enabled
        if check_groupB_key_leg == True:
            if key_pressed == Qt.Key_Up:
                if check_all == True:
                    # if all motors are selected the number of steps from zbr are taken 
                    print("all motors taking {} fine steps forwards".format(self.spinB_zbr_fine.value()))
                else:
                    if check_zbr == True:
                        print("ZBR: fine step: {} steps done forwards".format(self.spinB_zbr_fine.value()))
                    if check_zbc == True:
                        print("ZBC: fine step: {} steps done forwards".format(self.spinB_zbc_fine.value()))
                    if check_zdr == True:
                        print("ZDR: fine step: {} steps done forwards".format(self.spinB_zdr_fine.value()))
                    if check_zdc == True:
                        print("ZDC: fine step: {} steps done forwards".format(self.spinB_zdc_fine.value()))
            elif key_pressed == Qt.Key_Down:
                if check_all == True:
                    # if all motors are selected the number of steps from zbr are taken 
                    print("all motors taking {} fine steps backwards".format(self.spinB_zbr_fine.value()))
                else:
                    if check_zbr == True:
                        print("ZBR: fine step: {} steps done backwards".format(self.spinB_zbr_fine.value()))
                    if check_zbc == True:
                        print("ZBC: fine step: {} steps done backwards".format(self.spinB_zbc_fine.value()))
                    if check_zdr == True:
                        print("ZDR: fine step: {} steps done backwards".format(self.spinB_zdr_fine.value()))
                    if check_zdc == True:
                        print("ZDC: fine step: {} steps done backwards".format(self.spinB_zdc_fine.value()))
            elif key_pressed == Qt.Key_Left:
                if check_all == True:
                    # if all motors are selected the number of steps from zbr are taken 
                    print("all motors taking {} coarse steps forwards".format(self.spinB_zbr_fine.value()))
                else:
                    if check_zbr == True:
                        print("ZBR: coarse step: {} steps done forwards".format(self.spinB_zbr_coarse.value()))
                    if check_zbc == True:
                        print("ZBC: coarse step: {} steps done forwards".format(self.spinB_zbc_coarse.value()))
                    if check_zdr == True:
                        print("ZDR: coarse step: {} steps done forwards".format(self.spinB_zdr_coarse.value()))
                    if check_zdc == True:
                        print("ZDC: coarse step: {} steps done forwards".format(self.spinB_zdc_coarse.value()))
            elif key_pressed == Qt.Key_Right:
                if check_all == True:
                    # if all motors are selected the number of steps from zbr are taken 
                    print("all motors taking {} coarse steps backwards".format(self.spinB_zbr_fine.value()))
                else:
                    if check_zbr == True:
                        print("ZBR: coarse step: {} steps done backwards".format(self.spinB_zbr_coarse.value()))
                    if check_zbc == True:
                        print("ZBC: coarse step: {} steps done backwards".format(self.spinB_zbc_coarse.value()))
                    if check_zdr == True:
                        print("ZDR: coarse step: {} steps done backwards".format(self.spinB_zdr_coarse.value()))
                    if check_zdc == True:
                        print("ZDC: coarse step: {} steps done backwards".format(self.spinB_zdc_coarse.value()))
        elif check_groupB_key_x == True:
            if key_pressed == Qt.Key_Up:
                print("X takes {} fine steps forwards".format(self.spinB_x_fine.value()))
            elif key_pressed == Qt.Key_Down:
                print("X takes {} fine steps backwards".format(self.spinB_x_fine.value()))
            elif key_pressed == Qt.Key_Left:
                print("X takes {} coarse steps forwards".format(self.spinB_x_coarse.value()))
            elif key_pressed == Qt.Key_Right:
                print("X takes {} coarse steps backwards".format(self.spinB_x_coarse.value()))
        elif check_groupB_key_pr == True:
            if key_pressed == Qt.Key_Up:
                print("PR takes {} fine steps forwards".format(self.spinB_pr_fine.value()))
            elif key_pressed == Qt.Key_Down:
                print("PR takes {} fine steps backwards".format(self.spinB_pr_fine.value()))
            elif key_pressed == Qt.Key_Left:
                print("PR takes {} coarse steps forwards".format(self.spinB_pr_coarse.value()))
            elif key_pressed == Qt.Key_Right:
                print("PR takes {} coarse steps backwards".format(self.spinB_pr_coarse.value()))
        elif check_groupB_key_cr == True:
            if key_pressed == Qt.Key_Up:
                print("CR takes {} fine steps forwards".format(self.spinB_cr_fine.value()))
            elif key_pressed == Qt.Key_Down:
                print("CR takes {} fine steps backwards".format(self.spinB_cr_fine.value()))
            elif key_pressed == Qt.Key_Left:
                print("CR takes {} coarse steps forwards".format(self.spinB_cr_coarse.value()))
            elif key_pressed == Qt.Key_Right:
                print("CR takes {} coarse steps backwards".format(self.spinB_cr_coarse.value()))
        elif check_groupB_key_switch == True:
            if key_pressed == Qt.Key_Up:
                print("S takes {} fine steps forwards".format(self.spinB_s_fine.value()))
            elif key_pressed == Qt.Key_Down:
                print("S takes {} fine steps backwards".format(self.spinB_s_fine.value()))
            elif key_pressed == Qt.Key_Left:
                print("S takes {} coarse steps forwards".format(self.spinB_s_coarse.value()))
            elif key_pressed == Qt.Key_Right:
                print("S takes {} coarse steps backwards".format(self.spinB_s_coarse.value()))
                
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
            