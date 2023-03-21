#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 11:24:24 2023

@author: pgross
"""

from pytrinamic.connections import ConnectionManager
from pytrinamic.modules import TMCM1260
from pytrinamic.modules import TMCLModule
import time


#####   MOTOR SETUP   #####

def setup_motors():
    '''Aggregate function that goes through the entire motor setup.'''
    print('Connecting motors...')
    port_list = ConnectionManager().list_connections()
    time.sleep(0.5)
    module_list = connect_modules_usb(port_list)
    motor_list = connect_motors_modules(module_list)
    print('Connecting motors... done!')
    print('Setting up motors...')
    init_drive_settings(motor_list)
    init_ramp_settings(motor_list)
    print('Setting up motors... done!')
    return port_list, module_list, motor_list


def connect_modules_usb(port_list):
    '''Establish connection between Trinamic modules and USB ports.'''
    module_list = []
    for port in port_list:
        interface = ConnectionManager('--port ' + port).connect()
        module = TMCM1260(interface)
        module_list.append(module)
    return module_list


def connect_motors_modules(module_list):
    '''Activate motors on their respective Trinamic module.'''
    motor_list = []
    for module in module_list:
        motor = module.motors[0]
        motor_list.append(motor)
    return motor_list


def disconnect_motors():
    '''Disconnection routine; should be run at the end of the program.'''
    ConnectionManager().disconnect
    print('Motors disconnected!')


def init_drive_settings(motor_list):
    '''Set initial motor drive settings.'''
    for motor in motor_list:
        motor.drive_settings.max_current = 50
        motor.drive_settings.standby_current = 0
        motor.drive_settings.boost_current = 0
        # Microstep resolution:
        motor.drive_settings.microstep_resolution = motor.ENUM.MicrostepResolution16Microsteps
        # Toggle step interpolation (works only with 16 microsteps):
        motor.set_axis_parameter(motor.AP.Intpol, value=1)
        #print(motor, motor.drive_settings)
 

def init_ramp_settings(motor_list):
    '''Set initial motor ramp settings. Values are in pps and are now scaled 
    to microstep resolution.'''
    for motor in motor_list:
        # get mstep resolution factor:
        mstep_res_factor = motor.drive_settings.microstep_resolution
        # calculate msteps/revolution
        fsteps_per_rev = 200
        msteps_per_rev = 2 ** mstep_res_factor * fsteps_per_rev
        # set max values for ramp. trailing factors were tested for 16 msteps.
        motor.linear_ramp.max_velocity = 2000#msteps_per_rev * 10
        motor.linear_ramp.max_acceleration = msteps_per_rev * 5
        #print(motor, motor.linear_ramp)


def assign_motors(module_list, motor_list):
    '''This function handles the assignment of the physical motors to
    descriptive motor variables. This is solved by permanently storing a
    moduleID on the Trinamic motor driver module (using TMCL-IDE), 
    currently in the Global Parameter "Serial Address", (Number 66, Bank 0).
    Make sure to correctly match the moduleID with the descriptive variable 
    names (e.g. motor_L) in the if-elif statement below; adjust if needed.'''
    for i in range(0, len(module_list)):
        # Get the moduleID from the Trinamic module global parameters:
        moduleID = TMCLModule.get_global_parameter(module_list[i], module_list[i].GP0.SerialAddress, bank=0)
        # Assign motor variable names to modulIDs:
        if moduleID == 1:
            motor_L = motor_list[i]
        elif moduleID == 2:
            motor_R = motor_list[i]
        #elif moduleID == 3:
        #    motor_C =  motor_list[i]
    return motor_L, motor_R#, motor_C # add motors here...


def motor_status_message(motor):
    return str('moduleID: ' + motor.GP0.SerialAddress)

#####   MOVEMENT CONTROL   #####

def move_by(motor, msteps, velocity):
    motor.set_axis_parameter(motor.AP.RelativePositioningOption, 1)
    print('Moving by ' + str(msteps) + ' steps.')
    motor.move_to(motor.actual_position + msteps, velocity)
    
    # wait till position_reached
    while not motor.get_position_reached():
        print('Moving...')
        time.sleep(0.1)
    
    print('Moving completed.')
    
    
def move_to(motor, pos, velocity):
    motor.set_axis_parameter(motor.AP.RelativePositioningOption, 1)
    print('Moving to position ' + str(pos) + '.')
    motor.move_to(motor.actual_position + pos, velocity)
    
    # wait till position_reached
    while not motor.get_position_reached():
        print('Moving...')
        time.sleep(0.1)
    
    print('Moving completed.')
    
