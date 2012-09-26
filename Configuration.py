
from string import rjust
from MultimodalMiddlewareProtocol.util.Hashes import *
from MultimodalMiddlewareProtocol.Server import *

try:
    from xml.dom.minidom import Document, parse, parseString
except ImportError:
    raise ImportError, "The xml module is required!"

class configEvent:
    #class used to extract the configuration from the xml file
    eid = None
    deviceID = None
    instance = 0
'''
    def eventCopy (self, configEventToCopy):
        try:
            self.eid=configEventToCopy.eid
            self.deviceID=configEventToCopy.deviceID
            self.instance=configEventToCopy.instance
        except:
            print "erreur dans eventCopy!"
'''

class configDevice:
    #class used to extract the configuration from the xml file
    did = None
    instance = 0
    # the lists content the consumed en produced eventID
    # each element of the lists is a configEvent
    listOfAuthorizedProducedEvents = []
    listOfAuthorizedConsumedEvents = []
'''
    def deviceCopy(self, configDeviceToCopy):
        try:
            self.did=configDeviceToCopy.did
            self.instance=configDeviceToCopy.instance
            self.listOfAuthorizedProducedEvents=deepcopy(configDeviceToCopy.listOfAuthorizedProducedEvents) 
            self.listOfAuthorizedConsumedEvents=deepcopy(configDeviceToCopy.listOfAuthorizedConsumedEvents)
        except:
            print "erreur dans deviceCopy!"
'''

class TransformXMLToList:
    adressOfTheXML = None
    currentNode = None
    configDeviceList = []
    currentStringConfig=''
    unknowDevices = 'on'
    
    def getText(self, node):
           return node.childnodes[0].nodeValue

    def getXML(self):
        
        # recuperation of the xml file in a format handable by the xml.dom.minidom library
        self.configDeviceList=[]
        self.doc = parse (self.adressOfTheXML)
        self.unknowDevices = str(self.getRootElement().getElementsByTagName("unknowdevices")[0].attributes["default"].value)
        # extraction of the configDevice from the configuration
        for XMLdevice in self.getRootElement().getElementsByTagName("device"):
           currentConfigDevice = configDevice ()
                   # for each configDevice,
                   # recuperation of the id
           currentConfigDevice.did=XMLdevice.attributes["id"].value
                   # recuperation of the instance
           currentConfigDevice.instance=XMLdevice.attributes["instance"].value
                   # recuperation of the list of prdouced events
           XMLListOfAuthorizedProducedEvents = XMLdevice.getElementsByTagName("produces")[0].getElementsByTagName("event")
           currentConfigDevice.listOfAuthorizedProducedEvents = []
                       # in this list, for each event,
           for XMLProducedEvent in XMLListOfAuthorizedProducedEvents:
               currentConfigProducedEvent = configEvent ()
                       # recuperation of the id
               currentConfigProducedEvent.eid=XMLProducedEvent.attributes["id"].value
                       # recuperation of the deviceID
               currentConfigProducedEvent.deviceID=XMLProducedEvent.attributes["deviceID"].value
                       # recuperation of the instance
               currentConfigProducedEvent.instance=XMLProducedEvent.attributes["instance"].value
                       # adding the event to the list
               currentConfigDevice.listOfAuthorizedProducedEvents.append(currentConfigProducedEvent)
                # recuperation of the list of produced events
           XMLListOfAuthorizedConsumedEvents = XMLdevice.getElementsByTagName("consumes")[0].getElementsByTagName("event")
           currentConfigDevice.listOfAuthorizedConsumedEvents=[]
                       # in this list, for each event,
           for XMLConsumedEvent in XMLListOfAuthorizedConsumedEvents:
               currentConfigConsumedEvent = configEvent ()
                       # recuperation of the id
               currentConfigConsumedEvent.eid=XMLConsumedEvent.attributes["id"].value
                       # recuperation of the device
               currentConfigConsumedEvent.deviceID=XMLConsumedEvent.attributes["deviceID"].value
                       # recuperation of the instance
               currentConfigConsumedEvent.instance=XMLConsumedEvent.attributes["instance"].value      
                       # adding the event to the list
               currentConfigDevice.listOfAuthorizedConsumedEvents.append(currentConfigConsumedEvent)
                # et adding the device to the list
           self.configDeviceList.append(currentConfigDevice)
        self.currentStringConfig = str(self.doc.toprettyxml (indent=" "))
        self.doc.unlink()
        self.currentNode=None
        # return the list
        return self.configDeviceList
    
    def getRootElement (self):

        if self.currentNode == None:
            self.currentNode = self.doc.documentElement
        return self.currentNode
        
class xxxx:
    myTransformXMLToList = TransformXMLToList ()
    configuration = []
    unknowDevices = 'on'

    def getStringFromConfigDeviceList (self, liste):
        # method that returns astring from the configuration list
        stringList = 'configuration chargee: '
        stringList +='\n   unknowdevices: '+self.unknowDevices
        for device in liste:
            stringList+="\n   device id: "
            stringList+=rjust(str(device.did), 3)
            stringList+=" instance "
            stringList+=rjust(str(device.instance), 3)
            stringList+="\n        produces:"
            for producedEvent in device.listOfAuthorizedProducedEvents:
                stringList+="\n"
                stringList+="               eventID "
                stringList+=rjust(str(producedEvent.eid), 3)
                stringList+=rjust(" to deviceID ", 15)
                stringList+=rjust(str(producedEvent.deviceID), 3)
                stringList+=" instance "
                stringList+=rjust(str(producedEvent.instance), 3)               
            stringList+="\n        consumes:"                
            for consumedEvent in device.listOfAuthorizedConsumedEvents:
                stringList+="\n"
                stringList+="               eventID "
                stringList+=rjust(str(consumedEvent.eid), 3)
                stringList+=" from deviceID "
                stringList+=rjust(str(consumedEvent.deviceID), 3)
                stringList+=" instance "
                stringList+=rjust(str(consumedEvent.instance), 3) 
        return stringList    

    def getXMLFromAdress(self, adress):
        self.myTransformXMLToList.adressOfTheXML = adress
        self.configuration = self.myTransformXMLToList.getXML()
        self.unknowDevices = self.myTransformXMLToList.unknowDevices

    def getStringFromHashNetworkTableAndStringFromXML(self,devices):
        stringConfig = self.myTransformXMLToList.currentStringConfig
        docu = Document()
        xmlConnectedDevicesList = docu.createElement("connectedDevicesList")
        docu.appendChild(xmlConnectedDevicesList)
        for currentDevice in devices.hash.values():
            if currentDevice.deviceID!=0xFFFFFFFEL: # to not add GUI to sent devices list
                xmlDevice=docu.createElement("device")
                xmlDevice.setAttribute("name", str(currentDevice.name))
                xmlDevice.setAttribute("deviceID", str(currentDevice.deviceID))
                xmlDevice.setAttribute("instance", str(currentDevice.instance))
                xmlDevice.setAttribute("UCID", str(currentDevice.UCID))          
                xmlProduces=docu.createElement("produces")
                print (str(currentDevice.produces))
                for currentProducedEventID in currentDevice.produces.getContents():
                    if currentProducedEventID!=0xF0000003L: # to not add metatdata response to produced eventID list
                        xmlEventID=docu.createElement("eventID")
                        xmlEventID.setAttribute("id", str(currentProducedEventID))               
                        xmlProduces.appendChild(xmlEventID)
                xmlDevice.appendChild(xmlProduces)
                xmlConsumes=docu.createElement("consumes")
                for currentConsumedEventID in currentDevice.consumes.getContents():
                    if currentConsumedEventID!=0xF0000002L: # to not add metatdata request to produced eventID list
                        xmlEventID=docu.createElement("eventID")
                        xmlEventID.setAttribute("id", str(currentConsumedEventID))               
                        xmlConsumes.appendChild(xmlEventID)
                xmlDevice.appendChild(xmlConsumes)          
                xmlConnectedDevicesList.appendChild(xmlDevice)
        stringConnectedDevicesList = str(xmlConnectedDevicesList.toprettyxml (indent=" "))
        stringTotalConfig =stringConfig+"\nxxx connectedDevicesList xxx\n"+stringConnectedDevicesList

        return stringTotalConfig
       
    def setAuthorizationForSourceToSendEventToDestination(self,eventID,sourceDeviceID,sourceInstance,currentDestinationDeviceID,currentDestinationInstance):
        deviceConfigurationIsTested = False
        # by default, the authorization is not given
        authorizationForSourceToSendEventToDestination = False
        # if unknowndevice is on, then the authorization is given by default
        # unless if the device is in the list and can not send de evnt to the destination
        if self.unknowDevices == 'on':
            print 'unknowdevice est on! (1)'
            authorizationForSourceToSendEventToDestination = True        
        print 'TEST de la source'
        for deviceInConfiguration in self.configuration:
            print (str(deviceInConfiguration.did)+' ?=? '+str(sourceDeviceID)+' et '+str(deviceInConfiguration.instance)+' ?=? '+str(sourceInstance))
            if int(deviceInConfiguration.did) == sourceDeviceID:
                if int(deviceInConfiguration.instance) == sourceInstance:
                    print('la source est dans la liste...')
                    # deviceConfigurationIsTested is used to get out of the for if the device is found in the list and tested
                    deviceConfigurationIsTested = True
                    for eventConfiguration in deviceInConfiguration.listOfAuthorizedProducedEvents:
                        print (str(eventConfiguration.eid)+' ?=? '+str(eventID)+' et '+str(eventConfiguration.deviceID)+' ?=? '+str(currentDestinationDeviceID)+' ou all et '+str(eventConfiguration.instance)+' ?=? '+str(currentDestinationInstance)+' ou all')
                        if int(eventConfiguration.eid) == eventID:
                            if str(eventConfiguration.deviceID) == str(currentDestinationDeviceID) or str(eventConfiguration.deviceID) == 'all' :
                                if str(eventConfiguration.instance) == str(currentDestinationInstance) or str(eventConfiguration.instance) == 'all':
                                    print ('et peut envoyer l event a la destination')
                                    authorizationForSourceToSendEventToDestination = True
                                    break
                                else:
                                    # the device is in the list, can send the event to the destination but not to this instance
                                    authorizationForSourceToSendEventToDestination = False
                            else:
                                # the device is in the list, can send the event but not to this destination
                                authorizationForSourceToSendEventToDestination = False
                        else:
                            # the device is in the list but can not send this event
                            authorizationForSourceToSendEventToDestination = False
            # if self.unknowDevices == 'on', it is necessary to parse all the configuration
            # to be sure that the component is not in the configuration before giving authorisation
            if self.unknowDevices == 'off' and(authorizationForSourceToSendEventToDestination == True or deviceConfigurationIsTested == True):
                break      
        return authorizationForSourceToSendEventToDestination
            
    def setAuthorizationForDestinationToReceiveEventFromSource(self, eventID,sourceDeviceID,sourceInstance,currentDestinationDeviceID,currentDestinationInstance):
        deviceConfigurationIsTested = False
        # by default, the authorization is not given
        authorizationForDestinationToReceiveEventFromSource = False
        # if unknowndevice is on, then the authorization is given by default
        # unless if the device is in the list and can not send de evnt to the destination
        if self.unknowDevices == 'on':
            print 'unknowdevices est on! (2)'
            authorizationForDestinationToReceiveEventFromSource = True  
        print 'TEST de la destination'
        for deviceInConfiguration in self.configuration:
            print (str(deviceInConfiguration.did)+' ?=? '+str(currentDestinationDeviceID)+' et '+str(deviceInConfiguration.instance)+' ?=? '+str(currentDestinationInstance))
            if int(deviceInConfiguration.did) == currentDestinationDeviceID:
                if int(deviceInConfiguration.instance) == currentDestinationInstance:                
                    # deviceConfigurationIsTested is used to get out of the for if the device is found in the list and tested
                    deviceConfigurationIsTested = True
                    print('la destination est dans la liste...')
                    for eventConfiguration in deviceInConfiguration.listOfAuthorizedConsumedEvents:
                        print (str(eventConfiguration.eid)+' ?=? '+str(eventID)+' et '+str(eventConfiguration.deviceID)+' ?=? '+str(sourceDeviceID)+' ou all et '+str(eventConfiguration.instance)+' ?=? '+str(sourceInstance)+' ou all')
                        if int(eventConfiguration.eid) == eventID:
                            if str(eventConfiguration.deviceID) == str(sourceDeviceID) or str(eventConfiguration.deviceID) == 'all':
                                if str(eventConfiguration.instance) == str(sourceInstance) or str(eventConfiguration.instance) == 'all':
                                    print ('et peut recevoir l event de la source')
                                    authorizationForDestinationToReceiveEventFromSource = True
                                    break
                                else:
                                    # the device is in the list, can send the event to the destination but not to this instance
                                    authorizationForDestinationToReceiveEventFromSource = False
                            else:
                                # the device is in the list, can send the event but not to this destination
                                authorizationForDestinationToReceiveEventFromSource = False 
                        else:
                            # the device is in the list but can not send this event
                            authorizationForDestinationToReceiveEventFromSource = False                        
            # if self.unknowDevices == 'on', it is necessary to parse all the configuration
            # to be sure that the component is not in the configuration before giving authorisation
            if self.unknowDevices == 'off' and(authorizationForDestinationToReceiveEventFromSource == True or deviceConfigurationIsTested == True):
                break
        return authorizationForDestinationToReceiveEventFromSource

    def setAuthorization (self, eventID,sourceDeviceID,sourceInstance,currentDestinationDeviceID,currentDestinationInstance): 
        # if this is a metadata request or a metadata response, the authorization is given
        if eventID == 0xF0000002L:
            print "autorisation pour demande ESF"
            return True
        elif eventID == 0xF0000003L:
            print "autorisation pour reponse ESF"
            return True
        else:
            if self.setAuthorizationForSourceToSendEventToDestination(eventID,sourceDeviceID,sourceInstance,currentDestinationDeviceID,currentDestinationInstance):
                if self.setAuthorizationForDestinationToReceiveEventFromSource(eventID,sourceDeviceID,sourceInstance,currentDestinationDeviceID,currentDestinationInstance):
                    return True
            else:
                return False 
