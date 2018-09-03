"""
this script creates new empty data tables.
when initializing a new cage, run this script to create this empty data tables.
"""

import pandas as pd

# output path for the data table file.
dataFilepath = 'C:/Current Projects/PiCage/Code/emulator/'

# creates a 'mice Table' for basic data storage of a given mice.
miceTableName = 'miceTable'
miceTable = pd.DataFrame(columns=['mouseID','owner','geneticType','gender','dateOfBirth','comment'])
miceTable.to_csv(dataFilepath + miceTableName + '.csv', index=False)
del miceTable

# creates a 'CV table' for the mice to list all operation, procedures, cage tranfers, current location, etc.
miceCVTableName = 'miceCV_Table'
miceCVTable = pd.DataFrame(columns=['mouseID','date','eventDescription','returnLocation','weight','loggerName','dataFolderPath','comment'])
miceCVTable.to_csv(dataFilepath + miceCVTableName + '.csv', index=False)
del miceCVTable

# creates a 'RFID to mouseID' table, to appoint an RFID to a mice (the RFID
# chips are recycled into the system)
RFID_toMouseMap_TableName = 'RFID_to_mouseID_Table'
RFID_to_mouseID_Table = pd.DataFrame(columns=['mouseID','RFID','operation','date','loggerName','comment'])
RFID_to_mouseID_Table.to_csv(dataFilepath + RFID_toMouseMap_TableName + '.csv', index=False)
del RFID_to_mouseID_Table

# creates a 'mouse to tunnel to procedure mapping' table.
MouseTunnel_to_ProcedureMap_TableName = 'MouseAndTunnel_to_ProcedureMap_Table'
MouseAndTunnel_to_ProcedureMap_Table = pd.DataFrame(columns=['mouseID', 'tunnelID', 'userDefinedProcedureName','date','loggerName','comment'])
MouseAndTunnel_to_ProcedureMap_Table.to_csv(dataFilepath + MouseTunnel_to_ProcedureMap_TableName + '.csv', index=False)
del MouseAndTunnel_to_ProcedureMap_Table

# creates a general table for all 'session events' in the cage, containing
# refrences to the table above with a relevant line.
PiCageSessionEvents_TableName = 'PiCageSessionEvents'
PiCageSessionEvents_Table = pd.DataFrame(columns=['mouseID', 'tunnelID', 'date', 'numLicks', 'userProcedureName', 'dataTableName', 'dataEntryID'])
PiCageSessionEvents_Table.to_csv(dataFilepath + PiCageSessionEvents_TableName + '.csv', index=False)
del PiCageSessionEvents_Table

