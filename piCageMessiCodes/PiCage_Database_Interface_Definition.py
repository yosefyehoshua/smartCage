import os
os.chdir('C:\Current Projects\PiCage\Code')

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt

matplotlib.style.use('fivethirtyeight')
matplotlib.rcParams['font.size'] = 30
matplotlib.rcParams['figure.figsize'] = (20,15)

#%% table that should be defined (col names)

#mouseTable_columns           = ['mouseID','Owner','GeneticType',  'Gender','DateOfBirth']
#mouseLifeEventsTable_columns = ['mouseID', 'Date', 'loggerName',  'weight','eventDescription','comment','dataFolderName']
#mouseID_RFID_Table_columns   = ['mouseID', 'RFID',  'operation',    'date','loggerName','comment']
#mouseIDandTunnelID_UserFunction_Mapping_columns = ['mouseID', 'tunnelID', 'UserFunctionName','date','loggerName','comment']
#PoleDetectionExperimentTable_columns = ['sessionID','trialNum','IsPolePresent','mouseResponse','reactionTime']


PiCageSessionEventsTable_columns     = ['mouseID', 'tunnelID', 'Date', 'numLicks', 'UserFunctionName', 'dataTableName', 'dataEntryID']

#%% logger utility functions that should be defined

#LogMouse(mouseID, ownerName='None',geneticType='unknown',dateOfBirth='1/1/17',mouseGender='Female')
#LogMouseLifeEvent(mouseID, ownerName='None',geneticType='unknown',dateOfBirth='1/1/17',mouseGender='Female')
#LogNewMouseRFIDConnection(mouseID='', RFID='', date='1/1/17', opperation='Connect')
#UpdateUserDefinedProcedure(mouseID, tunnelID, userFunctionName, date, loggerName, comment)
#CreateNewExperimentTable(tableName='someDataTable',tableColumns=['col_A','col_B','col_C'])

#def ExampleUserFunction(mouseID, tunnelID, date):
#
#    numLicks = np.random.randint(5)
#    tableNames = ['Yair_WhiskerTask_Table','Adi_VisionTask_Table']
#    dataTableName = tableNames[np.random.randint(len(tableNames))]
#    dataEntryID = np.random.randint(200)
#    
#    # update data in the correct table
#    
#    
#    
#    return numLicks, dataTableName, dataEntryID

# calling ExampleUserFunction using only it's string
locals()['ExampleUserFunction']('ABC_DEF','#tunnel_1','1/1/2007')
      
LogPiCageTunnelSessionEvent(mouseID, date='', tunnelID='', )

#%% Unit Test

dataFilepath = 'C:/Current Projects/PiCage/Code/hackaton/'


# create tables
#miceTable                = pd.DataFrame(columns=['mouseID','Owner','GeneticType','Gender','DateOfBirth'])
#mouseLifeEventsTable     = pd.DataFrame(columns=['mouseID','Date','eventDescription','comment','dataFolderName','weight','loggerName'])
#mouseID_RFID_Table       = pd.DataFrame(columns=['mouseID','RFID','operation','date'])
#mouseIDandTunnelID_UserFunction_Mapping = pd.DataFrame(columns=['mouseID', 'tunnelID', 'UserFunctionName'])

PiCageSessionEventsTable = pd.DataFrame(columns=['mouseID','tunnelID','Date','numLicks','UserFunctionName','dataTableName','dataEntryID'])

#%%











#%% mice table Unit test

dataFilepath = 'C:/Current Projects/PiCage/Code/hackaton/'
miceTableName = 'miceTable'

# create table
miceTable = pd.DataFrame(columns=['mouseID','Owner','GeneticType','Gender','DateOfBirth','Comment'])
miceTable.loc[0] = ['NullMouse','TableCreator','Unknown','Unknown',pd.to_datetime('11/9/01'),'filler row']
miceTable.to_csv(dataFilepath + miceTableName + '.csv',index=False)

def LogNewMouse(mouseID='no ID', ownerName='unknown owner',geneticType='unknown genetic type',
                gender='unknown gender', dateOfBirth='Unknown date', comment='no comment'):
    T = pd.read_csv(dataFilepath + miceTableName + '.csv')
    
    # append entry to table
    newRowIndex = T.shape[0]+1
    T.loc[newRowIndex] = [mouseID,ownerName,geneticType,gender,dateOfBirth,comment]
    T.to_csv(dataFilepath + miceTableName + '.csv',index=False)

    print('-'*80)
    print('last 3 rows of the mice Table:')
    print('-'*25)
    print(T.loc[newRowIndex-3:,:])
    print('-'*80)

    return

# insert a few example entries
LogNewMouse(comment='checking default inits')
LogNewMouse(mouseID='IJK_778', ownerName='Adi', geneticType='C57',      gender='Male',   dateOfBirth=pd.to_datetime('21/7/16'), comment='for cage')
LogNewMouse(mouseID='AAD_667', ownerName='Amir',geneticType='Chat-CRE', gender='Female', dateOfBirth=pd.to_datetime('1/2/03'),  comment='for e-phys')
LogNewMouse(mouseID='ADF_123', ownerName='Yair',geneticType='Th-CRE',   gender='Male',   dateOfBirth=pd.to_datetime('1/8/06'),  comment='for Ca2+ imaging')
LogNewMouse(mouseID='ABG_332', ownerName='Ben', geneticType='WT',       gender='Female', dateOfBirth=pd.to_datetime('13/3/13'), comment='for vocalization')

#%% mouse major life events table unit test
    
dataFilepath = 'C:/Current Projects/PiCage/Code/hackaton/'
miceCVTableName = 'miceCV_Table'

# create table
miceCVTable = pd.DataFrame(columns=['mouseID','date','eventDescription','weight','loggerName','dataFolderPath','comment'])
miceCVTable.loc[0] =               ['NullMouse',pd.to_datetime('11/9/01'),'no description','NaN','Table creator','C:/randFolder/','init filler row']
miceCVTable.to_csv(dataFilepath + miceCVTableName + '.csv',index=False)

def LogMajorLifeEvent(mouseID='no ID', date='unknown date',eventDescription='no description', 
                      weight='NaN', loggerName='unknown logger', dataFolderPath='NaN', comment='no comment'):
    T = pd.read_csv(dataFilepath + miceCVTableName + '.csv')
    
    # append entry to table
    newRowIndex = T.shape[0]+1
    T.loc[newRowIndex] = [mouseID,date,eventDescription,weight,loggerName,dataFolderPath,comment]
    T.to_csv(dataFilepath + miceCVTableName + '.csv',index=False)

    print('-'*80)
    print('last 3 rows of the mice Table:')
    print('-'*25)
    print(T.loc[newRowIndex-3:,:])
    print('-'*80)

    return

# insert a few example entries
LogMajorLifeEvent(comment='checking default inits')
LogMajorLifeEvent(mouseID='IJK_778', loggerName='Adi',  date=pd.to_datetime('21/7/16'), eventDescription='Ca imaging experiment', 
                  weight=22.3, dataFolderPath='C:/CaImaging_18_3_17/', comment='amazing experiment!!')
LogMajorLifeEvent(mouseID='IJK_778', loggerName='Yair',  date=pd.to_datetime('21/8/16'), eventDescription='Ca imaging experiment', 
                  dataFolderPath='C:/Ca_Imaging_21_8_16/', comment='bad experiment. no cells')
LogMajorLifeEvent(mouseID='ADF_123', loggerName='Amir',  date=pd.to_datetime('23/5/18'), eventDescription='E-phys experiment', 
                  weight=28.3, dataFolderPath='C:/Ephys_25_3_17/', comment='a lot of spikes!')
LogMajorLifeEvent(mouseID='ABG_332', loggerName='Adi',  date=pd.to_datetime('13/3/13'), eventDescription='putting head bar', 
                  weight=34.7, comment='a lot of bleeding')


#%% mice RFID mapping Unit test

dataFilepath = 'C:/Current Projects/PiCage/Code/hackaton/'
RFID_toMouseMap_TableName = 'RFID_to_mouseID_Table'

# create table
RFID_to_mouseID_Table = pd.DataFrame(columns=['mouseID','RFID','operation','date','loggerName','comment'])
RFID_to_mouseID_Table.loc[0] = ['NullMouse','NullRFID','Null Op',pd.to_datetime('11/9/01'),'Table Creator','no comment']
RFID_to_mouseID_Table.to_csv(dataFilepath + RFID_toMouseMap_TableName + '.csv',index=False)

def LogNewMouseRFIDConnection(mouseID='no ID', RFID='unknown RFID',operation='no op',
                              date='unknown date', loggerName='unknown logger', comment='no comment'):
    T = pd.read_csv(dataFilepath + RFID_toMouseMap_TableName + '.csv')
    
    # append entry to table
    newRowIndex = T.shape[0]+1
    T.loc[newRowIndex] = [mouseID,RFID,operation,date,loggerName,comment]
    T.to_csv(dataFilepath + RFID_toMouseMap_TableName + '.csv', index=False)

    print('-'*80)
    print('last 3 rows of the mice Table:')
    print('-'*25)
    print(T.loc[newRowIndex-3:,:])
    print('-'*80)

    return

# insert a few example entries
LogNewMouseRFIDConnection(comment='checking default inits')
LogNewMouseRFIDConnection(mouseID='IJK_778', RFID='#HFsGF', operation='Connect',    date=pd.to_datetime('21/7/16'), loggerName='David', comment='fresh mouse for behavoir')
LogNewMouseRFIDConnection(mouseID='IJK_778', RFID='#HaaGD', operation='Disconnect', date=pd.to_datetime('1/8/16'),  loggerName='David', comment='mouse died in cage')
LogNewMouseRFIDConnection(mouseID='ABG_332', RFID='#H56YF', operation='Connect',    date=pd.to_datetime('1/8/06'),  loggerName='Stav', comment='for vocalization')
LogNewMouseRFIDConnection(mouseID='ABG_332', RFID='#HifGF', operation='Disconnect', date=pd.to_datetime('13/3/13'), loggerName='Stav', comment='didnt learn anything')
LogNewMouseRFIDConnection(mouseID='ADF_123', RFID='#H588F', operation='Connect',    date=pd.to_datetime('1/8/06'),  loggerName='Adi', comment='for behavoir')
LogNewMouseRFIDConnection(mouseID='ADH_453', RFID='#AvgGF', operation='Connect',    date=pd.to_datetime('1/8/06'),  loggerName='Adi', comment='for behavoir')

                          
#%% Mouse and Tunnel ID to User Defined Procedure Unit test

dataFilepath = 'C:/Current Projects/PiCage/Code/hackaton/'
MouseTunnel_to_ProcedureMap_TableName = 'MouseAndTunnel_to_ProcedureMap_Table'

# create table
MouseAndTunnel_to_ProcedureMap_Table = pd.DataFrame(columns=['mouseID', 'tunnelID', 'UserDefinedProcedureName','date','loggerName','comment'])
MouseAndTunnel_to_ProcedureMap_Table.loc[0] = ['NullMouse','NullTunnel','NullProcedure',pd.to_datetime('11/9/01'),'Table Creator','no comment']
MouseAndTunnel_to_ProcedureMap_Table.to_csv(dataFilepath + MouseTunnel_to_ProcedureMap_TableName + '.csv',index=False)

def UpdateUserDefinedProcedure(mouseID='unknown mouse', tunnelID='unknown Tunnel',UserDefinedProcedureName='unknown procedure',
                               date='unknown date', loggerName='unknown logger', comment='no comment'):
    T = pd.read_csv(dataFilepath + MouseTunnel_to_ProcedureMap_TableName + '.csv')
    
    # append entry to table
    newRowIndex = T.shape[0]+1
    T.loc[newRowIndex] = [mouseID,tunnelID,UserDefinedProcedureName,date,loggerName,comment]
    T.to_csv(dataFilepath + MouseTunnel_to_ProcedureMap_TableName + '.csv', index=False)

    print('-'*80)
    print('last 3 rows of the mice Table:')
    print('-'*25)
    print(T.loc[newRowIndex-3:,:])
    print('-'*80)

    return

# insert a few example entries
UpdateUserDefinedProcedure(comment='checking default inits')
UpdateUserDefinedProcedure(mouseID='IJK_778', tunnelID='#HFsGF', UserDefinedProcedureName='Whisker_GoNoGo_Yair', date=pd.to_datetime('21/7/16'), loggerName='David', comment='added storage of reaction time')
UpdateUserDefinedProcedure(mouseID='IJK_778', tunnelID='#HaaGD', UserDefinedProcedureName='Whisker_GoNoGo_Adi',  date=pd.to_datetime('1/8/16'),  loggerName='David', comment='now support up to 15 trials')
UpdateUserDefinedProcedure(mouseID='ABG_332', tunnelID='#H56YF', UserDefinedProcedureName='Whisker_GoNoGo_Yair', date=pd.to_datetime('1/8/06'),  loggerName='Stav', comment='also records video')
UpdateUserDefinedProcedure(mouseID='ABG_332', tunnelID='#HifGF', UserDefinedProcedureName='LightDetection_David',date=pd.to_datetime('13/3/13'), loggerName='Stav', comment='stores also whisker movment')
UpdateUserDefinedProcedure(mouseID='ADF_123', tunnelID='#H588F', UserDefinedProcedureName='Vocalization_SameNotSame_Stav',date=pd.to_datetime('1/8/06'),  loggerName='Adi', comment=' random comment')
                           
                           

#%% user defined table that is filled inside user defined function

dataFilepath = 'C:/Current Projects/PiCage/Code/hackaton/'


def CreateNewExperimentTable(tableName='someDataTable',tableColumns=['col_A','col_B','col_C']):
    assert('sessionID' in tableColumns)
    T = pd.DataFrame(columns=tableColumns)
    T.loc[0] = ['sessionID'] + ['NaN']*(len(tableColumns)-1)
    T.loc[0,'sessionID'] = 0
    T.to_csv(dataFilepath + tableName + '.csv',index=False)
    return


PoleDetectionExperimentTable_columns = ['sessionID','trialWithinSession','IsPolePresent','mouseResponse','reactionTime']
CreateNewExperimentTable(tableName='Yair_PoleDetectionTable',tableColumns=PoleDetectionExperimentTable_columns)



def RunPoleDetectionSession(mouseID, tunnelID, date):

    myTableName = 'Yair_PoleDetectionTable' # this should be hard coded by the user 
    
    T = pd.read_csv(dataFilepath + myTableName + '.csv')
    newSessionID = T.loc[T.shape[0]-1,'sessionID'] + 1

    stimOptions     = ['present', 'not present']
    responseOptions = ['lick', 'no lick']

    # decide on a random number of trials
    numTrials = np.random.randint(15)
    # simulate the trials    
    for trialInSession in range(numTrials):
        IsPolePresent = stimOptions[np.random.randint(len(stimOptions))]
        mouseResponse = responseOptions[np.random.randint(len(responseOptions))]
        reactionTime  = 1500*np.random.rand()
        
        # update information about current trial and append entry to table
        newRowIndex = T.shape[0]+1
        T.loc[newRowIndex] = [newSessionID,trialInSession+1,IsPolePresent,mouseResponse,reactionTime]
    
    # save table
    T.to_csv(dataFilepath + myTableName + '.csv', index=False)

    # collect output for the kernel
    numLicks = (T.loc[T.loc[:,'sessionID'] == newSessionID]['mouseResponse'] == 'lick').sum()
    dataTableName = myTableName
    dataEntryID = newSessionID
    
    return numLicks, dataTableName, dataEntryID

RunPoleDetectionSession('AVCDFDF', 'tunnel1', '1/1/15')
RunPoleDetectionSession('AVsdFDF', 'tunnel1', '1/5/15')
RunPoleDetectionSession('AVgggDF', 'tunnel1', '6/5/16')

# calling ExampleUserFunction using only it's string
#locals()['ExampleUserFunction']('ABC_DEF','#tunnel_1','1/1/2007')
    
        
#%% PiCage Session Events Table

dataFilepath = 'C:/Current Projects/PiCage/Code/hackaton/'
PiCageSessionEvents_TableName = 'PiCageSessionEvents'

# create table
PiCageSessionEvents_Table = pd.DataFrame(columns=['mouseID', 'tunnelID', 'date', 'numLicks', 'userFunctionName', 'dataTableName', 'dataEntryID'])
PiCageSessionEvents_Table.loc[0] = ['NullMouse','NullTunnel',pd.to_datetime('11/9/01'),0.0,'NullFunction','NullDataTable','NullDataEntry']
PiCageSessionEvents_Table.to_csv(dataFilepath + PiCageSessionEvents_TableName + '.csv',index=False)

def LogNewMouseRFIDConnection(mouseID='no ID', tunnelID='unknow tunnel', date='unknown date', numLicks=0.0,
                              userFunctionName='unspecified', dataTableName=np.nan, dataEntryID=np.nan):
    T = pd.read_csv(dataFilepath + PiCageSessionEvents_TableName + '.csv')
    
    # append entry to table
    newRowIndex = T.shape[0]+1
    T.loc[newRowIndex] = [mouseID, tunnelID, date, numLicks, userFunctionName, dataTableName, dataEntryID]
    T.to_csv(dataFilepath + PiCageSessionEvents_TableName + '.csv', index=False)

    print('-'*80)
    print('last 3 rows of the mice Table:')
    print('-'*25)
    print(T.loc[newRowIndex-3:,:])
    print('-'*80)

    return

# insert a few example entries
LogNewMouseRFIDConnection()
LogNewMouseRFIDConnection(mouseID='IJK_778', tunnelID='#HFsGF', date=pd.to_datetime('21/7/16'), numLicks=5.0, userFunctionName='David_whiskerTracking', dataTableName='David_Whisker1', dataEntryID=3)
LogNewMouseRFIDConnection(mouseID='IJK_778', tunnelID='#HaaGD', date=pd.to_datetime('1/8/16'),  numLicks=2.0, userFunctionName='David_func213',         dataTableName='David_Whisker2', dataEntryID=8)
LogNewMouseRFIDConnection(mouseID='ABG_332', tunnelID='#H56YF', date=pd.to_datetime('1/8/06'),  numLicks=0.0, userFunctionName='Stav_f1',               dataTableName='Adi_Whisker3', dataEntryID=2)
LogNewMouseRFIDConnection(mouseID='ABG_332', tunnelID='#HifGF', date=pd.to_datetime('13/3/13'), numLicks=0.0, userFunctionName='Stav_vocalization',     dataTableName='Amir_Pole_1', dataEntryID=5)
LogNewMouseRFIDConnection(mouseID='ADF_123', tunnelID='#H588F', date=pd.to_datetime('1/8/06'),  numLicks=3.0, userFunctionName='Adi_light_GNG',         dataTableName='Stav_Whisker1', dataEntryID=1)
LogNewMouseRFIDConnection(mouseID='ADH_453', tunnelID='#AvgGF', date=pd.to_datetime('1/8/06'),  numLicks=1.0, userFunctionName='Adi_whisker_GNG',       dataTableName='Ben_Vocalization3', dataEntryID=23)

                          
                          
                          
#%% sandbox



