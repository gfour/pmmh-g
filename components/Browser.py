import sys

from MultimodalMiddlewareProtocol import Hub, Server, Fields, Consts
from MultimodalMiddlewareProtocol.util.Hashes import HashLong
from MultimodalMiddlewareProtocol.servers.UDPServer import UDPServer


class MultimodalBrowser:
    
    def __init__(self):
        self.server = None
        self.hub = None
        self.serverIp = ""
        self.nReceived = 0
        self.nSent = 0
        self.updateCounters = True
        self.updateLogging = True
        self.errorHandler = None

    def connect(self):
        try:
            #self.errorHandler = new AlertExceptionHandler(this);
            self.server = UDPServer("", 6000)
            #//server = new TCPServer("", 6000)
            #//server = new SuperServer()
            self.server.errorHandler = self.errorHandler
            self.server.start()
            self.hub = Hub.MultimodalHub("hub", self.server)
            self.hub.errorHandler = self.errorHandler
            #self.hub.textOutput = log

            self.hub.setProcessor(self.process)
            self.hub.log("Connect #0")
        except:
            #if self.hub <> None:
            #    self.hub.log(sys.exc_inf()[0])
            if (self.errorHandler <> None):
                self.errorHandler.raiseException(sys.exc_inf()[0], "Error creating server", true)
            else:
                raise

    
    
    def process(self, eventId, UCID):
        try:
            self.hub.log("Processing Event: %s Source: %s" % (eventId, UCID))

            if eventId == 0xF0000000L:
                self.updateComponentList()

            if self.updateCounters == True:
                print "Received: %d Sent: %d" % (self.hub.received, self.hub.sent)


        except:
            traceback.print_exc()
            self.hub.log(sys.exc_info([0]))
            if (self.errorHandler <> None):
                self.errorHandler.raiseException(sys.exc_inf()[0], "Error processing message EventID : %s UCID: %s" % (eventId, UCID), false)
            else:
                raise    


    def updateComponentList(self):
        devices = self.hub.devices.getKeys()
        
        print "####################################################"
        for d in devices:
            print "Device: %s" % self.hub.devices.get(d).name
        print "####################################################"


if __name__ == '__main__':
    browser = MultimodalBrowser()
    browser.connect()
    
    raw_input()


