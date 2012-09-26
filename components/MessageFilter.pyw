# -*- coding: cp1252 -*-

try:
    from MultimodalMiddlewareProtocol.Device import MultimodalDevice
    from MultimodalMiddlewareProtocol import Fields
    from MultimodalMiddlewareProtocol import FieldFactory
    from MultimodalMiddlewareProtocol.servers.UDPServer import UDPServer
except ImportError:
    raise ImportError, "The MMP module is required!"

try:
    import wx
except ImportError:
    raise ImportError, "The wxPython module is required!"

class MaFenetreMessageFilter (wx.Frame):

    def __init__(self, parent, id, titre):
            
        wx.Frame.__init__(self, parent, id, titre)

        # IP adress of the MMH
        texte1=wx.StaticText(self,wx.ID_ANY,'IP adress of the MMhub: ')
        self.IPDuHub=wx.TextCtrl(self)
        self.IPDuHub.ChangeValue('127.0.0.1')

        # Message to filter
        texte2=wx.StaticText(self,wx.ID_ANY,'Message to filter')
        # event ID
        texte3=wx.StaticText(self,wx.ID_ANY,'EventID: ')
        self.EventIDChoisiIN=wx.TextCtrl(self)
        # displaying received message
        texte4=wx.StaticText(self,wx.ID_ANY,'Received: ')
        self.texte5=wx.StaticText(self,wx.ID_ANY,'...waiting...')

        # Comparaison criterion
        texte6=wx.StaticText(self,wx.ID_ANY,'comparaison')
        symbolList=['=','!=','>','<']
        self.combo1 = wx.ComboBox(self, wx.ID_ANY, value=symbolList[3], pos=wx.Point(10, 30), size=wx.Size(100,30), choices=symbolList)
        self.parametre=wx.TextCtrl(self)

        # Message to send
        texte7=wx.StaticText(self,wx.ID_ANY,'Message to send')
        # event ID
        texte8=wx.StaticText(self,wx.ID_ANY,'EventID: ')
        self.EventIDChoisiOUT=wx.TextCtrl(self)
        # displaying the message sent
        texte9=wx.StaticText(self,wx.ID_ANY,'Sent: ')
        self.texte10=wx.StaticText(self,wx.ID_ANY,'...waiting...')

        # CONNECT button
        self.boutonUpdate=wx.Button(self,wx.ID_ANY,'CONNECT')
        #self.Bind(wx.EVT_BUTTON, self.update, self.boutonUpdate)

        # window organisation
        boite1=wx.BoxSizer(wx.VERTICAL)
        boite2=wx.BoxSizer(wx.HORIZONTAL)
        boite3=wx.BoxSizer(wx.HORIZONTAL)
        boite4=wx.BoxSizer(wx.VERTICAL)
        boite5=wx.BoxSizer(wx.VERTICAL)
        boite6=wx.BoxSizer(wx.VERTICAL)
        boite7=wx.BoxSizer(wx.HORIZONTAL)
        boite8=wx.BoxSizer(wx.HORIZONTAL)
        boite9=wx.BoxSizer(wx.HORIZONTAL)
        boite10=wx.BoxSizer(wx.HORIZONTAL)

        boite2.AddSpacer(1)
        boite2.Add(texte1)
        boite2.AddSpacer(1)
        boite2.Add(self.IPDuHub)
        boite2.AddSpacer(1)

        boite7.AddSpacer(1)
        boite7.Add(texte3)
        boite7.AddSpacer(1)
        boite7.Add(self.EventIDChoisiIN)
        boite7.AddSpacer(1)

        boite8.AddSpacer(1)
        boite8.Add(texte4)
        boite8.AddSpacer(1)
        boite8.Add(self.texte5)
        boite8.AddSpacer(1)

        boite5.AddSpacer(1)
        boite5.Add(texte6)
        boite5.AddSpacer(10)
        boite5.Add(self.combo1)
        boite5.AddSpacer(1)
        boite5.Add(self.parametre)
        boite5.AddSpacer(1)

        boite9.AddSpacer(1)
        boite9.Add(texte8)
        boite9.AddSpacer(1)
        boite9.Add(self.EventIDChoisiOUT)
        boite9.AddSpacer(1)

        boite10.AddSpacer(1)
        boite10.Add(texte9)
        boite10.AddSpacer(1)
        boite10.Add(self.texte10)
        boite10.AddSpacer(1)
        
        boite4.Add(texte2)
        boite4.Add(boite7, flag=wx.ALIGN_CENTER | wx.ALL, border=10)
        boite4.Add(boite8, flag=wx.ALIGN_CENTER | wx.ALL, border=10)
        
        boite6.Add(texte7)
        boite6.Add(boite9, flag=wx.ALIGN_CENTER | wx.ALL, border=10)
        boite6.Add(boite10, flag=wx.ALIGN_CENTER | wx.ALL, border=10)

        boite3.Add(boite4, flag=wx.ALIGN_CENTER | wx.ALL, border=10)
        boite3.Add(boite5, flag=wx.ALIGN_CENTER | wx.ALL, border=10)
        boite3.Add(boite6, flag=wx.ALIGN_CENTER | wx.ALL, border=10)

        boite1.Add(boite2, flag=wx.ALIGN_CENTER | wx.ALL, border=10)
        boite1.Add(boite3, flag=wx.ALIGN_CENTER | wx.ALL, border=10)
        boite1.Add(self.boutonUpdate, flag=wx.ALIGN_CENTER | wx.ALL, border=10)

        self.SetSizerAndFit(boite1)

        self.Bind(wx.EVT_BUTTON, self.lancerlecomponent, self.boutonUpdate)

    def receiveCompareAndSend(self, command):
        
        recordIN = FieldFactory.fieldFromCodeList("LLLS")
        FieldFactory.readFields(recordIN, command.dataIn)

        recordOUT = FieldFactory.fieldFromCodeList("LLLS")

        # reception and display of the message received
        messageRecu=int(recordIN[3].get())
        self.texte5.SetLabel(str(messageRecu))

        #get comparaison symbol
        symbole=str(self.combo1.GetValue())
        Parametre=int(self.parametre.GetValue())
        EventIDOUT = long(int(self.EventIDChoisiOUT.GetValue()))
        messageAEnvoyer=''.join(['    ',str(messageRecu)])
        if symbole=='=':
            if messageRecu==Parametre:
                recordOUT[0].set(self.device.UCID)
                recordOUT[1].set(self.device.deviceID)
                recordOUT[2].set(EventIDOUT) # EventID
                recordOUT[3].set(messageAEnvoyer)
                # sending the message
                self.device.server.sendFields(None, recordOUT)
                # displaying of the message sent
                self.texte10.SetLabel(str(recordOUT[3].get()))

        elif symbole=='!=':
            if messageRecu!=Parametre:
                recordOUT[0].set(self.device.UCID)
                recordOUT[1].set(self.device.deviceID)
                recordOUT[2].set(EventIDOUT) # EventID
                recordOUT[3].set(messageAEnvoyer)
                self.device.server.sendFields(None, recordOUT)
                self.texte10.SetLabel(str(recordOUT[3].get()))

        elif symbole=='>':
            if messageRecu>Parametre:
                recordOUT[0].set(self.device.UCID)
                recordOUT[1].set(self.device.deviceID)
                recordOUT[2].set(EventIDOUT) # EventID
                recordOUT[3].set(messageAEnvoyer)
                self.device.server.sendFields(None, recordOUT)
                self.texte10.SetLabel(str(recordOUT[3].get()))

        elif symbole=='<':
            print ''.join([str(messageRecu),symbole,str(Parametre)])
            if messageRecu<Parametre:
                print ''.join(['***','ok','***'])
                recordOUT[0].set(self.device.UCID)
                recordOUT[1].set(self.device.deviceID)
                recordOUT[2].set(EventIDOUT) # EventID
                recordOUT[3].set(messageAEnvoyer)
                self.device.server.sendFields(None, recordOUT)
                self.texte10.SetLabel(str(recordOUT[3].get()))



    def lancerlecomponent (self, evenement):
        
        EventIDIN = long(int(self.EventIDChoisiIN.GetValue()))
        EventIDOUT = long(int(self.EventIDChoisiOUT.GetValue()))
        client = UDPServer("", 0)
        client.setMultimodalHubAddress((self.IPDuHub.GetValue(),6000))
        client.start()
        self.device = MultimodalDevice("MessageFilter1", client, 21L)
        self.device.consumes.append(EventIDIN)
        self.device.produces.append(EventIDOUT)
        self.device.eventProcessors[EventIDIN] = self.receiveCompareAndSend
        self.device.register()
 
class MonAppli (wx.App):
    def OnInit(self):
        fenetre = MaFenetreMessageFilter (None, wx.ID_ANY, 'MessageFilter1')
        fenetre.Show()
        return True


app=MonAppli(redirect=False)
#app=MonAppli()
app.MainLoop()
