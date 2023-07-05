# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 17:38:27 2023

@author: pschw
"""
# TODO:
# die microstep resolution muss anpassbar werden 
# invert direction
# (Einheit des Stroms: 255 für 100% (2.8 und 5.5A))
# Einheiten werden aktuell noch nicht angezeigt!!

# Save and load pos nur nötig beim start des Programms um, alte Positionen 
# wieder zu bekommen die resetet wurden?

# TODO: try if the program works with all 8 motors connected

''' known bugs:
    # in leg control: when switching from "selected leg control" radio button 
        to "all legs" radio button, the list of active motors is not properly 
        refreshed and no motors are active, even though the respective functions 
        runs. klicking on the radio button again then refreshes the module list.
    # improper disconnection when closing the window is not really fixed by 
        adding some sleep time in the disconnection function, nor by explicitly
        stopping the motors beforehand. the program seems to be stuck in the 
        event loop... best guess so far is that this might be a IPython issue
        and might work with the normal console.
    #
        
    fixed: 
'''
#
''' test runs:
    # tested all 4 leg motors, works as expected.
    # also tested the other 4 motors, works as expected.
'''

import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication)
from PyQt5.QtGui import QKeyEvent, QTextFormat, QKeySequence, QKeySequence, QFont, QColor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QShortcut
# from PyQt5.QtGui import QKeySequence
# from PyQt5.QtWidgets import QShortcut
from modules.gui.main_window_ui import Ui_MainWindow

from ..Motor import Motor 
from pytrinamic.connections import ConnectionManager



### Module setup and assignment ###
port_list = ConnectionManager().list_connections()
for port in port_list:
    Motor(port)
    
# # define list of all moduleIDs and sort connected modules accordingly:
ID_list = [11, 12, 13, 14, 15, 21, 22, 23, 24]
module_list = Motor.sort_module_list(ID_list)
# print(module_list)


# '''Choose names for the modules. Make sure to correctly match the correct 
# module with its descriptive variable name (e.g. motor_L) below; 
# adjust if needed.'''
'''Choose names for the modules. Make sure to correctly match the correct 
module with its descriptive variable name (e.g. motor_x) below; 
adjust if needed.'''
# TODO when connected motors are changed
module_zbr = module_list[0]
module_zbc = module_list[1]
module_zdr = module_list[2]
module_zdc = module_list[3]
# module_x = module_list[4]
# module_pr = module_list[5]
# module_cr = module_list[6]
# module_s = module_list[7]
# expand list as needed...


# hardware_config takes the mm or deg done on specific axis with one revolution of a motor
# the order follows the scheme from module_list
# pr and cr ([5], [6]) have deg units, the rest has mm
hardware_config = [0.5, 0.2, 0.5, 0.5, 0.2, 0.3, 0.3, 0.1]

# TODO: probably better with inst_var module_name or so...
# for testing:
# module_x = module_list[0]
# module_pr = module_list[1]
# module_cr = module_list[2]
# module_s = module_list[3]
# module_zbr, module_zbc = Motor.assign_modules() # module_zdr, module_zdc, module_x, module_pr, module_cr, module_s

# print(module_zbr.status_message())
# print(module_zbc.status_message())
# print(module_zdr.status_message())
# print(module_zdc.status_message())
# print(module_x.status_message())
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
        self.setup_default_values()
        self.setup_default_buttons()
        self.refresh_lcd_displays()
        self.connectSignalsSlots()
        self.show()
        
    ###   SETUP DEFAULTS   ###
    
    def setup_default_values(self):
        '''User input: Specify default values here.'''
        ### User input values (with allowed min-max range)
        # initial calculation of pps:
        self.pps_calculator()
        # Store lists for checkboxes and radioButtons:
        self.legs_boxlist = [self.checkB_zbr, self.checkB_zbc, self.checkB_zdr, self.checkB_zdc]
        self.legs_radioBlist = [self.radioB_all_motors, self.radioB_single_motor]

        # self.rot_radioBlist = [self.radioB_pr, self.radioB_cr]
        # list of all labels:
        self.label_list = [self.label_zbr, self.label_zbc, self.label_zdr, self.label_zdc,
                           self.label_x, self.label_pr, self.label_cr, self.label_s]
        # Set default motor and module that is active initially:
        self.reset_active_modules()
        self.goto_zero_setup()
        self.all_legs_setup()
        self.unit_conversion()
        # setting Tabbar colors right 
        for i in range(0, 5):
                self.tabWidget.tabBar().setTabTextColor(i, QColor(249, 148, 6))
                if i>2:
                    self.tabWidget.tabBar().setTabTextColor(i, QColor(19, 42, 136))


    def setup_default_buttons(self):
        # Mode selection radioB:
        self.radioB_permanent_when_pushed.setChecked(True)
        #self.mode = 1
        # Leg motor selection radio buttons:
        self.radioB_all_motors.setChecked(True) # all motors
        # if max RPM spinBox changes its value, the maximum of the mastered spinBoxes change accordingly
        # connect if master RPM spinBox from legs changes 
        #self.spinB_max_RPM.valueChanged.connect(self.RPM_master) ### MOVED TO A PLACE WHERE IT ACTUALLY CALLED
        # connect if the given run RPM changes
        # self.spinB_RPM.valueChanged.connect(self.pps_calculator) ### MOVED TO A PLACE WHERE IT ACTUALLY CALLED
        # by default the first tab with all legs is selected, thus the active_module list gets fed 
        # with all the leg modules
        #self.refresh_module_list(1) ### NOT NEEDED because reset_active_modules is called during setup
        
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
        
    ###   SAVE AND LOAD POSITIONS   ###
    
    def save_pos(self):
        '''Save stored module positions (displayed in store_lcds) to external file.'''
        with open('saved_positions.txt', 'w') as f:
            for row in self.store_lcds:
                for col in row:
                    # print(col.value())
                    f.write("%s " % int(col.value()))
                f.write("\n")
        print('Saved all positions to file!') #TODO: fix store to save msteps, not mm/deg!
        
    def load_pos(self):
        '''Load module positions from external file:'''
        with open('saved_positions.txt', 'r') as f:
            i = 0
            for row in f:
                rowlist = row[:-2].split() # drop trailing '\n' and split at '\s'
                for j in range(0, len(self.store_lcds[0])):
                    self.store_lcds[i][j].display(rowlist[j]) # update lcd
                i += 1 # set counter for next module_idx
        # update module positions from the values in store_lcds:
        for pos_idx in range (0, len(self.store_lcds[0])):
            self.update_pos(pos_idx)
        # Status message:
        print('Loaded all saved positions from file!')
        
    def update_pos(self, pos_idx):
        '''Update module positions from store_lcds values.'''
        for module in module_list:
        #TODO: when connected motors are changed
        #TODO: store module_positions as msteps, not in real units
            if module.motor == module_zbr.motor:
                module.module_positions[pos_idx] = int(self.store_lcds[0][pos_idx].value())
            elif module.motor == module_zbc.motor:
                module.module_positions[pos_idx] = int(self.store_lcds[1][pos_idx].value())
            elif module.motor == module_zdr.motor:
                module.module_positions[pos_idx] = int(self.store_lcds[2][pos_idx].value())
            elif module.motor == module_zdc.motor:
                module.module_positions[pos_idx] = int(self.store_lcds[3][pos_idx].value())
            # if module.motor == module_x.motor:
            # elif module.motor == module_x.motor:
            #     module.module_positions[pos_idx] = int(self.store_lcds[4][pos_idx].value())
            # elif module.motor == module_pr.motor:
            #     module.module_positions[pos_idx] = int(self.store_lcds[5][pos_idx].value())
            # elif module.motor == module_cr.motor:
            #     module.module_positions[pos_idx] = int(self.store_lcds[6][pos_idx].value())
            # elif module.motor == module_s.motor:
            #     module.module_positions[pos_idx] = int(self.store_lcds[7][pos_idx].value())
            # for testing:
            # print(self.active_modules, module.module_positions[pos_idx])
            
        
    ###   CALCULATORS (for unit conversion to pps)   ###
        
    def pps_calculator(self):
        for module in module_list:
            module.rpm = self.spinB_RPM.value()
            module.pps = round(module.rpm * module.msteps_per_rev/60) 
        
    def mm_deg_to_steps(self, mm_deg ,i):
        msteps = round(mm_deg / hardware_config[i]* self.msteps_per_rev, 3)
        self.msteps = msteps
    
    def unit_conversion(self):
        i = 0
        for module in module_list:
            module.factor = hardware_config[i]/module.msteps_per_rev
            i += 1
    
    ###   BUTTON SIGNAL AND SLOT CONNECTIONS   ###
    
    def connectSignalsSlots(self):
        
        ##  STORE BUTTONS  ##
        # store_pos argument represents the coulmn index of the store_lcd matrix:
        self.pushB_store_A.clicked.connect(lambda: self.store_pos(0))
        self.pushB_store_B.clicked.connect(lambda: self.store_pos(1))
        self.pushB_store_C.clicked.connect(lambda: self.store_pos(2))
        
        ##  GOTO BUTTONS  ##
        # goto argument represents the coulmn index of the store_lcd matrix:
        self.pushB_go_to_A.clicked.connect(lambda: self.multi_module_control(lambda: self.goto(0)))
        self.pushB_go_to_B.clicked.connect(lambda: self.multi_module_control(lambda: self.goto(1)))
        self.pushB_go_to_C.clicked.connect(lambda: self.multi_module_control(lambda: self.goto(2)))
        self.pushB_go_to_0.clicked.connect(lambda: self.multi_module_control(lambda: self.goto(3)))
        
        ##  ABSOLUTE POSITION BUTTONS  ##
        # abs_pos argument represents the motor: 0 = X, 1 = PR/CR
        self.pushB_start_x.clicked.connect(lambda: self.abs_pos(0))
        self.pushB_start_pr.clicked.connect(lambda: self.abs_pos(1))
        self.pushB_start_cr.clicked.connect(lambda: self.abs_pos(2))
        
        ## SAVE AND LOAD POSITIONS TO FILE BUTTONS ##
        self.pushB_savepos.clicked.connect(self.save_pos)
        self.pushB_loadpos.clicked.connect(self.load_pos)
                
        ##  PERMANENT MOVE  ##
        # Z: 
        self.pushB_upwards1.clicked.connect(lambda: self.multi_module_control(self.permanent_right))
        self.pushB_downwards1.clicked.connect(lambda: self.multi_module_control(self.permanent_left))
        self.pushB_stop_legs.clicked.connect(lambda: self.multi_module_control(self.stop_motor))
        # self.pushB_stop_legs.clicked.connect(lambda: print('all leg motors stopped'))
        # X: 
        self.pushB_forwards1.clicked.connect(self.permanent_right)
        self.pushB_backwards1.clicked.connect(self.permanent_left)
        self.pushB_stop_x.clicked.connect(self.stop_motor)
        # PR:
        self.pushB_clockwise_pr1.clicked.connect(self.permanent_right)
        self.pushB_counterclockwise_pr1.clicked.connect(self.permanent_left)
        self.pushB_stop_pr.clicked.connect(self.stop_motor)
        # CR:
        self.pushB_clockwise_cr1.clicked.connect(self.permanent_right)
        self.pushB_counterclockwise_cr1.clicked.connect(self.permanent_left)
        self.pushB_stop_cr.clicked.connect(self.stop_motor)
        
        ##  WHEN PUSHED MOVE  ##
        # Z:
        self.pushB_upwards2.pressed.connect(lambda: self.multi_module_control(self.permanent_right))
        self.pushB_upwards2.released.connect(lambda: self.multi_module_control(self.stop_motor))
        self.pushB_downwards2.pressed.connect(lambda: self.multi_module_control(self.permanent_left))
        self.pushB_downwards2.released.connect(lambda: self.multi_module_control(self.stop_motor))
        # X:
        self.pushB_forwards2.pressed.connect(self.permanent_right)
        self.pushB_forwards2.released.connect(self.stop_motor)
        self.pushB_backwards2.pressed.connect(self.permanent_left)
        self.pushB_backwards2.released.connect(self.stop_motor)
        # PR:
        self.pushB_clockwise_pr2.pressed.connect(self.permanent_right)
        self.pushB_clockwise_pr2.released.connect(self.stop_motor)
        self.pushB_counterclockwise_pr2.pressed.connect(self.permanent_left)
        self.pushB_counterclockwise_pr2.released.connect(self.stop_motor)
        # CR:
        self.pushB_clockwise_cr2.pressed.connect(self.permanent_right)
        self.pushB_clockwise_cr2.released.connect(self.stop_motor)
        self.pushB_counterclockwise_cr2.pressed.connect(self.permanent_left)
        self.pushB_counterclockwise_cr2.released.connect(self.stop_motor)
    
        ##  MOTOR SELECTION  ##
        # Activate correct module(s) on tab change:
        self.tabWidget.currentChanged.connect(self.reset_active_modules)
        # Leg motor selection:
        # if the all_motors radioB is clicked, all leg motors are selected:
        self.radioB_all_motors.clicked.connect(lambda: self.refresh_module_list(0))
        # active_module list is refreshed when single_motor radioB and single_motor checkBoxes are clicked:
        self.checkB_zbr.toggled.connect(lambda: self.refresh_module_list(1))
        self.checkB_zbc.toggled.connect(lambda: self.refresh_module_list(1))
        self.checkB_zdr.toggled.connect(lambda: self.refresh_module_list(1))
        self.checkB_zdc.toggled.connect(lambda: self.refresh_module_list(1))
        
        ##  GENERAL GUI BEHAVIOUR  ##
        # Leg motor checkbox checkability:
        # if single_motor is active, the checkboxes are enabled 
        self.radioB_single_motor.clicked.connect(self.enable_motorselection)
        # if all_motors is active the checkboxes for the individual legs are unchackable
        self.radioB_all_motors.clicked.connect(self.all_legs_setup)
        # quit application and end program:
        self.pushB_quit.clicked.connect(self.close)
        # refresh rpm when value is changed:
        self.spinB_RPM.valueChanged.connect(self.pps_calculator)



    ###   KEYBOARD CONTROL   ###
    
    def keyPressEvent(self, event: QKeyEvent) -> None: 
        # event gets defined and keys are specified below 
        if self.radioB_key_control.isChecked() == True:
            key_pressed = event.key()
            if key_pressed == Qt.Key_S:
                self.multi_module_control(self.fine_step_left)
                #print('Fine steps left with:', str(self.active_modules), 'and', str(self.spinB_RPM.value()), 'RPM')
            if key_pressed == Qt.Key_A:
                self.multi_module_control(self.coarse_step_left)
                # print('Coarse steps left with:', str(self.active_modules), 'and', str(self.spinB_RPM.value()), 'RPM')
            if key_pressed == Qt.Key_W:
                self.multi_module_control(self.fine_step_right)
                #print('Fine steps right with:', str(self.active_modules), 'and', str(self.spinB_RPM.value()), 'RPM')
            if key_pressed == Qt.Key_D:
                self.multi_module_control(self.coarse_step_right)
                #print('Coarse steps right with:', str(self.active_modules), 'and', str(self.spinB_RPM.value()), 'RPM')
            
            
            
    ###   LCD TABLE FUNCTIONS   ###
    
    def store_pos(self, pos_idx):
        '''Store position of current active modules in a special instance
        variable for later use. Argument pos_idx (type=int) refers to the 
        index of the "stored position" column.'''
        # iterate over active modules:
        # TODO when connected motors are changed
        for module in self.active_modules:
            # Save current module position.
            module.module_positions[pos_idx] = module.motor.actual_position
            # find correct LCD for display of saved position value using the
            # store_lcds matrix-like list:
            # 1st dimension = row_idx (= module_idx),
            # 2nd dimension = col_idx (= pos_idx)
            if module.motor == module_zbr.motor:
                self.store_lcds[0][pos_idx].display(module_zbr.factor*module.module_positions[pos_idx])
            elif module.motor == module_zbc.motor:
                self.store_lcds[1][pos_idx].display(module_zbc.factor*module.module_positions[pos_idx])
            elif module.motor == module_zdr.motor:
                self.store_lcds[2][pos_idx].display(module_zdr.factor*module.module_positions[pos_idx])
            elif module.motor == module_zdc.motor:
                self.store_lcds[3][pos_idx].display(module_zdc.factor*module.module_positions[pos_idx])
            # elif module.motor == module_x.motor:
            #     self.store_lcds[4][pos_idx].display(module_x.factor*module.module_positions[pos_idx])

            # elif module.motor == module_pr.motor:
            #     self.store_lcds[5][pos_idx].display(module_pr.factor*module.module_positions[pos_idx])
            # elif module.motor == module_cr.motor:
            #     self.store_lcds[7][pos_idx].display(module_cr.factor*module.module_positions[pos_idx])
            # elif module.motor == module_s.motor:
            #     self.store_lcds[8][pos_idx].display(module_s.factor*module.module_positions[pos_idx])
            
    def refresh_lcd_displays(self):
        '''Update the status LCDs.'''
        self.lcd_current_zbr.display(module_zbr.factor*module_zbr.motor.actual_position)
        self.lcd_current_zbc.display(module_zbc.factor*module_zbc.motor.actual_position)
        self.lcd_current_zdr.display(module_zdr.factor*module_zdr.motor.actual_position)
        self.lcd_current_zdc.display(module_zdc.factor*module_zdc.motor.actual_position)
        # self.lcd_current_x.display(module_x.factor*module_x.motor.actual_position)
        # self.lcd_current_pr.display(module_pr.factor*module_pr.motor.actual_position)
        # self.lcd_current_cr.displaymodule_cr.factor*(module_cr.motor.actual_position)
        # self.lcd_current_s.display(module_s.factor*module_s.motor.actual_position)
            
        
    def goto(self, pos_idx):
        '''Motor moves to the stored module_position on index pos_idx.'''
        # calculate correct pps:
        # pps = round(self.spinB_RPM.value() * self.module.msteps_per_rev/60)
        # get pos to move to:
        if pos_idx == 3:
            self.module.motor.move_to(self.module.pos_zero, self.module.pps)
            print('go to 0')
        else:
            pos = self.module.module_positions[pos_idx]
            # move motor to pos and print status message:
            self.module.motor.move_to(pos, self.module.pps)
            print('go to', pos)
            
    def goto_zero_setup(self):
        for module in module_list:
            # Save zero module position.
            module.pos_zero = 0
            #TODO: add set_zero button and add save last position, both in same file
            #TODO: add initialization that restores all positions after module disconnect; 
            # maybe there is a way to save the last pos on the module and restore automatically?

    
    
    ###   MODULE MANAGEMENT   ###
    
    def select_module(self, m):
        '''Module selection for single module use.'''
        self.module = m
        self.motor = self.module.motor
        # override list of active modules:
        self.active_modules = [self.module]
        print('Selected motor: Motor', self.module.moduleID)
        #print(self.module.status_message())
        
    def reset_active_modules(self):
        '''Reset list of active modules to tab default.'''
        # Legs:
        if self.tabWidget.currentIndex() == 0:
            # set buttons correctly:
            self.radioB_all_motors.setChecked(True)
            self.radioB_single_motor.setChecked(False)
            self.all_legs_setup()
            # refresh active module list:
            self.refresh_module_list(0)
            # print('modules for legs selected')
        
        # X:
        elif self.tabWidget.currentIndex() == 1:
            self.refresh_module_list(2)
            # print('module for x selected')
        
        # PR:
        elif self.tabWidget.currentIndex() == 2:
            self.refresh_module_list(3)
           # print('module for pr selected')
        
        # CR:
        elif self.tabWidget.currentIndex() == 3:
            self.refresh_module_list(4)
           # print('module for cr selected')
            
        # S:
        elif self.tabWidget.currentIndex() == 4:
            self.refresh_module_list(5)
            # print('module for s selected')
            
    def refresh_module_list(self, select):
        for label in self.label_list:
            label.setFont(QFont('Arial', 20, weight=QFont.Normal))
            
        self.active_modules = []
        self.active_label_list = []

        # TODO when connected motors are changed
        # TODO: after switching from single to all legs, motors do not respond 
        # even though they are in the list of active_modules... fix!
                        
        if select == 0:
            self.active_modules.append(module_zbr)
            self.active_modules.append(module_zbc)
            self.active_modules.append(module_zdr)
            self.active_modules.append(module_zdc) # continue this list if necessary...
            
            # set labels active along with modules to keep track which motor is running
            self.active_label_list.append(self.label_zbr)
            self.active_label_list.append(self.label_zbc)
            self.active_label_list.append(self.label_zdr)
            self.active_label_list.append(self.label_zdc)
            print('All leg motors are selected')                            
                                       
        if select == 1: 
            for box in self.legs_boxlist:
                if box.isChecked() == True:
                    if box == self.checkB_zbr:
                        self.active_modules.append(module_zbr)
                        self.active_label_list.append(self.label_zbr)
                        print('ZBR appended')
                    if box == self.checkB_zbc:  
                        self.active_modules.append(module_zbc)
                        self.active_label_list.append(self.label_zbc)
                        print('ZBC appended')
                    if box == self.checkB_zdr:                   
                        self.active_modules.append(module_zdr)
                        self.active_label_list.append(self.label_zdr)
                        print('ZDR appended')
                    if box == self.checkB_zdc:
                        self.active_modules.append(module_zdc)
                        self.active_label_list.append(self.label_zdc)
                        print('ZDC appended')
                    
        if select == 2:
            # self.select_module(module_x) # TODO
            self.active_label_list = [self.label_x]
            # print('moduleID', module_x.moduleID, 'selected')
            print('X selected')
                    
        if select == 3:
            # self.select_module(module_pr) # TODO
            self.active_label_list = [self.label_pr]
            # print('moduleID', module_pr.moduleID, 'selected')
            print('PR selected')
            
        if select == 4:
            # self.select_module(module_cr) # TODO
            self.active_label_list = [self.label_cr]
            # print('moduleID', module_cr.moduleID, 'selected')
            print('CR selected')
                    
        if select == 5:
            # self.select_module(module_s) # TODO
            self.active_label_list = [self.label_s]
            # print('moduleID', module_s.moduleID, 'selected')
            print('S selected')
        
        for label in self.active_label_list:
            label.setFont(QFont('Arial', 20, weight=QFont.Bold))
                    
        # if select == 2:
        #     self.select_module(module_x)
        #     print('moduleID', module_x.moduleID, 'selected')
        #     print('X selected')
                    
        # if select == 3:
        #     for button in self.rot_radioBlist:
        #         if button.isChecked() == True:
        #             if button == self.radioB_cr:
        #                 self.select_module(module_cr)
        #                 print('moduleID', self.module.moduleID, 'selected')
        #             elif button == self.radioB_pr:
        #                 self.select_module(module_pr)
        #                 print('moduleID', self.module.moduleID, 'selected')
        #     # print('moduleID dummy selected')
                    
        # if select == 4:
        #     self.select_module(module_s)
        #     print('moduleID', module_s.moduleID, 'selected')
        #     print('S selected')
            
    def multi_module_control(self, action):
        '''Add multi motor control capability. Argument "action" is one of
        the motor control functions below (e.g., single_step).'''
        # iterate over all active modules and apply the action function:
        for module in self.active_modules:
            # Changing label color of active motors 
            for label in self.active_label_list:
                label.setStyleSheet('color: red')
            # Prevent blocking of the application by the while loop:
            QApplication.processEvents()
            # initial refresh:
            self.refresh_lcd_displays()
            # set module and motor: TODO: IS THIS NEEDED?
            self.module = module
            self.motor = module.motor
            action()
            # final refresh:
            self.refresh_lcd_displays()
        # iterate over all active modules and refresh LCDs:
        for module in self.active_modules:
            print(module.motor.get_position_reached())
            # Check if motor is active:
            while not (module.motor.get_position_reached() == 1):
                # Prevent blocking of the application by the while loop:
                QApplication.processEvents()
                # Refresh LCD
                self.refresh_lcd_displays()
            for label in self.active_label_list:
                label.setStyleSheet('color: red')
                
    def abs_pos(self, motor): # TODO: check if this works
        for label in self.active_label_list:
            label.setStyleSheet('color: red')
        # if motor == 0:
        #     # self.mm_deg_to_steps(self.dspinB_deg_axis_x.value(), 4)
        #     # self.motor.move_to(self.msteps, self.module.pps)
        #     print('Motor x moving to position:', str(self.dspinB_mm_axis_x.value()))
        # elif motor == 1:
        #     # self.mm_deg_to_steps(self.dspinB_deg_axis_pr.value(), 5)
        #     # self.motor.move_to(self.msteps, self.module.pps)
        #     print('Motor pr moving to position:', str(self.dspinB_deg_axis_pr.value()))
        # elif motor == 2:
        #     # self.mm_deg_to_steps(self.dspinB_deg_axis_cr.value(), 6)
        #     # self.motor.move_to(self.msteps, self.module.pps)
        #     print('Motor cr moving to position:', str(self.dspinB_deg_axis_cr.value()))
        
    ###   MOTOR CONTROL FUNCTIONS   ###
    
    def stop_motor(self):
        '''Stop signal to all motors; can always be sent to the motors.'''
        for label in self.active_label_list:    
          label.setStyleSheet('color: black')
        self.module.motor.stop()
        # do not use time.sleep here!
        # set target_position to actual_position for the multi_control loop:
        act_pos = self.module.motor.get_axis_parameter(self.module.motor.AP.ActualPosition)
        self.module.motor.set_axis_parameter(self.module.motor.AP.TargetPosition, act_pos)
        # print status message
        print('Motor', self.module.moduleID, 'stopped!')
        # Reset label color of motor to black 
        # for label in self.active_label_list:    
        #   label.setStyleSheet('color: black')
    
    def permanent_left(self):
        for label in self.active_label_list:    
          label.setStyleSheet('color: red')
        if self.radioB_permanent_when_pushed.isChecked() == True:
            # correct calling of motor...
            self.motor.rotate(-self.module.pps)
            print('Rotating left with', str(self.spinB_RPM.value()), 'rpm')
    
    def permanent_right(self):
        for label in self.active_label_list:    
          label.setStyleSheet('color: red')
        if self.radioB_permanent_when_pushed.isChecked() == True:
            self.motor.rotate(self.module.pps)
            print('Rotating right with', str(self.spinB_RPM.value()), 'rpm')
            
    def fine_step_left(self):
        msteps = self.module.msteps_per_fstep * self.spinB_fine.value()
        # self.motor.move_by(-self.msteps, self.pps)
        self.motor.move_by(-msteps, self.module.pps)
        print('Fine step left with Module', str(self.module.moduleID), 'at', str(self.spinB_RPM.value()), 'RPM')
        
    def coarse_step_left(self):
        msteps = self.module.msteps_per_fstep * self.spinB_coarse.value()
        # self.motor.move_by(-self.msteps, self.pps)
        self.motor.move_by(-msteps, self.module.pps)
        print('Coarse step left with Module:', str(self.module.moduleID), 'at', str(self.spinB_RPM.value()), 'RPM')
        
    def fine_step_right(self):
        msteps = self.module.msteps_per_fstep * self.spinB_fine.value()
        self.motor.move_by(msteps, self.module.pps)
        print('Fine step right with Module:', str(self.module.moduleID), 'at', str(self.spinB_RPM.value()), 'RPM')
        
    def coarse_step_right(self):
        msteps = self.module.msteps_per_fstep * self.spinB_coarse.value()
        self.motor.move_by(msteps, self.module.pps)
        print('Coarse step right with Module:', str(self.module.moduleID), 'at', str(self.spinB_RPM.value()), 'RPM')



    ###   CHECKABILITY   ###
 
    def enable_motorselection(self):
        # uncheck the checkBoxes for individual motor selection and 
        # make checkboxes for leg motors checkable
        for box in self.legs_boxlist:
            box.setChecked(False)
            box.setCheckable(True)
            box.setEnabled(True) 
        self.active_modules = []

    
    def all_legs_setup(self):
        # unchecking the checkBoxes of the individual motor selection and
        # setting checkBoxes uncheckable 
        for box in self.legs_boxlist:
            box.setChecked(True)
            box.setEnabled(False)

def run_app():   
    app = 0
    '''Initialize GUI control flow management. Requires passing argument 
    vector (sys.argv) or empty list [] as arg; the former allows to pass 
    configuration commands on startup to the program from the command 
    line, if such commands were implemented. If app is already open, 
    use that one, otherwise open new app:'''
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
            
