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

import struct
import MultimodalMiddlewareProtocol.Consts

#TODO: must fix Unicode read/write

class Writer:
    
    def __init__(self):
        self.reset()
        
    def get(self):
        return self.stream
    
    def reset(self):
        self.stream = ''
        self.pointer = 0  
    
    def add(self, p):
        self.stream+=p
        self.pointer+=len(p)    
    
    def writeInt(self, i):
        si = struct.pack("!i", i)
        self.add(si)
        
    def writeLong(self, l):
        sl = struct.pack("!q", long(l))
        self.add(sl)
        
    def writeByte(self, b):
        sb = struct.pack("!b", b)
        self.add(sb)
        
    def writeShort(self, s):
        ss = struct.pack("!h", s)
        self.add(ss)
        
    def writeChar(self, c):
        sc = struct.pack("!c", c)
        self.add(sc)
        
    def writeWideChar(self, wc):
        bwc = wc.encode("utf-16")
        for c in bwc[2:]: # Skip two first bytes - BOM marker
            self.writeChar(c)        
        
    def writeString(self, s):
        self.add(s)
        
    def writeWideString(self, ws):
        self.writeWideChar(ws)                
    
    def writeDouble(self, d):
        sd = struct.pack("!d", d)
        self.add(sd)
        
class Reader:   
    
    def __init__(self, s=None):
        self.set(s)
        
    def get(self):
        return self.stream
    
    def set(self, s):
        self.stream = s
        self.pointer = 0  #len(self.stream)
    
    def reset(self):
        #self.stream = ''
        self.pointer = 0  
    
    def move(self, p):
        #self.stream+=p
        #self.pointer+=len(p)
        self.pointer=p
    
    def read(self, type):
        rs = struct.calcsize(type)
        r = struct.unpack(type,self.stream[self.pointer:self.pointer+rs])[0]
        self.pointer+=rs
        #print "Type: %s Size: %d Value: %s" % (type, rs, r)
        return r
    
    def readInt(self):
        return self.read("!i")
        
    def readLong(self):
        return self.read("!q")
        
    def readByte(self):
        return self.read("!b")
        
    def readShort(self):
        return self.read("!h")
        
    def readChar(self):
        return self.read("!c")
    
    def readWideChar(self):
        return (self.readByte() + self.readByte()).encode("utf-16")
        
    def readString(self, size):
        r = self.stream[self.pointer:self.pointer+size]
        self.pointer += size
        return r
    
    def readWideString(self, size):
        wc = ""
        for x in range(size * 2): #Read 2x the size in bytes - String without BOM!!!
            wc+=self.readByte()
        return wc.encode("utf-16")
            
    def readDouble(self, d):
        return self.read("!d")
    
    def decode(self, s):
        r = []
        for x in list(s):
            if x == Consts.CHAR_BYTE: 
                r.append(self.readByte())
            elif x == Consts.CHAR_SHORT: 
                r.append(self.readShort())
            elif x == Consts.CHAR_INTEGER: 
                r.append(self.readInt())
            elif x == Consts.CHAR_LONG: 
                r.append(self.readLong())
            elif x == Consts.CHAR_SHORTSTRING:
                size = self.readByte() 
                r.append(self.readString(size))
            elif x == Consts.CHAR_CHAR: 
                r.append(self.readChar())
            elif x ==  Consts.CHAR_DOUBLECHAR: 
                r.append(self.readDoubleChar())
            elif x == Consts.CHAR_LONGSTRING:
                size = self.readInt() 
                r.append(self.readString(size))
            elif x == Consts.CHAR_WIDESTRING:
                size = self.readInt() 
                r.append(self.readString(size))
            elif x == Consts.CHAR_ARRAY or x == Consts.CHAR_ARRAYU:
                r.append(self.readByte())
            elif x == Consts.CHAR_RECORD: 
                raise "not implemented"
            elif x == Consts.CHAR_UNDEFINED: 
                raise "not defined"
            else:
                raise "unknow format string: "+x
        return r
                
