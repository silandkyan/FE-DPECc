# FE-DPECc
Fast Exchange Diamond Paris-Edinbourgh Cell control

written by Philip Groß & Peter Schwörer, GEOW Uni Heidelberg, 2023

This Python program offers a graphical user interface (GUI) for manipulating the 8 motor axes of a Paris-Edinbourgh Cell platform. The motors are stepper motors of the company Trinamic, which are set up and controlled by the Trinamic's open-source PyTrinamic Python library. The communication between the PC and the motor control modules is achieved via USB connection.


## Prerequisites

The following programs or Python packages are needed to successfully run FE-DPECc:

- Python 3 and several of it's standard packages. The program was developed and tested with Python 3.9.
- PyTrinamic v0.2.4 (or later?) for module communication and motor control. For installation instructions, visit [https://github.com/trinamic/PyTrinamic](https://github.com/trinamic/PyTrinamic).
- Trinamic's TMCL-IDE for initial module testing and setup.
- PyQt5 (for the GUI), which is the Python wrapper for Qt5.
- 8 Trinamic stepper motors with integrated controller modules (currently 4x PD60-4-1260 and 4x PD86-3-1260) with TMCL firmware (can be installed).
- something else???


## Setup

### Hardware setup

1. Connect all modules to the PC via USB cables. USB switches can be used if the PC does not offer 8 free USB connectors.
2. Connect all motors to an external power supply unit. For details, consult Trinamic's module hardware manuals.
3. Launch TMCL-IDE and test the modules/motors separately. If new modules are used, or after firmware update, ensure that each module does have a user-assigned moduleID. Consult the "sort_module_list" classmethod of the "Motor" class for details. If needed, the assignment of moduleIDs to module functionality can be changed in gui_connections.py.

Now the motors should run with TMCL-IDE. Make sure to have correct settings in terms of motor current, etc. to prevent any damage.

Connection to the modules works also, if the motors themselves are not connected to the external power supply. Settings and motor positions are saved in the modules as long as they are powered via USB (and externally?). If the USB is disconnected, the motor positions are reset to zero, irrespective of their physical position!

### Software setup

In addition to the external dependencies listed above, in order to run the FE-DPECc software, all files and subdirectories within "/FE-DPECc/src" are required. If you downloaded the GitHub repository, all these files should be available within the correct directory structure. The structure tree looks like this:

```
├── /FE-DPECc/src
│   ├── fedpecc.py                  (main program; run this file with Python)
│   ├── saved_positions.txt         (file for external storage of motor positions)
│   ├── /modules                    (all sub-packages are stored here)
│   │   ├── Motor.py                (definition of Motor class)
│   │   ├── /gui                    (contains all GUI-related files)
│   │   │   ├── gui_connections.py  (definition of GUI behaviour)
│   │   │   ├── main_window_ui.py   (definition of GUI content and appearence)
│   │   │   ├── main window.ui      (XML-file, contains all GUI elements)
```
        
Other files that may also be present within the /src directory are not required to run.

To run FE-DPECc from the Linux bash, navigate to the /src directory and execute the following command:
`python fedpecc.py`
This will open the FE-DPECc GUI which manages all further interaction with the program.

## Platform and axes description
For a detailed platform description, consult the technical paper ABC. The following gives only a minimal overview on the platform hardware. FE-DPECc allows to position the platform relative to the ion beam along 3 axes, using 6 motors, and also controls 2 additional capabilities of the platform, each of which uses one motor. Therefore, the in total 8 motors are organized in functional groups.

Position group:

- z-axis, 4 (PD86-3-1260) leg motors that adjusts the elevation of the platform relative to the beam
- x-axis, 1 (PD60-4-1260) motor that horizontally translates the platform position perpendicular to the beam
- pr-axis, 1 (PD60-4-1260) motor that rotates the platform around a vertical axis through the platform center (sample/experiment chamber)

Other groups:

- cr-axis, 1 (PD60-4-1260) motor for rotation of the experiment cell along a vertical axis from a beam-through configuration to several other configurations (e.g., Raman- or microscope-through config.)
- s-axis, 1 (PD60-4-1260) motor for sample change

These functional groups are also found as such within the GUI.

drawing of platform...


## Functionality and GUI
with images...

The GUI is organized in 4 areas:

- Motor control area (upper left)
- Positions area (upper right)
- Mode and information area (lower left)
- Drive settings area (lower right)

In the following, the displays and functions within the respective areas are explained.

### Motor control area
Here, the active motor group can be selected via the tabs in the upper part of the area. Changing tabs activates the motor/s of the respective motor group and deactivates all other motors. Only the z-axis (legs) motor group allows to manually select (i.e., set as active/inactive) individual motors of this group.

Depending on which mode is selected in the Mode and information area (below), the active motors can then be controlled directly using either the buttons present in the area or the WASD-keys on the keyboard. Detailed information on the button/key press behaviour is given in the Mode and information area.

### Positions area
This area gives a tabulated overview on the current position (first LCD column) of all motors (rows), highlights the currently active motors (bold font/color, or whatever), and displays stored motor positions (2nd to 4th column). 

The "Save Pos" button writes the currently stored positions to an external file (/FE-DPECc/src/saved_positions.txt). After a restart of the program, these positions can be read from the file via the "Load Pos" button.

The "store" buttons below the position columns write the positions of all active modules into the corresponding position fields.

Similarly, the "go to" buttons tell the currently active motors to go to the absolute position written within the respective position LCDs. 

### Mode and information area
This area contains some information on the motor and program behaviour. The radio buttons allow to switch the operating mode of the motor control: If the mode "permanent/when pushed" is selected, motor control is achieved via the control buttons in the Motor control area. 

These buttons are deactivated if the mode "keyboard control" is selected. Instead, the motors can now be controlled via key presses of the WASD keys, which results in a stepwise motor motion: One "fine" step for the W and S keys, one "coarse" step for the A and D keys. The stepsize can be adjusted in the Drive settings area.

For precise motor control it is advisable to use single key presses (i.e., not to keep the keys pressed), especially if multiple motors are controlled simultaneously. (maybe this should be hard-coded...)

### Drive settings area
In this area, the user can change certain motor drive settings. These settings always affect the behaviour of all motors, not only the active ones. 

The spinboxes on the left of the area allow to set the stepsizes of the "fine" and "coarse" motor steps, as integer value representing the number of full motor steps to rotate by. The defaults are 1 and 10 full steps, respectively. As an example, for a motor with 200 fullsteps per complete rotation, a value of 1 would mean that one step corresponds to a rotation by 1.8°.

The spinbox on the right of the area allows to set a value for the motor rotation velocity in rounds per minute (RPM). The rotation direction can be inverted by clicking on the "invert direction" button, or by chosing a negative RPM value.



