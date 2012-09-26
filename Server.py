#    MultimodalMiddlewareProtocol
#    Copyright (C) 2008 Nilo Menezes - Multitel ASBL
#
#    This library is free software; you can redistribute it and/or
#    modify it under the terms of the GNU Lesser General Public
#    License as published by the Free Software Foundation; either
#    version 2.1 of the License, or (at your option) any later version.
#
#    This library is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with this library; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

class IServer:
    def send(self, destination, fields):
        pass

    def getProtocolId(self):
        pass

    def getProtocolName(self):
        pass

    def getServerAddress(self):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def setReceiver(self, receiver):
        pass
    
    
class IClient:
    def receive(self, sender, data):
        pass
    def log(self, text):
        pass
    
    
class NetworkAddress:    
    def __init__ (self, ucid, server, address):
        self.ucid = ucid
        self.server = server
        self.address = address
 
class CommandHeader:
    def __init__(self, mUCID, mDeviceID, mEventID, sender, dataIn):
        self.mUCID = mUCID
        self.mDeviceID = mDeviceID
        self.mEventID = mEventID
        self.sender = sender
        self.dataIn = dataIn

  
class NetworkDevice:
    def __init__(self, name, produces, consumes, netAddress, UCID, deviceID, instance):
        self.name = name
        self.produces = produces
        self.consumes = consumes
        self.netAddress = netAddress
        
        self.UCID = UCID
        self.deviceID = deviceID
        self.instance = instance

