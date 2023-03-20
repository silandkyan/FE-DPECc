# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 17:38:27 2023

@author: pschw
"""

# Fragen:
    
# - Wie kann man einen Variablen output gestalten?
# - Wie kann die Wählbarkeit der Motoren und gleichzeitige Speicherung der Positionen und RPM funktionieren: wie kann ein pushButton 
# einen Tab mastern?
# - Control Übersicht: welche Motoren sind mit welchen parametern am laufen?
# - Startbuttons für pos control und permanent?
# - wie merkt man sich (im falle, dass das interface für alle Motoren gleich bleibt), bei welchem Motor welche Positon A bzw. B,C,D ist?
# (-> also elegante Lösung?)
# - wie muss man die statusabfrage rev verstehen? im falle, dass die Umdrehungen stets hoch gezählt werden ist ja nicht eine rev Anzahl gespeichert
# für eine besitmmte Position.


# interface mit drei Tabs und settings am besten als Untertabs in den jeweiligen Funktionen
# invert motor direction ist falls falsch angeschlossen: dann werden alle forwards Funktionen zu backwards Funktionen 
# Revolutions bzw. deg / mm ist ein entweder oder: manche Motoren sollen in deg fahren (Probenwechsler, Drehkranz) manche in Distanz
# start button für permanent
# einen counter hinzufügen der mit den schirtten nach oben zählt: für permanent wenn start button da ist, für when pushed und für pos control 

# Zu beheben:
    
# - Tabs sollen einen Namen anzeigen: main und settings 
# - Die checkBoxen für pos overwrite werden nicht richtig als gecheckt angezeigt -> allg keine gute Lösung pushButton wäre besser geeignet 
# - Die forwards Funktion bei Permanent muss am anfang beim checken der checkBox ein forwards signal emittieren -> oder mit start button!
# - Elegantere Lösung für exklusive groupBoxen
# - label ändern nur konstant die Farbe einen timer einzustellen nach welchem die Farbe wieder geändert wird geht noch nicht?!

import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication)
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut
from modules.gui.main_window_ui import Ui_MainWindow


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
        self.set_allowed_ranges()
        self.connectSignalsSlots()
        self.timer = QTimer()
        self.show()
        
        

            
        
    def set_allowed_ranges(self):
        pass
        
    def RPM_master(self):
        current = self.spinB_max_RPM.value()
        self.spinB_RPM_pos_control.setMaximum(current)
        self.spinB_RPM_permanent.setMaximum(current)
        self.spinB_RPM_when_pushed.setMaximum(current)
        self.spinB_RPM_settings.setMaximum(current)
        
        
            
    def connectSignalsSlots(self): 
        pass
    # connections for enabling group boxes exclusively
    
        # set exclusive for leg tab:
        # self.groupB_mselection_leg.clicked.connect(lambda: self.groupB_manager(1)) 
        # self.groupB_permanent_leg.clicked.connect(lambda: self.groupB_manager(2))
        # self.groupB_when_pushed_leg.clicked.connect(lambda: self.groupB_manager(3))
        # self.groupB_key_control_leg.clicked.connect(lambda: self.groupB_manager(4))
        # # set exclusive for x direction:
        # self.groupB_pos_control_x.clicked.connect(lambda: self.groupB_manager(5))
        # self.groupB_permanent_x.clicked.connect(lambda: self.groupB_manager(6))
        # self.groupB_when_pushed_x.clicked.connect(lambda: self.groupB_manager(7))
        # self.groupB_key_control_x.clicked.connect(lambda: self.groupB_manager(8)) 
        # # set exclusive for pr:
        # self.groupB_pos_control_pr.clicked.connect(lambda: self.groupB_manager(9))
        # self.groupB_when_pushed_pr.clicked.connect(lambda: self.groupB_manager(11))
        # self.groupB_key_control_pr.clicked.connect(lambda: self.groupB_manager(12)) 
        # # set exclusive for cr:
        # self.groupB_pos_control_cr.clicked.connect(lambda: self.groupB_manager(13))
        # self.groupB_key_control_cr.clicked.connect(lambda: self.groupB_manager(14)) 
        # # set exclusive for switch:
        # self.groupB_switch.clicked.connect(lambda: self.groupB_manager(15))
        # self.groupB_key_control_switch.clicked.connect(lambda: self.groupB_manager(16))
        
        
    # # connections for position control:
        
    #     # connections for the position pushButtons:
    #     self.pushB_pos_A.clicked.connect(lambda: self.position("A"))
    #     self.pushB_pos_B.clicked.connect(lambda: self.position("B"))
    #     self.pushB_pos_C.clicked.connect(lambda: self.position("C"))
    #     self.pushB_pos_D.clicked.connect(lambda: self.position("D"))
        
    #     # connections for the overwrite functions:
    #     self.shortcut_A = QShortcut(QKeySequence('Ctrl+A'), self)
    #     self.shortcut_A.activated.connect(lambda: self.overwrite(1))
    #     self.shortcut_B = QShortcut(QKeySequence('Ctrl+B'), self)
    #     self.shortcut_B.activated.connect(lambda: self.overwrite(2))
    #     self.shortcut_C = QShortcut(QKeySequence('Ctrl+C'), self)
    #     self.shortcut_C.activated.connect(lambda: self.overwrite(3))
    #     self.shortcut_D = QShortcut(QKeySequence('Ctrl+D'), self)
    #     self.shortcut_D.activated.connect(lambda: self.overwrite(4))
    
    # # connections for permanent:
        
    #     self.pushB_stop.clicked.connect(self.stop)
    #     self.pushB_start.clicked.connect(self.permanent)

        
    # # connections for when pushed:
        
    #     self.pushB_forwards.pressed.connect(self.forwards_when_pushed)
    #     self.pushB_backwards.pressed.connect(self.backwards_when_pushed)
        
    # # connections for invert motor direction:
        
    #     #self.pushB_invert_direction.clicked.connect(self.invert)
        
        
        
    # # general functions:
    
    # def forwards(self):
    #     print("running forwards with chosen RPM")                       
    # def backwards(self):
    #     print("running backwards with chosen RPM")
        
    
    

    # functions for setting exclusive groupBoxes:
    
    def groupB_manager(self, gbox):
        if gbox == 1:
            self.groupB_permanent.setChecked(False)
            self.groupB_when_pushed.setChecked(False)
            self.groupB_key_control.setChecked(False)
        if gbox == 2:
            self.groupB_pos_control.setChecked(False)
            self.groupB_when_pushed.setChecked(False)
            self.groupB_key_control.setChecked(False)
        if gbox == 3:
            self.groupB_permanent.setChecked(False)
            self.groupB_pos_control.setChecked(False)
            self.groupB_key_control.setChecked(False)
        if gbox == 4:
            self.groupB_permanent.setChecked(False)
            self.groupB_when_pushed.setChecked(False)
            self.groupB_pos_control.setChecked(False) 
            
        if gbox == 5:
            self.groupB_permanent_x.setChecked(False)
            self.groupB_when_pushed_x.setChecked(False)
            self.groupB_key_control_x.setChecked(False)
        if gbox == 6:
            self.groupB_pos_control_x.setChecked(False)
            self.groupB_when_pushed_x.setChecked(False)
            self.groupB_key_control_x.setChecked(False)
        if gbox == 7:
            self.groupB_pos_control_x.setChecked(False)
            self.groupB_permanent_x.setChecked(False)
            self.groupB_key_control_x.setChecked(False)
        if gbox == 8:
            self.groupB_pos_control_x.setChecked(False)
            self.groupB_permanent_x.setChecked(False)
            self.groupB_when_pushed_x.setChecked(False)
            
        if gbox == 9:
            self.groupB_permanent_pr.setChecked(False)
            self.groupB_when_pushed_pr.setChecked(False)
            self.groupB_key_control_pr.setChecked(False)
        if gbox == 11:
            self.groupB_pos_control_pr.setChecked(False)
            self.groupB_permanent_pr.setChecked(False)
            self.groupB_key_control_pr.setChecked(False)
        if gbox == 12:
            self.groupB_pos_control_pr.setChecked(False)
            self.groupB_permanent_pr.setChecked(False)
            self.groupB_when_pushed_pr.setChecked(False)
            
        if gbox == 13:
            self.groupB_key_control_pr.setChecked(False)
        if gbox == 14:
            self.groupB_pos_control_pr.setChecked(False)
            
        if gbox == 15:
            self.groupB_key_control_switch.setChecked(False)
        if gbox == 16:
            self.groupB_switch.setChecked(False)

     
    # functions for position control: 
        
    # def position(self, position):
    #         print("going to position {}".format(position))
            
    # def overwrite(self, pos):
    #     if pos == 1:
    #         self.lcdNumber.display(self.counter)
    #         print("position A overwritten to parameter shown by LCD")
    #         self.label_overwrite_A.setStyleSheet("QLabel {color: red;}")
    #     elif pos == 2:
    #         self.lcdNumber_3.display(self.counter) 
    #         print("position B overwritten to parameter shown by LCD")
    #         self.label_overwrite_B.setStyleSheet("QLabel {color: red;}")
    #         time.sleep(3)
    #     elif pos == 3:
    #         self.lcdNumber_5.display(self.counter)
    #         print("position C overwritten to parameter shown by LCD") 
    #         self.label_overwrite_C.setStyleSheet("QLabel {color: red;}")
    #     elif pos == 4:
    #         self.lcdNumber_7.display(self.counter) 
    #         print("position D overwritten to parameter shown by LCD")
    #         self.label_overwrite_D.setStyleSheet("QLabel {color: red;}")
            
    # # functions for permanent:
        
    # def permanent(self):
    #     self.timer_interval(1/(self.spinB_RPM_permanent.value() * self.spinB_RPM_when_pushed.value()) * 60000)
    #     self.timer.start()
    #     radio_for = self.radioB_forwards.isChecked()
    #     if radio_for == True:
    #         self.timer.timeout.connect(lambda: self.count(1))
    #         print("adjusting to new RMP and direction")
    #         time.sleep(3)
    #         self.forwards()
    #     else: 
    #         self.timer.timeout.connect(lambda: self.count(2))
    #         print("adjusting to new RMP and direction")
    #         time.sleep(3)
    #         self.backwards()

        
    # def stop(self):
    #     self.timer.stop()
    #     print("motor is stopping, ramp down from {} RPM".format(self.spinB_RPM_permanent.value()))
    #     time.sleep(3)
    #     print("motor stopped!")
        
    # # functions for keyboard control:
 
    # def keyPressEvent(self, event: QKeyEvent) -> None: # pass keys to call the functions 
    #     key_pressed = event.key()
    #     key_print = self.groupB_key_control.isChecked() # key_print makes sure, that only steps are made if the key_control groupBox is enabled
    #     if key_print == True:
    #         if key_pressed == Qt.Key_Up:
    #             print("fine step: {} steps done forwards with {} RPM".format(self.spinB_single_steps.value(), self.spinB_RPM_settings.value()))
    #             self.counter += float((self.spinB_single_steps.value()) / self.spinB_steps_per_revo.value())
    #         elif key_pressed == Qt.Key_Down:
    #             print("fine step: {} steps done backwards with {} RPM".format(self.spinB_single_steps.value(), self.spinB_RPM_settings.value()))
    #             self.counter -= float((self.spinB_single_steps.value()) / self.spinB_steps_per_revo.value())
    #         elif key_pressed == Qt.Key_Left:
    #             print("coarse step: {} steps done forwards with {} RPM".format(self.spinB_multi_steps.value(), self.spinB_RPM_settings.value()))
    #             self.counter += float((self.spinB_multi_steps.value()) / self.spinB_steps_per_revo.value())
    #         elif key_pressed == Qt.Key_Right:
    #             print("coarse step: {} steps done backwards with {} RPM".format(self.spinB_multi_steps.value(), self.spinB_RPM_settings.value()))
    #             self.counter -= float((self.spinB_multi_steps.value()) / self.spinB_steps_per_revo.value())
            
                
    # # functions for when pushed:
    
    # # steps_per_min is a variable which claculates the frequence of steps, according to the RPM per revolution (specified on second tab)
    # # and the RPM given in the spin box (factor 60000 is due to scaling from miliseconds to minutes)
    # def forwards_when_pushed(self):  
    #     steps_per_min = 1/(self.spinB_steps_per_revo.value() * self.spinB_RPM_when_pushed.value()) * 60000
    #     self.pushB_forwards.setAutoRepeatInterval(steps_per_min)
    #     print("running forwards with {} RPM".format(self.spinB_RPM_when_pushed.value()))

    # def backwards_when_pushed(self):
    #     steps_per_min = 1/(self.spinB_steps_per_revo.value() * self.spinB_RPM_when_pushed.value()) * 60000
    #     self.pushB_backwards.setAutoRepeatInterval(steps_per_min)
    #     print("running backwards with {} RPM".format(self.spinB_RPM_when_pushed.value()))

        
        
    # function for invert motor direction:
        
        

          
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
            