3#%% User Functions

import distutils.util
import datetime
import serial
from dateutil.parser import parse
import pandas as pd

USB_PORT = "/dev/ttyUSB0"
serial_dev = serial.Serial(USB_PORT, baudrate=9600)

# verify mouse identity
def verifyMouseIdentity():
    identifyMouse = False
    while not identifyMouse:
        mouseName = raw_input('Enter mouse name: ')
        mouseRFID = ''
        print('Scan RFID')
        while True:
            RFID_lastChar = serial_dev.read()           
            if RFID_lastChar == '\r':
                break
            elif(RFID_lastChar.isalpha() or RFID_lastChar.isdigit()):   # reading the RFID
                mouseRFID = mouseRFID + RFID_lastChar
        # go to miceTable and make sure mouseName and mouseRFID match:
        # if you are wroge:
        print('there is a mismatch between the Mouse Name and the RFID, please try again')
        # if you are right:
        identifyMouse = True
    print('mouse identified')        

# check in 
def checkIn():
    isMouseNew = raw_input('Is the mouse new in the cage? ')
    isMouseNewBool = distutils.util.strtobool(isMouseNew)
    if isMouseNewBool:
        # collect information about the mouse
        dateEntry = datetime.datetime.now().date()
        exprName = raw_input('Enter your name: ')
        mouseName = raw_input('Enter mouse name: ')
        mouseGenotype = raw_input('Enter mouse Genotype: ')
        mouseDOB = raw_input('Enter DOB of the mouse: ')
        mouseGen = raw_input('Enter M for male and F for female ')
        mouseRFID = ''
        print('Scan RFID')
        while True:
            RFID_lastChar = serial_dev.read()           
            if RFID_lastChar == '\r':
                break
            elif(RFID_lastChar.isalpha() or RFID_lastChar.isdigit()):
                mouseRFID = mouseRFID + RFID_lastChar
        isMouseInject = raw_input('Is the mouse injected with a virus? ')
        isMouseInjectBool = distutils.util.strtobool(isMouseInject)
        if isMouseInjectBool:
            mouseInjectionDate = raw_input('Enter mouse injection date: ')
            mouseVirus = raw_input('What virus was injected? ')
        isMouseInCage = True
        # save the information in miceTable
    else:
        verifyMouseIdentity()
        # write check-in in the log file
        dateIn = datetime.datetime.now()
    
# check out
def checkOut():
    verifyMouseIdentity()
    isPermanent = raw_input('Is the mouse going to be back to the cage? ')
    isPermanentBool = distutils.util.strtobool(isPermanent)
    if not isPermanentBool:
        isMouseInCage = False
        dateLeave = datetime.datetime.now().date()
    else:
        # write check-out in log file
        dateOut = datetime.datetime.now()
        reasonOut = raw_input('Enter the reason you are taking the mouse out of the cage ')

# add procedure to mouse CV
def addProcedure():
    mouseName = raw_input('Enter mouse name: ')
    newProcedure = raw_input('Enter procedure name: ')
    dateProcedureUser = raw_input('Enter procedure date: ')
    dateProcedure = parse(dateProcedureUser)
    # write in mouse CV
    
