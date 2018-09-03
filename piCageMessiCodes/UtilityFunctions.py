#%%
import RPi.GPIO as GPIO
import Adafruit_MPR121.MPR121 as MPR121
import serial
import wiringpi
import sys
from picamera import PiCamera
import cPickle as pickle
from InitializationFunctions import findBasicParameters
from InitializationFunctions import InitialDevices
from time import sleep
import datetime

#%% Utility Functions

# Light On
def utility_LightOn():
    if 'PIN_LED' in tunnelParams:
        GPIO.output(tunnelParams['PIN_LED'], 1)
    
# Light Off
def utility_LightOff():
    if 'PIN_LED' in tunnelParams:
        GPIO.output(tunnelParams['PIN_LED'], 0)
    
# Move Pole
def utility_MovePole(angle):
    if 'PIN_SERVO' in tunnelParams:
        wiringpi.pwmWrite(tunnelParams['PIN_SERVO'], angle)

# Give Water
def utility_GiveWater(WATER_PULSE_DURATION):
    GPIO.output(tunnelParams['PIN_WATER'], 1)
    sleep(WATER_PULSE_DURATION)
    GPIO.output(tunnelParams['PIN_WATER'], 0)
    
# Take Picture
def utility_TakePicture(imagesDir):
    global CameraObject
    CameraObject.capture(imagesDir + '_' + str(datetime.datetime.now()) + '.jpg')