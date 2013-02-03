SunV2
===========

Dependencies
-----------
Code Composer Studio 5

Quick start
-----------
$ mspdebug rf2500 'prog Sun_firmware.txt'


Flashing the TI MSP430 Launchpad via Code Composer Studio 5
-----------

### Windows 7 or Linux (Ubuntu 12.04)
- File > New > CCS Project
- Family: MSP430, Variant: MSP430G2553, Empty Project
- Add file: remotecontrol.cpp
- Right click on project > Properties
    - Build > Advanced Options > Language Options > Enable "Treat C files as C++ files"

### Windows 7
- Load program: Run > Debug

### Linux
- Right click on project > Properties
    - Build > Steps > Apply Predefined Step > TI-TXT
- Load program via terminal: $ mspdebug rf2500 'prog <PATH_TO_PROJECT>/Debug/<PROJECT_NAME>.txt'

