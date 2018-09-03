
class Tunnel:
    stimulusDevicesList = []
    responseDevicesList = []
    tasksList = []
    tunnelName = ''


    def __init__(self, tunnelName, tasksList):
        self.tunnelName = tunnelName
        self.tasksList = tasksList

    def addDeviceTolist(self, list, device):
        if device not in list:
            list.append(device)

    def getDevices(self):
        return self.stimulusDevicesList, self.responseDevicesList

