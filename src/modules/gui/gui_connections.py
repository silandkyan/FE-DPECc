# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 17:38:27 2023

@author: pschw
"""

# die microstep resolution muss anpassbar werden 
# invert direction?! gebraucht oder nicht 

import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication)
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut
from modules.gui.main_window_ui import Ui_MainWindow
import time 

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
        # if max RPM spinBox changes its value, the maximum of the mastered spinBoxes change accordingly
        # connect if master RPM spinBox from legs changes 
        self.spinB_max_RPM.valueChanged.connect(self.RPM_master)
        # connect if the given run RPM changes
        self.spinB_RPM.valueChanged.connect(self.pps_calculator)
        # by default the first tab with all legs is selected, thus the active_module list gets fed 
        # with all the leg modules
        self.refresh_motor_list(1)
        
        # self.module = module_R
        # self.module = module_R.motor
        # self.active_modules = [self.module]
        
        # store_lcds is a matrix which displays all the saved positions for the individual motors 
        # by accessing their actual position function 
        self.store_lcds = [[self.lcd_A_zbr, self.lcd_B_zbr, self.lcd_C_zbr],
                           [self.lcd_A_zbc, self.lcd_B_zbc, self.lcd_C_zbc],
                           [self.lcd_A_zdr, self.lcd_B_zdr, self.lcd_C_zdr],
                           [self.lcd_A_zdc, self.lcd_B_zdc, self.lcd_C_zdc],
                           [self.lcd_A_x, self.lcd_B_x, self.lcd_C_x],
                           [self.lcd_A_pr, self.lcd_B_pr, self.lcd_C_pr],
                           [self.lcd_A_cr, self.lcd_B_cr, self.lcd_C_cr],
                           [self.lcd_A_s, self.lcd_B_s, self.lcd_C_s]]
        # hardware config takes in the mm or deg values shown by absolute pos spinBox 
        # done by one revolution of motor on specific axis
        self.hardware_config = [0, 0, 0, 0, 0, 0, 0, 0]
                                
    def RPM_master(self):
        max_RPM = self.spinB_max_RPM.value()
        self.spinB_RPM.setMaximum(max_RPM)
    
    def pps_calculator(self):
        pps = round(self.spinB_RPM.value() * 200*16 / 60) 
        self.pps = pps
        
    def mm_deg_to_steps(self, mm_deg ,hrdwr_idx):
        msteps = round(mm_deg / self.hardware_config[hrdwr_idx]* 200*16, 3)
        self.msteps = msteps
    
    def connectSignalsSlots(self):
    # connections for store buttons 
        # given parameters represent the coulmn index of the store_lcd matrix 
        self.pushB_store_A.clicked.connect(lambda: self.store_pos(0))
        self.pushB_store_B.clicked.connect(lambda: self.store_pos(1))
        self.pushB_store_C.clicked.connect(lambda: self.store_pos(2))
    # connections for positional pushButtons
        self.pushB_go_to_A.clicked.connect(lambda: self.goto(0))
        self.pushB_go_to_B.clicked.connect(lambda: self.goto(1))
        self.pushB_go_to_C.clicked.connect(lambda: self.goto(2))
        
    # connections for absolute position pushButtons:
        # absolute for x
        self.pushB_start_x.clicked.connect(lambda: self.abs_pos(0))
        #ablsolute for pr and cr
        self.pushB_start_pr_cr.clicked.connect(lambda: self.abs_pos(1))
        
    # connections for selecting right module(s) for the right tab 
        self.tabWidget.currentChanged.connect(self.reset_active_modules)
        
    # connections for checkability of leg motors
        # if single_motor is active, the checkboxes are enabled 
        self.radioB_single_motor.clicked.connect(self.enable_motorselection)
        # if all_motors is active the checkboxes for the individual legs are unchackable
        self.radioB_all_motors.clicked.connect(self.all_legs_setup)
        
    # connections for leg motor selection
        # if the all leg radioButton is pressed, all the motors are selected
        self.radioB_all_motors.clicked.connect(lambda: self.refresh_motor_list(1))
        # if select leg motor is enabled, the list is refreshed when new motors are chosen
        self.checkB_zbr.toggled.connect(lambda: self.refresh_motor_list(2))
        self.checkB_zbc.toggled.connect(lambda: self.refresh_motor_list(2))
        self.checkB_zdr.toggled.connect(lambda: self.refresh_motor_list(2))
        self.checkB_zdc.toggled.connect(lambda: self.refresh_motor_list(2))

    # connections for the pr/cr radioButtons
        #self.radioB_pr.pressed.connect(lambda: self.select_module(module_pr))
        #self.radioB_cr.pressed.connect(lambda: self.select_module(module_cr))
        self.radioB_pr.pressed.connect(lambda: print('module pr selected'))
        self.radioB_cr.pressed.connect(lambda: print('module cr selected'))
        
    # connections for permanent and when pushed functions on their specific tab
        # permanent for legs 
        #self.pushB_upwards1.clicked.connect(lambda: self.multi_module_control(self.permanent_left))
        self.pushB_upwards1.clicked.connect(self.permanent_right)
        #self.pushB_downwards1.clicked.connect(lambda: self.multi_module_control(self.permanent_right))
        self.pushB_downwards1.clicked.connect(self.permanent_left) 
        #self.pushB_stop_legs.clicked.connect(lambda: self.multi_module_control(self.stop_motor))
        self.pushB_stop_legs.clicked.connect(lambda: print('all leg motors stopped'))
        # when pushed for legs 
        #self.pushB_upwards.pressed.connect(lambda: self.multi_module_control(permanent_right))
        #self.pushB_upwards2.released.connect(lambda: self.multi_module_control(self.stop_motor))
        self.pushB_upwards2.pressed.connect(self.permanent_right)
        self.pushB_upwards2.released.connect(self.stop_motor)
        #self.pushB_downwards.pressed.connect(lambda: self.multi_module_control(self.permanent_left))
        #self.pushB_downwards2.released.connect(lambda: self.multi_module_control(self.stop_motor))
        self.pushB_downwards2.pressed.connect(self.permanent_left)
        self.pushB_downwards2.released.connect(self.stop_motor)
        
        # permanent for x 
        self.pushB_forwards1.clicked.connect(self.permanent_right)
        self.pushB_backwards1.clicked.connect(self.permanent_left)
        self.pushB_stop_x.clicked.connect(self.stop_motor)
        # when pushed for x 
        self.pushB_forwards2.pressed.connect(self.permanent_right)
        self.pushB_forwards2.released.connect(self.stop_motor)
        self.pushB_backwards2.pressed.connect(self.permanent_left)
        self.pushB_backwards2.released.connect(self.stop_motor)

        # permanent for pr and cr    
        self.pushB_clockwise1.clicked.connect(self.permanent_right)
        self.pushB_counterclockwise1.clicked.connect(self.permanent_left)
        self.pushB_stop_pr_cr.clicked.connect(self.stop_motor)
        # when pushed for pr and cr 
        self.pushB_clockwise2.pressed.connect(self.permanent_right)
        self.pushB_clockwise2.released.connect(self.stop_motor)
        self.pushB_counterclockwise2.pressed.connect(self.permanent_left)
        self.pushB_counterclockwise2.released.connect(self.stop_motor)
        # quit application and end program 
        self.pushB_quit.clicked.connect(self.close)
        
        
        #self.pushB_switch.clicked.connect(self.permanent_left)

        
    def store_pos(self, pos_idx):
        '''Store position of current active modules in a special instance
        variable for later use. Argument pos_idx (type=int) refers to the 
        index of the "stored position" column.'''
        # iterate over active modules:
        for module in self.active_modules:
            # Save current module position.
            module.module_positions[pos_idx] = module.motor.actual_position
            # find correct LCD for display of saved position value using the
            # store_lcds matrix-like list:
            # 1st dimension = row_idx (= module_idx),
            # 2nd dimension = col_idx (= pos_idx)
            # if module.motor == module_zbr.motor:
            #     self.store_lcds[0][pos_idx].display(module.module_positions[pos_idx])
            # elif module.motor == module_zbc.motor:
            #     self.store_lcds[1][pos_idx].display(module.module_positions[pos_idx])
            # elif module.motor == module_zdr.motor:
            #     self.store_lcds[2][pos_idx].display(module.module_positions[pos_idx])
            # elif module.motor == module_zdc.motor:
            #     self.store_lcds[3][pos_idx].display(module.module_positions[pos_idx])
            # elif module.motor == module_x.motor:
            #     self.store_lcds[4][pos_idx].display(module.module_positions[pos_idx])
            # elif module.motor == module_pr.motor:
            #     self.store_lcds[5][pos_idx].display(module.module_positions[pos_idx])
            # elif module.motor == module_cr.motor:
            #     self.store_lcds[7][pos_idx].display(module.module_positions[pos_idx])
            # elif module.motor == module_s.motor:
            #     self.store_lcds[8][pos_idx].display(module.module_positions[pos_idx])


    def select_module(self, m):
        '''Module selection for single module use.'''
        self.module = m
        self.motor = self.module.motor
        # override list of active modules:
        self.active_modules = [self.module]
        print('Selected motor: Motor', self.module.moduleID)
        #print(self.module.status_message()) 

    # def set_mode(self, mode):
    #     self.mode = mode
    #     print('Mode:', mode)
    
    def reset_active_modules(self):
        if self.tabWidget.currentIndex() == 0:
            self.refresh_motor_list(1)
            print('modules for legs selected')
        if self.tabWidget.currentIndex() == 1:
            #self.select_module(module_x)
            print('module for x selected')
        if self.tabWidget.currentIndex() == 2:
            #self.select_module(module_pr)
            print('module for pr selected')
        if self.tabWidget.currentIndex() == 3:
            #self.select_module(module_s)
            print('module for s selected')
            
    def refresh_motor_list(self, select):
        self.active_modules = []
        boxlist = [self.checkB_zbr, self.checkB_zbc,self.checkB_zdr, self.checkB_zdc]
                        
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
                        #self.active_modules.append(module_L)
                        print('ZBC appended')
                    if box == self.checkB_zdr:                   
                        #self.active_modules.append(module_zdr)
                        print('ZDR appended')
                    if box == self.checkB_zdc:
                        #self.active_modules.append(module_zdc)
                        print('ZDC appended')
        # update single active module and motor:
        if len(self.active_modules) == 1:
            self.module = self.active_modules[0]
            self.motor = self.module.motor
        # Status message:
        print('Selected motor(s):')
        for module in self.active_modules:
            print('Motor', module.moduleID)
        
    def multi_module_control(self, action):
        for module in self.active_modules:
            self.module = module
            self.motor = module.motor
            action()
        # iterate over all active modules and refresh LCDs:
        for module in self.active_modules:
            # Check if motor is active:
            while not module.motor.get_position_reached():
                # Prevent blocking of the application by the while loop:
                QApplication.processEvents()
                # Refresh LCD
                self.refresh_lcd_displays()
                
    def refresh_lcd_displays(self):
        '''Update the status LCDs.'''
        # self.lcd_current_zbr.display(module_zbr.motor.actual_position)
        # self.lcd_current_zbc.display(module_zbc.motor.actual_position)
        # self.lcd_current_zdr.display(module_zdr.motor.actual_position)
        # self.lcd_current_zdc.display(module_zdc.motor.actual_position)
        # self.lcd_current_x.display(module_x.motor.actual_position)
        # self.lcd_current_pr.display(module_pr.motor.actual_position)
        # self.lcd_current_cr.display(module_cr.motor.actual_position)
        # self.lcd_current_s.display(module_s.motor.actual_position)
        # time.sleep(0.1)
        
        
        
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
        #self.motor.move_by(-self.msteps, self.pps)
        print('Fine steps left with:', str(self.active_modules), 'and', str(self.spinB_RPM.value()), 'RPM')
        
    def coarse_step_left(self):
        #msteps = self.module.msteps_per_fstep * self.spinB_coarse.value()
        #self.motor.move_by(-self.msteps, self.pps)
        print('Coarse steps left with:', str(self.active_modules), 'and', str(self.spinB_RPM.value()), 'RPM')
        
    def fine_step_right(self):
        #msteps = self.module.msteps_per_fstep * self.spinB_fine.value()
        #self.motor.move_by(self.msteps, self.pps)
        print('Fine steps right with:', str(self.active_modules), 'and', str(self.spinB_RPM.value()), 'RPM')
        
    def coarse_step_right(self):
        #msteps = self.module.msteps_per_fstep * self.spinB_coarse.value()
        #self.motor.move_by(self.msteps, self.pps)
        print('Coarse steps right with:', str(self.active_modules), 'and', str(self.spinB_RPM.value()), 'RPM')

    def keyPressEvent(self, event: QKeyEvent) -> None: 
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
        
    
    # functions for enabling checkability 
    def enable_motorselection(self):
        # make checkboxes for leg motors checkable 
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
    def goto(self, pos_idx):
        # iterate over all active modules and apply the action function:
        for module in self.active_modules:
            # initial refresh:
            #self.refresh_lcd_displays()
            pps = round(self.rpmBox.value() * module.msteps_per_rev/60)
            pos = module.module_positions[pos_idx]
            module.motor.move_to(pos, pps)
            print('go to', pos)
        for module in self.active_modules:
            # Check if motor is active:
            while not module.motor.get_position_reached():
                # Prevent blocking of the application by the while loop:
                QApplication.processEvents()
                # Refresh LCD
                self.refresh_lcd_displays()

    def abs_pos(self, motor): 
        if motor == 0:
            # self.mm_deg_to_steps(self.dspinB_deg_axis_x.value(), 0)
            # self.motor.move_to(self.msteps, self.pps)
            print('Motor x moving to position:', str(self.dspinB_mm_axis_x.value()))
        elif motor == 1:
            # self.mm_deg_to_steps(self.dspinB_deg_axis_pr_cr.value(), 1)
            # self.motor.move_to(self.msteps, self.pps)
            print('Motor pr moving to position:', str(self.dspinB_deg_axis_pr_cr.value()))

        

                
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
            
