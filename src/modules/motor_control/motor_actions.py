#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 14:22:10 2023

@author: pgross
"""

import time

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