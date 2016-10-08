#!/usr/bin/python
#    Copyright (C) 2017  Masahiro Tsuji
#
#    This file is part of PyDrone.
#
#    PyDrone is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    PyDrone is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with PyDrone.  If not, see <http://www.gnu.org/licenses/>.
#

# Python Standard Library Imports
import os
import fcntl
from struct import pack, unpack

# External Imports
pass

# Custom Imports
pass

class I2CBus:
    
    I2C_SLAVE = 0x0703
    def __init__(self, busnumber=1):
        self.busnumber = busnumber
        self.fd = os.open("/dev/i2c-{}".format(busnumber), os.O_RDWR)
        self.addr = None

    def _set_addr(self, addr):
        if self.addr != addr:
            ret = fcntl.ioctl(self.fd, I2CBus.I2C_SLAVE, addr)
            self.addr = addr
            return ret
        else:
            return 0
    
    def _write_byte(self, b_data):
        return os.write(self.fd, pack('B', b_data))
        
    def _write(self, data_bytes):
        return os.write(self.fd, data_str)
    
    def write(self, address, reg, data):
        data = pack('B', reg) + data
        self._set_addr(address)
        return os.write(self.fd,data)

    def read(self, address, reg, len):
        self._set_addr(address)
        self._write_byte(reg)
        return os.read(self.fd,len)

class I2CDevice:
    def __init__(self, address, i2c = I2CBus()):
        self.address = address
        self.i2c = i2c

    def readBit(self, reg, bitNum):
        return self.readBits(reg, bitStart, 1)
    
    def writeBit(self, reg, bitNum, data):
        return self.writeBits(reg, bitNum, 1, data)
    
    def readBits(self, reg, bitStart, length):
        b = self.readU8(reg)
        b >>= (bitStart - length + 1)
        b &= (1<<length)-1
        return b
    
    def writeBits(self, reg, bitStart, length, data):
        b = self.readU8(reg)
        mask = ((1<<length)-1) << (bitStart - length + 1)
        data <<= (bitStart - length + 1)
        data &= mask
        b &= ~(mask)
        b |= data
        return self.writeU8(reg, b)

    def readBytes(self, reg, length):
        return self.i2c.read(self.address, reg, length)

    def writeU8(self, reg, data_U8):
        return self.i2c.write(self.address, reg, pack('B', data_U8))

    write8 = writeU8
    
    def writeS16(self, reg, data_S16):
        return self.i2c.write(self.address, reg, pack('>h', data_S16))

    def readU8(self, reg):
        # Read an unsigned byte from the I2C device
        result = self.i2c.read(self.address, reg, 1)
        return unpack("B", result)[0]

    def readS8(self, reg):
        # Read an unsigned byte from the I2C device
        result = self.i2c.read(self.address, reg, 1)
        return unpack("b", result)[0]

    def readU16(self, reg):
        # Read an unsigned byte from the I2C device
        result = self.i2c.read(self.address, reg, 2)
        return unpack(">H", result)[0]

    def readS16(self, reg):
        # Read an unsigned byte from the I2C device
        result = self.i2c.read(self.address, reg, 2)
        return unpack(">h", result)[0]

