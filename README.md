Instructions for Code Composer Studio 5
-----------

### Windows 8 or Linux (Ubuntu 12.04)
- File > New > CCS Project
- Family: MSP430, Variant: MSP430G2553, Empty Project
- Add file: remotecontrol.cpp
- Right click on project > Properties
    - Build > Advanced Options > Language Options > Enable "Treat C files as C++ files"

### Windows 8
- Load Program: Run > Debug

### Linux
- Right click on project > Properties
    - Build > Steps > Apply Predefined Step > TI-TXT
- In terminal: $ mspdebug rf2500 'prof <PATH_TO_PROJECT>/Debug/<PROJECT_NAME>.txt'

