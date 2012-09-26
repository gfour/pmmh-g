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
import socket
import thread
import traceback

from MultimodalMiddlewareProtocol.Server import *
from MultimodalMiddlewareProtocol.Consts import *
from MultimodalMiddlewareProtocol.Fields import *


class Datagram:
    def __init__(self, data):
        self.data = data
        self.address = None
    
    def setAddress(self, address):
        self.address = address
    

class UDPServer (IServer):

    # Creates a new instance of UDPServer 
    def __init__(self, serverIP, portNumber):
        self.receiver = None
        self.server = None
        self.portNumber = "6000"
        self.serverIp = ""
        self.nReceived = 0
        self.nSent = 0
        self.receiving = False
        self.receivingThread = None
        self.multimodalHubAddress = ""
        self.DATAGRAM_SIZE = 10240
        self.errorHandler = None
        self.serverIp = serverIP;
        self.portNumber = portNumber

    def getMultimodalHubAddress(self):
        return self.multimodalHubAddress

    def setMultimodalHubAddress(self, address):
        self.multimodalHubAddress = address

    def sendFields(self, destination, fields):
        data = FieldFactory.writeFields(fields)
        self.send(destination, data)

    def send(self, destination, data):
        if self.receiving: 
            d = Datagram(data)
            try:
                if destination != None:
                    d.setAddress(destination.address)                    
                else:
                    d.setAddress(self.getMultimodalHubAddress())
                
                #print "Data: %s" % d.data
                #print d.data
                #print type(d.data)
                #print d.address

                self.server.sendto(d.data, 0, d.address)
                self.nSent+=1
            except:
                if self.errorHandler <> None:
                    errorHandler.raiseException(sys.exc_info()[0], "UDPServer::send error sending package", true);
                else:
                    traceback.print_exc()
                    self.stop()
                    raise
                   
            finally:
                d = None


    def getProtocolId(self):
        return Consts.PROT_UDP


    def getProtocolName(self):
        return "UDP"

    def getServerURL(self):
        try:
            return "datagram://" + self.server.getLocalAddress() + ":" + self.server.getLocalPort()
        except:
            return "Error retrieving Server URL"+sys.exc_info()[0]


    def getServerAddress(self):
        try:
            return NetworkAddress(0L, self, self.getServerURL())
        except:
            if self.errorHandler <> None:
                self.errorHandler.raiseException(sys.exc_info()[0], "UDPServer::getServerAddress", false)
            return None


    def start(self):
        self.activate()


    def stop(self):
        self.log("UDPServer::Stop")
        self.receiving = False
        self.receivingThread = None

        if self.server <> None:
            try:
                self.log("UDPServer::Stop Closing connection")
                self.server.close()
                self.server = None
            except:
                if self.errorHandler <> None:
                    self.errorHandler.raiseException(sys.exc_info()[0], "UDPServer::stop finalization error", false)
                else:
                    raise

    def setReceiver(self, receiver):
        self.receiver = receiver

    def activate(self):
        try:
            if self.server <> None:
                self.stop()

            self.nSent = 0
            self.nReceived = 0
            
            try:
                self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
                self.server.bind( (self.serverIp, self.portNumber) )
                #if (self.server.getMaximumLength() < this.DATAGRAM_SIZE)
                #    this.DATAGRAM_SIZE = server.getMaximumLength();
                self.receiving = True;
            except:
                self.log("UDPServer::activate -> Error creating server: %s ~ %d : %s" % (self.serverIp,self.portNumber,sys.exc_info()[0]))
                self.stop()
                if self.errorHandler <> None:
                    self.errorHandler.raiseException(sys.exc_info()[0], "UDPServer::activate error creating server", true)
                
                raise           
            self.receivingThread = thread.start_new_thread(self.run, () )
        except:
            if self.errorHandler <> None:
                self.errorHandler.raiseException(sys.exc_info()[0], "UDPServer::activate Activation error", true)
            else:
                raise


    def log(self, m):
        if self.receiver <> None:
            self.receiver.log(m)
        else:
            print m
            

    def run(self):
        counter = 0
        received = 0
        buffer = ""
        addrFrom = (),
        self.receiving = True
        self.log("Receiving")
        while (self.receiving):
            try:

                (buffer, addrFrom) = self.server.recvfrom(self.DATAGRAM_SIZE)

                received = len(buffer)
                self.nReceived+=1
                if (self.receiver <> None):
                    self.receiver.receive(NetworkAddress(0, self, addrFrom), buffer)

            except:
                counter+=1
                self.log("UdpServer::Run: Rec: %d DS: %d  Counter: %d Ex: %s" % (received,  self.DATAGRAM_SIZE, counter, sys.exc_info()))
                traceback.print_exc()
                if self.errorHandler <> None:
                    self.errorHandler.raiseException(sys.exc_info()[0], "UDPServer::run " + received + "/" + self.DATAGRAM_SIZE + " [" + counter + "] ", true)
                else:
                    raise    

        self.receiving = False
        self.stop()

