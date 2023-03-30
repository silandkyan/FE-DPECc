#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 16:37:43 2023

@author: pgross
"""

import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication)
from pytrinamic.connections import ConnectionManager
from .main_window_simple_ui import Ui_MainWindow
from ..Motor import Motor
#from ..motor_control import assign_motors


### Motor setup and assignment ###


port_list = ConnectionManager().list_connections()
for port in port_list:
    Motor(port)
    
module_L, module_R = Motor.assign_modules()

print(module_L.status_message())
print(module_R.status_message())



class Window(QMainWindow, Ui_MainWindow):
    '''This custom class inherits from QMainWindow class and the custom 
    Ui_MainWindow class from main_window_ui.py file. That file is created 
    from main_window.ui using the pyuic5 command line program, e.g.:
    pyuic5 -x main_window.ui -o main_window_ui.py
    '''
     
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('Motor Control Panel -- MoCoPa')
        # setup functions:
        self.set_allowed_ranges()
        self.set_default_values()
        self.connectSignalsSlots()
        self.show()
        
    
    def set_default_values(self):
        '''User input: Specify default values here.'''
        ### User input values (with allowed min-max ranges)
        # rpm for all constant speed modes (single, multi, constant):
        self.rpmBox.setValue(10)    # default rpm
        # amount of single steps in multistep mode:
        self.multistep_numberBox.setValue(10)   # amount of single steps 
        
        ### Hardware settings values (with allowed min-max ranges)
        # motor steps:
        self.stepsBox.setValue(200)         # number of motor steps
        # motor microsteps:
        self.microstepsBox.setValue(256)    # number of microsteps
        # motor rpm (could also be derived from other params...)
        self.rpm_minBox.setValue(0)         # min rpm value
        self.rpm_maxBox.setValue(300)       # max rpm value
        # Motor selection radio buttons:
        self.motor1_radioButton.setChecked(True) # Motor 1 is default
        # Motor selection checkBoxes:
        self.motor1_checkBox.setChecked(True)
        # Mode selection checkBoxes and mode:
        self.mode_single.setChecked(True)
        self.mode = 1
        # Set default motor that is active initially:

        self.module = module_L
        self.motor = module_L.motor
        self.active_modules = [self.module]

        
        
    def connectSignalsSlots(self):
        '''This function defines the widget behaviour with Qt's 
        signal-and-slot mechanism.'''
        ### general ###
        # Close window and end program:
        self.quitButton.clicked.connect(self.close)
        self.mode_single.pressed.connect(lambda: self.set_mode(1))
        self.mode_multi.pressed.connect(lambda: self.set_mode(2))
        self.mode_perm.pressed.connect(lambda: self.set_mode(3))
        
        ### single ###
        # Motor selection radioButtons:
        self.motor1_radioButton.pressed.connect(lambda: self.select_module(module_L))
        self.motor2_radioButton.pressed.connect(lambda: self.select_module(module_R))
        # Rotation Buttons:
        self.s_left.clicked.connect(self.left)
        self.s_right.clicked.connect(self.right)
        self.s_stop.clicked.connect(self.stop_motor)
        
        ### multi ###
        # Motor selection checkBoxes:
        self.motor1_checkBox.toggled.connect(self.refresh_module_list)
        self.motor2_checkBox.toggled.connect(self.refresh_module_list)
        # Rotation Buttons:
        self.m_left.clicked.connect(lambda: self.multi_module_control(self.left))
        self.m_right.clicked.connect(lambda: self.multi_module_control(self.right))
        self.m_stop.clicked.connect(lambda: self.multi_module_control(self.stop_motor))

        
        
    def select_module(self, m):
        '''Module selection for single module use.'''
        self.module = m
        self.motor = self.module.motor
        print('Selected motor: Motor', self.module.moduleID)
        #print(self.module.status_message())
        
    def set_mode(self, mode):
        self.mode = mode
        print('Mode:', mode)
        
    def left(self):
        print('Mode:', self.mode)
        if self.mode == 1:
            self.single_step_left()
        elif self.mode == 2:
            self.multi_step_left()
        elif self.mode == 3:
            self.perm_rot_left()
            
    def right(self):
        print('Mode:', self.mode)
        if self.mode == 1:
            self.single_step_right()
        elif self.mode == 2:
            self.multi_step_right()
        elif self.mode == 3:
            self.perm_rot_right()
            
    def refresh_module_list(self):
        '''Module selection for multi module use.'''
        self.active_modules = []
        boxlist = [self.motor1_checkBox, self.motor2_checkBox]
        for box in boxlist:
            if box.isChecked() == True:
                if box == self.motor1_checkBox:
                    self.active_modules.append(module_L)
                elif box == self.motor2_checkBox:
                    self.active_modules.append(module_R)
        print('Selected motor(s):')
        for module in self.active_modules:
            print('Motor', module.moduleID)
        
    def multi_module_control(self, action):
        for module in self.active_modules:
            self.module = module
            self.motor = module.motor
            action()
        
            
    def single_step_left(self):
        msteps = self.module.msteps_per_fstep
        pps = round(self.rpmBox.value() * self.module.msteps_per_rev/60)
        self.motor.move_by(-msteps, pps)
        print('single fullstep left')
        print(-msteps)
        
    def single_step_right(self):
        msteps = self.module.msteps_per_fstep
        pps = round(self.rpmBox.value() * self.module.msteps_per_rev/60)
        self.motor.move_by(msteps, pps)
        print('single fullstep right')
        print(msteps)
        
    def multi_step_left(self):
        msteps = self.module.msteps_per_fstep * self.multistep_numberBox.value()
        pps = round(self.rpmBox.value() * self.module.msteps_per_rev/60)
        self.motor.move_by(-msteps, pps)
        print(str(self.multistep_numberBox.value()), 'fullsteps left with', str(self.rpmBox.value()), 'rpm')
        
    def multi_step_right(self):
        msteps = self.module.msteps_per_fstep * self.multistep_numberBox.value()
        pps = round(self.rpmBox.value() * self.module.msteps_per_rev/60)
        self.motor.move_by(msteps, pps)
        print(str(self.multistep_numberBox.value()), 'fullsteps right with', str(self.rpmBox.value()), 'rpm')
        
    def perm_rot_left(self):
        # motor speed calculated from: rpmBox * msteps_per_rev / 60sec
        pps = round(self.rpmBox.value() * self.module.msteps_per_rev/60)
        self.motor.rotate(-pps)
        print('Rotating left with', str(self.rpmBox.value()), 'rpm')
        
    def perm_rot_right(self):
        pps = round(self.rpmBox.value() * self.module.msteps_per_rev/60)
        self.motor.rotate(pps)
        print('Rotating right with', str(self.rpmBox.value()), 'rpm')
        
    def stop_motor(self):
        self.module.motor.stop()
        print('Motor', self.module.moduleID, 'stopped!')
        
        
    def set_allowed_ranges(self):
        '''Specify allowed min-max ranges for values that can 
        be changed in the GUI. These should usually be fine...'''
        ### User input values (with allowed min-max ranges)
        # rpm for all constant speed modes (single, multi, constant):
        self.rpmBox.setMinimum(0)
        self.rpmBox.setMaximum(999)
        # amount of single steps in multistep mode:
        self.multistep_numberBox.setMinimum(0)
        self.multistep_numberBox.setMaximum(999)
        ### Hardware settings values
        # motor steps:
        self.stepsBox.setMinimum(0)
        self.stepsBox.setMaximum(999)
        # motor microsteps:
        self.microstepsBox.setMinimum(0)
        self.microstepsBox.setMaximum(9999)
        # motor rpm (could also be derived from other params...)
        self.rpm_minBox.setMinimum(0)
        self.rpm_minBox.setMaximum(999)
        self.rpm_maxBox.setMinimum(0)
        self.rpm_maxBox.setMaximum(999)
        

def run_app():
    app = 0
    '''Initialize GUI control flow management. Requires passing
    argument vector (sys.argv) or empty list [] as arg; the former allows
    to pass configuration commands on startup to the program from the
    command line, if such commands were implemented.'''
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
