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

#Type Codes

UNDEFINED = 0
BYTE = 1
SHORT = 2
INTEGER = 3
LONG = 4
SHORTSTRING = 5
CHAR = 6
DOUBLECHAR = 7
LONGSTRING = 8
WIDESTRING = 9
ARRAY = 10
RECORD = 11
    
#Type mappings to single char

CHAR_BYTE = 'B'
CHAR_SHORT = 'X'
CHAR_INTEGER = 'I'
CHAR_LONG = 'L'
CHAR_SHORTSTRING = 's'
CHAR_CHAR = 'C'
CHAR_DOUBLECHAR = 'D'
CHAR_LONGSTRING = 'S'
CHAR_WIDESTRING = 'W'
CHAR_ARRAY = 'A'
CHAR_ARRAYU = 'a' # Just Create an array, not type or number of elements is assigned
CHAR_RECORD = 'R'
CHAR_UNDEFINED = 'U'

# Protocols
   
PROT_UDP = 0
PROT_TCP = 1
PROT_BLUETOOTH_UDP = 2

