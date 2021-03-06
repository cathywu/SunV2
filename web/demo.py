# Demo website for SunV2
# 
# Usage: python demo.py
# Click buttons to demonstrate the various functions
#
# @author micaelawiseman, cathywu

from flask import Flask
from flask import render_template
import interface
import time
from Sun import Sun

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("buttons.html")

@app.route("/dimon")
def dimOn():
    # put in pyserial here
    s = interface.connect()
    interface.dim_on(s,count=10,delay=1)
    return "Dimmed on"

@app.route("/dimoff")
def dimOff():
    # put in pyserial here
    s = interface.connect()
    interface.dim_off(s,count=10,delay=1)
    return "Dimmed off"

@app.route("/turnon")
def turnOn():
    # put in pyserial here
    s = interface.connect()
    interface.turn_on(s)
    return "Turning on"

@app.route("/turnoff")
def turnOff():
    # put in pyserial here
    s = interface.connect()
    interface.turn_off(s)
    return "Turning off"

@app.route("/sunriseTime")
def sunriseTime():
    s = Sun()
    return "%s" % s.wake_time

@app.route("/demo")
def demo():
    s = interface.connect()
    while True:
        interface.turn_on(s)
        time.sleep(5)
        interface.turn_off(s)
        time.sleep(5)
    return "Demo!"

if __name__ == "__main__":
    app.debug = True
    app.run()
