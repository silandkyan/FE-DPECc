#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 11:24:03 2023

@author: pgross
"""

from pytrinamic.connections import ConnectionManager
from pytrinamic.modules import TMCM1260
from pytrinamic.modules import TMCLModule
#from motor_control import assign_motors
import time


##### General functions #####

def disconnect_motors():
    '''Disconnection routine; should be run at the end of the program.'''
    for inst in Motor.instances:
        inst.motor.stop()
    ConnectionManager().disconnect
    print('Motors disconnected!')


##### Motor class definition #####

class Motor(TMCM1260):
    instances = []
    def __init__(self, port):
        self.port = port
        self.interface, self.module, self.motor = self.setup_motor(self.port)
        self.__class__.instances.append(self)
    
    
        ### MOTOR SETUP ###
        
    def init_drive_settings(self, motor):
        '''Set initial motor drive settings. Values are in pps and are now scaled 
        to microstep resolution.'''
        motor.drive_settings.max_current = 50
        motor.drive_settings.standby_current = 0
        motor.drive_settings.boost_current = 0
        # Fullsteps/revolution:
        self.fsteps_per_rev = 200
        # set mstep resolution:
        self.mstep_res_factor = motor.ENUM.MicrostepResolution16Microsteps
        motor.drive_settings.microstep_resolution = self.mstep_res_factor
        # calculate msteps/revolution
        self.msteps_per_fstep = 2 ** self.mstep_res_factor
        self.msteps_per_rev = self.msteps_per_fstep * self.fsteps_per_rev
        # Toggle step interpolation (works only with 16 microsteps):
        motor.set_axis_parameter(motor.AP.Intpol, value=1)
        #print(motor, motor.drive_settings)

    def init_ramp_settings(self, motor):
        '''Set initial motor ramp settings. Values are in pps and are now scaled 
        to microstep resolution.'''
        # set max values for ramp. trailing factors were tested for 16 msteps.
        motor.linear_ramp.max_velocity = self.msteps_per_rev * 10
        motor.linear_ramp.max_acceleration = self.msteps_per_rev * 5
        #print(motor, motor.linear_ramp)
            
    def setup_motor(self, port):
        '''Aggregate function that goes through the entire motor setup.'''
        # Establish connection between Trinamic module and USB port:
        self.interface = ConnectionManager('--port ' + port).connect()
        self.module = TMCM1260(self.interface)
        # Activate motor on its respective Trinamic module:
        self.motor = self.module.motors[0]
        self.motorID = TMCLModule.get_global_parameter(self.module, self.module.GP0.SerialAddress, bank=0)
        print('Connecting motor', self.motorID, '... done!')
        self.init_drive_settings(self.motor)
        self.init_ramp_settings(self.motor)
        print('Setting up motor', self.motorID, '... done!')
        return self.interface, self.module, self.motor
    
    def status_message(self):
        return str('motorID: ' + str(self.motorID))
    
    
    ### MOVEMENT CONTROL ###

    def move_by_msteps(self, msteps, velocity):
        '''Wrapper function for Pytrinamics move_by that also gives 
        automatic status messages.'''
        self.motor.set_axis_parameter(self.motor.AP.RelativePositioningOption, 1)
        print('Moving by ' + str(msteps) + ' steps.')
        self.motor.move_to(self.motor.actual_position + msteps, velocity)
        # wait till position_reached
        while not self.motor.get_position_reached():
            print('Moving...')
            time.sleep(0.2)
        print('Moving completed.')
        
    def move_to_pos(self, pos, velocity):
        '''Wrapper function for Pytrinamics move_to that also gives 
        automatic status messages.'''
        self.motor.set_axis_parameter(self.motor.AP.RelativePositioningOption, 1)
        print('Moving to position ' + str(pos) + '.')
        self.motor.move_to(pos, velocity)
        # wait till position_reached
        while not self.motor.get_position_reached():
            print('Moving...')
            time.sleep(0.2)
        print('Moving completed.')


### Motor assignment ###

# port_list = ConnectionManager().list_connections()

# m1 = Motor(port_list[0])        
# m2 = Motor(port_list[1])

# print(m1.status_message())
# print(m2.status_message())
#