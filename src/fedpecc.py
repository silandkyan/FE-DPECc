#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 16:38:18 2023

@author: pgross
"""

#####   Importing Packages   #####

from modules.gui.gui_connections import run_app
#from modules.gui.gui_simple import run_app



#####   Main GUI program starts here   #####
if __name__ == "__main__":
    # Start main program with event handling loop:
    app = run_app()
    
    # add a method to close all motor connections if the program exits or 
    # in case of error

