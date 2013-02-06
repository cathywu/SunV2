# Interface between UART firmware, the Google Calendar, and the demo website
# 
# Usage: python interface.py
# But better to run this via cron or demo website
# 
# @author cathywu

import serial
from Sun import Sun, PWD
from datetime import datetime, timedelta
from time import sleep

TURNON = 'w'
TURNOFF = 's'
DIMON = 'd'
DIMOFF = 'a'
REMEMBER = 'r'

def acquire():
    fname = "%s/calendar.lock" % PWD
    import os
    if os.path.exists(fname):
        return False
    open(fname,'w').close()
    return True

def release():
    fname = "%s/calendar.lock" % PWD
    import os
    os.remove(fname)

def connect():
    return serial.Serial('/dev/ttyACM0',9600,timeout=1)

def disconnect(ser):
    ser.close()
    release()

def turn_on(ser):
    ser.write(TURNON)

def turn_off(ser):
    ser.write(TURNOFF)

def dim_on(ser,count=1,delay=None):
    for i in range(count):
        ser.write(DIMON)
        if delay:
            sleep(delay)

def dim_off(ser,count=1,delay=None):
    for i in range(count):
        ser.write(DIMOFF)
        if delay:
            sleep(delay)

def remember(ser):
    ser.write(remember)

if __name__ == "__main__":
    sun = Sun()
    wake_time = sun.wake_time
    print wake_time
    if datetime.now() > wake_time and datetime.now() < wake_time + timedelta(minutes=30):
        if not acquire():
            print "Locked"
        else:
            s = connect()
            dim_on(s,count=20,delay=90)
            disconnect()
