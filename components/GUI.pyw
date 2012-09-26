try:
    from MultimodalMiddlewareProtocol.Device import MultimodalDevice
    from MultimodalMiddlewareProtocol import Fields
    from MultimodalMiddlewareProtocol import FieldFactory
    from MultimodalMiddlewareProtocol.servers.UDPServer import UDPServer
    from MultimodalMiddlewareProtocol.Configuration import *
except ImportError:
    raise ImportError, "The MMP module is required!"

try:
    from xml.dom.minidom import Document, parse, parseString
except ImportError:
    raise ImportError, "The xml module is required!"

try:
    import wx
    import wx.grid as gridlib
except ImportError:
    raise ImportError, "The wxPython module is required!"

import time



class GUIWindow (wx.Frame):


    
    configuration = ""
    
    def __init__(self, parent, id, titre):
        
        wx.Frame.__init__(self, parent, id, titre)

        self.myTranslator = None
        self.displayedColHeads=[]
        self.displayedRowHeads=[]
        self.colNumber=len(self.displayedColHeads)
        self.rowNumber=len(self.displayedRowHeads)
        self.panel = wx.Panel(self)
        self.tableau = gridlib.Grid(self.panel, size=(500,200)) #,-1,size=(500,200))
        self.tableau.CreateGrid(self.rowNumber,self.colNumber)
        self.tableau.SetColLabelSize(60)
        self.tableau.SetRowLabelSize(100)
        self.tableau.EnableDragColSize(False)
        self.tableau.EnableDragColMove(False)
        self.tableau.EnableDragRowSize(False)
        self.tableUpdate(self.displayedColHeads,self.displayedRowHeads,'')
        self.tableau.Bind(gridlib.EVT_GRID_CELL_LEFT_CLICK, self.changement)    
        
        font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(9)
        self.tableau.SetLabelFont(font)

        # IPadress of the MMH
        texte1=wx.StaticText(self,wx.ID_ANY,'IP adress of the MMhub: ')
        self.IPDuHub=wx.TextCtrl(self)
        self.IPDuHub.ChangeValue('127.0.0.1')

        # a button to connect the GUI to the hub
        self.ConnectionButton=wx.Button(self,wx.ID_ANY,'CONNECT the GUI',wx.Point (100,200), wx.Size (250,30))

        # User name
        staticTextUserName=wx.StaticText(self,wx.ID_ANY,'             User name: ')
        self.userName=wx.TextCtrl(self)
        self.userName.ChangeValue('ZooOwner')
        
        # Configuration name
        staticTextConfigurationName=wx.StaticText(self,wx.ID_ANY,'Configuration name: ')
        self.configurationName=wx.TextCtrl(self)
        self.configurationName.ChangeValue('feed the animals')
        
        # a button to send a configuration request
        self.configurationRequestButton=wx.Button(self,wx.ID_ANY,'Configuration Request',wx.Point (100,200), wx.Size (250,30))

        # a button to send the new configuration
        self.sendNewConfigurationButton=wx.Button(self,wx.ID_ANY,'Send new configuration',wx.Point (100,200), wx.Size (250,30))
        self.Bind(wx.EVT_BUTTON, self.getNewConfiguration, self.sendNewConfigurationButton)
        
        # check box for unknowdevices
        self.unknowdevices = wx.CheckBox ( self, -1, 'unknowdevices' )
        self.unknowdevices.SetValue(True)

        # window organisation
        boite1=wx.BoxSizer(wx.VERTICAL)
        boite2=wx.BoxSizer(wx.HORIZONTAL)
        boite3=wx.BoxSizer(wx.HORIZONTAL)
        boite4=wx.BoxSizer(wx.HORIZONTAL)
        boite1.Add(self.unknowdevices,   flag=wx.ALIGN_CENTER | wx.ALL, border=10)
        boite1.Add(self.panel,  flag=wx.EXPAND | wx.ALL, border=10)

        boite2.AddSpacer(1)
        boite2.Add(texte1)
        boite2.AddSpacer(1)
        boite2.Add(self.IPDuHub)
        boite2.AddSpacer(1)

        boite1.Add(boite2, flag=wx.ALIGN_CENTER | wx.ALL, border=10)
        
        boite1.Add(self.ConnectionButton,  flag=wx.ALIGN_CENTER | wx.ALL, border=10)
        boite1.Add(self.configurationRequestButton,  flag=wx.ALIGN_CENTER | wx.ALL, border=10)

        boite3.AddSpacer(1)
        boite3.Add(staticTextUserName)
        boite3.AddSpacer(1)
        boite3.Add(self.userName)
        boite3.AddSpacer(1)

        boite1.Add(boite3, flag=wx.ALIGN_CENTER | wx.ALL, border=10)

        boite4.AddSpacer(1)
        boite4.Add(staticTextConfigurationName)
        boite4.AddSpacer(1)
        boite4.Add(self.configurationName)
        boite4.AddSpacer(1)

        boite1.Add(boite4, flag=wx.ALIGN_CENTER | wx.ALL, border=10)
        
        boite1.Add(self.sendNewConfigurationButton,  flag=wx.ALIGN_CENTER | wx.ALL, border=10)
        
        self.SetSizerAndFit(boite1)
        
    def tableUpdate(self, colHeads, rowHeads, config):
        
        ##### columns heads #####
        #########################

        if len(colHeads)==0 and self.tableau.GetNumberCols()!=0:
            self.displayedColHeads=[]
            self.tableau.DeleteCols(numCols=self.tableau.GetNumberCols())
            
        if len(colHeads)!=0:
          
            # col1 is always the longest
            if len(colHeads)>=len(self.displayedColHeads):
                col1=colHeads
                col2=self.displayedColHeads
                toDo1="add"
            else:                                           
                col1=self.displayedColHeads 
                col2=colHeads
                toDo1="delete"  

            lengthOfcol1=len(col1)
            i=0
                
            while i < lengthOfcol1:
                # ADD if i is over the last colHead of col2 (self.displayedColHeads[i] does not exist) -CASE3-
                if i>=len(col2) and toDo1=="add":
                    self.displayedColHeads.insert(i,colHeads[i])
                    self.tableau.AppendCols()

                # DELETE if i is over the last colHead of col2 (self.displayedColHeads[i] does not exist) -CASE5-                
                elif i>=len(col2) and toDo1=="delete":
                    l1=len(col1)
                    numberOfColumnsToDelete= len(col1)-len(col2)
                    self.tableau.DeleteCols(pos=i,numCols=numberOfColumnsToDelete)
                    lengthOfcol1-=numberOfColumnsToDelete
                    for j in range (numberOfColumnsToDelete):
                        del self.displayedColHeads[l1-1-j]

                # the two colHeads are the same, -CASE2-
                elif colHeads[i]==self.displayedColHeads[i]:
                    pass
                
                # ADD if i is not over the last colHead of col2 and the two colHeads are differents, -CASE4-
                elif colHeads[i]!=self.displayedColHeads[i] and toDo1=="add":
                    self.displayedColHeads.insert(i,colHeads[i])
                    self.tableau.InsertCols(pos=i)

                # DELETE if i is not over the last colHead of col2 and the two colHeads are differents -CASE6-  
                elif colHeads[i]!=self.displayedColHeads[i] and toDo1=="delete":
                    self.tableau.DeleteCols(pos=i)
                    lengthOfcol1-=1
                    del self.displayedColHeads[i]
                    i-=1

                i+=1
   
            self.displayedColHeads=colHeads
            
            # display new colHeads
            for nbrCol in range(len(self.displayedColHeads)):
                content11=str(self.displayedColHeads[nbrCol]['deviceName']+'\n'+\
                             self.displayedColHeads[nbrCol]['instance']+'\n'+\
                             self.displayedColHeads[nbrCol]['eventName'])
                self.tableau.SetColLabelValue (nbrCol, content11)
            self.tableau.AutoSizeColumns()
                
        self.displayedColHeads=colHeads
   
        ##### rows heads #####
        ######################

        if len(rowHeads)==0 and self.tableau.GetNumberRows()!=0:
            self.displayedRowHeads=[]
            self.tableau.DeleteRows(numRows=self.tableau.GetNumberRows())

        if len(rowHeads)!=0:
            
            # row1 is always the longest
            if len(rowHeads)>=len(self.displayedRowHeads):
                row1=rowHeads
                row2=self.displayedRowHeads
                toDo2="add"
            else:                                           
                row1=self.displayedRowHeads 
                row2=rowHeads
                toDo2="delete"

            lengthOfrow1=len(row1)
            k=0
                
            while k < lengthOfrow1:
                
                # ADD if i is over the last rowHead of row2 (self.displayedRowHeads[i] does not exist) -CASE13-
                if k>=len(row2) and toDo2=="add":
                    self.displayedRowHeads.insert(k,rowHeads[k])
                    self.tableau.AppendRows()

                # DELETE if i is over the last rowHead of row2 (self.displayedRowHeads[i] does not exist) -CASE15-                
                elif k>=len(row2) and toDo2=="delete":
                    l2=len(row1)
                    numberOfRowsToDelete= len(row1)-len(row2)
                    self.tableau.DeleteRows(pos=k,numRows=numberOfRowsToDelete)
                    lengthOfrow1-=numberOfRowsToDelete
                    for l in range (numberOfRowsToDelete):
                        del self.displayedRowHeads[l2-1-l]

                # the two rowHeads are the same, -CASE12-
                elif rowHeads[k]==self.displayedRowHeads[k]:
                    pass
                
                # ADD if k is not over the last rowHead of row2 and the two rowHeads are differents, -CASE14-
                elif rowHeads[k]!=self.displayedRowHeads[k] and toDo2=="add":
                    self.displayedRowHeads.insert(k,rowHeads[k])
                    self.tableau.InsertRows(pos=k)

                # DELETE if k is not over the last rowHead of row2 and the two rowHeads are differents -CASE16-  
                elif rowHeads[k]!=self.displayedRowHeads[k] and toDo2=="delete":
                    self.tableau.DeleteRows(pos=k)
                    lengthOfrow1-=1
                    del self.displayedRowHeads[k]
                    k-=1

                k+=1

            self.displayedRowHeads=rowHeads
        
            # display new rowHeads
            for nbrRow in range(len(self.displayedRowHeads)):
                content12=str(self.displayedRowHeads[nbrRow]['deviceName']+'\n'+\
                             self.displayedRowHeads[nbrRow]['instance']+'\n'+\
                             self.displayedRowHeads[nbrRow]['eventName'])
                self.tableau.SetRowLabelValue (nbrRow, content12)
            self.tableau.AutoSizeRows()

        self.displayedRowHeads=rowHeads

    def displayConfiguration (self, precedentProducersListLength, precedentConsumersListLength):  # change 02/05
        # firstKey is the authorization for the producer to send the eventID to the consumer
        # secondKey is the authorization for the consumer to receive the eventID from the producer
        # each cell of tableau has a firtKey and a secondKey
        # if both are "yes" the cell is green, else the cell is red (or black if the eventIDs are not the same)
            
        # check each new cell in tableau

        i=0
 
        while i < len(self.displayedRowHeads):
            
            j=0
            while j < len(self.displayedColHeads):
                # only refresh new cells
                if i<precedentProducersListLength and j<precedentConsumersListLength:
                    pass
                else:                   
                    # authorisation is refused by default
                    firstKey = "no"
                    secondKey = "no"
                    # except if configUnknowDevices is "on"
                    if self.myTranslator.configUnknowDevices=="on":
                        firstKey = "yes"
                        secondKey = "yes"

                    ### test for firstKey ###
                    
                    # check if the producer i is in the configuration
                    for currentConfigDevice in self.myTranslator.configDevicesList:
                        if self.displayedRowHeads[i]['did']==currentConfigDevice.did:
                            # if the ID of the producer is in the configuration, authorisation to send has to be explicitly set 
                            firstKey="no"
                            # if the instance is the same, 
                            if self.displayedRowHeads[i]['instance']==currentConfigDevice.instance:
                                # go in the listOfAuthorizedProducedEvents...
                                for currentAuthorizedProducedEvent in currentConfigDevice.listOfAuthorizedProducedEvents:
                                    # to see if the producer can send the event
                                    if currentAuthorizedProducedEvent.eid ==self.displayedRowHeads[i]['eventID']:
                                        # to the consumer (deviceID+instance)
                                        if currentAuthorizedProducedEvent.deviceID == self.displayedColHeads[j]['did'] or\
                                           currentAuthorizedProducedEvent.deviceID == 'all':
                                            if currentAuthorizedProducedEvent.instance == self.displayedColHeads[j]['instance'] or\
                                               currentAuthorizedProducedEvent.instance == 'all':
                                                firstKey = "yes"

                    ### test for secondKey ###
                    
                    # check if the consumer i is in the configuration
                    for currentConfigDevice in self.myTranslator.configDevicesList:
                        if self.displayedColHeads[j]['did']==currentConfigDevice.did:
                            # if the ID of the consumer is in the configuration, authorisation to receive has to be explicitly set 
                            secondKey="no"
                            # if the instance is the same, 
                            if self.displayedColHeads[j]['instance']==currentConfigDevice.instance:
                                # go in the listOfAuthorizedConsumedEvents...
                                for currentAuthorizedConsumedEvent in currentConfigDevice.listOfAuthorizedConsumedEvents:
                                    # to see if the consumer can receive the event
                                    if currentAuthorizedConsumedEvent.eid ==self.displayedColHeads[j]['eventID']:
                                        # from the producer (deviceID+instance)
                                        if currentAuthorizedConsumedEvent.deviceID == self.displayedRowHeads[i]['did'] or\
                                           currentAuthorizedConsumedEvent.deviceID == 'all':
                                            if currentAuthorizedConsumedEvent.instance == self.displayedRowHeads[i]['instance'] or\
                                               currentAuthorizedConsumedEvent.instance == 'all':
                                                secondKey = "yes"
                    if self.displayedRowHeads[i]['eventID'] != self.displayedColHeads[j]['eventID']:
                        self.tableau.SetCellBackgroundColour(i, j, wx.BLACK)                                                    
                    elif firstKey =='yes' and secondKey == 'yes':
                        self.tableau.SetCellBackgroundColour(i, j, wx.GREEN)
                    elif self.displayedRowHeads[i]['eventID'] == self.displayedColHeads[j]['eventID']: 
                        self.tableau.SetCellBackgroundColour(i, j, wx.RED)
                j+=1
            i+=1

    def changement(self,evt):
        rowNumber = evt.GetRow()
        colNumber = evt.GetCol()
        currentColour = self.tableau.GetCellBackgroundColour(rowNumber,colNumber)
        if currentColour == wx.RED:
            self.tableau.SetCellBackgroundColour(rowNumber, colNumber, wx.GREEN)
        if currentColour == wx.GREEN:
            self.tableau.SetCellBackgroundColour(rowNumber, colNumber, wx.RED)
        self.tableau.ForceRefresh()

    def getNewConfiguration (self, evenement):

        unknowdevices='off'
        userName = self.userName.GetValue()
        configName = self.configurationName.GetValue()
        if self.unknowdevices.GetValue() == True:
            unknowdevices='on'         
        
        newConfig=[]
        for i in range (len(self.displayedRowHeads)): 
            for j in range (len(self.displayedColHeads)):        
                if self.tableau.GetCellBackgroundColour(i,j) == wx.GREEN:
                    newConfigElement={}
                    newConfigElement['sourceDeviceID']=self.displayedRowHeads[i]['did']
                    newConfigElement['sourceDeviceInstance']=self.displayedRowHeads[i]['instance']
                    newConfigElement['eventID']=self.displayedRowHeads[i]['eventID']
                    newConfigElement['destinationDeviceID']=self.displayedColHeads[j]['did']                
                    newConfigElement['destinationDeviceInstance']=self.displayedColHeads[j]['instance']
                    newConfig.append(newConfigElement)
                
        self.myTranslator.sendNewConfiguration(userName, configName,unknowdevices, newConfig)     



class connectedDevice:


    
    did = None
    name = ''
    instance = 0
    # list that contain event produced and consumed
    # each elemnt of the lists is a configEvent
    listOfProducedEvents = []
    listOfConsumedEvents = []



class producerOrConsumer:


    
    deviceName =''
    deviceID=''
    instance=''
    eventName=''
    eventID=''

    

class translator:



    def __init__(self, myGUIComponent, myWindow):
        self.DeviceIDAndESFDictionnary = {}
        self.configDevicesList=[]
        self.connectedDevicesList=[]
        self.producersList=[]
        self.consumersList=[]
        self.state=0
        self.count=0
        self.displayTheConfigurationIfReceived = 'yes'
        self.precedentConnectedDevicesListLength=0
        self.myGUIComponent = myGUIComponent
        self.myWindow = myWindow
    
    def getConfigurationAndConnectedDevicesListFromString (self, stringToDecompose):
        self.configDevicesList=[] 
        self.connectedDevicesList=[] 
        XMLConfigurationAndConnectedDevicesList=stringToDecompose.split("xxx connectedDevicesList xxx")

        ###########################################       
        # recuperation of the configuration !copy from Configuration.py!
        XMLConfigurationString = parseString(XMLConfigurationAndConnectedDevicesList[0])
        self.configUnknowDevices = str(XMLConfigurationString.getElementsByTagName("unknowdevices")[0].attributes["default"].value)
        # extraction of the configDevice from the configuration
        for XMLdevice in XMLConfigurationString.getElementsByTagName("device"):
           currentConfigDevice = configDevice ()
                   # for each configDevice,
                   # recuperation of the id
           currentConfigDevice.did=XMLdevice.attributes["id"].value
                   # recuperation of the instance
           currentConfigDevice.instance=XMLdevice.attributes["instance"].value
                   # recuperation of the list of the produced events
           XMLListOfAuthorizedProducedEvents = XMLdevice.getElementsByTagName("produces")[0].getElementsByTagName("event")
           currentConfigDevice.listOfAuthorizedProducedEvents = []
                       # in the list, for each event,
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
                # recuperation of the list of the consumed events
           XMLListOfAuthorizedConsumedEvents = XMLdevice.getElementsByTagName("consumes")[0].getElementsByTagName("event")
           currentConfigDevice.listOfAuthorizedConsumedEvents=[]
                       # in the list, for each event,
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
                # and adding the device to the list
           self.configDevicesList.append(currentConfigDevice)
        ###########################################   

        ###########################################   
        # recuperation of the connected devices from the list
        XMLConnectedDevicesListString = parseString(XMLConfigurationAndConnectedDevicesList[1])
        for XMLdevice in XMLConnectedDevicesListString.getElementsByTagName("device"):
           currentConnectedDevice = connectedDevice ()
                   # for each connectedDevice,
                   # recuperation of the deviceID
           currentConnectedDevice.did=XMLdevice.attributes["deviceID"].value
                   # recuperation of the name
           currentConnectedDevice.name=XMLdevice.attributes["name"].value
                   # recuperation of the instance
           currentConnectedDevice.instance=XMLdevice.attributes["instance"].value
                   # recuperation of the produced events list
           XMLListOfProducedEvents = XMLdevice.getElementsByTagName("produces")[0].getElementsByTagName("eventID")
           currentConnectedDevice.listOfProducedEvents = []
                       # in this list, for each event,
           for XMLProducedEvent in XMLListOfProducedEvents:
               #currentProducedEvent = event ()
                       # recuperation of the id
               #currentProducedEvent.eid=XMLProducedEvent.attributes["id"].value
               currentConnectedDevice.listOfProducedEvents.append(XMLProducedEvent.attributes["id"].value)
                   # recuperation of the consumed events list
           XMLListOfConsumedEvents = XMLdevice.getElementsByTagName("consumes")[0].getElementsByTagName("eventID")
           currentConnectedDevice.listOfConsumedEvents = []
                       # in this list, for each event,
           for XMLConsumedEvent in XMLListOfConsumedEvents:
               #currentConsumedEvent = event ()
                       # recuperation of the id
               #currentConsumedEvent.eid=XMLConsumedEvent.attributes["id"].value
               currentConnectedDevice.listOfConsumedEvents.append(XMLConsumedEvent.attributes["id"].value)
                # and the device is added to the connectedDeviceslist
           self.connectedDevicesList.append(currentConnectedDevice)
        ###########################################   

    def getConfiguration(self, command, stringConfiguration):

        self.precedentConnectedDevicesListLength=len(self.connectedDevicesList)
        
        self.getConfigurationAndConnectedDevicesListFromString(stringConfiguration)


        self.count=0
        self.DeviceIDAndESFDictionnary = {}
        
        stringList = 'configuration chargee: '
        for device in self.configDevicesList:
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

        stringList2 = 'devices connectes:\n'

        for device2 in self.connectedDevicesList:
            stringList2+="\n   device id: "
            stringList2+=rjust(str(device2.did), 3)
            stringList2+=" name: "
            stringList2+=rjust(str(device2.name), 20)
            stringList2+=" instance "
            stringList2+=rjust(str(device2.instance), 3)
            stringList2+="\n        produces:"
            for producedEvent in device2.listOfProducedEvents:
                stringList2+="\n"
                stringList2+="               eventID "
                stringList2+=rjust(str(producedEvent), 3)          
            stringList2+="\n        consumes:"                
            for consumedEvent in device2.listOfConsumedEvents:
                stringList2+="\n"
                stringList2+="               eventID "
                stringList2+=rjust(str(consumedEvent), 3)
        

        # If the last compoenent is disconnected, no more ESF will be received and the tableUpdate will not be done
        if len(self.connectedDevicesList)==0 and self.precedentConnectedDevicesListLength!=0:
            self.generateProducersListAndConsumersList()
            self.myWindow.tableUpdate(self.consumersList,self.producersList,'')

    def configRequest(self, command):
        self.myGUIComponent.configurationRequest(command)       

    def connectAndDisconnectTheComponent(self, command):
        stateBeforeChange = self.state

        IPAdressOfTheHub = self.myWindow.IPDuHub.GetValue()
        # if the component is already connected, it will be stopped
        if self.state:
            self.state=0
            self.myWindow.ConnectionButton.SetLabel('CONNECT the GUI')          
        # else, it will be started
        else:
            self.state=1
            self.myWindow.ConnectionButton.SetLabel('DISCONNECT the GUI')
        self.myGUIComponent.startAndStopTheComponent(command, stateBeforeChange, IPAdressOfTheHub)

    def stockESF(self, DeviceID, ESF):
        self.count+=1
        self.DeviceIDAndESFDictionnary[str(DeviceID)]=ESF
        if self.count ==len(self.connectedDevicesList):
            
            precedentProducersListLength=len(self.producersList)
            precedentConsumersListLength=len(self.consumersList)
            
            self.generateProducersListAndConsumersList()
            
            self.myWindow.tableUpdate(self.consumersList,self.producersList,'')

            self.myWindow.displayConfiguration(precedentProducersListLength, precedentConsumersListLength)            
              
    def getEventNameFromEventID (self, eventId):
        for currentESF in self.DeviceIDAndESFDictionnary.values():
            XMLESF=parseString(currentESF)
            for currentXMLEvent in XMLESF.getElementsByTagName("event"):
                if str(currentXMLEvent.attributes["id"].value)==str(eventId):
                    return currentXMLEvent.attributes["description"].value
        return 'no description'      

    def generateProducersListAndConsumersList (self):
        # generate de producersList and consumersList with deviceName, deviceID, instance, eventName and eventID

        self.producersList=[]
        self.consumersList=[]
        
        for currentConnectedDevice in self.connectedDevicesList:
            for currentEventID in currentConnectedDevice.listOfProducedEvents:
                currentProducer = {}
                currentProducer['deviceName']=str(currentConnectedDevice.name)
                currentProducer['did']=str(currentConnectedDevice.did)
                currentProducer['instance']=str(currentConnectedDevice.instance)
                currentProducer['eventID']=str(currentEventID)
                currentProducer['eventName']=str(self.getEventNameFromEventID(currentEventID))
                if currentProducer['eventName']!='no description':  # ESF is necessary
                    self.producersList.append(currentProducer)
            for currentEventID in currentConnectedDevice.listOfConsumedEvents:
                currentConsumer = {}
                currentConsumer['deviceName']=str(currentConnectedDevice.name)
                currentConsumer['did']=str(currentConnectedDevice.did)
                currentConsumer['instance']=str(currentConnectedDevice.instance)
                currentConsumer['eventID']=str(currentEventID)
                currentConsumer['eventName']=str(self.getEventNameFromEventID(currentEventID))
                if currentConsumer['eventName']!='no description':    # ESF is necessary
                    self.consumersList.append(currentConsumer)

    def sendNewConfiguration(self, userName, configName, unknowdevices, newConfig):

        doc = Document()
        xmlUserConfig = doc.createElement("userconfig")
        doc.appendChild(xmlUserConfig)
        xmlUserName=doc.createElement("user")
        xmlUserName.setAttribute("name", userName.encode())
        xmlUserConfig.appendChild(xmlUserName)
        xmlConfigurationName=doc.createElement("config")
        xmlConfigurationName.setAttribute("name", configName.encode())
        xmlUserConfig.appendChild(xmlConfigurationName)
        xmlUnknowDevices=doc.createElement("unknowdevices")
        xmlUnknowDevices.setAttribute("default", unknowdevices.encode())
        xmlUserConfig.appendChild(xmlUnknowDevices)
        xmlAssignInstances=doc.createElement("assigninstances")
        xmlAssignInstances.setAttribute("mode", "on")
        xmlUserConfig.appendChild(xmlAssignInstances)
        xmlDevices=doc.createElement("devices")
        xmlUserConfig.appendChild(xmlDevices)

        newConfigLength = len(newConfig)

        # flagList will store the information about the treatement of the element in newConfig list
        #0: nothing done
        #1: sourceDevice already registred in the xml document
        #2: destinationDevice already registred in the xml document
        #3: sourceDevice and destinationDevice already registred in the xml document
        flagList=[]
        for h in range (newConfigLength):
            flagList.append(0)
            
        # parse the newConfig list ...
        i=0
        while i < newConfigLength:
            
            # ...to put all producers (not already registered) in the xml document
            if flagList[i]==0 or flagList[i]==2:
                # for each element, create a device in the xml document
                xmlDevice=doc.createElement("device")
                xmlDevice.setAttribute("id", newConfig[i]['sourceDeviceID'].encode())
                xmlDevice.setAttribute("instance", newConfig[i]['sourceDeviceInstance'].encode())
                xmlDevices.appendChild(xmlDevice)
                xmlProduces=doc.createElement("produces")
                xmlDevice.appendChild(xmlProduces)
                xmlConsumes=doc.createElement("consumes")
                xmlDevice.appendChild(xmlConsumes)
                xmlEvent=doc.createElement("event")
                xmlEvent.setAttribute("id", newConfig[i]['eventID'].encode())
                xmlEvent.setAttribute("deviceID", newConfig[i]['destinationDeviceID'].encode())
                xmlEvent.setAttribute("instance", newConfig[i]['destinationDeviceInstance'].encode())
                xmlProduces.appendChild(xmlEvent)
                # indicate that the producer of this element of the newConfig List has been registered
                flagList[i]+=1
                # check in the rest of the newConfig list if the device appears ...
                j = i+1
                while j < newConfigLength:
                    # ... as a producer not already registered
                    if newConfig[j]['sourceDeviceID']==newConfig[i]['sourceDeviceID'] \
                       and newConfig[j]['sourceDeviceInstance']==newConfig[i]['sourceDeviceInstance']\
                       and (flagList[j]==0 or flagList[j]==2):
                        xmlEvent=doc.createElement("event")
                        xmlEvent.setAttribute("id", newConfig[j]['eventID'].encode())
                        xmlEvent.setAttribute("deviceID", newConfig[j]['destinationDeviceID'].encode())
                        xmlEvent.setAttribute("instance", newConfig[j]['destinationDeviceInstance'].encode())
                        xmlProduces.appendChild(xmlEvent)
                        # indicate that the producer of this element of the newConfig List has been registered
                        flagList[j]+=1
                    j+=1
                # check in all the the newConfig list if the device appears ...
                k = 0
                while k < newConfigLength:
                    # ... as a consumer not already registered
                    if newConfig[k]['destinationDeviceID']==newConfig[i]['sourceDeviceID'] \
                       and newConfig[k]['destinationDeviceInstance']==newConfig[i]['sourceDeviceInstance']\
                       and (flagList[k]==0 or flagList[k]==1):
                        xmlEvent=doc.createElement("event")
                        xmlEvent.setAttribute("id", newConfig[k]['eventID'].encode())
                        xmlEvent.setAttribute("deviceID", newConfig[k]['sourceDeviceID'].encode())
                        xmlEvent.setAttribute("instance", newConfig[k]['sourceDeviceInstance'].encode())
                        xmlConsumes.appendChild(xmlEvent)
                        # indicate that the consumer of this element of the newConfig List has been registered
                        flagList[k]+=2                          
                    k+=1
                    
            # ...to put all consumers (not already registered) in the xml document
            if flagList[i]==0 or flagList[i]==1:
                # for each element, create a device in the xml document
                xmlDevice=doc.createElement("device")
                xmlDevice.setAttribute("id", newConfig[i]['destinationDeviceID'].encode())
                xmlDevice.setAttribute("instance", newConfig[i]['destinationDeviceInstance'].encode())
                xmlDevices.appendChild(xmlDevice)
                xmlProduces=doc.createElement("produces")
                xmlDevice.appendChild(xmlProduces)
                xmlConsumes=doc.createElement("consumes")
                xmlDevice.appendChild(xmlConsumes)
                xmlEvent=doc.createElement("event")
                xmlEvent.setAttribute("id", newConfig[i]['eventID'].encode())
                xmlEvent.setAttribute("deviceID", newConfig[i]['sourceDeviceID'].encode())
                xmlEvent.setAttribute("instance", newConfig[i]['sourceDeviceInstance'].encode())
                xmlConsumes.appendChild(xmlEvent)
                # indicate that the consumer of this element of the newConfig List has been registered
                flagList[i]+=2
                # check in the rest of the newConfig list if the device appears ...
                l = i+1
                while l < newConfigLength:
                    # ... as a producer not already registered
                    if newConfig[l]['sourceDeviceID']==newConfig[i]['sourceDeviceID'] \
                       and newConfig[l]['sourceDeviceInstance']==newConfig[i]['sourceDeviceInstance']\
                       and (flagList[l]==0 or flagList[l]==2):
                        xmlEvent=doc.createElement("event")
                        xmlEvent.setAttribute("id", newConfig[l]['eventID'].encode())
                        xmlEvent.setAttribute("deviceID", newConfig[l]['destinationDeviceID'].encode())
                        xmlEvent.setAttribute("instance", newConfig[l]['destinationDeviceInstance'].encode())
                        xmlProduces.appendChild(xmlEvent)
                        # indicate that the producer of this element of the newConfig List has been registered
                        flagList[l]+=1
                    l+=1
                # check in all the the newConfig list if the device appears ...
                m = 0
                while m < newConfigLength:
                    # ... as a consumer not already registered
                    if newConfig[m]['destinationDeviceID']==newConfig[i]['destinationDeviceID'] \
                       and newConfig[m]['destinationDeviceInstance']==newConfig[i]['destinationDeviceInstance']\
                       and (flagList[m]==0 or flagList[m]==1):
                        xmlEvent=doc.createElement("event")
                        xmlEvent.setAttribute("id", newConfig[m]['eventID'].encode())
                        xmlEvent.setAttribute("deviceID", newConfig[m]['sourceDeviceID'].encode())
                        xmlEvent.setAttribute("instance", newConfig[m]['sourceDeviceInstance'].encode())
                        xmlConsumes.appendChild(xmlEvent)
                        # indicate that the consumer of this element of the newConfig List has been registered
                        flagList[m]+=2                          
                    m+=1
            i+=1

        fileName = 'Configuration file - '+userName.encode()+'-'+configName.encode()
        xmlNewConfig = doc.toprettyxml (indent="     ")
        stringToSend='xxx the message begins here xxx\n'+fileName+'\nxxx newConfig xxx\n'+xmlNewConfig
        self.myGUIComponent.sendNewConfiguration(stringToSend)
            
            

            
            
        
class GUIComponent:


    
    stringXMLESF="""
                    <esf>
                        <event id="0xFFFFFFFDL" description="Configuration Request">
                            <field name="request" type="string"/>
                        </event>
                    </esf>
                 """

    def __init__(self):
        self.myTranslator=None
        
    def configurationRequest(self, command):
        
        record = FieldFactory.fieldFromCodeList("LLLS")    
        # encapsulate the message
        record[0].set(self.device.UCID)
        record[1].set(self.device.deviceID)
        record[2].set(0xFFFFFFFDL) # EventID for Configuration Request
        record[3].set('xxx the message begins here xxx\n')

        self.device.server.sendFields(None, record)

    def askTheESF (self):
        if self.myTranslator.state:
            #creation of the message to send
            messageAEnvoyer = {"type":"1","destinationUCID":"","query":""}
        
            record = FieldFactory.fieldFromCodeList("LLLS")

            # concatenation en string >> http://www.skymind.com/~ocrow/python_string/
            messageEnvoye=''.join(['    ',str(messageAEnvoyer)])

           # encapsulate the message
            record[0].set(self.device.UCID)
            record[1].set(self.device.deviceID)
            record[2].set(0xF0000002L) # EventID
            record[3].set(messageEnvoye)

            # sending the message
            self.device.server.sendFields(None, record)

    def sendESF(self, command):
        try:
            messageToSend=''.join(['    ',self.stringXMLESF])
        except:
            messageToSend=''

        record = FieldFactory.fieldFromCodeList("LLLS")    
        # encapsulate the message
        record[0].set(self.device.UCID)
        record[1].set(self.device.deviceID)
        record[2].set(0xF0000003L) # EventID for Metadata Response
        record[3].set(messageToSend)

        self.device.server.sendFields(None, record)

    def receiveESF(self, command):

        recordConfig = FieldFactory.fieldFromCodeList("LLLS")
        FieldFactory.readFields(recordConfig, command.dataIn)

        deviceID = recordConfig[1].get()
        ESF = recordConfig[3].get()
        
        self.myTranslator.stockESF (deviceID,ESF)

    def getMetaDataConfiguration(self, command):
        recordConfig = FieldFactory.fieldFromCodeList("LLLS")
        FieldFactory.readFields(recordConfig, command.dataIn)

        configuration = recordConfig[3].get()

        self.myTranslator.getConfiguration (command, configuration)

        self.askTheESF ()         

    def sendNewConfiguration(self,stringToSend):
        record = FieldFactory.fieldFromCodeList("LLLS")    
        # encapsulate the message
        record[0].set(self.device.UCID)
        record[1].set(self.device.deviceID)
        record[2].set(0xFFFFFFFDL) # EventID for Configuration Request
        record[3].set(stringToSend)

        self.device.server.sendFields(None, record)
        
                
    def startAndStopTheComponent (self, command, currentState, IPAdressOfTheHub):
        
        # if the component is already connected, it stops
        if currentState:
            self.device.disconnect()
            self.client.stop()
            
        # else, it starts
        else:
            self.client = UDPServer("", 0)
            # recuperation of the IP adressof the MMH. port=6000
            self.client.setMultimodalHubAddress((IPAdressOfTheHub,6000))
            self.client.start()

            self.device = MultimodalDevice("GUI", self.client, 0xFFFFFFFEL)
            # adding the EventID to the produced event list
            self.device.produces.append(0xFFFFFFFDL)
            
            # adding the EventID to the consumed event list
            self.device.consumes.append(0xFFFFFFFEL)
            
            # getMetaDataConfiguration is called at each reception of an event 0xFFFFFFFEL
            self.device.eventProcessors[0xFFFFFFFEL] = self.getMetaDataConfiguration

            # adding 0xF0000002 for Metadata Request = " I produce ESF request "
            self.device.produces.append(0xF0000002L)  

            # adding 0xF0000003 for Metadata Response = " I consume ESF response "
            self.device.consumes.append(0xF0000003L)
            
            # receiveESF is called at each reception of an event 0xF0000003L
            self.device.eventProcessors[0xF0000003L] = self.receiveESF        

                        
            self.device.register()
            
class MonAppli (wx.App):
    def OnInit(self):
        
        self.myWindow = GUIWindow (None, wx.ID_ANY, 'GUI')
        self.myGUIComponent = GUIComponent()   
        myTranslator = translator(self.myGUIComponent,self.myWindow)

        self.myGUIComponent.myTranslator = myTranslator

        self.myWindow.myTranslator = myTranslator
        self.myWindow.Bind(wx.EVT_BUTTON, myTranslator.connectAndDisconnectTheComponent, self.myWindow.ConnectionButton)
        self.myWindow.Bind(wx.EVT_BUTTON, myTranslator.configRequest, self.myWindow.configurationRequestButton)
        
        self.myWindow.Show()

        return True

app=MonAppli(redirect=False)
app.MainLoop()
