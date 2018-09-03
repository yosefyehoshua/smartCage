#%% Monitoring Program

import cPickle as pickle
import RPi.GPIO as GPIO
from time import sleep
import datetime
import socket

# flash water to asure water supply throgh the tubes
def flashWater():
    tunnelsDict = pickle.load(open("tunnelsDict.p", "rb"))
    tunnelsList = tunnelsDict.keys()
    for tunnelName in tunnelsList:
        pinWater = tunnelsDict[tunnelName]['PIN_WATER']
        GPIO.output(pinWater, 1)
        sleep(30)
        GPIO.output(pinWater, 0)
        
#%%
hFlash = 10
mFlash = 0
hMonitorDrink = 7
hMonitorTunnels = 18
hIPaddress1 = 9
hIPaddress2 = 21
while True:
    H = datetime.datetime.now().hour
    M = datetime.datetime.now().minute
    # flash water once in 24 hours
    if H==hFlash and M==mFlash:
        flashWater()
    # check drinking of all mice in last 24 hours
    if H==hMonitorDrink and M==0:

    # check that tunnels are opened once in 24 hours
    if H==hMonitorTunnels and M==0:

    # check entries and also IR beam
    # write IP address in a file and upload it to Dropbox twice in 24 hours
    if (H==hIPaddress1 or H==hIPaddress2) and M==0:
        IPaddr = socket.gethostbyname(socket.gethostname())
        IPaddressFile = open("monitoringFiles/currentIPaddress.txt","w")
        IPaddressFile.write("the current IP of the RPi in the basement is: " + str(IPaddr))
        IPaddressFile.close()
    sleep(60*40)
        
        
        