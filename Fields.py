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

import Consts
import FieldFactory

class Field:
       
    def __init__(self):
        self.code='U'
    
    def getCode(self):
        return self.code;

    def read(self, r):
        pass
    
    def write(self, w):
        pass

class ArrayField(Field):
    
    def __init__(self, nelements=0, type=None):
        self.nelements = 0
        self.subcode = Consts.CHAR_UNDEFINED
        self.elements = []
        self.code = Consts.CHAR_ARRAY
        if nelements<>0:
            self.setNelemAndType(nelements, type)
       
    def setNelemAndType(self, nelem, type):
        self.nelements = nelem
        self.subcode = type
        self.createElements()
    
    def getNelem(self):
        return self.nelements
    
    def getSubCode(self):
        return self.subcode
    
    def getPackedCode(self):
        return "A"+((self.nelements & 0xFF00)>>8)+(self.nelements & 0xFF)+self.subcode
    
    def get(self, x):
        return self.elements[x]
    
    def getContents(self):
        return [x.get() for x in self.elements]
    
    def set(self, x, field):
        self.elements[x]=field
    
    def add(self, field):
        if(field.getCode()==self.subcode):
            if(self.elements==None):
                self.elements = []
            self.elements.append(field)
            self.nelements+=1
            return True
        else:
            return False
    
    def copyLongVector(self, source):
        self.setNelemAndType(len(source), Consts.CHAR_LONG)
        for x in range(len(source)):
            self.elements[x].set(source[x])

    def createElements(self):
        self.elements = []
        for x in range(self.nelements):
            self.elements.append(FieldFactory.fieldFromCode(self.subcode))

    def read(self, r):
        self.subcode = r.readChar()
        self.nelements = r.readShort()
        self.createElements()
        #print "Subcode: %s nElements: %s " % (self.subcode, self.nelements)
        for x in range(self.nelements):
            self.elements[x].read(r)

    
    def write(self, w):
        w.writeChar(self.subcode)
        w.writeShort(self.nelements)
        for x in range(self.nelements):
            self.elements[x].write(w)
    
    def __del__(self):
        FieldFactory.destroyFieldVector(self.elements)
        self.elements = None



class ByteField(Field):
       
    def __init__(self, b=None):
        Field.__init__(self)
        self.code = Consts.CHAR_BYTE
        self.set(b)

    def read(self, r):
        self.value = r.readByte()

    def write(self, w):
        w.writeByte(self.value);
    
    def set(self, b):
        self.value = b
    
    def get(self):
        return self.value


class CharField(Field):

    def __init__(self, c=None):
        Field.__init__(self)
        self.code = Consts.CHAR_CHAR
        self.set(c)        

    def read(self, r):
        self.value = r.readChar()

    def write(self, w):
        w.writeChar(self.value);
        
    def set(self, c):
        self.value = c
    
    def get(self):
        return self.value


class DoubleCharField(Field):
    def __init__(self, d=None):
        Field.__init__(self)
        self.code = Consts.CHAR_DOUBLECHAR
        self.set(d)        
    #TODO: fix unicode reading
    def read(self, r):
        self.value = r.readChar();
    #TODO: fix unicode writing
    def write(self, w):
        w.writeDoubleChar(self.value)
    
    def set(self, c):
        self.value = c
    
    def get(self):
        return self.value


class IntegerField(Field):
    
    def __init__(self, i=None):
        Field.__init__(self)
        self.code = Consts.CHAR_INTEGER;
        self.set(i)
    
    def read(self, r):
        self.value = r.readInt()

    def write(self, w):
        w.writeInt(self.value)
    
    def set(self, i):
        self.value = i
    
    def get(self):
        return self.value


class LongField(Field):
    
    def __init__(self, l = None):
        Field.__init__(self)
        self.code = Consts.CHAR_LONG
        self.set(l)

    def read(self, r):
        self.value = r.readLong()

    def write(self, w):
        #print self.value
        w.writeLong(self.value)
    
    def set(self,l):
        self.value = l
    
    def get(self):
        return self.value


class LongStringField(Field):

    def __init__(self, s = None):
        Field.__init__(self)
        self.code = Consts.CHAR_LONGSTRING
        self.set(s)
    
    def read(self, r):
        s = r.readInt()
        self.value = r.readString(s)
    
    def write(self, w):
        #w.writeInt(self.value.len)
        w.writeString(self.value)
    
    def set(self, s):
        self.value = s
    
    def get(self):
        return self.value


class ShortField(Field):
    
    def __init__(self, b=None):
        self.code = Consts.CHAR_SHORT
        self.set(b)
    
    def read(self, r) :
        self.value = r.readShort()

    def write(self, w):
        w.writeShort(self.value)
    
    def set(self, b):
        self.value = b
    
    def get(self):
        return self.value;

class ShortStringField(Field):
    
    def __init__(self, s=None):
        self.code = Consts.CHAR_SHORTSTRING
        self.set(s);

    def read(self, r):
        s = r.readByte() # String size
        self.value = r.readString(s) # Must read s bytes!
        if(len(self.value)<>s):
            raise "String Lenght Mismatch !"

    def write(self, w):
        l = len(self.value)
        if (l>255):
            raise "Short String should be shorter than 255 chars."
        w.writeByte(l)
        w.writeString(self.value)

    def set(self, s):
        self.value = s
    
    def get(self):
        return self.value;



class WideStringField:
    
    def __init__(self, b=None):
        self.code = Consts.CHAR_WIDESTRING
        self.set(b)
       
    def read(self, r):
        s = r.readInt();
        self.value = r.readWideString(s);
    
    def write(self, w):
        wBytes = self.value.encode("UTF-16");
        l = len(wBytes)
        w.writeInt(l);
        w.writeWideString(wBytes);

    def set(self, b):
        self.value = b
    
    def get(self):
        return self.value
