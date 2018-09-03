## Initialization Functions

#%%
import RPi.GPIO as GPIO
import Adafruit_MPR121.MPR121 as MPR121
import serial
import wiringpi
import sys
from picamera import PiCamera
import cPickle as pickle

#%% Initialization functions

def findBasicParameters(tunnelID):
    """
    Find and define the basic parameters of program <-> Raspberry Pi
    communication.
    :param tunnelID:  tunnel ID, format: // todo ask for tunnel format.
    :return: tunnel communication parameters dictionary.
    """
    # Load the dictionary of tunnels properties
    tunnelsDict = pickle.load(open("tunnelsDict.p", "rb"))
    tunnelParams = tunnelsDict[tunnelID]

    # make sure that essential fields exist
    assert('USB_PORT' in tunnelParams.keys())
    assert('PIN_WATER' in tunnelParams.keys())
    assert('PIN_LICK_DETECT' in tunnelParams.keys())
    return tunnelParams
 
def InitialDevices(tunnelParams, cameraOn):
    """
    Initializing Devices connected to Raspberry Pi (via GPIO or not?) // todo ask if all devices connected to RP GPIO
    :param tunnelParams: tunnel communication parameters.
    :param cameraOn: boolean - camera is on/off.
    :return: tuple serial_dev, CameraObject // todo don't know, what obj. are: serial_dev, CameraObject
    """
    # camera
    if cameraOn:
        CameraObject = PiCamera()
    
    # GPIOs
    GPIO.setmode(GPIO.BCM)
    
    # touch sensor
    cap = MPR121.MPR121()
    if not cap.begin():
        print('Error initializing MPR121 Lick Detector. Check your wiring!')
        sys.exit(1)
    cap = MPR121.MPR121()
    
    # RFID reader
    serial_dev = serial.Serial(tunnelParams['USB_PORT'], baudrate=9600)
    
    # water valve
    GPIO.setup(tunnelParams['PIN_WATER'], GPIO.OUT, initial= GPIO.LOW)
    
    # servo motor
    if 'PIN_SERVO' in tunnelParams:
        wiringpi.wiringPiSetupGpio()
        wiringpi.pinMode(tunnelParams['PIN_SERVO'], wiringpi.GPIO.PWM_OUTPUT)       # PWM output
        # divide down clock: Servo's want 50 Hz frequency output, PWM Frequency in Hz = 19,200,000 Hz / pwmClock / pwmRange
        wiringpi.pwmSetClock(192)
        wiringpi.pwmSetRange(2000)
    
    # LED
    if 'PIN_LED' in tunnelParams:
        GPIO.setup(tunnelParams['PIN_LED'], GPIO.OUT, initial = GPIO.LOW)
    
    return serial_dev, CameraObject
