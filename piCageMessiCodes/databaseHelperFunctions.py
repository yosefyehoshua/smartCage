#%% database helper functions
import pandas as pd
import numpy as np
from PiCage_Database_Interface_Definition import dataFilepath, miceTableName, \
    miceCVTableName, RFID_toMouseMap_TableName, \
    MouseTunnel_to_ProcedureMap_TableName, PiCageSessionEvents_TableName


def LogNewMouse(mouseID=np.nan, ownerName=np.nan,geneticType=np.nan, gender=np.nan, dateOfBirth=np.nan, comment=np.nan):
    """
    Insert entry to mouse table, meaning it logs (adds) in a new
    mouse to 'mice Table' (the basic table).
    :param mouseID: mouse ID, format: ABC_123.
    :param ownerName: owner name (usually the researcher name).
    :param geneticType: the genetic type of the mouse
    :param gender: male/female
    :param dateOfBirth: date Of Birth: DD/MM/YY
    :param comment: related comment on the mouse
    :return: None
    """
    T = pd.read_csv(dataFilepath + miceTableName + '.csv')
    
    # append entry to table
    newRowIndex = T.shape[0]+1
    T.loc[newRowIndex] = [mouseID,ownerName,geneticType,gender,dateOfBirth,comment]
    T.to_csv(dataFilepath + miceTableName + '.csv',index=False)
    return

def LogMajorLifeEvent(mouseID=np.nan, date=np.nan, eventDescription=np.nan, returnLocation=np.nan,
                      weight=np.nan, loggerName=np.nan, dataFolderPath=np.nan, comment=np.nan):
    """
    Insert entry mouse life events AKA 'mice CV Table', meaning
    it logs (adds) new events of a given mouse to 'mice CV Table'.
    :param mouseID: mouse ID, format: ABC_123.
    :param date: events date. format: date = pd.to_datetime('DD/MM/YY')
    :param eventDescription: small description of the event ('Ca imaging experiment', etc.)
    :param returnLocation: return location (old cage?) for the mouse.
    :param weight: weight of the mouse
    :param loggerName: logger name (usually the researcher name).
    :param dataFolderPath: the data folder Path. C:/blabla.
    :param comment: related comment on events.
    :return: None.
    """
    T = pd.read_csv(dataFilepath + miceCVTableName + '.csv')
    
    # append entry to table
    newRowIndex = T.shape[0]+1
    T.loc[newRowIndex] = [mouseID,date,eventDescription,returnLocation,weight,loggerName,dataFolderPath,comment]
    T.to_csv(dataFilepath + miceCVTableName + '.csv',index=False)
    return

def LogNewMouseRFIDConnection(mouseID=np.nan, RFID=np.nan, operation=np.nan, date=np.nan, loggerName=np.nan, comment=np.nan):
    """
    Connect/disconnect mouse with a specific RFID chip.
    :param mouseID:  mouse ID, format: ABC_123.
    :param RFID: RFID serial number
    :param operation: connect/disconnect from RFID // todo ask for 'operation' arg. meaning.
    :param date: connect/disconnect date from RFID. format: date = pd.to_datetime('DD/MM/YY')
    :param loggerName: logger name (usually the researcher name).
    :param comment: related comment on event.
    :return: None.
    """
    T = pd.read_csv(dataFilepath + RFID_toMouseMap_TableName + '.csv')
    
    # append entry to table
    newRowIndex = T.shape[0]+1
    T.loc[newRowIndex] = [mouseID,RFID,operation,date,loggerName,comment]
    T.to_csv(dataFilepath + RFID_toMouseMap_TableName + '.csv', index=False)
    return

def UpdateUserDefinedProcedure(mouseID=np.nan, tunnelID=np.nan, userDefinedProcedureName=np.nan, date=np.nan, loggerName=np.nan, comment=np.nan):
    """
    Update the procedure name that should be run for
    'mouseID' & 'tunnelID' pair. meaning it updates a new procedure for a
    specific tunnel & mouse.
    :param mouseID: mouse ID, format: ABC_123.
    :param tunnelID:  tunnel ID, format: // todo ask for tunnel format.
    :param userDefinedProcedureName: the new procedure name.
    :param date: procedure initialization date. format: date = pd.to_datetime('DD/MM/YY')
    :param loggerName: logger name (usually the researcher name).
    :param comment: related comment on event.
    :return: None.
    """
    T = pd.read_csv(dataFilepath + MouseTunnel_to_ProcedureMap_TableName + '.csv')
    
    # append entry to table
    newRowIndex = T.shape[0]+1
    T.loc[newRowIndex] = [mouseID,tunnelID,userDefinedProcedureName,date,loggerName,comment]
    T.to_csv(dataFilepath + MouseTunnel_to_ProcedureMap_TableName + '.csv', index=False)
    return


def LogNewMouseTunnelEntrySession(mouseID=np.nan, tunnelID=np.nan, date=np.nan, numLicks=0.0, 
                           userProcedureName=np.nan, dataTableName=np.nan, dataEntryID=np.nan):
    """
    Updates the main table.
    :param mouseID: mouse ID, format: ABC_123.
    :param tunnelID:  tunnel ID, format: // todo ask for tunnel format.
    :param date: update date. format: date = pd.to_datetime('DD/MM/YY')
    :param numLicks: water quantity the mouse drank.
    :param userProcedureName: Procedure and user name (e.g. 'Whisker_GoNoGo_Yair', 'LightDetection_David').
    :param dataTableName: the name of the data table which the new session occurred.
    :param dataEntryID: row number of the new session in dataTableName.
    :return: None.
    """
    T = pd.read_csv(dataFilepath + PiCageSessionEvents_TableName + '.csv')
    
    # append entry to table
    newRowIndex = T.shape[0]+1
    T.loc[newRowIndex] = [mouseID, tunnelID, date, numLicks, userProcedureName, dataTableName, dataEntryID]
    T.to_csv(dataFilepath + PiCageSessionEvents_TableName + '.csv', index=False)
    return


def GetMouseID_from_RFID(currRFID):
    """
    Convert RFID serial no. to mouseID.
    :param currRFID: current RFID serial no.
    :return: current mouse ID, that corresponds the the given RFID no.
    """
    T = pd.read_csv(dataFilepath + RFID_toMouseMap_TableName + '.csv')
    
    currMouseID = T.loc[T['RFID'] == currRFID,'mouseID'].values
    return currMouseID[0]

def GetMouseProcedure_from_mID_tID(currMouseID, currTunnelID):
    """
    Gets the procedure name that needed to apply for current mouseID & tunnelID.
    :param currMouseID: current ID, format: ABC_123.
    :param currTunnelID: current tunnel ID.
    :return: relevant 'procedure name'.
    """
    T = pd.read_csv(dataFilepath + MouseTunnel_to_ProcedureMap_TableName + '.csv')
    
    mID_tID_allRows = T.loc[np.logical_and(T['mouseID'] == currMouseID, T['tunnelID'] == currTunnelID)]
    mostRecentDateInd = pd.to_datetime(mID_tID_allRows['date']).argmax()
    currUserProcedureName = mID_tID_allRows.loc[mostRecentDateInd,'userDefinedProcedureName']
    return currUserProcedureName
