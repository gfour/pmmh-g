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
import sys
import traceback

from MultimodalMiddlewareProtocol import Server, Fields, FieldFactory
from MultimodalMiddlewareProtocol.util.Hashes import HashLong
from MultimodalMiddlewareProtocol.util.Streamers import Reader, Writer



class MultimodalDevice (Server.IClient):
    MMDevice_Init = 0
    MMDevice_Registering = 1
    MMDevice_Registered = 2
    MMDevice_Disconnecting = 3
    MMDevice_Disconnected = 4
    
    
    # Creates a new instance of MultimodalDevice
    def __init__(self, name, server, deviceID):
        self.name = name
        self.produces = []
        self.consumes = []
        self.clients = HashLong()
        self.suppliers = HashLong()
        self.server = server
        self.deviceID= deviceID
        self.eventProcessors = {}
        server.setReceiver(self)
        self.state = 0
        self.UCID = 0

        
        #self.eventProcessors.add()
        self.eventProcessors[0xF0000001L] = self.confirmSubscription
           
    def log(self, text):
        print "LOG: %s" % (text)
    
    def register(self):
        self.state = MultimodalDevice.MMDevice_Registering
        
        #MMArrayField fProduces, fConsumes;
        record = FieldFactory.fieldFromCodeList("LLLAAs")
        record[0].set(self.UCID)
        record[1].set(self.deviceID)
        record[2].set(0xF0000000L) # EventID
        record[3].copyLongVector(self.produces)
        record[4].copyLongVector(self.consumes)
        record[5].set(self.name) # Device Name
        self.server.sendFields(None, record)
        
    ##########################################################
    #modified by ND  

    def disconnect(self):
        self.state = MultimodalDevice.MMDevice_Disconnecting
        
        record = FieldFactory.fieldFromCodeList("LLLI")
        record[0].set(self.UCID)
        record[1].set(self.deviceID)
        record[2].set(0xF0000006L) # EventID for disconnection
        record[3].set(0)
        self.server.sendFields(None, record)

    #modified by ND
    ##########################################################    
    
    def confirmSubscription(self, command):        
        record = FieldFactory.fieldFromCodeList("LLLLAAL")
        fProduces = record[4]
        fConsumes = record[5]
        try: 
            FieldFactory.readFields(record, command.dataIn)
            self.deviceId = command.mDeviceID.get()
            self.UCID = record[3].get()
            
            for x in fProduces.elements:
                self.clients.addOrUpdate(x, self.UCID) # Add eventID - UCID to producers list

            for x in fConsumes.elements:
                self.suppliers.addOrUpdate(x, self.UCID) # Add eventID - UCID to consumers list

            self.state = MultimodalDevice.MMDevice_Registered
        except Exception:
            raise
        finally:
            record = None
            fProduces = None
            fConsumes = None
    
    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name
   
    
    def receive(self, sender, data):
        dataIn = Reader(data[:]) # Copies data to dataIn
        mUCID = Fields.LongField()
        mDeviceID= Fields.LongField()
        mEventID= Fields.LongField()
        try:
            if(data==None):
                self.log("Data received as null")
                return

            if(sender==None):
                self.log("Sender received as null")
                return

            if(len(data)<9):
                self.log("Datagram with incorrect size received: %d" % (len(data)))
                return

            mUCID.read(dataIn)
            mDeviceID.read(dataIn)
            mEventID.read(dataIn)
            
            #print "UCID: %s DeviceID: %s EventID: %s" % (mUCID.get(), mDeviceID.get(), mEventID.get())
            
            
            dataIn.reset(); # As 3 fields were read... rewind the stream
            try:
                #print self.eventProcessors
                #print mEventID.get()
                if self.eventProcessors.has_key(mEventID.get()):
                    command = self.eventProcessors[mEventID.get()]
                    command(Server.CommandHeader(mUCID, mDeviceID, mEventID, sender, dataIn))
                else: # If a standard command processor is not available, try to find a forwarder
                    forwarder = self.eventProcessors[0]
                    forwarder(Server.CommandHeader(mUCID, mDeviceID, mEventID, sender, dataIn))
            except: 
                    traceback.print_exc()
                    print("Unhandled EventID: %s received from UCID: %s" % (mEventID.get(), mUCID.get()))
            
        except:
            self.log(sys.exc_info()[0])
            raise
        
        finally:
            dataIn=None
            mUCID=None
            mDeviceID=None
            mEventID=None
            
