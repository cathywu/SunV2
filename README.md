SunV2
===========

Dependencies
-----------
- Code Composer Studio 5
- mspdebug [https://launchpad.net/ubuntu/quantal/+source/mspdebug]

Quick start
-----------
- $ mspdebug rf2500 'prog Sun\_firmware.txt'


Flashing the TI MSP430 Launchpad via Code Composer Studio 5
-----------

### Windows 7 or Ubuntu 12.04
- File > New > CCS Project
- Family: MSP430, Variant: MSP430G2553, Empty Project
- Right click on project > Properties
    - Build > Advanced Options > Language Options > Enable "Treat C files as C++ files"

### Ubuntu (keeps CCS project and repository in sync)
- Right click on project > Properties
    - Build > Steps > Apply Predefined Step > TI-TXT
- $ cd \<REPO\_DIR\>
- Add file: $ ln -s remotecontrol.cpp \<PATH\_TO\_PROJECT\>
- Export binary: Project > Build All
- Link binary to repo: $ ln \<PATH\_TO\_PROJECT\>/Debug/\<PROJECT\_NAME\>.txt Sun\_firmware.txt 
- Load program via terminal: $ mspdebug rf2500 'prog Sun\_firmware.txt'

### Windows 7 (will need to copy files back to repo)
- Add file: remotecontrol.cpp
- Load program: Run > Debug

