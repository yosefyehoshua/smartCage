#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 16:31:28 2017

@author: yair_deitcher
"""
import pandas as pd
tunnelID='#H588F'

def getMouseFromTable(rfid):
    table = pd.read_csv('rfid_to_mouseID_Table.csv')
    table['date'] = pd.to_datetime(table['date'])  
    rowsRfid=table.loc[table['RFID'] == rfid]
    rightRow=rowsRfid.loc[rowsRfid['date']==rowsRfid['date'].max()]
    #assert(rightRow['operation'].values[0]=='Disconnect')
    mouseID=rightRow['mouseID'].values[0]
    return mouseID


def getFunctionNameFromTable():
    global mouseID
    global tunnelID
    table = pd.read_csv('MouseAndTunnel_to_ProcedureMap_Table.csv')
    functionName=table.loc[(table['mouseID'] == mouseID) & (table['tunnelID']==tunnelID),'UserDefinedProcedureName'].values[0]
    return functionName


mouseID=getMouseFromTable('#H56YF')
functionName=getFunctionNameFromTable()