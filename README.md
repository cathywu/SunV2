SunV2: a sunrise when you want one
===========

We've made a better version of the sun, one that rises on command, does not disappear like the Boston sun, and can be custom tailored to any night-shifted college student's schedule. It is essentially a light dimmer that talks to your computer, and it determines the best time to rise based on your Google Calendar. SunV2 slowly dims a light on as to emulate sunrise.

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
- Make sure you have the above hardware and have installed the above software
- Connect the positive end of the LED to Pin P1.0 (LED1) and the negative end of the LED to GND
- Make sure the IR LED is within a few feet and pointed at the IR reciever
  of the dimmer
- Plug in the LaunchPad via USB
- Flash the firmware: $ `mspdebug rf2500 'prog Sun_firmware.txt'`
- Make the Sun executable: $ `chmod u+x web/interface.py`
- Run the Sun regularly: $ `crontab -e`
    - Add the line: `*/5 * * * 1-5 python <PATH_TO_REPO>/web/interface.py >> <PATH_TO_REPO>/log.log`
- Run the Sun script once, to authenticate your Google account: $ `python web/Sun.py`
- Make sure that the `src/calendar.dat` file is readable and writeable: $ `chmod a+rw src/calendar.dat`

Troubleshooting / Other features
-----------
- To check the log for errors: $ `tail -f <PATH_TO_REPO>/log.log`
- To manually remote control the dimmer: $ `screen /dev/ttyACM0 9600`
    - Use keys ASDW to control the dimmer
- To run the demo web interface: $ `python web/demo.py`
    - Then, navigate to localhost and click buttons to control the dimmer
- To just check your Google Calendar "sunrise" time without controlling any lights, just run: $ `python web/Sun.py`

Flashing the Launchpad via Code Composer Studio 5 (development setup)
-----------
### Windows 7 or Ubuntu 12.04
- File > New > CCS Project
- Family: MSP430, Variant: MSP430G2553, Empty Project
- Right click on project > Properties
    - Build > Advanced Options > Language Options > Enable "Treat C files as C++ files"

### Ubuntu (keeps CCS project and repository in sync)
- Right click on project > Properties
    - Build > Steps > Apply Predefined Step > TI-TXT
- $ `cd <REPO_DIR>`
- Add code: $ `ln -s src/ <PATH_TO_PROJECT>/src`
- Export binary: Project > Build All
- Link binary to repo: $ `ln <PATH_TO_PROJECT>/Debug/<PROJECT_NAME>.txt bin/Sun_firmware.txt`
- Load program via terminal: $ `mspdebug rf2500 'prog bin/Sun_firmware.txt'`

### Windows 7 (will need to copy files back to repo)
- Add code: src/
- Load program: Run > Debug

References
-----------
- Pin reference for the Launchpad [https://github.com/energia/Energia/wiki/Hardware#wiki-LaunchPad_MSP430G2553]
- Software UART on the MSP430 [https://github.com/wendlers/msp430-softuart]
- PySerial [http://pyserial.sourceforge.net/shortintro.html]

Feature requests
-----------
- Rain dance: to make the sun go away (snooze)
