#! /usr/bin/env python3

import RPi.GPIO as GPIO
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)

# Create a dictionary called pins to store the pin number, name, and pin state:
pins = {
    #5:  {"name": "Five", "state": False},
    16: {"name": "Backyard Lights", "state": False},
    6:  {'name': 'Shed Lights', 'state': False},
    26: {'name': 'Stained Glass', 'state': False},
}

# Set each pin as an output and make it high:
for pin in pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)


@app.route("/")
def main():
    # For each pin, read the pin state and store it in the pins dictionary:
    for pin in pins:
        pins[pin]["state"] = GPIO.input(pin) == GPIO.LOW

    # Put the pin dictionary into the template data dictionary:
    templateData = {"pins": pins}

    # Pass the template data into the template main.html and return it to the user
    return render_template("main.html", **templateData)


# The function below is executed when someone requests a URL with the pin number and action in it:
@app.route("/<changePin>/<action>")
def action(changePin, action):
    # Convert the pin from the URL into an integer:
    changePin = int(changePin)
    deviceName = pins[changePin]["name"]
    if action == "on":
        GPIO.output(changePin, GPIO.LOW)
    if action == "off":
        GPIO.output(changePin, GPIO.HIGH)
    if action == "toggle":
        # Read the pin and set it to whatever it isn't (that is, toggle it):
        GPIO.output(changePin, not GPIO.input(changePin))

    return redirect(url_for("main"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
