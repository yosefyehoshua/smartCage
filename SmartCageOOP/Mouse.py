def getTask(tunnel):



class Mouse:

    mouseRFID = ''
    tunnelsList = []

    def __init__(self, mouseRFID):
        self.mouseRFID = mouseRFID

    def enterTunnel(self, tunnel):
        task = getTask(tunnel)

    def addTunnelsToList(self, tunnel):
        if tunnel not in self.tunnelsList:
            self.tunnelsList.append(tunnel)

