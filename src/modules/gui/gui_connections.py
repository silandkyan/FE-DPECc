# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 17:38:27 2023

@author: pschw
"""

# Zu beheben:
    
# - Elegantere Lösung für exklusive groupBoxen
# - bei all leg betrieb: wie viel RPM wird eingestellt?! und wie wirds realisiert?
# - die RPM müssten für jeden motor einzeln gepseichert werden aber wenn mehrere Motoren ausgewählt sind
#   welche RPM sollen die Motoren dann annehmen?
# - die parameter sind immer überschreibbar auch wenn man in anderem Tab ist: ändern?!
# - die ganzen globalen Variablen in Klassenvariablen umwandeln?!
# - Codeabfolge umordnen, sodass die connecitons direkt über den funktionen stehen?!
# -> lohnt sich das überhaupt je nach dem wie viel noch verändert wird
# - wie wichitg ist es, dass die spin Boxen den Wert anzeigen den man zuvor eingestellt hat? 


# Offen:
    
# - Funktionen die den motoren mitteilen wie viele RPM sie machen sollen? 
# - Funktionen oder variablen die mm bzw. deg mit gegebener RPM Zahl in pps umrechnen 
# - Die LCD anzeigen für die individuellen Motoren in save und show stat Funktionen 
# - jedes mal wenn sich die microstep resolution für einen Motor ändert muss mit der 
# init drive settings funktion connected werden und mit der init ramp settings funktion


# als nächstes:

# - die invert Buttons verknüpfen 
# - einstellen, dass sich jedes mal, wenn sich die spin Box Werte für die RPM ändern, mit dem Motor connected
# wird und ihm die Änderung mitgeteilt wird 
# - set allowed ranges für die leg RPM spin Boxen noch anpassen

# Gui fusion mit motor control:

# - eine wrapper funktion für permanent modus ODER die obere bzw. untere Anschlagsposition wählen?
# - wie kann when pushed realisiert werden?
# - bei keyboard control muss auch noch eine Geschwindigkeit angegeben werden und dann move by steps funktion nehmen 
# - einfache TMCL funktion für invert motor direction?
# - umrechnungsfunktion von mm auf der Achse bzw. deg auf msteps

import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication)
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut
from modules.gui.main_window_ui import Ui_MainWindow

from ..Motor import Motor 
from pytrinamic.connections import ConnectionManager


# settings...

# port_list = ConnectionManager().list_connections()
# for port in port_list:
#     Motor(port)
    
# module_L, module_R = Motor.assign_modules()

# print(module_L.status_message())
# print(module_R.status_message())




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
        self.spinB_leg_max_RPM.valueChanged.connect(self.RPM_master)
        # connect if a master RPM spinBox from x changes
        self.spinB_x_max_RPM.valueChanged.connect(self.RPM_master)
        # connect if a master RPM spinBox from pr/cr changes
        self.spinB_pr_max_RPM.valueChanged.connect(self.RPM_master)
        # (cr and switch are not mentioned, since they dont have RPM spinBoxes)
    
        
    def check(self):
    # function is called whenever motors should do something to make sure the selected motors
    # are running in specified mode
    # when there is a radioButton group only one of them has to be checked since they have exclusive property
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


        
    def RPM_master(self):

        max_legs = self.spinB_leg_max_RPM.value()
        self.spinBox_RPM_leg.setMaximum(max_legs)
        
        max_x = self.spinB_x_max_RPM.value()
        self.spinB_RPM_x.setMaximum(max_x)
        
        max_pr = self.spinB_pr_max_RPM.value()
        self.spinB_RPM_pr.setMaximum(max_pr)

        max_s = self.spinB_s_max_RPM.value()
        self.spinB_RPM_s.setMaximum(max_s)
        
        
    def pps_calculator(self):
        pps = round(self.spinB_RPM_permanent_x.value() * self.motor.msteps_per_rev / 60)
        return pps 
    
    
    def connectSignalsSlots(self): 

    # checkboxes for individual motors are only be checkable if single motor radioButton is enabled
        # enables checkability for the motor checkBoxes
        self.radioB_single_motor.clicked.connect(self.enable_motorselection)
        #self.radioB_single_motor.clicked.connect(lambda: self.select_module(module_R))
        # disables checkability and changes values to unchecked 
        self.radioB_all_motors.clicked.connect(self.all_legs_setup)
        #self.radioB_all_motors.clicked.connect(lambda: self.select_module(module_L))
        #self.radioB_all_motors.clicked.connect(self.refresh_motor_list)
        
        
        
        #change pages when pushButton for different pages is clicked 
        self.pushB_s_cr.clicked.connect(lambda: self.stackedW_settings_s.setCurrentIndex(1))
        self.pushB_s_cr_2.clicked.connect(lambda: self.stackedW_settings_s.setCurrentIndex(0))
        
    # same three buttons share different funcitionalities permanent,
    # when pushed and keyboard control which are enabled with these connect_... funcitons
        #functions for leg
        self.radioB_permanent_leg.pressed.connect(self.connection_permanent)
        self.radioB_when_pushed_leg.pressed.connect(self.connection_when_pushed)
        self.radioB_key_control_leg.pressed.connect(lambda: self.key_control(1))
        #functions for x
        self.radioB_permanent_x.pressed.connect(self.connection_permanent)
        self.radioB_when_pushed_x.pressed.connect(self.connection_when_pushed)
        self.radioB_key_control_x.pressed.connect(lambda: self.key_control(2))
        #functions for pr
        self.radioB_key_control_pr.pressed.connect(lambda: self.key_control(3))
        self.radioB_key_control_s.pressed.connect(lambda: self.key_control(4))
        self.radioB_key_control_cr.pressed.connect(lambda: self.key_control(5))
    
        
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
        self.pushB_stop_x.clicked.connect(self.stop)
        # ablsolute for pr
        self.pushB_start_pr.clicked.connect(lambda: self.absolute_pos(2))
        self.pushB_stop_pr.clicked.connect(self.stop)
        
    # connections for specimen switch
        self.pushB_switch.clicked.connect(self.next_specimen)
        
        
    # connections for the overwrite functions:
        # connnecitons for leg  position overwrite 
        self.shortcut = QShortcut(QKeySequence('Ctrl+U'), self)
        self.shortcut.activated.connect(lambda: self.overwrite(1))
        self.shortcut = QShortcut(QKeySequence('Ctrl+D'), self)
        self.shortcut.activated.connect(lambda: self.overwrite(2))
        # connections for x position overwrite 
        self.shortcut = QShortcut(QKeySequence('Ctrl+A'), self)
        self.shortcut.activated.connect(lambda: self.overwrite(3))
        self.shortcut = QShortcut(QKeySequence('Ctrl+B'), self)
        self.shortcut.activated.connect(lambda: self.overwrite(4))
        # connections for pr position overwrite 
        self.shortcut = QShortcut(QKeySequence('Ctrl+X'), self)
        self.shortcut.activated.connect(lambda: self.overwrite(5))
        self.shortcut = QShortcut(QKeySequence('Ctrl+Y'), self)
        self.shortcut.activated.connect(lambda: self.overwrite(6))
        
    def select_module(self, m):
        self.module = m
        self.motor = self.module.motor
        #print('Selected motor:', self.motor)
        print(self.module.status_message())
        
    
    
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
            print("PR is heading for position X: {}".format(self.lcd_pos_X.value()))
        if position == 6:
            # pr is heading for position shown by lower LCD: -15 by default
            print("PR is heading for position Y: {}".format(self.lcd_pos_Y.value()))
            
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
                print("ZDC going all the way down: {}mm".format(self.lcd_pos_down.value()))
                
    def absolute_pos(self, pos):
        if pos  == 1:
            print("X is going to absolute position: {}mm with {} RPM".format(self.dspinB_mm_axis_x.value(), self.spinB_RPM_x.value()))
        else: 
            print("PR is going ot absolute position: {}deg with {} RPM".format(self.dspinBox_deg_on_axis_pr.value(), self.spinB_RPM_pr.value()))
            
    def overwrite(self, pos):
    # this function should feature an output for the motor position in microsteps at the moment and display it in LCDs
        if pos == 1:
            # get int(self.motor.actual_position) as value for LCD
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
            self.label_overwrite_X.setStyleSheet("QLabel {color: red;}")
        elif pos == 6:
            print("position Y overwritten to parameter shown by LCD")
            self.label_overwrite_Y.setStyleSheet("QLabel {color: red;}")
       
        
       
        
       
        
       
        
       
        
    def connection_permanent(self):
        self.pushB_forwards_leg.clicked.connect(lambda: self.permanent(1))  
        self.pushB_backwards_leg.clicked.connect(lambda: self.permanent(2))
        self.pushB_stop_leg.clicked.connect(self.stop)    

        self.pushB_forwards_x.clicked.connect(lambda: self.permanent(3))  
        self.pushB_backwards_x.clicked.connect(lambda: self.permanent(4))
        self.pushB_stop_x1.clicked.connect(self.stop) 
        
        self.pushB_lefthand.clicked.connect(lambda: self.permanent(5))
        self.pushB_righthand.clicked.connect(lambda: self.permanent(6))
        self.pushB_stop_pr1.clicked.connect(self.stop) 
    
    def connection_when_pushed(self):
        self.pushB_forwards_leg.pressed.connect(lambda: self.when_pushed(1)) 
        self.pushB_backwards_leg.pressed.connect(lambda: self.when_pushed(2))
        self.pushB_stop_leg.clicked.connect(self.stop)    

        self.pushB_forwards_x.pressed.connect(lambda: self.when_pushed(3))  
        self.pushB_backwards_x.pressed.connect(lambda: self.when_pushed(4))
        self.pushB_stop_x1.clicked.connect(self.stop) 
        
        self.pushB_lefthand.pressed.connect(lambda: self.when_pushed(5))  
        self.pushB_righthand.pressed.connect(lambda: self.when_pushed(6))
        self.pushB_stop_pr1.clicked.connect(self.stop)  
        
        
    # functions for keyboard control:
    def key_control(self, mode, event: QKeyEvent) -> None:
        key_pressed = event.key()
        self.check()
        if mode == 1:
        # functions for leg keyboard control 
            # fine step left 
            if key_pressed == Qt.Key_Up:
                # check if all or single mode is active -> if single is active: which motors 
                if check_all == True:
                    # if all motors are selected the number of steps from zbr are taken 
                    print("all motors taking {} fine steps forwards".format(self.spinB_leg_fine.value()))
                else:
                    if check_zbr == True:
                        print("ZBR: fine step: {} steps done forwards".format(self.spinB_leg_fine.value()))
                    if check_zbc == True:
                        print("ZBC: fine step: {} steps done forwards".format(self.spinB_leg_fine.value()))
                    if check_zdr == True:
                        print("ZDR: fine step: {} steps done forwards".format(self.spinB_leg_fine.value()))
                    if check_zdc == True:
                        print("ZDC: fine step: {} steps done forwards".format(self.spinB_leg_fine.value()))
            # fine step right
            elif key_pressed == Qt.Key_Down:
                # check if all or single mode is active -> if single is active: which motors
                if check_all == True:
                    # if all motors are selected the number of steps from zbr are taken 
                    print("all motors taking {} fine steps backwards".format(self.spinB_leg_fine.value()))
                else:
                    if check_zbr == True:
                        print("ZBR: fine step: {} steps done backwards".format(self.spinB_leg_fine.value()))
                    if check_zbc == True:
                        print("ZBC: fine step: {} steps done backwards".format(self.spinB_leg_fine.value()))
                    if check_zdr == True:
                        print("ZDR: fine step: {} steps done backwards".format(self.spinB_leg_fine.value()))
                    if check_zdc == True:
                        print("ZDC: fine step: {} steps done backwards".format(self.spinB_leg_fine.value()))
            # coarse step left 
            elif key_pressed == Qt.Key_Left:
                # check if all or single mode is active -> if single is active: which motors
                if check_all == True:
                    # if all motors are selected the number of steps from zbr are taken 
                    print("all motors taking {} coarse steps forwards".format(self.spinB_leg_coarse.value()))
                else:
                    if check_zbr == True:
                        print("ZBR: coarse step: {} steps done forwards".format(self.spinB_leg_coarse.value()))
                    if check_zbc == True:
                        print("ZBC: coarse step: {} steps done forwards".format(self.spinB_leg_coarse.value()))
                    if check_zdr == True:
                        print("ZDR: coarse step: {} steps done forwards".format(self.spinB_leg_coarse.value()))
                    if check_zdc == True:
                        print("ZDC: coarse step: {} steps done forwards".format(self.spinB_leg_coarse.value()))
            # coarse step right
            elif key_pressed == Qt.Key_Right:
                # check if all or single mode is active -> if single is active: which motors
                if check_all == True:
                    # if all motors are selected the number of steps from zbr are taken 
                    print("all motors taking {} coarse steps backwards".format(self.spinB_leg_coarse.value()))
                else:
                    if check_zbr == True:
                        print("ZBR: coarse step: {} steps done backwards".format(self.spinB_leg_coarse.value()))
                    if check_zbc == True:
                        print("ZBC: coarse step: {} steps done backwards".format(self.spinB_leg_coarse.value()))
                    if check_zdr == True:
                        print("ZDR: coarse step: {} steps done backwards".format(self.spinB_leg_coarse.value()))
                    if check_zdc == True:
                        print("ZDC: coarse step: {} steps done backwards".format(self.spinB_leg_coarse.value()))
        if mode == 2:
        # key controls for x 
            # fine step forwards
            if key_pressed == Qt.Key_Up:
                print("X takes {} fine steps forwards".format(self.spinB_x_fine.value()))
            # fine step backwards
            elif key_pressed == Qt.Key_Down:
                print("X takes {} fine steps backwards".format(self.spinB_x_fine.value()))
            # coarse step forwards
            elif key_pressed == Qt.Key_Left:
                print("X takes {} coarse steps forwards".format(self.spinB_x_coarse.value()))
            # coarse step backwards
            elif key_pressed == Qt.Key_Right:
                print("X takes {} coarse steps backwards".format(self.spinB_x_coarse.value()))
                
        if mode == 3:
        # key controls for pr
            if key_pressed == Qt.Key_Up:
                print("PR takes {} fine steps forwards".format(self.spinB_pr_fine.value()))
            elif key_pressed == Qt.Key_Down:
                print("PR takes {} fine steps backwards".format(self.spinB_pr_fine.value()))
            elif key_pressed == Qt.Key_Left:
                print("PR takes {} coarse steps forwards".format(self.spinB_pr_coarse.value()))
            elif key_pressed == Qt.Key_Right:
                print("PR takes {} coarse steps backwards".format(self.spinB_pr_coarse.value()))
                
        if mode == 4:
        # key controls for cr
            if key_pressed == Qt.Key_Up:
                print("CR takes {} fine steps forwards".format(self.spinB_cr_fine.value()))
            elif key_pressed == Qt.Key_Down:
                print("CR takes {} fine steps backwards".format(self.spinB_cr_fine.value()))
            elif key_pressed == Qt.Key_Left:
                print("CR takes {} coarse steps forwards".format(self.spinB_cr_coarse.value()))
            elif key_pressed == Qt.Key_Right:
                print("CR takes {} coarse steps backwards".format(self.spinB_cr_coarse.value()))
                
        if mode == 5:
        # key controls for switch
            if key_pressed == Qt.Key_Up:
                print("S takes {} fine steps forwards".format(self.spinB_s_fine.value()))
            elif key_pressed == Qt.Key_Down:
                print("S takes {} fine steps backwards".format(self.spinB_s_fine.value()))
            elif key_pressed == Qt.Key_Left:
                print("S takes {} coarse steps forwards".format(self.spinB_s_coarse.value()))
            elif key_pressed == Qt.Key_Right:
                print("S takes {} coarse steps backwards".format(self.spinB_s_coarse.value()))
            
            
        
    # functions for permanent:
    def permanent(self, mode):
        self.check()
        if mode == 1:
            if check_all == True:
                print("all motors are running permanently forwards on {} RPM".format(self.spinBox_RPM_leg.value()))
            # single mode: check which motor is selected
            else:
                self.check() # properties have to be checked again in case of directions change 
                if check_zbr == True:
                        print("ZBR is running permanently forwards on {} RPM".format(self.spinBox_RPM_leg.value()))

                if check_zbc == True:
                        print("ZBC is running permanently forwards on {} RPM".format(self.spinBox_RPM_leg.value()))

                if check_zdr == True:
                        print("ZDR is running permanently forwards on {} RPM".format(self.spinBox_RPM_leg.value()))

                if check_zdc == True:
                        print("ZDC is running permanently forwards on {} RPM".format(self.spinBox_RPM_leg.value()))
        if mode == 2:
            if check_all == True:
                print("all motors are running permanently backwards on {} RPM".format(self.spinBox_RPM_leg.value()))
            # single mode: check which motor is selected
            else:
                self.check() # properties have to be checked again in case of directions change 
                if check_zbr == True:
                        print("ZBR is running permanently backwards on {} RPM".format(self.spinBox_RPM_leg.value()))

                if check_zbc == True:
                        print("ZBC is running permanently backwards on {} RPM".format(self.spinBox_RPM_leg.value()))

                if check_zdr == True:
                        print("ZDR is running permanently backwards on {} RPM".format(self.spinBox_RPM_leg.value()))

                if check_zdc == True:
                        print("ZDC is running permanently backwards on {} RPM".format(self.spinBox_RPM_leg.value()))
        if mode == 3:
            pps = self.pps_calculator()
            print("X is running permanently forwards on {} RPM".format(self.spinB_RPM_x.value()))
            #self.motor.motor.rotate(pps)
        if mode == 4:
            pps = self.pps_calculator()
            print("X is running permanently backwards on {} RPM".format(self.spinB_RPM_x.value()))
            #self.motor.motor.rotate(-pps)
            
        if mode  == 5:
            pps = self.pps_calculator()
            print("PR is running permanently lefthand on {} RPM".format(self.spinB_RPM_pr.value()))
            #self.motor.motor.rotate(-pps)
        if mode == 6:
            pps = self.pps_calculator()
            print("PR is running permanently righthand on {} RPM".format(self.spinB_RPM_pr.value()))
            #self.motor.motor.rotate(-pps)
            
    def when_pushed(self, mode):
        self.check()
        if mode == 1:
            if check_all == True:
                steps_per_min = 1/(400 * self.spinBox_RPM_leg.value()) * 60000
                self.pushB_forwards_leg.setAutoRepeatInterval(steps_per_min)
                print("all motors are running forwards on {} RPM".format(self.spinBox_RPM_leg.value()))
            # single mode: check which motor is selected
            else:
                self.check() # properties have to be checked again in case of directions change 
                if check_zbr == True:
                    steps_per_min = 1/(400 * self.spinBox_RPM_leg.value()) * 60000
                    self.pushB_forwards_leg.setAutoRepeatInterval(steps_per_min)
                    print("ZBR is running forwards on {} RPM".format(self.spinBox_RPM_leg.value()))

                if check_zbc == True:
                    steps_per_min = 1/(400 * self.spinBox_RPM_leg.value()) * 60000
                    self.pushB_forwards_leg.setAutoRepeatInterval(steps_per_min)
                    print("ZBC is running forwards on {} RPM".format(self.spinBox_RPM_leg.value()))

                if check_zdr == True:
                    steps_per_min = 1/(400 * self.spinBox_RPM_leg.value()) * 60000
                    self.pushB_forwards_leg.setAutoRepeatInterval(steps_per_min)
                    print("ZDR is running forwards on {} RPM".format(self.spinBox_RPM_leg.value()))

                if check_zdc == True:
                    steps_per_min = 1/(400 * self.spinBox_RPM_leg.value()) * 60000
                    self.pushB_forwards_leg.setAutoRepeatInterval(steps_per_min)
                    print("ZDC is running forwards on {} RPM".format(self.spinBox_RPM_leg.value()))
        if mode == 2:
            if check_all == True:
                steps_per_min = 1/(400 * self.spinBox_RPM_leg.value()) * 60000
                self.pushB_backwards_leg.setAutoRepeatInterval(steps_per_min)
                print("all motors are running backwards on {} RPM".format(self.spinBox_RPM_leg.value()))
            # single mode: check which motor is selected
            else:
                self.check() # properties have to be checked again in case of directions change 
                if check_zbr == True:
                        steps_per_min = 1/(400 * self.spinBox_RPM_leg.value()) * 60000
                        self.pushB_backwards_leg.setAutoRepeatInterval(steps_per_min)
                        print("ZBR is running backwards on {} RPM".format(self.spinBox_RPM_leg.value()))

                if check_zbc == True:
                        steps_per_min = 1/(400 * self.spinBox_RPM_leg.value()) * 60000
                        self.pushB_backwards_leg.setAutoRepeatInterval(steps_per_min)
                        print("ZBC is running backwards on {} RPM".format(self.spinBox_RPM_leg.value()))

                if check_zdr == True:
                        steps_per_min = 1/(400 * self.spinBox_RPM_leg.value()) * 60000
                        self.pushB_backwards_leg.setAutoRepeatInterval(steps_per_min)
                        print("ZDR is running backwards on {} RPM".format(self.spinBox_RPM_leg.value()))

                if check_zdc == True:
                        steps_per_min = 1/(400 * self.spinBox_RPM_leg.value()) * 60000
                        self.pushB_backwards_leg.setAutoRepeatInterval(steps_per_min)
                        print("ZDC is running backwards on {} RPM".format(self.spinBox_RPM_leg.value()))
        if mode == 3:
            steps_per_min = 1/(400 * self.spinB_RPM_x.value()) * 60000
            self.pushB_forwards_x.setAutoRepeatInterval(steps_per_min)
            pps = self.pps_calculator()
            print("X is running forwards on {} RPM".format(self.spinB_RPM_x.value()))
            # make step 
        if mode == 4:
            steps_per_min = 1/(400 * self.spinB_RPM_x.value()) * 60000
            self.pushB_backwards_x.setAutoRepeatInterval(steps_per_min)
            pps = self.pps_calculator()
            print("X is running backwards on {} RPM".format(self.spinB_RPM_x.value()))
            # make step
            
        if mode == 5:
            steps_per_min = 1/(400 * self.spinB_RPM_pr.value()) * 60000
            self.pushB_lefthand.setAutoRepeatInterval(steps_per_min)
            pps = self.pps_calculator()
            print("PR is running lefthand on {} RPM".format(self.spinB_RPM_pr.value()))
            # make step
        if mode == 6:
            steps_per_min = 1/(400 * self.spinB_RPM_pr.value()) * 60000
            self.pushB_righthand.setAutoRepeatInterval(steps_per_min)
            pps = self.pps_calculator()
            print("PR is running righthand on {} RPM".format(self.spinB_RPM_pr.value()))
            # make step
        
    def stop(self):
        #self.motor.motor.stop()
        print("Motor stopped!")    
    
        
    # function for specimen switch specimen
    def next_specimen(self):
        print("take next specimen from mag")
        
    # function for invert motor direction:
        # maybe by a simple command from given tmcl 
                
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
            
