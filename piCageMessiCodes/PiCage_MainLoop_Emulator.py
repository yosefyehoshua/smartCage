import os
os.chdir('C:\Current Projects\PiCage\Code')

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import time

matplotlib.style.use('fivethirtyeight')
matplotlib.rcParams['font.size'] = 30
matplotlib.rcParams['figure.figsize'] = (20,15)


#%% create empty tables

dataFilepath = 'C:/Current Projects/PiCage/Code/emulator/'

miceTableName = 'miceTable'
miceTable = pd.DataFrame(columns=['mouseID','owner','geneticType','gender','dateOfBirth','comment'])
miceTable.to_csv(dataFilepath + miceTableName + '.csv',index=False)
del miceTable

miceCVTableName = 'miceCV_Table'
miceCVTable = pd.DataFrame(columns=['mouseID','date','eventDescription','returnLocation','weight','loggerName','dataFolderPath','comment'])
miceCVTable.to_csv(dataFilepath + miceCVTableName + '.csv',index=False)
del miceCVTable

RFID_toMouseMap_TableName = 'RFID_to_mouseID_Table'
RFID_to_mouseID_Table = pd.DataFrame(columns=['mouseID','RFID','operation','date','loggerName','comment'])
RFID_to_mouseID_Table.to_csv(dataFilepath + RFID_toMouseMap_TableName + '.csv',index=False)
del RFID_to_mouseID_Table

MouseTunnel_to_ProcedureMap_TableName = 'MouseAndTunnel_to_ProcedureMap_Table'
MouseAndTunnel_to_ProcedureMap_Table = pd.DataFrame(columns=['mouseID', 'tunnelID', 'userDefinedProcedureName','date','loggerName','comment'])
MouseAndTunnel_to_ProcedureMap_Table.to_csv(dataFilepath + MouseTunnel_to_ProcedureMap_TableName + '.csv',index=False)
del MouseAndTunnel_to_ProcedureMap_Table

PiCageSessionEvents_TableName = 'PiCageSessionEvents'
PiCageSessionEvents_Table = pd.DataFrame(columns=['mouseID', 'tunnelID', 'date', 'numLicks', 'userProcedureName', 'dataTableName', 'dataEntryID'])
PiCageSessionEvents_Table.to_csv(dataFilepath + PiCageSessionEvents_TableName + '.csv',index=False)
del PiCageSessionEvents_Table


#%% database helper functions

# insert entry to mouse table
def LogNewMouse(mouseID=np.nan, ownerName=np.nan,geneticType=np.nan, gender=np.nan, dateOfBirth=np.nan, comment=np.nan):
    T = pd.read_csv(dataFilepath + miceTableName + '.csv')
    
    # append entry to table
    newRowIndex = T.shape[0]+1
    T.loc[newRowIndex] = [mouseID,ownerName,geneticType,gender,dateOfBirth,comment]
    T.to_csv(dataFilepath + miceTableName + '.csv',index=False)
    return

# insert entry to mouse life events 
def LogMajorLifeEvent(mouseID=np.nan, date=np.nan, eventDescription=np.nan, returnLocation=np.nan,
                      weight=np.nan, loggerName=np.nan, dataFolderPath=np.nan, comment=np.nan):
    T = pd.read_csv(dataFilepath + miceCVTableName + '.csv')
    
    # append entry to table
    newRowIndex = T.shape[0]+1
    T.loc[newRowIndex] = [mouseID,date,eventDescription,returnLocation,weight,loggerName,dataFolderPath,comment]
    T.to_csv(dataFilepath + miceCVTableName + '.csv',index=False)
    return

# connect/disconnect mouse with a specific RFID
def LogNewMouseRFIDConnection(mouseID=np.nan, RFID=np.nan, operation=np.nan, date=np.nan, loggerName=np.nan, comment=np.nan):
    T = pd.read_csv(dataFilepath + RFID_toMouseMap_TableName + '.csv')
    
    # append entry to table
    newRowIndex = T.shape[0]+1
    T.loc[newRowIndex] = [mouseID,RFID,operation,date,loggerName,comment]
    T.to_csv(dataFilepath + RFID_toMouseMap_TableName + '.csv', index=False)
    return

# update the procedure name that should be run for (mouseID, tunnelID) pair
def UpdateUserDefinedProcedure(mouseID=np.nan, tunnelID=np.nan, userDefinedProcedureName=np.nan, date=np.nan, loggerName=np.nan, comment=np.nan):
    T = pd.read_csv(dataFilepath + MouseTunnel_to_ProcedureMap_TableName + '.csv')
    
    # append entry to table
    newRowIndex = T.shape[0]+1
    T.loc[newRowIndex] = [mouseID,tunnelID,userDefinedProcedureName,date,loggerName,comment]
    T.to_csv(dataFilepath + MouseTunnel_to_ProcedureMap_TableName + '.csv', index=False)

    return

# update the 
def LogNewMouseTunnelEntrySession(mouseID=np.nan, tunnelID=np.nan, date=np.nan, numLicks=0.0, 
                           userProcedureName=np.nan, dataTableName=np.nan, dataEntryID=np.nan):
    T = pd.read_csv(dataFilepath + PiCageSessionEvents_TableName + '.csv')
    
    # append entry to table
    newRowIndex = T.shape[0]+1
    T.loc[newRowIndex] = [mouseID, tunnelID, date, numLicks, userProcedureName, dataTableName, dataEntryID]
    T.to_csv(dataFilepath + PiCageSessionEvents_TableName + '.csv', index=False)
    return


# convert RFID to mouseID
def GetMouseID_from_RFID(currRFID):
    T = pd.read_csv(dataFilepath + RFID_toMouseMap_TableName + '.csv')
    
    currMouseID = T.loc[T['RFID'] == currRFID,'mouseID'].values
    return currMouseID[0]

# get procedure name that we need to apply for current mouseID and tunnelID
def GetMouseProcedure_from_mID_tID(currMouseID, currTunnelID):
    T = pd.read_csv(dataFilepath + MouseTunnel_to_ProcedureMap_TableName + '.csv')
    
    mID_tID_allRows = T.loc[np.logical_and(T['mouseID'] == currMouseID, T['tunnelID'] == currTunnelID)]
    mostRecentDateInd = pd.to_datetime(mID_tID_allRows['date']).argmax()
    currUserProcedureName = mID_tID_allRows.loc[mostRecentDateInd,'userDefinedProcedureName']
    return currUserProcedureName


#%% example template of a user defined function and table to store data into

def CreateNewExperimentTable(tableName='someDataTable',tableColumns=['col_A','col_B','col_C']):
    assert('sessionID' in tableColumns)
    T = pd.DataFrame(columns=tableColumns)
    T.to_csv(dataFilepath + tableName + '.csv',index=False)
    return

PoleDetectionExperiment_TableColumns = ['sessionID','trialWithinSession','IsPolePresent','mouseResponse','wasRewardGiven','reactionTime']
CreateNewExperimentTable(tableName='Yair_PoleDetectionTable',tableColumns=PoleDetectionExperiment_TableColumns)

def RunPoleDetectionSession(mouseID, tunnelID, date):

    myTableName = 'Yair_PoleDetectionTable' # this should be hard coded by the user 
    
    T = pd.read_csv(dataFilepath + myTableName + '.csv')
    if T.shape[0] == 0:
        newSessionID = 0
    else:
        newSessionID = T.loc[T.shape[0]-1,'sessionID'] + 1

    stimOptions          = ['present', 'not present']
    responseOptions      = ['lick', 'no lick']
    isRewardGivenOptions = ['reward given', 'no reward']

    # decide on a random number of trials
    numTrials = np.random.randint(15)
    # simulate the trials    
    for trialInSession in range(numTrials):
        IsPolePresent = stimOptions[np.random.randint(len(stimOptions))]
        mouseResponse = responseOptions[np.random.randint(len(responseOptions))]
        rewardGiven   = isRewardGivenOptions[np.random.randint(len(isRewardGivenOptions))]
        reactionTime  = 1500*np.random.rand()
        
        # update information about current trial and append entry to table
        newRowIndex = T.shape[0]+1
        T.loc[newRowIndex] = [newSessionID,trialInSession+1,IsPolePresent,mouseResponse,rewardGiven,reactionTime]
    
    # save table
    T.to_csv(dataFilepath + myTableName + '.csv', index=False)

    # collect output for the kernel
    numLicks = (T.loc[T.loc[:,'sessionID'] == newSessionID]['mouseResponse'] == 'lick').sum()
    dataTableName = myTableName
    dataEntryID = newSessionID
    
    return numLicks, dataTableName, dataEntryID

#%% define database starting position (insert a few mice to the cage etc.)

# log several mice
LogNewMouse(mouseID='ABC_123', ownerName='Adi' , geneticType='C57'     , gender='Male',   
            dateOfBirth=pd.to_datetime('1/10/17',dayfirst=True), comment='for cage only')

LogNewMouse(mouseID='DEF_456', ownerName='Adi' , geneticType='C57'     , gender='Female', 
            dateOfBirth=pd.to_datetime('17/10/17',dayfirst=True),  comment='for cage only')

LogNewMouse(mouseID='HIJ_789', ownerName='Yair', geneticType='Th-Cre'  , gender='Male',   
            dateOfBirth=pd.to_datetime('10/10/17',dayfirst=True),  comment='for cage + Ca imaging')

LogNewMouse(mouseID='KLM_345', ownerName='Amir', geneticType='Chat-Cre', gender='Male',   
            dateOfBirth=pd.to_datetime('3/10/17',dayfirst=True),  comment='for E-phys')

# log several mice events
LogMajorLifeEvent(mouseID='ABC_123', loggerName='Adi', date=pd.to_datetime('2/11/17',dayfirst=True), eventDescription='head bar + RFID', 
                  returnLocation='PiCage_1',weight=21.3, comment='head bar very stable')

LogMajorLifeEvent(mouseID='HIJ_789', loggerName='Yair', date=pd.to_datetime('1/11/17',dayfirst=True), eventDescription='virus injections (GCaMP6s)', 
                  returnLocation='PiCage_1',weight=25.3, comment='good injection')

LogMajorLifeEvent(mouseID='HIJ_789', loggerName='Yair', date=pd.to_datetime('13/11/17',dayfirst=True), eventDescription='head bar + RFID', 
                  returnLocation='PiCage_1',weight=25.7, comment='head bar OK')

LogMajorLifeEvent(mouseID='HIJ_789', loggerName='Yair', date=pd.to_datetime('22/11/17',dayfirst=True), eventDescription='Calcium Experiment', 
                  returnLocation='PiCage_1',weight=26.3, dataFolderPath='C:/CaImaging_22_11_17/', comment='lots of cells!')

LogMajorLifeEvent(mouseID='DEF_456', loggerName='Adi', date=pd.to_datetime('28/11/17',dayfirst=True), eventDescription='head bar + RFID', 
                  returnLocation='PiCage_1',weight=24.6, comment='head bar stable')

# connect RFID to mouseID
LogNewMouseRFIDConnection(mouseID='ABC_123', RFID='#aabbcc', operation='Connect', date=pd.to_datetime('2/11/17',dayfirst=True) , loggerName='Adi', comment='fresh mouse for behavoir')
LogNewMouseRFIDConnection(mouseID='DEF_456', RFID='#dddeee', operation='Connect', date=pd.to_datetime('13/11/17',dayfirst=True), loggerName='Yair', comment='fresh mouse for behavoir')
LogNewMouseRFIDConnection(mouseID='HIJ_789', RFID='#hijklm', operation='Connect', date=pd.to_datetime('18/11/17',dayfirst=True), loggerName='Adi', comment='fresh mouse for behavoir')

# define procedures to work on all mice
UpdateUserDefinedProcedure(mouseID='HIJ_789', tunnelID='tunnel_1', userDefinedProcedureName='RunPoleDetectionSession', date=pd.to_datetime('18/11/17',dayfirst=True), loggerName='Yair', comment='pole detection go no go task')
UpdateUserDefinedProcedure(mouseID='ABC_123', tunnelID='tunnel_1', userDefinedProcedureName='RunPoleDetectionSession', date=pd.to_datetime('19/11/17',dayfirst=True), loggerName='Adi', comment='using Yairs function')
UpdateUserDefinedProcedure(mouseID='DEF_456', tunnelID='tunnel_1', userDefinedProcedureName='RunPoleDetectionSession', date=pd.to_datetime('19/11/17',dayfirst=True), loggerName='Adi', comment='using Yairs function')

# list of starting mice in cage (for randomization)
currListOfMiceRFIDsInCage = ['#aabbcc','#dddeee','#hijklm']
                       
#%% while true main loop

currTunnelID = 'tunnel_1'
maxNumOfMouseTunnelEntries = 40

for i in range(maxNumOfMouseTunnelEntries):
    
    if np.random.rand() < 0.5:
    # either mouse enters tunnel
        
        # read/sense mouse RFID
        currRFID = currListOfMiceRFIDsInCage[np.random.randint(len(currListOfMiceRFIDsInCage))]
        
        # register mouse entry time
        currDate = pd.to_datetime('now')
        
        # convert RFID to mouseID
        currMouseID = GetMouseID_from_RFID(currRFID)
        
        # read which procedure we need to apply
        currUserProcedureName = GetMouseProcedure_from_mID_tID(currMouseID, currTunnelID)
    
        # run the correct function
        nurrNumLicks, currDataTableName, currDataEntryID = locals()[currUserProcedureName](currMouseID, currTunnelID, currDate)
    
        # log the current session in the sessions table
        LogNewMouseTunnelEntrySession(mouseID=currMouseID, tunnelID=currTunnelID, date=currDate, numLicks=nurrNumLicks, 
                                      userProcedureName=currUserProcedureName, dataTableName=currDataTableName, dataEntryID=currDataEntryID)
        print('%s: logged new tunnel session. (mouseID, num Licks) = ("%s", %d)' %(currDate,currMouseID,nurrNumLicks))


    # either user inserts an update (inserts a new mouse to the cage etc).
    if np.random.rand() < 0.1:
        
        newMouseID = 'FDG_' + str(np.random.randint(10)) + str(np.random.randint(10)) + str(np.random.randint(10))
        newRFID    = '#as_' + str(np.random.randint(10)) + str(np.random.randint(10)) + str(np.random.randint(10)) + str(np.random.randint(10))
        newDate    = pd.to_datetime('now')
        newEventDescription = 'head bar + RFID'
        
        currListOfMiceRFIDsInCage.append(newRFID)
        
        LogNewMouse(mouseID=newMouseID, ownerName='Yossi', geneticType='AI9', gender='Female', dateOfBirth=newDate)
        print('-'*35 + '\\'*5)
        print('%s: logged new mouse ID = "%s"' %(newDate,newMouseID))
        
        LogMajorLifeEvent(mouseID=newMouseID, loggerName='Yossi', date=newDate, eventDescription=newEventDescription, 
                          returnLocation='PiCage_1',weight=20.0 + np.random.rand()*10)
        print('%s: logged new mouse life event = "%s"' %(newDate, newEventDescription))

        LogNewMouseRFIDConnection(mouseID=newMouseID, RFID=newRFID, operation='Connect', date=newDate, loggerName='Yossi')
        print('%s: logged new (mouseID,RFID) connection = ("%s", "%s")' %(newDate,newMouseID,newRFID))

        UpdateUserDefinedProcedure(mouseID=newMouseID, tunnelID=currTunnelID, userDefinedProcedureName='RunPoleDetectionSession', 
                                   date=newDate, loggerName='Yossi', comment='using Yairs function')
        print('%s: logged new procedure (mouseID,tunnelID,function) = ("%s", "%s", "%s")' %(newDate,newMouseID,currTunnelID,'RunPoleDetectionSession'))
        print('-'*35 + '/'*5)
        
    # wait some random amount of time
    time.sleep(np.random.rand()+np.random.rand())


