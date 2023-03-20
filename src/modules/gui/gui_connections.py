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
    
# - einstellen, dass sich jedes mal, wenn sich die spin Box Werte für die RPM ändern, mit dem Motor connected
# wird und ihm die Änderung mitgeteilt wird 

import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication)
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtCore import Qt
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
    # when there is a radioButton group only one of them has to be checked since they have exclusive property
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
    # the individual spinBoxes for max motor RPM are all operating on the same spinBoxes, 
    # thus the maxima for each motor have to be saved for each one individually
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
        
    # setting the key control groupBoxes exclusive
        self.groupB_key_control_leg.clicked.connect(lambda: self.groupB_manager(17))
        self.groupB_key_control_x.clicked.connect(lambda: self.groupB_manager(18))
        self.groupB_key_control_pr.clicked.connect(lambda: self.groupB_manager(19))
        self.groupB_key_control_cr.clicked.connect(lambda: self.groupB_manager(20))
        self.groupB_key_control_switch.clicked.connect(lambda: self.groupB_manager(21))
    # checkboxes for individual motors are only be checkable if single motor radioButton is enabled
        # enables checkability for the motor checkBoxes
        self.radioB_single_motor.clicked.connect(self.enable_motorselection)
        # disables checkability and changes values to unchecked 
        self.radioB_all_motors.clicked.connect(self.all_legs_setup)
        
    # positional pushButtons
        # go to position leg 
        self.pushB_pos_up.clicked.connect(lambda: self.go_to(1))
        self.pushB_pos_down.clicked.connect(lambda: self.go_to(2))
        # go to position x 
        self.pushB_pos_A.clicked.connect(lambda: self.go_to(3))
        self.pushB_pos_B.clicked.connect(lambda: self.go_to(4))
        # go to position pr
        self.pushB_pos_X.clicked.connect(lambda: self.go_to(5))
        self.pushB_pos_Y.clicked.connect(lambda: self.go_to(6))
        # go to position cr
        self.pushB_pos_raman.clicked.connect(lambda: self.go_to(7))
        self.pushB_pos_ion_beam.clicked.connect(lambda: self.go_to(8))
        
    # absolute position pushButtons:
        # absolute for x
        self.pushB_start_x.clicked.connect(lambda: self.absolute_pos(1))
        self.pushB_stop_x.clicked.connect(lambda: self.stop(2))
        # ablsolute for pr
        self.pushB_start_pr.clicked.connect(lambda: self.absolute_pos(2))
        self.pushB_stop_pr.clicked.connect(lambda: self.stop(3))
    
    # next page pushButton for settings 
        # change pages in settings for leg
        self.pushB_settings_leg_1.clicked.connect(lambda: self.stackedW_settings_leg.setCurrentIndex(1))
        self.pushB_settings_leg_2.clicked.connect(lambda: self.stackedW_settings_leg.setCurrentIndex(2))
        self.pushB_settings_leg_3.clicked.connect(lambda: self.stackedW_settings_leg.setCurrentIndex(3))
        self.pushB_settings_leg_4.clicked.connect(lambda: self.stackedW_settings_leg.setCurrentIndex(0))
        # change pages in settings for pr and cr 
        self.pushB_settings_pr_cr_1.clicked.connect(lambda: self.stackedW_settings_pr_cr.setCurrentIndex(1))
        self.pushB_settings_pr_cr_2.clicked.connect(lambda: self.stackedW_settings_pr_cr.setCurrentIndex(0))
        
        
    
    # functions which are supposed to save the motor stats everytime the selected motor gets disabled 
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
        self.shortcut_C = QShortcut(QKeySequence('Ctrl+X'), self)
        self.shortcut_C.activated.connect(lambda: self.overwrite(5))
        self.shortcut_D = QShortcut(QKeySequence('Ctrl+Y'), self)
        self.shortcut_D.activated.connect(lambda: self.overwrite(6))
    
    # connections for permanent: 
        # connections für permanent legs
        self.pushB_stop_leg.clicked.connect(lambda: self.stop(1))
        self.pushB_start_leg.clicked.connect(lambda: self.permanent(1))
        # connections für permanent x
        self.pushB_stop_x.clicked.connect(lambda: self.stop(2))
        self.pushB_start_x.clicked.connect(lambda: self.permanent(2))

        
    # connections for when pushed:
        # connections for when pushed leg
        self.pushB_forwards_leg.pressed.connect(lambda: self.forwards_when_pushed(1))
        self.pushB_backwards_leg.pressed.connect(lambda: self.backwards_when_pushed(1))
        # connections for when pushed x
        self.pushB_forwards_x.pressed.connect(lambda: self.forwards_when_pushed(2))
        self.pushB_backwards_x.pressed.connect(lambda: self.backwards_when_pushed(2))
        # connections for when pushed pr
        self.pushB_lefthand.pressed.connect(lambda: self.forwards_when_pushed(3))
        self.pushB_righthand.pressed.connect(lambda: self.backwards_when_pushed(3))

    # # connections for invert motor direction:
        
    #     #self.pushB_invert_direction.clicked.connect(self.invert)
        
    
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
            
        if gbox == 17:
            self.groupB_key_control_x.setChecked(False)
            self.groupB_key_control_pr.setChecked(False)
            self.groupB_key_control_cr.setChecked(False)
            self.groupB_key_control_switch.setChecked(False)
        if gbox == 18:
            self.groupB_key_control_leg.setChecked(False)
            self.groupB_key_control_pr.setChecked(False)
            self.groupB_key_control_cr.setChecked(False)
            self.groupB_key_control_switch.setChecked(False)
        if gbox == 19:
            self.groupB_key_control_x.setChecked(False)
            self.groupB_key_control_leg.setChecked(False)
            self.groupB_key_control_cr.setChecked(False)
            self.groupB_key_control_switch.setChecked(False)
        if gbox == 20:
            self.groupB_key_control_x.setChecked(False)
            self.groupB_key_control_pr.setChecked(False)
            self.groupB_key_control_leg.setChecked(False)
            self.groupB_key_control_switch.setChecked(False)
        if gbox == 21:
            self.groupB_key_control_x.setChecked(False)
            self.groupB_key_control_pr.setChecked(False)
            self.groupB_key_control_cr.setChecked(False)
            self.groupB_key_control_leg.setChecked(False)
            
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
        # this function is somehow supposed to take the values from the spinBoxes and lcd and save it 
        # for every motor 
        pass
    
    # this function lets the motors drive to the position which are shown by the LCDs in microsteps    
    def go_to(self, position):
        # at first direction gets checked and then there is a check for which motors are selected 
        self.check() # update which mode is active: single or all motors
        
        # position control for leg 
        if position == 1:
            if check_all == True:
                self.all_motors(1)
            else: 
                self.single_motors(1)
        if position == 2:
            if check_all == True:
                self.all_motors(2)
            else: 
                self.single_motors(2)
                
        # positon control for x  
        if position == 3:
            # x is heading for position shown by upper LCD: 500 by default 
            print("X is heading for position A: {}".format(self.lcd_pos_A.value()))
        if position == 4:
            # x is heading for position shown by lower LCD: -500 by default
            print("X is heading for position B: {}".format(self.lcd_pos_B.value()))
            
        # positon control for pr
        if position == 5:
            # pr is heading for position shown by upper LCD: 15 by default 
            print("PR is heading for position X: {}".format(self.lcd_pos_C.value()))
        if position == 6:
            # pr is heading for position shown by lower LCD: -15 by default
            print("PR is heading for position Y: {}".format(self.lcd_pos_D.value()))
            
        # positon control for cr
        if position == 7:
            # cr is heading for position shown by upper LCD: 90 by default 
            print("CR is heading for position raman: {}".format(self.lcd_pos_raman.value()))
        if position == 8:
            # cr is heading for position shown by lower LCD: 0 by default
            print("CR is heading for position ion beam: {}".format(self.lcd_pos_ion_beam.value()))
           
    # all motors and single motors are functions for leg tab
    def all_motors(self, direction):
        if direction == 1:
            # motors go to saved position shown on upper LCD
            print("ZBC/ZDC/ZBR/ZCR are heading for all the way up: {}mm".format(self.lcd_pos_up.value()))
        else:
            # motors go to saved position shown on lower LCD
            print("ZBC/ZDC/ZBR/ZCR are heading for all the way down: {}mm".format(self.lcd_pos_down.value()))
            
    def single_motors(self, direction):
        if direction == 1:
            # selected motors go to saved position shown by LCD
            if check_zbr == True:
                print("ZBR going all the way up: {}mm".format(self.lcd_pos_up.value()))
            if check_zbc == True:
                print("ZBC going all the way up: {}mm".format(self.lcd_pos_up.value()))
            if check_zdr == True:
                print("ZDR going all the way up: {}mm".format(self.lcd_pos_up.value()))
            if check_zdc == True:
                print("ZDC going all the way up: {}mm".format(self.lcd_pos_up.value()))
        else:
            if check_zbr == True:
                print("ZBR going all the way down: {}mm".format(self.lcd_pos_down.value()))
            if check_zbc == True:
                print("ZBC going all the way down: {}mm".format(self.lcd_pos_down.value()))
            if check_zdr == True:
                print("ZDR going all the way down: {}mm".format(self.lcd_pos_down.value()))
            if check_zdc == True:
                print("ZDC going all the way down: {}mm".format(self.lcd_pos_down.value()))#
                
    def absolute_pos(self, pos):
        if pos  == 1:
            print("X is going to absolute position: {}mm with {} RPM".format(self.dspinB_mm_axis_x.value(), self.spinB_RPM_pos_control_x.value()))
        else: 
            print("PR is going ot absolute position: {}deg with {} RPM".format(self.dspinBox_deg_on_axis_pr.value(), self.spinB_RPM_pr_pos_control.value()))
            
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
        elif pos == 5:
            print("position X overwritten to parameter shown by LCD") 
            self.label_overwrite_C.setStyleSheet("QLabel {color: red;}")
        elif pos == 6:
            print("position Y overwritten to parameter shown by LCD")
            self.label_overwrite_D.setStyleSheet("QLabel {color: red;}")
            
    # functions for permanent:
    def permanent(self, function):
        # permanent functions for legs 
        if function == 1:
        # run all motors on specified RPM
            # update which mode is active: single or all motors
            self.check()
            # all motors mode 
            if check_all == True:
                if check_forwards_leg == True:
                    print("all leg motors are running forwards on {} RPM".format(self.spinB_RPM_permanent_leg.value()))
                else:
                    print("all leg motors are running backwards on {} RPM".format(self.spinB_RPM_permanent_leg.value()))
            # single mode: check which motor is selected
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
        # permanent functions for x
        else:
            if check_forwards_x == True:
                print("X is running forwards on {} RPM".format(self.spinB_RPM_permanent_x.value()))
            else: 
                print("X is running backwards on {} RPM".format(self.spinB_RPM_permanent_x.value()))
    
    #stop function for permanent mode in leg and x
    def stop(self, function):
        if function == 1:
            # stop all motors: doesn't matter if only one or two are selected 
            print("all leg motors stopped!")
        if function == 2:
            # stop x motor
            print("motor for x movement stopped!")
        if function == 3:
            # stop pr motor
            print("motor for pr rotation stopped!")

    # functions for keyboard control:
    def keyPressEvent(self, event: QKeyEvent) -> None: # pass keys to call the functions 
        # event gets defined and keys are specified below 
        key_pressed = event.key()
        self.check() # update which mode is active: single or all motors or key control mode from other function 
        
        # key controls for leg
        if check_groupB_key_leg == True:
            # fine step left 
            if key_pressed == Qt.Key_Up:
                # check if all or single mode is active -> if single is active: which motors 
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
            # fine step right
            elif key_pressed == Qt.Key_Down:
                # check if all or single mode is active -> if single is active: which motors
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
            # coarse step left 
            elif key_pressed == Qt.Key_Left:
                # check if all or single mode is active -> if single is active: which motors
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
            # coarse step right
            elif key_pressed == Qt.Key_Right:
                # check if all or single mode is active -> if single is active: which motors
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
                        
        # key controls for x
        elif check_groupB_key_x == True:
            if key_pressed == Qt.Key_Up:
                print("X takes {} fine steps forwards".format(self.spinB_x_fine.value()))
            elif key_pressed == Qt.Key_Down:
                print("X takes {} fine steps backwards".format(self.spinB_x_fine.value()))
            elif key_pressed == Qt.Key_Left:
                print("X takes {} coarse steps forwards".format(self.spinB_x_coarse.value()))
            elif key_pressed == Qt.Key_Right:
                print("X takes {} coarse steps backwards".format(self.spinB_x_coarse.value()))
                
        # key controls for pr
        elif check_groupB_key_pr == True:
            if key_pressed == Qt.Key_Up:
                print("PR takes {} fine steps forwards".format(self.spinB_pr_fine.value()))
            elif key_pressed == Qt.Key_Down:
                print("PR takes {} fine steps backwards".format(self.spinB_pr_fine.value()))
            elif key_pressed == Qt.Key_Left:
                print("PR takes {} coarse steps forwards".format(self.spinB_pr_coarse.value()))
            elif key_pressed == Qt.Key_Right:
                print("PR takes {} coarse steps backwards".format(self.spinB_pr_coarse.value()))
        # key controls for cr
        elif check_groupB_key_cr == True:
            if key_pressed == Qt.Key_Up:
                print("CR takes {} fine steps forwards".format(self.spinB_cr_fine.value()))
            elif key_pressed == Qt.Key_Down:
                print("CR takes {} fine steps backwards".format(self.spinB_cr_fine.value()))
            elif key_pressed == Qt.Key_Left:
                print("CR takes {} coarse steps forwards".format(self.spinB_cr_coarse.value()))
            elif key_pressed == Qt.Key_Right:
                print("CR takes {} coarse steps backwards".format(self.spinB_cr_coarse.value()))
        # key controls for switch
        elif check_groupB_key_switch == True:
            if key_pressed == Qt.Key_Up:
                print("S takes {} fine steps forwards".format(self.spinB_s_fine.value()))
            elif key_pressed == Qt.Key_Down:
                print("S takes {} fine steps backwards".format(self.spinB_s_fine.value()))
            elif key_pressed == Qt.Key_Left:
                print("S takes {} coarse steps forwards".format(self.spinB_s_coarse.value()))
            elif key_pressed == Qt.Key_Right:
                print("S takes {} coarse steps backwards".format(self.spinB_s_coarse.value()))
                
    # functions for when pushed:
    
    # steps_per_min is a variable which calculates the frequence of steps, according to the RPM per revolution (given in settings)
    # and the RPM given in the spin box (factor 60000 is due to scaling from miliseconds to minutes)
    def forwards_when_pushed(self, function):  
        self.check() # update which mode is active: single or all motors or when pushed mode from other function 
        # when pushed forwards for leg
        if function == 1:
            if check_all == True:
                # if all motors are running the step amount per rotation gets derived form settings of zbr
                steps_per_min = 1/(self.spinB_zbr_steps_per_rev.value() * self.spinB_RPM_when_pushed_leg.value()) * 60000
                self.pushB_forwards_leg.setAutoRepeatInterval(steps_per_min)
                print("all motors running forwards with {} RPM".format(self.spinB_RPM_when_pushed_leg.value()))
            else:
                if check_zbr == True:
                    steps_per_min = 1/(self.spinB_zbr_steps_per_rev.value() * self.spinB_RPM_when_pushed_leg.value()) * 60000
                    self.pushB_forwards_leg.setAutoRepeatInterval(steps_per_min)
                    print("ZBR is running forwards with {} RPM".format(self.spinB_RPM_when_pushed_leg.value()))
                if check_zbc == True:
                    steps_per_min = 1/(self.spinB_zbc_steps_per_rev.value() * self.spinB_RPM_when_pushed_leg.value()) * 60000
                    self.pushB_forwards_leg.setAutoRepeatInterval(steps_per_min)
                    print("ZBC is running forwards with {} RPM".format(self.spinB_RPM_when_pushed_leg.value()))
                if check_zdr == True:
                    steps_per_min = 1/(self.spinB_zdr_steps_per_rev.value() * self.spinB_RPM_when_pushed_leg.value()) * 60000
                    self.pushB_forwards_leg.setAutoRepeatInterval(steps_per_min)
                    print("ZDR is running forwards with {} RPM".format(self.spinB_RPM_when_pushed_leg.value()))
                if check_zdc == True:
                    steps_per_min = 1/(self.spinB_zdc_steps_per_rev.value() * self.spinB_RPM_when_pushed_leg.value()) * 60000
                    self.pushB_forwards_leg.setAutoRepeatInterval(steps_per_min)
                    print("ZDC is running forwards with {} RPM".format(self.spinB_RPM_when_pushed_leg.value()))#
        # when pushed forwards for x            
        if function == 2:
                steps_per_min = 1/(self.spinB_x_steps_per_rev.value() * self.spinB_RPM_when_pushed_x.value()) * 60000
                self.pushB_forwards_x.setAutoRepeatInterval(steps_per_min)
                print("X is running forwards with {} RPM".format(self.spinB_RPM_when_pushed_x.value()))
        # when pushed lefthand for pr
        if function == 3:
                steps_per_min = 1/(self.spinB_pr_steps_per_rev.value() * self.spinB_RPM_when_pushed_pr.value()) * 60000
                self.pushB_lefthand.setAutoRepeatInterval(steps_per_min)
                print("PR is running lefthand with {} RPM".format(self.spinB_RPM_when_pushed_pr.value()))    

    def backwards_when_pushed(self, function):
        self.check() # update which mode is active: single or all motors or when pushed mode from other function
        # when pushed backwards for leg 
        if function == 1:
            if check_all == True:
                # if all motors are running the step amount per rotation gets derived form settings of zbr
                steps_per_min = 1/(self.spinB_zbr_steps_per_rev.value() * self.spinB_RPM_when_pushed_leg.value()) * 60000
                self.pushB_backwards_leg.setAutoRepeatInterval(steps_per_min)
                print("all motors running backwards with {} RPM".format(self.spinB_RPM_when_pushed_leg.value()))
            else:
                if check_zbr == True:
                    steps_per_min = 1/(self.spinB_zbr_steps_per_rev.value() * self.spinB_RPM_when_pushed_leg.value()) * 60000
                    self.pushB_backwards_leg.setAutoRepeatInterval(steps_per_min)
                    print("ZBR is running backwards with {} RPM".format(self.spinB_RPM_when_pushed_leg.value()))
                if check_zbc == True:
                    steps_per_min = 1/(self.spinB_zbc_steps_per_rev.value() * self.spinB_RPM_when_pushed_leg.value()) * 60000
                    self.pushB_backwards_leg.setAutoRepeatInterval(steps_per_min)
                    print("ZBC is running backwards with {} RPM".format(self.spinB_RPM_when_pushed_leg.value()))
                if check_zdr == True:
                    steps_per_min = 1/(self.spinB_zdr_steps_per_rev.value() * self.spinB_RPM_when_pushed_leg.value()) * 60000
                    self.pushB_backwards_leg.setAutoRepeatInterval(steps_per_min)
                    print("ZDR is running backwards with {} RPM".format(self.spinB_RPM_when_pushed_leg.value()))
                if check_zdc == True:
                    steps_per_min = 1/(self.spinB_zdc_steps_per_rev.value() * self.spinB_RPM_when_pushed_leg.value()) * 60000
                    self.pushB_backwards_leg.setAutoRepeatInterval(steps_per_min)
                    print("ZDC is running backwards with {} RPM".format(self.spinB_RPM_when_pushed_leg.value()))#
        # when pushed backwards for x       
        if function == 2:
                steps_per_min = 1/(self.spinB_x_steps_per_rev.value() * self.spinB_RPM_when_pushed_x.value()) * 60000
                self.pushB_backwards_x.setAutoRepeatInterval(steps_per_min)
                print("X is running backwards with {} RPM".format(self.spinB_RPM_when_pushed_x.value()))
        # when pushed righthand for pr
        if function == 3:
                steps_per_min = 1/(self.spinB_pr_steps_per_rev.value() * self.spinB_RPM_when_pushed_pr.value()) * 60000
                self.pushB_righthand.setAutoRepeatInterval(steps_per_min)
                print("PR is running righthand with {} RPM".format(self.spinB_RPM_when_pushed_pr.value()))
        
        
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
            