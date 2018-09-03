# TODO
# ----
# Must:
# 	* Make sure that the program does not end
# 	* Implement listenToRFIDreader: call "onRFIDevent" when the mouse enters the tunnel
# 	* Implement isSessionRunning: check if the previous thread is still running
# 	* Implement closeSession: terminate old session and report an error.
# 		* Decide if something has to be saved to the DB table
#  	* Implement getMouseFromTable: read mouseID from DB based on its rfid
# 	* Implement getFunctionNameFromTable
#  	* Implement callFunctionInNewThread: probably according to the instructions
# 	* Implement writeResultToTable
# 	* Implement saveError: decide how do we notice the user when an error occurred
# 	* Register to sessionEnded: when the thread is done, call sessionEnded and pass the "tableID, keyID, numOfLicks"
# 
# 
# Optional:
# 	* Decide about the date+time format in the system
# 	* Decide if global variables are fine
# 		* Probably yes: https://stackoverflow.com/questions/13881395/in-python-what-is-a-global-statement
# 
# DONE
# ----
# 
# 

import sys
from datetime import datetime
from multiprocessing.pool import ThreadPool

global mouseID
global tunnelID
global startDateTime
global currentSession
global functionName
global pool

def listenToRFIDreader():
	pass

def isSessionRunning():
	global currentSession
	return currentSession.ready()

def closeSession():
	global pool
	pool.terminate()

	saveError("New enter during seesion")

def getMouseFromTable(rfid):
	pass

def getFunctionNameFromTable():
	global mouseID
	global tunnelID

	pass

def callFunctionInNewThread(functionName):
	global mouseID
	global tunnelID
	global startDateTime
	global currentSession

	currentSession = pool.apply_async(runFunction, (functionName, mouseID, tunnelID, startDateTime), callback=sessionEnded) # tuple of args for foo


def runFunction(functionName, mouseID, tunnelID, startDateTime):
	# In a new thread:
	# import function
	# call functionName(mouseID, tunnelID, startDateTime)
	# return thread handler

def sessionEnded(handler):
	global mouseID
	global tunnelID
	global startDateTime
	global functionName
	global currentSession

	tableID, keyID, numOfLicks = currentSession.get()

	if not keyExists(tableID, keyID):
		writeResultToTable(mouseID, tunnelID, startDateTime, functionName, numOfLicks, tableID, keyID)
	else:
		saveError("Existing key")

def writeResultToTable(mouseID, tunnelID, startDateTime, functionName, numOfLicks, tableID, keyID):
	pass

def saveError(err):
	pass

def onRFIDevent(rfid):
	global mouseID
	global tunnelID
	global startDateTime
	global functionName


	if isSessionRunning():
		closeSession()

	try:
		startDateTime = str(datetime.now())
		mouseID = getMouseFromTable(rfid)
		functionName = getFunctionNameFromTable()
		currentSession = callFunctionInNewThread(functionName)
		# Register to sessionEnded
	except:
		saveError("Function error")


if __name__ == "__main__":
	tunnelID = sys.argv[1]
	pool = ThreadPool(processes=1)
	listenToRFIDreader()
	# continue running