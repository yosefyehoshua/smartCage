####################################################
###### Train mice to get water in the tunnels ######
####################################################

import InitializationFunctions
import pandas as pd
import databaseHelperFunctions
import UtilityFunctions

def trainMice_waterInTunnels(tunnelID,currRFID):
    
    # find tunnel hardware parameters
    tunnelParams = InitializationFunctions.findBasicParameters(tunnelID)
    currDateTime = pd.to_datetime('now')
    currMouseID = databaseHelperFunctions.GetMouseID_from_RFID(currRFID)
    
    # extract mouse data from all tunnels
    
    
    # logic
    miceConditionsTable = pd.read_csv(dataFilepath + 'miceConditions' + '.csv')
    ind = miceConditionsTable.ix[miceConditionsTable['MouseID']==currMouseID]
    mouseCond = miceConditionsTable['water restriction'][ind]
    if mouseCond=='y':  
    
    # decision: give water or not
    if decision:
        # give water
        WATER_PULSE_DURATION = 0.085 #sec
        UtilityFunctions.utility_GiveWater(WATER_PULSE_DURATION)