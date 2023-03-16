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

def connect_modules_usb(port_list):
    module_list = []
    for port in port_list:
        interface = ConnectionManager('--port ' + port).connect()
        module = TMCM1260(interface)
        module_list.append(module)
    return module_list

def connect_motors_modules(module_list):
    motor_list = []
    for module in module_list:
        motor = module.motors[0]
        motor_list.append(motor)
    return motor_list

def init_drive_settings(motor_list):
    for motor in motor_list:
        motor.drive_settings.max_current = 50
        motor.drive_settings.standby_current = 0
        motor.drive_settings.boost_current = 0
        motor.drive_settings.microstep_resolution = motor.ENUM.MicrostepResolution4Microsteps
        #print(motor, motor.drive_settings)
    
def init_ramp_settings(motor_list):
    for motor in motor_list:
        motor.linear_ramp.max_velocity = 200
        motor.linear_ramp.max_acceleration = 400
        #print(motor, motor.linear_ramp)

def setup_motors():
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

def assign_motors(module_list, motor_list):
    for i in range(0, len(module_list)):
        moduleID = TMCLModule.get_global_parameter(module_list[i], gp_type=TMCM1260.GP0.SerialAddress, bank=0)
        if moduleID == 1:
            motor_L = motor_list[i]
        elif moduleID == 2:
            motor_R = motor_list[i]
    return motor_L, motor_R


# set move_by relative to the actual position
#motor.set_axis_parameter(motor.AP.RelativePositioningOption, 1)

# clear position counter
#motor.actual_position = 0

# start rotating motor for 5 sek
#print("Rotating...")
#motor.rotate(20000)
#time.sleep(2)

# stop rotating motor
#print("Stopping...")
#motor.stop()

#