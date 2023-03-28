#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 11:01:10 2023

@author: pgross
"""

    

    
def select_module(self, m):
    '''Module selection for single module control.'''
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
        
def multi_module_control(self, action):
    '''Add multi motor control capability. Argument "action" is one of
    the motor control functions below (e.g., single_step).'''
    # iterate over all active modules and apply the action function:
    for module in self.active_modules:
        self.module = module
        self.motor = module.motor
        action()
        
def single_step_left(self):
    '''Single fullstep mode. Required amount of msteps and pulse freqency
    are calculated from the module settings and the value of rpmBox.'''
    # initialize movement parameters for one fullstep:
    msteps = self.module.msteps_per_fstep
    pps = round(self.rpmBox.value() * self.module.msteps_per_rev/60)
    # move by needed amount of msteps at pps velocity in negative direction:
    self.motor.move_by(-msteps, pps)
    # Status message:
    print('single fullstep left')
    print(-msteps)
    
def single_step_right(self):
    '''As above.'''
    msteps = self.module.msteps_per_fstep
    pps = round(self.rpmBox.value() * self.module.msteps_per_rev/60)
    # move by needed amount of msteps at pps velocity in positive direction:
    self.motor.move_by(msteps, pps)
    print('single fullstep right')
    print(msteps)
    
def multi_step_left(self):
    '''Multiple fullsteps mode. Required amount of msteps and pulse freqency
    are calculated from the module settings, specified amount of fullsteps
    and the value of rpmBox.'''
    # initialize movement parameters for required fullsteps:
    msteps = self.module.msteps_per_fstep * self.multistep_numberBox.value()
    pps = round(self.rpmBox.value() * self.module.msteps_per_rev/60)
    # move by needed amount of msteps at pps velocity in negative direction:
    self.motor.move_by(-msteps, pps)
    # Status message:
    print(str(self.multistep_numberBox.value()), 'fullsteps left with', str(self.rpmBox.value()), 'rpm')
    
def multi_step_right(self):
    '''As above.'''
    msteps = self.module.msteps_per_fstep * self.multistep_numberBox.value()
    pps = round(self.rpmBox.value() * self.module.msteps_per_rev/60)
    # move by needed amount of msteps at pps velocity in positive direction:
    self.motor.move_by(msteps, pps)
    # Status message:
    print(str(self.multistep_numberBox.value()), 'fullsteps right with', str(self.rpmBox.value()), 'rpm')
    
def perm_rot_left(self):
    '''Permanent rotation mode. Required pulse frequency is calculated
    from the module settings and the value of rpmBox.'''
    # motor speed calculated from: rpmBox * msteps_per_rev / 60sec
    pps = round(self.rpmBox.value() * self.module.msteps_per_rev/60)
    # Rotate in negative direction:
    self.motor.rotate(-pps)
    # Status message:
    print('Rotating left with', str(self.rpmBox.value()), 'rpm')
    
def perm_rot_right(self):
    '''As above.'''
    pps = round(self.rpmBox.value() * self.module.msteps_per_rev/60)
    # Rotate in positive direction:
    self.motor.rotate(pps)
    # Status message:
    print('Rotating right with', str(self.rpmBox.value()), 'rpm')
    
def stop_motor(self):
    '''Stop signal, can always be sent to the motor.'''
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
    