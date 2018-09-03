from picamera import PiCamera
from time import sleep
import pandas as pd
import numpy as np
import datetime
import time
import os.path
import RPi.GPIO as GPIO
import Adafruit_MPR121.MPR121 as MPR121
import serial
#import wiringpi
import sys

##############################################
# script params
##############################################
      
##############################################
# define some helper functions
##############################################

# initializing the devices
def InitialDevices():
    
    GPIO.setmode(GPIO.BCM)      # activating the GPIOs
    
    if not cap.begin():
        print 'Error initializing MPR121 Lick Detector. Check your wiring!'
        sys.exit(1)
    
    #wiringpi.wiringPiSetupGpio()
    #wiringpi.pinMode(PIN_SERVO, wiringpi.GPIO.PWM_OUTPUT)       # PWM output
    # divide down clock: Servo's want 50 Hz frequency output, PWM Frequency in Hz = 19,200,000 Hz / pwmClock / pwmRange
    #wiringpi.pwmSetClock(192)
    #wiringpi.pwmSetRange(2000)

    serial_dev = serial.Serial(USB_PORT, baudrate=9600)  # initial the RFID reader 
    GPIO.setup(PIN_WATER, GPIO.OUT, initial= GPIO.LOW)   # initial the water valve

    GPIO.setup(PIN_LED, GPIO.OUT, initial = GPIO.LOW)    # initial the LED

    GPIO.setup(PIN_POLE_1, GPIO.OUT, initial = GPIO.LOW)
    GPIO.setup(PIN_POLE_2, GPIO.OUT, initial = GPIO.LOW)
    return serial_dev

# start stimulus
def StartStimulus(trialType):
    if stimulusType == 'light' and trialType == 'Go':
        GPIO.output(PIN_LED, 1)     # light on
    if stimulusType == 'pole':
        if trialType == 'Go':
            GPIO.output(PIN_POLE_1, 1)
            GPIO.output(PIN_POLE_2, 0)
        elif trialType == 'NoGo':
            GPIO.output(PIN_POLE_2, 1)
            GPIO.output(PIN_POLE_1, 0)
            

# stop stimulus
def StopStimulus():
    if stimulusType == 'light':
        GPIO.output(PIN_LED, 0)     # light off
    if stimulusType == 'pole':
        GPIO.output(PIN_POLE_1, 0)
        GPIO.output(PIN_POLE_2, 0)

# run a trial of a task
def runTrial_task(trialType,mouseRFID,stimulusOff,giveReward):
    StartStimulus(trialType)   # start stimulus
    t_end_response = time.time() + RESPONSE_WINDOW
    t_end_stimulus = time.time() + STIMULATION_DURATION
    responseTimes = []
    while time.time() < t_end_response:                                
        if time.time() >= t_end_stimulus and stimulusOff == 0:
            StopStimulus()  # stop stimulus
            stimulusOff = 1
        if cap.is_touched(PIN_LICK_DETECTOR):
            currResponseTime = time.time()
            responseTimes.append(currResponseTime)
            print 'a lick is detected!'
            if trialType == 'Go' and giveReward==1:
                GPIO.output(PIN_WATER, 1)                            
                sleep(WATER_PULSE_DURATION)
                GPIO.output(PIN_WATER, 0)
                print 'Gave a reward' 
                giveReward = 0
#        CameraObject.capture(imagesDir + mouseRFID + '_' + str(time.time()) + '.jpg')
#        print 'taking a picture!'
        sleep(0.05)  # time interval for lick detection
    return responseTimes

# run trial of a training
def runTrial_training(mouseRFID):
    t_end_lick = time.time() + RESPONSE_WINDOW
    responseTimes = []
    sleep(DELAY_RFID_WATER_TRAINING_WINDOW)
    GPIO.output(PIN_WATER, 1)                            
    sleep(WATER_PULSE_DURATION)
    GPIO.output(PIN_WATER, 0)
    print 'Gave water' 
    while time.time() < t_end_lick:
        if cap.is_touched(PIN_LICK_DETECTOR):
            responseTimes.append(time.time())
            break
#    CameraObject.capture(imagesDir + mouseRFID + '_' + str(datetime.datetime.now()) + '.jpg')
#    print 'taking a picture!'
    return responseTimes

def taking_a_picture():
    global Camflag
    if Camflag:
        try:
            CameraObject = PiCamera()  # define camera object
        except:
            if Camflag:
                Camflag = False
                print("Camera stopped at " + str(datetime.datetime.now()) + "!!!")
            return
        CameraObject.capture(imagesDir + mouseRFID + '_' + str(datetime.datetime.now()) + '.jpg')
        print('taking a picture!')
        sleep(1)
        CameraObject.close()
        return



def lick_before_drink_training(mouseRFID):
    t_end_lick = time.time() + RESPONSE_WINDOW
    responseTimes = []
    #chance for first lick
    while time.time() < t_end_lick:
        if cap.is_touched(PIN_LICK_DETECTOR):
            responseTimes.append(time.time())
            GPIO.output(PIN_WATER, 1)                            
            sleep(WATER_PULSE_DURATION)
            GPIO.output(PIN_WATER, 0)
            print('Gave water')
            #taking_a_picture()
            break
            
    t_end_listening = time.time() + LISTENING_WINDOW
    #listening to additional licks after first one
    while time.time() < t_end_listening:
        if cap.is_touched(PIN_LICK_DETECTOR):
            responseTimes.append(time.time())
            sleep(0.1)
    return responseTimes


def cont_or_timeout(mouseRFID):
    # more than NUMBER_OF_VISITS visits
    if len(allRFIDs[mouseRFID][1]) >= NUMBER_OF_VISITS:
        deltaT = allRFIDs[mouseRFID][1][-1] - allRFIDs[mouseRFID][1][-NUMBER_OF_VISITS]
        deltaT_sec = deltaT.total_seconds() # # of seconds between the last visit and the visit NUMBER_OF_VISITS ago
    # less than NUMBER_OF_VISITS visits
    else:
        deltaT_sec = []     # empty is larger than everything
    if deltaT_sec <= TIME_UNIT:
        cont = 0
    else:
        cont = 1
        
    return cont 
                    
def calculate_response(responseTimes):
    # write the response                
    if len(responseTimes)>0:
        currMouseResponse = 'Lick'
    else:
        currMouseResponse = 'NoLick'
    return currMouseResponse


def close_devices():
    GPIO.cleanup()
 
##############################################

tunnelID = 1

USB_PORT_user = "/dev/ttyUSB1"
PIN_WATER_user = 25   
PIN_LICK_DETECTOR_user = 3# pin in the lick detector that is connected to the water spout

PIN_POLE_DETECTOR_1 = 21
PIN_POLE_DETECTOR_1 = 27
# choose stimulus type: light or pole
stimulusType_user = 'pole'

# choose the task type: 
    # Training - no task, the mice adjust to the tunnels and learn to get their water there
    #  Go/NoGo - stimulation with Go condition and NoGo condition
        # in the Go/NoGo task, choose the task phase:
            # 5-blocks - 5 Go trails and then 5 NoGo trials, and so on
            # random

#currTaskType = 'Training'
currTaskType = 'Go/NoGo'
#currTaskPhase = 'none' 
currTaskPhase = '5-blocks'




##############################################
# main loop
##############################################
#def mainloop_runSmartcage(USB_PORT_user,PIN_WATER_user,PIN_LICK_DETECTOR_user,stimulusType_user,tunnelID,currTaskType,currTaskPhase):
    
    ###### make global variables ######
    
# the numbers from the user are tunnel-unique
global USB_PORT
USB_PORT = USB_PORT_user
global PIN_WATER
PIN_WATER = PIN_WATER_user
global PIN_LICK_DETECTOR
PIN_LICK_DETECTOR = PIN_LICK_DETECTOR_user
global stimulusType
stimulusType = stimulusType_user

# constant numbers and strings
# camera params
global imagesDir
imagesDir = '/home/pi/mountpoint/SmartCage_Pics_2018/'
# data params
dataframeDir      = '/home/pi/smartcageData/'
dataframeFilename = 'miceActivityDataFrame_tunnel' + str(tunnelID) + '_' + str(datetime.datetime.now().date()) + '.csv'
dataframeColumnNames = ['mouseEntryTime', 'stimulusTime', 'tunnelID', 'mouseRFID', 'taskType', 'phaseID',
                    'stimulusType','trialType','mouseResponse', 'manipulation', 'responseTimes']
# general params: 
# constant pins numbers
global PIN_LED
PIN_LED = 20

global PIN_POLE_1
PIN_POLE_1 = 26  

global PIN_POLE_2
PIN_POLE_2 = 13  


global WATER_PULSE_DURATION
WATER_PULSE_DURATION = 0.05  #0.072
global RESPONSE_WINDOW
RESPONSE_WINDOW = 2

global LISTENING_WINDOW
LISTENING_WINDOW = 2


DELAY_RFID_WATER_TRAINING_WINDOW = 2
global STIMULATION_DURATION
STIMULATION_DURATION = 1
# limiting the number of visits per time unit
global TIME_UNIT
TIME_UNIT = 5*60        # 5 min in sec
global NUMBER_OF_VISITS
NUMBER_OF_VISITS = 50   # 10 visits
# training protocol
TRIALS_PER_BLOCK = 5

global allRFIDs
allRFIDs = {}   # dic of all mice to count the blocks, [0] contains # of enteries and [1] contains list of entry times

# activation
global Camflag
Camflag = True


PIN_LICK_DETECTOR
global cap
cap = MPR121.MPR121()       # defining lick detector
    
# initialization
serial_dev = InitialDevices()
print('Initializing devices')
mouseRFID = ''
 
while True:
    
    
    # waiting for a mouse
    RFID_lastChar = serial_dev.read()
            
    if RFID_lastChar == '\r':     # we have a full RFID, we identified the mouse
    
        print('a mouse entered tunnel #' + str(tunnelID))
        # record the entry time
        mouseEntryDatetime = datetime.datetime.now()
           
        # take an image of the mouse
        # format: CameraObject.capture(name of image including its path) 
#        CameraObject.capture(imagesDir + mouseRFID + '_entry_' + str(mouseEntryDatetime) + '.jpg')
              
        numTrials = 1   # for now, one trial per entry
        
        for trial in range(numTrials):
            giveReward = 0
            if not(mouseRFID in allRFIDs):
                allRFIDs[mouseRFID] = [0,[]]
                
            if currTaskType == 'Go/NoGo':           
                # choose: Go or No-Go trial?
                if currTaskPhase == '5-blocks':
                    if (allRFIDs[mouseRFID][0] % (2*TRIALS_PER_BLOCK)) < TRIALS_PER_BLOCK:
                        trialType = 'Go'
                        giveReward = 1
                    else:
                        trialType = 'NoGo'
                        giveReward = 0
                    allRFIDs[mouseRFID][0] += 1    # counting the trials for each mouse
                elif currTaskPhase == 'randomPIN_LICK_DETECTOR':
                    randInd = np.random.randint(2, high=4, size=1)
                    if randInd == 2:
                        trialType = 'Go'
                        giveReward = 1
                    elif randInd == 3:
                        trialType = 'NoGo'
                        giveReward = 0

                stimulusOff = 0
            
            # check if the mouse is allowed to participate or it needs to wait
            allRFIDs[mouseRFID][1].append(mouseEntryDatetime)   # writing entry times
            
            cont = cont_or_timeout(mouseRFID)
            
            if cont == 0:
                    print 'NO WATER - - - WAIT!!!!'
                    # create dataframe row
                    currEventRow = pd.DataFrame(index=[0], columns=dataframeColumnNames)
                    # fill the row with datacurrEventRow['mouseEntryTime'] = mouseEntryDatetime
                    currEventRow['mouseEntryTime'] = mouseEntryDatetime
                    currEventRow['trialType']      = 'TimeOut'
                    currEventRow['tunnelID']       = tunnelID
                    currEventRow['mouseRFID']      = mouseRFID
                    print currEventRow
            elif cont == 1:
                # running the trial
                if currTaskType == 'Training':
                    responseTimes = lick_before_drink_training(mouseRFID)
                    currMouseResponse = calculate_response(responseTimes)
                    
                    # create dataframe row
                    currEventRow = pd.DataFrame(index=[0],columns=dataframeColumnNames)
                    # fill the row with data
                    currEventRow['mouseEntryTime'] = mouseEntryDatetime
                    currEventRow['tunnelID']       = tunnelID
                    currEventRow['mouseRFID']      = mouseRFID
                    currEventRow['taskType']       = currTaskType
                    currEventRow['mouseResponse']  = currMouseResponse
                    currEventRow.set_value(0,'responseTimes',responseTimes)
                    print currEventRow
                elif currTaskType == 'Go/NoGo':
                    # maybe add time of waiting with random durations
                    stimulusStartTime = time.time()
                     
                    responseTimes = runTrial_task(trialType,mouseRFID,stimulusOff,giveReward)
                    currMouseResponse = calculate_response(responseTimes)
                    
                    # create dataframe row
                    currEventRow = pd.DataFrame(index=[0],columns=dataframeColumnNames)
                    # fill the row with data
                    currEventRow['mouseEntryTime'] = mouseEntryDatetime
                    currEventRow['stimulusTime']   = stimulusStartTime
                    currEventRow['tunnelID']       = tunnelID
                    currEventRow['mouseRFID']      = mouseRFID
                    currEventRow['taskType']       = currTaskType
                    currEventRow['phaseID']        = currTaskPhase
                    currEventRow['stimulusType']   = stimulusType
                    currEventRow['trialType']      = trialType
                    currEventRow['mouseResponse']  = currMouseResponse
                    currEventRow.set_value(0,'responseTimes',responseTimes)
                    print currEventRow
                
            # append to file (if there is no file it will be created)
            if not os.path.isfile(dataframeDir+ dataframeFilename):
                currEventRow.to_csv(dataframeDir+ dataframeFilename, mode='a', index=False, header=True)
            else:
                currEventRow.to_csv(dataframeDir+ dataframeFilename, mode='a', index=False, header=False)
                
            mouseRFID = ''
#           close_devices()                
    
    elif(RFID_lastChar.isalpha() or RFID_lastChar.isdigit()):   # reading the RFID
        mouseRFID = mouseRFID + RFID_lastChar
   
##############################################

