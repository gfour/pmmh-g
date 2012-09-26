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

from MultimodalMiddlewareProtocol.Server import *

class HashLong:
    def __init__(self):
        self.hash = {}
        
    def addOrUpdate(self, k, v):
        if not self.hash.has_key(k):
            self.hash[k] = []
        l = self.hash[k]         
        l.append(v)
        
    ##########################################################
    #modified by ND

    def delete (self, UCIDToDelete):
        # pour chaque liste contenue dans le hashLong,
        for currentUCIDList in self.hash.values():
            #essai de supprimer le UCID
            try:
                currentUCIDList.remove(UCIDToDelete)
            except:
                pass
        
    #modified by ND
    ##########################################################
            
    def get(self, k):
        if self.hash.has_key(k):
            return self.hash[k]
        else:
            return None
  
    def getKeys(self):
        return self.hash.keys()
        
        
class HashNetworkTable:
    
    def __init__(self):
        self.hash = { }
    
    def addOrUpdate(self, key, name, produces, consumes, netAddress, deviceID, instance):
        self.addOrUpdateNetworkDevice(key, NetworkDevice(name, produces, consumes, netAddress, key, deviceID, instance))
    
    def addOrUpdateNetworkDevice(self, key, d):
        self.hash[key] = d
        print ("Adding device... liste UCID: "+str(self.hash.keys()))

    ##########################################################
    #modified by ND

    def delete (self, key):
        # deleting the device (the key is the UCID)
        del self.hash[key]        
        print ("Deleting device... liste UCID: "+str(self.hash.keys()))

    #modified by ND
    ##########################################################
    
    def get(self, key):
        if self.hash.has_key(key):
            return self.hash[key]
        else:
            return None
    
    def getDevicebyIndex(i):
        deviceList = self.hash.keys()
        try:
            return self.hash.get(self.hash.keys[i])
        except:
            return None
        
    def getKeys(self):
        return self.hash.keys()

    ##########################################################
    #modified by ND

    def getInstanceToSet (self, deviceID):
        listOfInstance=[]
        # parse the connected device list and get instances of the devices with the same deviceID
        for currentDevice in self.hash.values():
            if currentDevice.deviceID == deviceID:
                listOfInstance.append(currentDevice.instance)
        # give the highest instance number
        if len(listOfInstance) != 0:
            listOfInstance.sort()
            listOfInstance=listOfInstance[::-1]
            # add 1 to the hihgest instance number
            InstanceToSet=int(listOfInstance[0])+1
        else:
            InstanceToSet = 0
        return InstanceToSet     

    def getFirstUCIDFromDeviceID (self, deviceID):
        for currentUCID in self.hash.keys():
            if self.hash[currentUCID].deviceID == deviceID:
                return currentUCID

    def getNetworkAddressFromUCID (self, UCID):
        for currentUCID in self.hash.keys():
            if self.hash[currentUCID].UCID == UCID:
                return self.hash[currentUCID].netAddress

    #modified by ND
    ##########################################################
