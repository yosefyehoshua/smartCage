# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import RPi.GPIO as GPIO
import time

pinNumber = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(pinNumber,GPIO.IN)

print('Loop starts')
while True:
    channel = GPIO.wait_for_edge(pinNumber,GPIO.RISING)
    if channel:
        print('Mouse entered')
        time.sleep(0.1)

GPIO.cleanup()

