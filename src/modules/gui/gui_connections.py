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
# from PyQt5.QtGui import QKeySequence
# from PyQt5.QtWidgets import QShortcut
from modules.gui.main_window_ui import Ui_MainWindow
# import time 

from ..Motor import Motor 
from pytrinamic.connections import ConnectionManager



### Module setup and assignment ###
port_list = ConnectionManager().list_connections()
for port in port_list:
    Motor(port)
    
# define list of all moduleIDs and sort connected modules accordingly:
ID_list = [11, 12, 13, 14, 15, 21, 22, 23, 24]
module_list = Motor.sort_module_list(ID_list)

'''Choose names for the modules. Make sure to correctly match the correct 
module with its descriptive variable name (e.g. motor_L) below; 
adjust if needed.'''
module_zbr = module_list[0]
module_zbc = module_list[1]
# module_zdr = module_list[2]
# module_zdc = module_list[3]
# module_x = module_list[4]
# module_pr = module_list[5]
# module_cr = module_list[6]
# module_s = module_list[7]
# expand list as needed...

# TODO: probably better with inst_var module_name or so...

# module_zbr, module_zbc = Motor.assign_modules() # module_zdr, module_zdc, module_x, module_pr, module_cr, module_s

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
        self.setup_default_values()
        self.setup_default_buttons()
        self.refresh_lcd_displays()
        self.connectSignalsSlots()
        self.show()
        
        
        
    ###   SETUP DEFAULTS   ###
    
    def setup_default_values(self):
        '''User input: Specify default values here.'''
        ### User input values (with allowed min-max ranges)
        # rpm for all constant speed modes (single, multi, constant):
        self.spinB_RPM.setValue(20)    # default rpm
        # initial calculation of pps:
        self.pps_calculator()
        # max allowed value for rpm: # NEEDED???
        self.spinB_max_RPM.setValue(120)    # rpm
        # amount of fsteps in coarse mode:
        self.spinB_coarse.setValue(10)   # amount of fsteps
        # amount of fsteps in fine mode:
        self.spinB_fine.setValue(1)   # amount of fsteps
        # Store lists for checkboxes and radioButtons:
        self.legs_boxlist = [self.checkB_zbr, self.checkB_zbc, self.checkB_zdr, self.checkB_zdc]
        self.legs_radioBlist = [self.radioB_all_motors, self.radioB_single_motor]
        self.rot_radioBlist = [self.radioB_pr, self.radioB_cr]
        # Set default motor and module that is active initially:
        self.reset_active_modules()
        
    def setup_default_buttons(self):
        # Mode selection radioB:
        self.radioB_permanent_when_pushed.setChecked(True)
        #self.mode = 1
        # Leg motor selection radio buttons:
        self.radioB_all_motors.setChecked(True) # all motors
        # PR/CR motor selection radio buttons:
        self.radioB_pr.setChecked(True) # all motors
        # because radioB_all_motors is checked by default, 
        # checkBoxes for motorselection are disabled at setup:
        self.checkB_zbr.setCheckable(False)
        self.checkB_zbc.setCheckable(False)
        self.checkB_zdr.setCheckable(False)
        self.checkB_zdc.setCheckable(False)
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
        # hardware config takes in the mm or deg values shown by absolute pos spinBox 
        # done by one revolution of motor on specific axis
        self.hardware_config = [0, 0, 0, 0, 0, 0, 0, 0]
        
        
        
    ###   SAVE AND LOAD POSITIONS   ###
    
    def save_pos(self):
        '''Save stored module positions (displayed in store_lcds) to external file.'''
        with open('saved_positions.txt', 'w') as f:
            for row in self.store_lcds:
                for col in row:
                    # print(col.value())
                    f.write("%s " % int(col.value()))
                f.write("\n")
        print('Saved all positions to file!')
        
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
        for module in self.active_modules:
            if module.motor == module_zbr.motor:
                module.module_positions[pos_idx] = int(self.store_lcds[0][pos_idx].value())
            elif module.motor == module_zbc.motor:
                module.module_positions[pos_idx] = int(self.store_lcds[1][pos_idx].value())
            # elif module.motor == module_zdr.motor:
            #     module.module_positions[pos_idx] = int(self.store_lcds[2][pos_idx].value())
            # elif module.motor == module_zdc.motor:
            #     module.module_positions[pos_idx] = int(self.store_lcds[3][pos_idx].value())
            # elif module.motor == module_x.motor:
            #     module.module_positions[pos_idx] = int(self.store_lcds[4][pos_idx].value())
            # elif module.motor == module_pr.motor:
            #     module.module_positions[pos_idx] = int(self.store_lcds[5][pos_idx].value())
            # elif module.motor == module_cr.motor:
            #     module.module_positions[pos_idx] = int(self.store_lcds[6][pos_idx].value())
            # elif module.motor == module_s.motor:
            #     module.module_positions[pos_idx] = int(self.store_lcds[7][pos_idx].value())
            
            
        
    ###   CALCULATORS (for unit conversion to pps)   ###
        
    def RPM_master(self): ### TODO: IS THIS NEEDED???
        max_RPM = self.spinB_max_RPM.value()
        self.spinB_RPM.setMaximum(max_RPM)
    
    def pps_calculator(self):
        for module in module_list:
            module.rpm = self.spinB_RPM.value()
            module.pps = round(module.rpm * module.msteps_per_rev/60) 
        
    def mm_deg_to_steps(self, mm_deg ,hrdwr_idx):
        msteps = round(mm_deg / self.hardware_config[hrdwr_idx]* 200*16, 3)
        self.msteps = msteps
    
    
    
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
        
        ##  ABSOLUTE POSITION BUTTONS  ##
        # abs_pos argument represents the motor: 0 = X, 1 = PR/CR # TODO
        self.pushB_start_x.clicked.connect(lambda: self.abs_pos(0))
        self.pushB_start_pr_cr.clicked.connect(lambda: self.abs_pos(1))
        
        ## SAVE AND LOAD POSITIONS TO FILE BUTTONS ##
        self.pushB_savepos.clicked.connect(self.save_pos)
        self.pushB_loadpos.clicked.connect(self.load_pos)
        
        ### TODO: TEST IF X, CR/PR and S MOTORS WORK PROPERLY
        
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
        # PR/CR:
        self.pushB_clockwise1.clicked.connect(self.permanent_right)
        self.pushB_counterclockwise1.clicked.connect(self.permanent_left)
        self.pushB_stop_pr_cr.clicked.connect(self.stop_motor)
        
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
        # PR/CR:
        self.pushB_clockwise2.pressed.connect(self.permanent_right)
        self.pushB_clockwise2.released.connect(self.stop_motor)
        self.pushB_counterclockwise2.pressed.connect(self.permanent_left)
        self.pushB_counterclockwise2.released.connect(self.stop_motor)

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
        # PR/CR selection: # TODO
        # self.radioB_pr.pressed.connect(lambda: self.select_module(module_pr))
        # self.radioB_cr.pressed.connect(lambda: self.select_module(module_cr))
        self.radioB_pr.clicked.connect(lambda: print('dummy: module pr selected'))
        self.radioB_cr.clicked.connect(lambda: print('dummy: module cr selected'))
        
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
        for module in self.active_modules:
            # Save current module position.
            module.module_positions[pos_idx] = module.motor.actual_position
            # find correct LCD for display of saved position value using the
            # store_lcds matrix-like list:
            # 1st dimension = row_idx (= module_idx),
            # 2nd dimension = col_idx (= pos_idx)
            if module.motor == module_zbr.motor:
                self.store_lcds[0][pos_idx].display(module.module_positions[pos_idx])
            elif module.motor == module_zbc.motor:
                self.store_lcds[1][pos_idx].display(module.module_positions[pos_idx])
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
            
    def refresh_lcd_displays(self):
        '''Update the status LCDs.'''
        self.lcd_current_zbr.display(module_zbr.motor.actual_position)
        self.lcd_current_zbc.display(module_zbc.motor.actual_position)
        # self.lcd_current_zdr.display(module_zdr.motor.actual_position)
        # self.lcd_current_zdc.display(module_zdc.motor.actual_position)
        # self.lcd_current_x.display(module_x.motor.actual_position)
        # self.lcd_current_pr.display(module_pr.motor.actual_position)
        # self.lcd_current_cr.display(module_cr.motor.actual_position)
        # self.lcd_current_s.display(module_s.motor.actual_position)
        # time.sleep(0.1) # DO NOT sleep here, breaks motor behaviour...
        
    def goto(self, pos_idx):
        '''Motor moves to the stored module_position on index pos_idx.'''
        # calculate correct pps:
        # pps = round(self.spinB_RPM.value() * self.module.msteps_per_rev/60)
        # get pos to move to:
        pos = self.module.module_positions[pos_idx]
        # move motor to pos and print status message:
        self.module.motor.move_to(pos, self.module.pps)
        print('go to', pos)
    
    
    
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
            for box in self.legs_boxlist:
                box.setChecked(False)
            # refresh active module list:
            self.refresh_module_list(0)
            # print('modules for legs selected')
        
        # X:
        elif self.tabWidget.currentIndex() == 1:
            self.refresh_module_list(2)
            # print('module for x selected')
        
        # PR/CR:
        elif self.tabWidget.currentIndex() == 2:
            self.radioB_pr.setChecked(True)
            self.radioB_cr.setChecked(False)
            # self.select_module(module.module_pr)
            # print('module for pr or cr selected')
        
        # S:
        elif self.tabWidget.currentIndex() == 3:
            self.refresh_module_list(4)
            # print('module for s selected')
            
    def refresh_module_list(self, select):
        self.active_modules = []
        # TODO: after switching from single to all legs, motors do not respond 
        # even though they are in the list of active_modules... fix!
                        
        if select == 0:
            self.active_modules.append(module_zbr)
            self.active_modules.append(module_zbc)
            # self.active_modules.append(module_zdr)
            # self.active_modules.append(module_zdc) # continue this list if necessary...
            print('All leg motors are selected')                              
                                       
        if select == 1:     
            for box in self.legs_boxlist:
                if box.isChecked() == True:
                    if box == self.checkB_zbr:
                        self.active_modules.append(module_zbr)
                        print('ZBR appended')
                    if box == self.checkB_zbc:  
                        self.active_modules.append(module_zbc)
                        print('ZBC appended')
                    # if box == self.checkB_zdr:                   
                    #     self.active_modules.append(module_zdr)
                    #     print('ZDR appended')
                    # if box == self.checkB_zdc:
                    #     self.active_modules.append(module_zdc)
                    #     print('ZDC appended')
                    
        if select == 2:
            # self.select_module(module_x) # TODO
            # print('moduleID', module_x.moduleID, 'selected')
            print('X selected')
                    
        if select == 3:
            # self.select_module(module_pr) # TODO
            # print('moduleID', module_pr.moduleID, 'selected')
            print('moduleID dummy selected')
                    
        if select == 4:
            # self.select_module(module_s) # TODO
            # print('moduleID', module_s.moduleID, 'selected')
            print('S selected')
            
    
    def multi_module_control(self, action):
        '''Add multi motor control capability. Argument "action" is one of
        the motor control functions below (e.g., single_step).'''
        # iterate over all active modules and apply the action function:
        for module in self.active_modules:
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
            # Check if motor is active:
            while not module.motor.get_position_reached():
                # Prevent blocking of the application by the while loop:
                QApplication.processEvents()
                # Refresh LCD
                self.refresh_lcd_displays()
                
    def abs_pos(self, motor): # TODO: check if this works
        if motor == 0:
            # self.mm_deg_to_steps(self.dspinB_deg_axis_x.value(), 0)
            # self.motor.move_to(self.msteps, self.module.pps)
            print('Motor x moving to position:', str(self.dspinB_mm_axis_x.value()))
        elif motor == 1:
            # self.mm_deg_to_steps(self.dspinB_deg_axis_pr_cr.value(), 1)
            # self.motor.move_to(self.msteps, self.module.pps)
            print('Motor pr moving to position:', str(self.dspinB_deg_axis_pr_cr.value()))
            
                
        
    ###   MOTOR CONTROL FUNCTIONS   ###
    
    def stop_motor(self):
        '''Stop signal to all motors; can always be sent to the motors.'''
        self.module.motor.stop()
        # do not use time.sleep here!
        # set target_position to actual_position for the multi_control loop:
        act_pos = self.module.motor.get_axis_parameter(self.module.motor.AP.ActualPosition)
        self.module.motor.set_axis_parameter(self.module.motor.AP.TargetPosition, act_pos)
        # print status message
        print('Motor', self.module.moduleID, 'stopped!')
    
    def permanent_left(self):
        if self.radioB_permanent_when_pushed.isChecked() == True:
            # correct calling of motor...
            self.motor.rotate(-self.module.pps)
            print('Rotating left with', str(self.spinB_RPM.value()), 'rpm')
    
    def permanent_right(self):
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
        # make checkboxes for leg motors checkable 
        self.checkB_zbr.setCheckable(True)
        self.checkB_zbc.setCheckable(True)
        self.checkB_zdr.setCheckable(True)
        self.checkB_zdc.setCheckable(True)
        self.active_modules = []
    
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
            
