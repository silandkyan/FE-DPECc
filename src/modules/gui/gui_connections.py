# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 17:38:27 2023

@author: pschw
"""

# jeder Motor braucht seine eignene spinbox für die mm oder deg pro umdrehung
# die go to funktion überarbeiten 
# aus pr und cr entweder radiobuttons machen oder dass cr irgendwie nur über keyboard gesteuert wird 
# wenn ein neuer Tab mit einem einzigen motor geöffnet wird muss das richtige modul selected werden 

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
    
#module_zbr, module_zbc = Motor.assign_modules() # module_zdr, module_zdc, module_x, module_pr, module_cr, module_s

# print(module_zbr.status_message())
# print(module_zbc.status_message())
# print(module_zdr.status_message())
# print(module_zdc.status_message())
# print(module_pr.status_message())
# print(module_cr.status_message())
# print(module_s.status_message())



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
        self.spinB_max_RPM.valueChanged.connect(self.RPM_master)
        # connect if a master RPM spinBox from x changes
        self.refresh_motor_list(1)
        # self.module = module_R
        # self.module.motor = module_R.motor
        # self.active_modules = [self.module]

        
    def RPM_master(self):
        max_RPM = self.spinB_max_RPM.value()
        self.spinBox_RPM.setMaximum(max_RPM)
    
    def pps_calculator(self):
        pps = round(self.spinB_RPM.value() * 200*16 / 60) 
        self.pps = pps
        
    def mm_deg_to_steps(self, mm_deg ,mm_deg_per_rev):
        msteps = round(mm_deg / mm_deg_per_rev * 200*16, 3)
        self.msteps = msteps
    
    def connectSignalsSlots(self): 
    # connections for positional pushButtons
        # go to position leg 
        self.pushB_pos_u.clicked.connect(lambda: self.multi_module_control(self.go_to(1)))
        self.pushB_pos_d.clicked.connect(lambda: self.multi_module_control(self.go_to(2)))
        # go to position x 
        self.pushB_pos_a.clicked.connect(lambda: self.multi_module_control(self.go_to(3)))
        self.pushB_pos_b.clicked.connect(lambda: self.multi_module_control(self.go_to(4)))
        # go to position pr
        self.pushB_pos_x.clicked.connect(lambda: self.multi_module_control(self.go_to(5)))
        self.pushB_pos_y.clicked.connect(lambda: self.multi_module_control(self.go_to(6)))
        # go to position cr
        self.pushB_pos_r.clicked.connect(lambda: self.multi_module_control(self.go_to(7)))
        self.pushB_pos_i.clicked.connect(lambda: self.multi_module_control(self.go_to(8)))
        
    # connections for absolute position pushButtons:
        # absolute for x
        #self.pushB_start_x.clicked.connect(lambda: self.select_module(module_x))
        self.pushB_start_x.clicked.connect(lambda: self.go_to(9))
        self.pushB_stop_x.clicked.connect(self.stop_motor)
        #ablsolute for pr and cr
        self.pushB_start_pr_cr.clicked.connect(lambda: self.multi_module_control(self.go_to(10)))
        self.pushB_stop_pr_cr.clicked.connect(self.stop_motor)
        
    # connections for specimen switch
        # self.pushB_switch.clicked.connect(self.next_specimen)
    
        
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
        # connections for cr overwrite 
        self.shortcut = QShortcut(QKeySequence('Ctrl+R'), self)
        self.shortcut.activated.connect(lambda: self.overwrite(7))
        self.shortcut = QShortcut(QKeySequence('Ctrl+I'), self)
        self.shortcut.activated.connect(lambda: self.overwrite(8))
            
            
        # self.radioB_permanent_when_pushed.pressed.connect(lambda: self.set_mode(1))
        
        
        self.radioB_single_motor.clicked.connect(self.enable_motorselection)
        self.radioB_all_motors.clicked.connect(self.all_legs_setup)
        
        # if the all leg radioButton is pressed, all the motors are selected
        self.radioB_all_motors.clicked.connect(lambda: self.refresh_motor_list(1))
        
        # if select leg motor is enabled, the list is refreshed when new motors are chosen
        self.checkB_zbr.toggled.connect(lambda: self.refresh_motor_list(2))
        self.checkB_zbc.toggled.connect(lambda: self.refresh_motor_list(2))
        self.checkB_zdr.toggled.connect(lambda: self.refresh_motor_list(2))
        self.checkB_zdc.toggled.connect(lambda: self.refresh_motor_list(2))
        
        self.checkB_pr.toggled.connect(lambda: self.refresh_motor_list(2))
        self.checkB_cr.toggled.connect(lambda: self.refresh_motor_list(2))
        
        # connections for the individual buttons
        #self.pushB_upwards1.clicked.connect(lambda: self.multi_module_control(self.permanent_left))
        self.pushB_upwards1.clicked.connect(self.permanent_right)
        #self.pushB_downwards1.clicked.connect(lambda: self.multi_module_control(self.permanent_right))
        self.pushB_downwards1.clicked.connect(self.permanent_left) 
        #self.pushB_stop_legs.clicked.connect(lambda: self.multi_module_control(self.stop_motor))
        self.pushB_stop_legs.clicked.connect(lambda: print('all leg motors stopped'))
        
        #self.pushB_upwards.pressed.connect(lambda: self.multi_module_control(permanent_right))
        #self.pushB_upwards2.released.connect(lambda: self.multi_module_control(self.stop_motor))
        self.pushB_upwards2.pressed.connect(self.permanent_right)
        self.pushB_upwards2.released.connect(self.stop_motor)
        #self.pushB_downwards.pressed.connect(lambda: self.multi_module_control(self.permanent_left))
        #self.pushB_downwards2.released.connect(lambda: self.multi_module_control(self.stop_motor))
        self.pushB_downwards2.pressed.connect(self.permanent_left)
        self.pushB_downwards2.released.connect(self.stop_motor)
        
        
        #self.pushB_forwards1.clicked.connect(lambda: self.select_module(module_x))
        self.pushB_forwards1.clicked.connect(self.permanent_right)
        #self.pushB_backwards1.clicked.connect(lambda: self.select_module(module_x))
        self.pushB_backwards1.clicked.connect(self.permanent_left)
        #self.pushB_stop_x.clicked.connect(lambda: self.select_module(module_x))
        self.pushB_stop_x.clicked.connect(self.stop_motor)
        
        #self.pushB_forwards2.clicked.connect(lambda: self.select_module(module_x))
        self.pushB_forwards2.pressed.connect(self.permanent_right)
        self.pushB_forwards2.released.connect(self.stop_motor)
        #self.pushB_backwards2.clicked.connect(lambda: self.select_module(module_x))
        self.pushB_backwards2.pressed.connect(self.permanent_left)
        self.pushB_backwards2.released.connect(self.stop_motor)

        

        #self.pushB_clockwise1.clicked.connect(lambda: self.select_module(module_pr))
        self.pushB_clockwise1.clicked.connect(self.permanent_right)
        #self.pushB_counterclockwise1.clicked.connect(lambda: self.select_module(module_pr))
        self.pushB_counterclockwise1.clicked.connect(self.permanent_left)
        #self.pushB_stop_pr_cr.clicked.connect(lambda: self.select_module(module_pr))
        self.pushB_stop_pr_cr.clicked.connect(self.stop_motor)
        
        #self.pushB_clockwise1.clicked.connect(lambda: self.select_module(module_pr))
        self.pushB_clockwise2.pressed.connect(self.permanent_right)
        self.pushB_clockwise2.released.connect(self.stop_motor)
        #self.pushB_counterclockwise1.clicked.connect(lambda: self.select_module(module_pr))
        self.pushB_counterclockwise2.pressed.connect(self.permanent_left)
        self.pushB_counterclockwise2.released.connect(self.stop_motor)


        
        #self.pushB_switch.clicked.connect(lambda: self.select_module(module_s))
        #self.pushB_switch.clicked.connect(self.permanent_left)

        
    def select_module(self, m):
        '''Module selection for single module use.'''
        self.module = m
        self.motor = self.module.motor
        print('Selected motor: Motor', self.module.moduleID)
        #print(self.module.status_message()) 

    # def set_mode(self, mode):
    #     self.mode = mode
    #     print('Mode:', mode)
        
    def refresh_motor_list(self, select):
        self.active_modules = []
        boxlist = [self.checkB_zbr, self.checkB_zbc,self.checkB_zdr, self.checkB_zdc,
                        self.checkB_pr, self.checkB_cr]
        if select == 1:
            #self.active_modules.append(module_zbr, module_zbc) #, module_zdr, module_zdc
            print('All leg motors are selected')                              
                                       
        if select == 2:     
            for box in boxlist:
                if box.isChecked() == True:
                    if box == self.checkB_zbr:
                        #self.active_modules.append(module_R)
                        print('ZBR appended')
                    if box == self.checkB_zbc:  
                        #self.active_modules.append(module_R)
                        print('ZBC appended')
                    if box == self.checkB_zdr:                   
                        #self.active_modules.append(module_zdr)
                        print('ZDR appended')
                    if box == self.checkB_zdc:
                        #self.active_modules.append(module_zdc)
                        print('ZDC appended')
                    if box == self.checkB_pr:                   
                        #self.active_modules.append(module_pr)
                        self.radioB_all_motors.setChecked(True) # calling this function makes sure, when working with 
                        self.all_legs_setup()                   # pr/cr the leg motors are deleted from active module list
                        print('PR appended')
                    if box == self.checkB_cr:                   
                        #self.active_modules.append(module_cr)
                        self.radioB_all_motors.setChecked(True)
                        self.all_legs_setup()
                        print('CR appended')
        print('Selected motor(s):')
        for module in self.active_modules:
            print('Motor', module.moduleID)
        
    def multi_module_control(self, action):
        for module in self.active_modules:
            self.module = module
            self.motor = module.motor
            action()
            
    # def left(self):
    #     print('Mode:', self.mode)
    #     if self.mode == 1:
    #         self.permanent_left()

        
    # def right(self):
    #     print('Mode:', self.mode)
    #     if self.mode == 1:
    #         self.permanent_right()
            
            
    def permanent_left(self):
        if self.radioB_permanent_when_pushed.isChecked() == True:
            #self.motor.rotate(-self.pps)
            print('Rotating left with', str(self.spinB_RPM.value()), 'rpm')
    
    def permanent_right(self):
        if self.radioB_permanent_when_pushed.isChecked() == True:
            #self.motor.rotate(self.pps)
            print('Rotating right with', str(self.spinB_RPM.value()), 'rpm')
            
    def fine_step_left(self):
        #msteps = self.module.msteps_per_fstep * self.spinB_fine.value()
        #self.motor.move_by(-msteps, self.pps)
        print('Fine steps left with:', str(self.active_modules), 'and', str(self.spinB_RPM.value()), 'RPM')
        
    def coarse_step_left(self):
        #msteps = self.module.msteps_per_fstep * self.spinB_coarse.value()
        #self.motor.move_by(-msteps, self.pps)
        print('Coarse steps left with:', str(self.active_modules), 'and', str(self.spinB_RPM.value()), 'RPM')
        
    def fine_step_right(self):
        #msteps = self.module.msteps_per_fstep * self.spinB_fine.value()
        #self.motor.move_by(msteps, self.pps)
        print('Fine steps right with:', str(self.active_modules), 'and', str(self.spinB_RPM.value()), 'RPM')
        
    def coarse_step_right(self):
        #msteps = self.module.msteps_per_fstep * self.spinB_coarse.value()
        #self.motor.move_by(msteps, self.pps)
        print('Coarse steps right with:', str(self.active_modules), 'and', str(self.spinB_RPM.value()), 'RPM')

    def keyPressEvent(self, event: QKeyEvent) -> None: # pass keys to call the functions 
        # event gets defined and keys are specified below 
        key_pressed = event.key()
        if self.radioB_key_control.isChecked() == True:
            if key_pressed == Qt.Key_S:
                #self.multi_module_control(self.fine_step_left)
                print('Fine steps left with:', str(self.active_modules), 'and', str(self.spinB_RPM.value()), 'RPM')
            if key_pressed == Qt.Key_A:
                #self.multi_module_control(self.coarse_step_left)
                print('Coarse steps left with:', str(self.active_modules), 'and', str(self.spinB_RPM.value()), 'RPM')
            if key_pressed == Qt.Key_W:
                #self.multi_module_control(self.fine_step_right)
                print('Fine steps right with:', str(self.active_modules), 'and', str(self.spinB_RPM.value()), 'RPM')
            if key_pressed == Qt.Key_D:
                #self.multi_module_control(self.coarse_step_right)
                print('Coarse steps right with:', str(self.active_modules), 'and', str(self.spinB_RPM.value()), 'RPM')
            
    def stop_motor(self):
        #self.module.motor.stop()
        #print('Motor', self.module.moduleID, 'stopped!')
        print("Motors stopped")
        
        
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
        if position == 1:
            self.mm_deg_to_steps(self.lcd_pos_u.value(), self.spinB_mm_per_rev.value())
            #!!!mm_per_rev / deg_per_rev is individual for every axis, thus additional spinBoxes!!!
            #self.motor.move_to(self.msteps, self.pps)
            print('Going to position Up shown by according LCD')
        # positon control for x  
        if position == 2:
            self.mm_deg_to_steps(self.lcd_pos_d.value(), self.spinB_mm_per_rev.value())
            #!!!mm_per_rev / deg_per_rev is individual for every axis, thus additional spinBoxes!!!
            #self.motor.move_to(self.msteps, self.pps)
            print('Going to position Down shown by according LCD')
        if position == 3:
            self.mm_deg_to_steps(self.lcd_pos_a.value(), self.spinB_mm_per_rev.value())
            #!!!mm_per_rev / deg_per_rev is individual for every axis, thus additional spinBoxes!!!
            #self.motor.move_to(self.msteps, self.pps)
            print('Going to position A shown by according LCD')
        if position == 4:
            self.mm_deg_to_steps(self.lcd_pos_b.value(), self.spinB_mm_per_rev.value())
            #!!!mm_per_rev / deg_per_rev is individual for every axis, thus additional spinBoxes!!!
            #self.motor.move_to(self.msteps, self.pps)
            print('Going to position B shown by according LCD')
        if position == 5:
            self.mm_deg_to_steps(self.lcd_pos_x.value(), self.spinB_mm_per_rev.value())
            #!!!mm_per_rev / deg_per_rev is individual for every axis, thus additional spinBoxes!!!
            #self.motor.move_to(self.msteps, self.pps)
            print('Going to position X shown by according LCD')
        if position == 6:
            self.mm_deg_to_steps(self.lcd_pos_y.value(), self.spinB_mm_per_rev.value())
            #!!!mm_per_rev / deg_per_rev is individual for every axis, thus additional spinBoxes!!!
            #self.motor.move_to(self.msteps, self.pps)
            print('Going to position Y shown by according LCD')
        if position == 7:
            self.mm_deg_to_steps(self.lcd_pos_r.value(), self.spinB_mm_per_rev.value())
            #!!!mm_per_rev / deg_per_rev is individual for every axis, thus additional spinBoxes!!!
            #self.motor.move_to(self.msteps, self.pps)
            print('Going to position Raman shown by according LCD')
        if position == 8:
            self.mm_deg_to_steps(self.lcd_pos_i.value(), self.spinB_mm_per_rev.value())
            #!!!mm_per_rev / deg_per_rev is individual for every axis, thus additional spinBoxes!!!
            #self.motor.move_to(self.msteps, self.pps)
            print('Going to position Ion beam shown by according LCD')
        if position == 9:
            self.mm_deg_to_steps(self.dspinB_mm_axis_x.value(), self.spinB_mm_per_rev.value())
            #!!!mm_per_rev / deg_per_rev is individual for every axis, thus additional spinBoxes!!!
            #self.motor.move_to(self.msteps, self.pps)
            print('X is going to position chosen in spinBox according LCD')
        if position == 10:
            self.mm_deg_to_steps(self.dspinB_deg_axis_pr_cr.value(), self.spinB_mm_per_rev.value())
            #!!!mm_per_rev / deg_per_rev is individual for every axis, thus additional spinBoxes!!!
            #self.motor.move_to(self.msteps, self.pps)
            print('PR is going to position chosen in spinBox according LCD')

           
    def overwrite(self, pos):
    # this function should feature an output for the motor position in microsteps at the moment and display it in LCDs
        if pos == 1:
            # get int(self.motor.actual_position) as value for LCD
            print("position up overwritten to new parameter shown by LCD")
            self.label_overwrite_u.setStyleSheet("QLabel {color: red;}")
        elif pos == 2:
            print("position down overwritten to parameter shown by LCD")
            self.label_overwrite_d.setStyleSheet("QLabel {color: red;}")
        elif pos == 3:
            print("position A overwritten to new parameter shown by LCD")
            self.label_overwrite_a.setStyleSheet("QLabel {color: red;}")
        elif pos == 4:
            print("position B overwritten to parameter shown by LCD")
            self.label_overwrite_b.setStyleSheet("QLabel {color: red;}")
        elif pos == 5:
            print("position X overwritten to parameter shown by LCD") 
            self.label_overwrite_x.setStyleSheet("QLabel {color: red;}")
        elif pos == 6:
            print("position Y overwritten to parameter shown by LCD")
            self.label_overwrite_y.setStyleSheet("QLabel {color: red;}")
        elif pos == 7:
            print("position Raman overwritten to parameter shown by LCD")
            self.label_overwrite_r.setStyleSheet("QLabel {color: red;}")
        elif pos == 8:
            print("position Ion beam overwritten to parameter shown by LCD")
            self.label_overwrite_i.setStyleSheet("QLabel {color: red;}")
        
       

        

                
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
            
