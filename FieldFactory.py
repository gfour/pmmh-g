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
import Fields

from util.Streamers import Writer  

def fieldFromCode(code):
    # Type mappings to single char
    if code == Consts.CHAR_BYTE: 
        return Fields.ByteField()
    elif code == Consts.CHAR_SHORT: 
        return Fields.CharField();
    elif code == Consts.CHAR_INTEGER: 
        return Fields.IntegerField();
    elif code == Consts.CHAR_LONG: 
        return Fields.LongField();
    elif code == Consts.CHAR_SHORTSTRING: 
        return Fields.ShortStringField();
    elif code == Consts.CHAR_CHAR: 
        return Fields.CharField();
    elif code ==  Consts.CHAR_DOUBLECHAR: 
        return Fields.DoubleCharField();
    elif code == Consts.CHAR_LONGSTRING: 
        return Fields.LongStringField();
    elif code == Consts.CHAR_WIDESTRING: 
        return Fields.WideStringField();
    elif code == Consts.CHAR_ARRAY or code == Consts.CHAR_ARRAYU:
        return Fields.ArrayField();
    elif code == Consts.CHAR_RECORD: 
        return None # not implemented
    elif code == Consts.CHAR_UNDEFINED: 
        return None
    else:
        return None;
    
   
def readFields(fields, dIn):
    for x in fields:
        x.read(dIn)


def writeFields(fields):
    data = Writer()        
    for x in fields:
        x.write(data)
    return data.stream


def fieldFromCodeList(codelist):
    v = []
    s = len(codelist)
    i = 0
    c=""
    while(i<s):
        c = codelist[i]
        v.append(fieldFromCode(c))
        if(c=="a"):
            a = v[-1]
            a.setNelemAndType( int(codelist[i+2]) << 8 + int(codelist[i+3]), codelist[i+1])
            i+=3
        i+=1
    return v

#TODO: Check garbage collector for field destruction
def destroyFieldVector(v):
    #"if (v!=None):
    #    v.removeAllElements()
    #v=None
    pass
    
    
