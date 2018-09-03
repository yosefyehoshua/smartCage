# TODO
# ----
# Must:
# 	* Implement closeSession: terminate old session and report an error.
# 	* Decide if something has to be saved to the DB table
# 	* Implement saveError: decide how do we notice the user when an error occurred
# 
# 
# Optional:
# 	* Decide about the date+time format in the system
# 	* Decide if global variables are fine
# 	* Probably yes: https://stackoverflow.com/questions/13881395/in-python-what-is-a-global-statement
# 
# DONE
# ----
# 	* Implement listenToRFIDreader: call "onRFIDevent" when the mouse enters the tunnel
# 	* Make sure that the program does not end
# 	* Implement isSessionRunning: check if the previous thread is still running
#  	* Implement getMouseFromTable: read mouseID from DB based on its rfid
# 	* Implement getFunctionNameFromTable
#  	* Implement callFunctionInNewThread: probably according to the instructions
# 	* Implement writeResultToTable
# 	* Register to sessionEnded: when the thread is done, call sessionEnded and pass the "tableID, keyID, numOfLicks"
# 
# 

import sys
from datetime import datetime
from multiprocessing.pool import ThreadPool

import serial

from databaseHelperFunctions import GetMouseID_from_RFID, \
    GetMouseProcedure_from_mID_tID, LogNewMouseTunnelEntrySession

import RPi.GPIO as GPIO
import time

global cageID
global mouseID
global tunnelID
global startDateTime
global currentSession
global functionName
global pool


def getRFIDpinNumber():
    """
	Gets RFID pin Number
	:return: // todo returns 23 ????
	"""
    global tunnelID # // todo why this statment needs a GPIO number. user input a tunnel id -> needs to be presetted, means i pick the tunnelID

    return 23


def listenToRFIDreader():
    """
    calls "onRFIDevent" when the mouse enters the tunnel and keeps the program running.
    """
    pinNumber = getRFIDpinNumber()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pinNumber, GPIO.IN)

    USB_PORT = "/dev/ttyUSB0"
    serial_dev = serial.Serial(USB_PORT, baudrate=9600)

    while True:
        mouseRFID = ''
        waitingForRFIDStr = True

        channel = GPIO.wait_for_edge(pinNumber, GPIO.RISING)
        if channel:
            while waitingForRFIDStr:
                RFID_lastChar = serial_dev.read()
                RFID_lastChar = RFID_lastChar.decode('utf-8')
                if RFID_lastChar == '\r':  # we have a full RFID, we identified the mouse
                    onRFIDevent(mouseRFID)
                    waitingForRFIDStr = False
                elif (RFID_lastChar.isalpha() or RFID_lastChar.isdigit()):
                    mouseRFID = mouseRFID + RFID_lastChar

    GPIO.cleanup()


def isSessionRunning():
    """
    check if the previous thread (sessions) is still running
    :return: currentSession.ready() // todo boolean?
    """
    global currentSession
    return currentSession.ready()


def closeSession():
    """
    closes a session.
    """
    global pool
    pool.terminate()

    saveError("New enter during session")


def callFunctionInNewThread(relativePath, functionName):
    """
    calls a new function in new thread. # todo read about threads and semi parallel computation.
    :param relativePath:
    :param functionName:
    :return:
    """
    global mouseID
    global tunnelID
    global startDateTime
    global currentSession

    currentSession = pool.apply_async(runFunction, args=( relativePath, functionName, mouseID, tunnelID, startDateTime), callback=sessionEnded)  # tuple of args for foo


def runFunction(relativePath, functionName, mouseID, tunnelID, startDateTime): # todo exec for a given function.
    # split path to folder and file_name
    relativeFolder, fileName = relativePath.rsplit('\\', 1)

    # add folder to system path
    import sys
    sys.path.insert(0, relativeFolder)

    # look for function in fileName
    try:
        exec('from ' + fileName + ' import ' + functionName)
        tableID, keyID, numOfLicks = eval(functionName + '(mouseID, tunnelID, startDateTime)') # todo how to access this tuple????
    except:
        print('Sorry, function was not found')


def sessionEnded(handler): # func. has ended
    global cageID
    global mouseID
    global tunnelID
    global startDateTime
    global functionName
    global currentSession

    tableID, keyID, numOfLicks = currentSession.get()

    if not keyExists(tableID, keyID):
        LogNewMouseTunnelEntrySession(cageID, mouseID, tunnelID, startDateTime, numOfLicks, functionName, tableID, keyID)
    else:
        saveError("Existing key")


def saveError(err):
    print(err)


def onRFIDevent(rfid):
    global mouseID
    global tunnelID
    global startDateTime
    global functionName

    if isSessionRunning():
        closeSession()

    try:
        startDateTime = str(datetime.now())
        mouseID = GetMouseID_from_RFID(rfid)
        relativePath, functionName = GetMouseProcedure_from_mID_tID(mouseID, tunnelID) # todo add a path directory to this func. in the database file.
        currentSession = callFunctionInNewThread(relativePath, functionName)
    except:
        saveError("Function error")


if __name__ == "__main__":
    cageID = sys.argv[1]
    tunnelID = sys.argv[2]
    pool = ThreadPool(processes=1)
    listenToRFIDreader()
