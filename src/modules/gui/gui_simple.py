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
        self.stepsBox.setValue(400)         # number of motor steps
        # motor microsteps:
        self.microstepsBox.setValue(256)    # number of microsteps
        # motor rpm (could also be derived from other params...)
        self.rpm_minBox.setValue(0)         # min rpm value
        self.rpm_maxBox.setValue(300)       # max rpm value
        # Motor selection radio buttons:
        self.motor1_radioButton.setChecked(True) # Motor 1 is default
        # Motor selection checkBoxes:
        self.motor1_checkBox.setChecked(True)
        # Set default motor that is active initially:
        self.module = module_L
        self.motor = module_L.motor
        
        
    def connectSignalsSlots(self):
        '''This function defines the widget behaviour with Qt's 
        signal-and-slot mechanism.'''
        # Close window and end program:
        self.quitButton.clicked.connect(self.close)
        # Single step rotation:
        self.singlelButton.clicked.connect(self.single_step_left)
        self.singlerButton.clicked.connect(self.single_step_right)
        # Multi step rotation:
        self.multilButton.clicked.connect(self.multi_step_left)
        self.multirButton.clicked.connect(self.multi_step_right)
        # Continuous rotation:
        self.permlButton.clicked.connect(self.perm_rot_left)
        self.permrButton.clicked.connect(self.perm_rot_right)
        # Stop button:
        self.permstopButton.clicked.connect(self.stop_motor)
        self.multistopButton.clicked.connect(self.stop_motor)
        # Motor selection radio buttons:
        self.motor1_radioButton.pressed.connect(lambda: self.select_module(module_L))
        self.motor2_radioButton.pressed.connect(lambda: self.select_module(module_R))
        # Motor selection checkBoxes:
        self.motor1_checkBox.toggled.connect(self.refresh_motor_list)
        self.motor2_checkBox.toggled.connect(self.refresh_motor_list)
        
        
    def select_module(self, m):
        self.module = m
        self.motor = self.module.motor
        #print('Selected motor:', self.motor)
        print(self.module.status_message())
        
    def refresh_motor_list(self):
        self.active_modules = []
        boxlist = [self.motor1_checkBox, self.motor2_checkBox]
        for box in boxlist:
            if box.isChecked() == True:
                if box == self.motor1_checkBox:
                    self.active_modules.append(module_L)
                elif box == self.motor2_checkBox:
                    self.active_modules.append(module_R)
        print(self.active_modules)
        
    # function to control several motors at once
    
    # function for mode selection

    def single_step_left(self):
        pps = round(self.rpmBox.value() * self.module.msteps_per_rev/60)
        self.motor.move_by(-self.module.msteps_per_fstep, pps)
        print('single fullstep left')
        
    def single_step_right(self):
        pps = round(self.rpmBox.value() * self.module.msteps_per_rev/60)
        self.motor.move_by(self.module.msteps_per_fstep, pps)
        print('single fullstep right')
        
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
        
    def perm_rot_left(self, motor):
        # motor speed calculated from: rpmBox * msteps_per_rev / 60sec
        pps = round(self.rpmBox.value() * self.module.msteps_per_rev/60)
        self.motor.rotate(-pps)
        print('Rotating left with', str(self.rpmBox.value()), 'rpm')
        
    def perm_rot_right(self):
        pps = round(self.rpmBox.value() * self.module.msteps_per_rev/60)
        self.motor.rotate(pps)
        print('Rotating right with', str(self.rpmBox.value()), 'rpm')
        
    def stop_motor(self):
        self.motor.stop()
        print('Motor stopped!')
        
            
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
