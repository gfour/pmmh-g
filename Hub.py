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

import traceback

from MultimodalMiddlewareProtocol.Device import *
from MultimodalMiddlewareProtocol.Server import *
from MultimodalMiddlewareProtocol.Fields import *
from MultimodalMiddlewareProtocol.FieldFactory import *
from MultimodalMiddlewareProtocol.util.Hashes import *

##########################################################
#modified by ND

from MultimodalMiddlewareProtocol.Configuration import *

#modified by ND
##########################################################


class MultimodalHub(MultimodalDevice):
    
    # Creates a new instance of MultimodalHub 
    def __init__(self, name, server):
        MultimodalDevice.__init__(self, name, server, 0xFFFFFFFFL)
        self.processor=None
        self.devices=HashNetworkTable()
        self.producers=HashLong()
        self.consumers= HashLong()
        self.subscriptions= HashLong()
        self.UCIDCounter = 0
        self.sent =0
        self.received=0
        # Component Registration request
        self.eventProcessors[0xF0000000L] = self.registerComponent


        # Forwarder - handle all unknow events
        self.eventProcessors[0x0] = self.forward

        ##########################################################
        #modified by ND 

        # Component Disconnection request
        self.eventProcessors[0xF0000006L] = self.unRegisterComponent
   
        self.configurationManager=xxxx()

        self.configurationIsGet = "no"

        self.GUIConnected = "no"

        firstConfigAdress = '/usr/lib/python2.6/dist-packages/MultimodalMiddlewareProtocol/components/MMHConfiguration4.xml'

        self.getConfigurationFromAdress(firstConfigAdress)

    def getConfigurationFromAdress (self, adress):
        
        liste=[]

        print ('adress:'+adress)
        self.configurationManager.getXMLFromAdress(adress)
        self.configurationIsGet = 'on'
        print 'configuration chargee: '+self.configurationIsGet
        liste=self.configurationManager.configuration

        # display the configuration
        self.stringConfig = self.configurationManager.getStringFromConfigDeviceList(liste)
        print self.stringConfig

    def unRegisterComponent(self, command):

        deviceId = command.mDeviceID.get()
        
        if deviceId == 0xFFFFFFFEL:
                self.GUIConnected = "no"
                print "GUI disconnected!"
                
        UCID = command.mUCID.get()
        self.devices.delete(UCID)
        self.producers.delete(UCID)
        self.consumers.delete(UCID)
        
        if self.GUIConnected == "yes":
            print "component disconnected >> GUI information"
            self.sendConfigurationInformation()
        # a message of subscription update should be sent to components
            
        #modified by ND
        ##########################################################
    
    def registerComponent(self, command):
        #print "registerComponent"
        UCID=0
        record = FieldFactory.fieldFromCodeList("LLLAAs")
        fProduces = record[3]
        fConsumes = record[4]
        try: 
            FieldFactory.readFields(record, command.dataIn)
            deviceId = command.mDeviceID.get()            
            if(command.mUCID.get() == 0):
                self.UCIDCounter +=1
                UCID = self.UCIDCounter # Generates unique UCID for this hub
            else:
                UCID = command.mUCID.get() # Uses previously assigned UCID          
            deviceName = record[5].get()
            #print "Device registration request: %s" % (deviceName)
            
            #//System.out.println("UCID->"+UCID);
            #//System.out.println("Name->"+deviceName);
            
            ##########################################################
            #modified by ND

            # before adding the new component to the hashnetworktable, get the instance to give
            instance = self.devices.getInstanceToSet (deviceId)
            print ('nouvelle instance: '+str(instance))
            self.devices.addOrUpdate(UCID, deviceName, fProduces, fConsumes, command.sender, deviceId, instance);                 

            #modified by ND
            ##########################################################
            
            for x in fProduces.elements:
                self.producers.addOrUpdate(x.get(), UCID); # Add eventID - UCID to producers list
                #//System.out.println(UCID+" produces: "+((MMLongField) fProduces.get(x)).get());
                
            
            for x in fConsumes.elements:
                self.consumers.addOrUpdate(x.get(), UCID); # Add eventID - UCID to consumers list
                #//System.out.println(UCID+" consumes: "+((MMLongField) fConsumes.get(x)).get());

            self.generateRegistrationReply(command, UCID, fConsumes, fProduces);
            self.received+=1
            self.informProcessor(0xF0000000L, UCID);

            ##########################################################
            #modified by ND

            # a new component is registered >> the component list and the configuration are sent to the GUI
            if self.GUIConnected == "yes":
                print "new component >> GUI information"
                self.sendConfigurationInformation()

            if deviceId == 0xFFFFFFFEL:
                self.GUIConnected = "yes"
                print "GUI connected!"
                
            #modified by ND
            ##########################################################

        except:
            traceback.print_exc()
            raise
            
    def informProcessor(self, eventID, UCID):
        if(self.processor!=None):
            self.processor(eventID, UCID)

    ##########################################################
    #modified by ND

    def sendConfigurationInformation(self):
        newInfo = FieldFactory.fieldFromCodeList("LLLS")
        GUIUCID = self.devices.getFirstUCIDFromDeviceID(0xFFFFFFFEL)
        GUINetworkAddress=self.devices.getNetworkAddressFromUCID (GUIUCID)
        newInfo[0].set(GUIUCID)                                                                        # UCID
        newInfo[1].set(0xFFFFFFFEL)                                                                    # DeviceID
        newInfo[2].set(0xFFFFFFFEL)                                                                    # EventId                
        newInfo[3].set(''.join(['    ',self.configurationManager.getStringFromHashNetworkTableAndStringFromXML(self.devices)]))
        self.sent+=1
        print "envoi de la configuration"
        print ("stringConfig: "+self.configurationManager.getStringFromHashNetworkTableAndStringFromXML(self.devices))
        self.server.sendFields(GUINetworkAddress, newInfo)         # inform the GUI about a new connection

    def respondToGUIMessage(self, command):
        command.dataIn.reset()
        fileNameAndNewConfig=command.dataIn.stream
        fileNameAndNewConfigCorrected=fileNameAndNewConfig.split("xxx the message begins here xxx\n")
        splitedFileNameAndNewConfig=fileNameAndNewConfigCorrected[1].split("\nxxx newConfig xxx\n")

        if splitedFileNameAndNewConfig[0]=='':
            # configRequest received > send the informations
            print 'configRequest Received'
            reply = FieldFactory.fieldFromCodeList("LLLS")

            reply[0].set(command.mUCID.get())                                                            # UCID
            reply[1].set(command.mDeviceID.get())                                                        # DeviceID
            reply[2].set(0xFFFFFFFEL)                                                                    # EventId                                                        
            reply[3].set(''.join(['    ',self.configurationManager.getStringFromHashNetworkTableAndStringFromXML(self.devices)]))          
            self.sent+=1
            print "envoi de la configuration"
            print ("stringConfig: "+self.configurationManager.getStringFromHashNetworkTableAndStringFromXML(self.devices))
            command.sender.server.sendFields(command.sender, reply)         # repond a Configuration request
        else:
            # the message contains a new configuration
            fileName=splitedFileNameAndNewConfig[0]+'.xml'
            #fileName=fileName.replace('\n','')
            f = open(str(fileName),'w')
            f.write(splitedFileNameAndNewConfig[1])
            f.close()
            adress="/usr/lib/python2.6/dist-packages/MultimodalMiddlewareProtocol/components/"+str(fileName)
            #print ('adress of the new configuration: '+adress)
            self.getConfigurationFromAdress(adress)
            

    #modified by ND
    ##########################################################
        
    def generateRegistrationReply(self, command, UCID, fConsumes, fProduces):
        reply = FieldFactory.fieldFromCodeList("LLLLAAL")

        reply[0].set(UCID)                                             # UCID
        reply[1].set(command.mDeviceID.get())                          # DeviceID
        reply[2].set(0xF0000001L)                                      # EventId
        reply[3].set(UCID)                                             # UCID
        # Calculates the Suppliers and Consumers list
        reply[4]=self.calculateSuppliers(UCID, fConsumes)              # Suppliers
        reply[5]=self.calculateClients(UCID, fProduces)                # Clients
        reply[6].set(9000)                                             # Time to live
        self.sent+=1
        #print reply
        command.sender.server.sendFields(command.sender, reply)         # Answers the Registration request
    
    def calculateClients(self, UCID, fProduces):
        return self.calculateMatch(UCID, fProduces, self.consumers)

    
    def calculateSuppliers(self, UCID, fConsumes):
        return self.calculateMatch(UCID, fConsumes, self.producers)

    
    def calculateMatch(self, UCID, my, others):
        lMy = Fields.ArrayField()
        vMy = []
        eventId=0
        
        for x in my.elements:
            eventId = x.get()
           
            otherList=others.get(eventId)
            
            if(otherList<>None):
                if(not (len(otherList)==1 and otherList[0]==UCID)):
                    vMy.append(eventId)

        lMy.copyLongVector(vMy)
        return lMy

    
    def setProcessor(self, processor):
        self.processor = processor

    
    def forward(self, command):
        eventID = command.mEventID.get()

        ##########################################################
        #modified by ND

        # recuperation of source deviceID
        sourceDeviceID = command.mDeviceID.get()
        # recuperation of source instance
        sourceInstance = self.devices.get(command.mUCID.get()).instance
        # recuperation of the UCID list wich consume the eventID
        destinationUCIDList = self.consumers.get(eventID)
        self.received+=1
        # if the GUI send a message (eventID 0xFFFFFFFDL)
        if sourceDeviceID == 0xFFFFFFFEL and command.mEventID.get() == 0xFFFFFFFDL:
            self.respondToGUIMessage(command)
        # else normal behaviour
        elif(destinationUCIDList!=None):
            # for each consumer,
            for currentDestinationUCID in destinationUCIDList:
                # recuperation of the  DeviceID and instance
                currentDestinationDeviceID = self.devices.get(currentDestinationUCID).deviceID
                currentDestinationInstance = self.devices.get(currentDestinationUCID).instance
                # test if the producer can send eventID to consumer
                if self.configurationIsGet == 'no' or self.configurationManager.setAuthorization (eventID,sourceDeviceID,sourceInstance,currentDestinationDeviceID,currentDestinationInstance):               
                    sendto = self.devices.get(currentDestinationUCID).netAddress
                    try:
                        #//System.out.println("Forward - sending");
                        command.dataIn.reset()
                        command.sender.server.send(sendto, command.dataIn.stream)
                        self.sent+=1
                    except:
                        pass

        #modified by ND
        ##########################################################

        self.informProcessor(eventID, command.mUCID.get())      
