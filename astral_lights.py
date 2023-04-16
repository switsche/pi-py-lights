#! /usr/bin/env python3

import logging
import datetime
import astral_timer
import RPi.GPIO as GPIO

logging.basicConfig(
    format="%(levelname)s %(asctime)s: %(message)s",
    level=logging.INFO,
    filename="astral_lights.log",
)

at = astral_timer.AstralTimer("Salem")
day = datetime.datetime.today()
sun = at.city.sun(date=day, local=True)

GPIO.setmode(GPIO.BCM)

pins = [5, 6]

for pin in pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)

while True:
    at.sunset_info(sun)
    at.wait_until("sunset", day)
    for pin in pins:
        GPIO.output(pin, GPIO.LOW)

    at.wait_until("dusk", day)
    for pin in pins:
        GPIO.output(pin, GPIO.HIGH)

    day += datetime.timedelta(days=1)
