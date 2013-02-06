SunV2
===========

Hardware
-----------
- Lutron IR Dimmer with IR Receiver [http://www.amazon.com/Lutron-MIR-600THW-WH-600-Watt-Infrared-Receiver/dp/B000JJYJMM/]
- MSP430 LaunchPad [https://estore.ti.com/Product3.aspx?ProductId=2031]
- IR LED Emitter 940nm [http://www.digikey.com/product-detail/en/LTE-5208A/160-1061-ND/153250]

Software
-----------
- mspdebug [https://launchpad.net/ubuntu/quantal/+source/mspdebug]
- Code Composer Studio 5 (if you want to change the firmware)
- Python 2.7.3
- Google APIs Client Library for Python [http://code.google.com/p/google-api-python-client/wiki/OAuth2Client]
- Commandline flags module for Python [http://code.google.com/p/python-gflags/]
- pip (optional, to help install the following)
- flask (optional, for the demo website)
- pyserial

Quick start
-----------
- $ mspdebug rf2500 'prog Sun\_firmware.txt'
- $ chmod u+x web/interface.py
- $ crontab -e
- Add the line: */5 * * * 1-5 python <PATH_TO_REPO>/web/interface.py

Flashing the TI MSP430 Launchpad via Code Composer Studio 5 (setup for changing the firmware)
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
- Add code: $ ln -s src/ \<PATH\_TO\_PROJECT\>/src
- Export binary: Project > Build All
- Link binary to repo: $ ln \<PATH\_TO\_PROJECT\>/Debug/\<PROJECT\_NAME\>.txt bin/Sun\_firmware.txt 
- Load program via terminal: $ mspdebug rf2500 'prog bin/Sun\_firmware.txt'

### Windows 7 (will need to copy files back to repo)
- Add code: src/
- Load program: Run > Debug

