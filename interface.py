import serial
from Sun import Sun
from datetime import datetime
from time import sleep

TURNON = 'w'
TURNOFF = 's'
DIMON = 'd'
DIMOFF = 'a'
REMEMBER = 'r'

def connect():
    return serial.Serial('/dev/ttyACM0',9600,timeout=1)

def turn_on(ser):
    ser.write(TURNON)

def turn_off(ser):
    ser.write(TURNOFF)

def dim_on(ser,count=1,delay=None):
    for i in range(count):
        ser.write(DIMON)
        if delay:
            sleep(delay)

def dim_off(ser):
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
    while datetime.now() < wake_time:
        sleep(10)
    s = connect()
    dim_on(s,count=20,delay=1)
