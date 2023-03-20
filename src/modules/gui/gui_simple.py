#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 16:37:43 2023

@author: pgross
"""

import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication)
from .main_window_simple_ui import Ui_MainWindow
from ..motor_control import (setup_motors, assign_motors, move_by)


### Motor setup and assignment ###
port_list, module_list, motor_list = setup_motors()
motor_L, motor_R = assign_motors(module_list, motor_list)

#motor = motor_L

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
        # Set default motor that is active initially:
        self.motor = motor_L
        
        
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
        self.motor1_radioButton.pressed.connect(lambda: self.select_motor(motor_L))
        self.motor2_radioButton.pressed.connect(lambda: self.select_motor(motor_R))

        
    def select_motor(self, m):
        self.motor = m
        print('Selected motor:', self.motor)

    def single_step_left(self):
        move_by(self.motor, -16, round(self.rpmBox.value()*3200/60))
        #print('single step left')
        
    def single_step_right(self):
        move_by(self.motor, 16, round(self.rpmBox.value()*3200/60))
        print('single step right')
        
    def multi_step_left(self):
        move_by(self.motor, -16 * self.multistep_numberBox.value(), round(self.rpmBox.value()*3200/60))
        print(str(self.multistep_numberBox.value()), 'steps left with', str(self.rpmBox.value()), 'rpm')
        
    def multi_step_right(self):
        move_by(self.motor, 16 * self.multistep_numberBox.value(), round(self.rpmBox.value()*3200/60))
        print(str(self.multistep_numberBox.value()), 'steps right with', str(self.rpmBox.value()), 'rpm')
        
    def perm_rot_left(self):
        # motor speed calculated from: rpmBox * msteps_per_rev / 60sec
        self.motor.rotate(-round(self.rpmBox.value()*3200/60))
        print('Rotating left with', str(self.rpmBox.value()), 'rpm')
        
    def perm_rot_right(self):
        self.motor.rotate(round(self.rpmBox.value()*3200/60))
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
