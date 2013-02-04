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
    return "Dimming on..."

@app.route("/dimoff")
def dimOff():
    # put in pyserial here
    s = interface.connect()
    interface.dim_off(s,count=10,delay=1)
    return "Dimming off..."

@app.route("/turnon")
def turnOn():
    # put in pyserial here
    s = interface.connect()
    interface.turn_on(s)
    return "Turning on..."

@app.route("/demo")
def demo():
    s = interface.connect()
    i = 0
    while i < 3:
        interface.turn_on(s)
        time.sleep(5)
        interface.turn_off(s)
        time.sleep(5)
        i += 1
    return "Demo!"

@app.route("/turnoff")
def turnOff():
    # put in pyserial here
    s = interface.connect()
    interface.turn_off(s)
    return "Turning off..."

@app.route("/sunriseTime")
def sunriseTime():
    s = Sun()
    return "%s" % s.wake_time

if __name__ == "__main__":
    app.debug = True
    app.run()
