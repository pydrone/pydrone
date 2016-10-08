#!/usr/bin/python3

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

import sys
import socket
import time
from struct import pack 

from pilot.joystick_hid import JoystickHID

if(len(sys.argv) ==3):
    ipaddr = sys.argv[1]
    port = int(sys.argv[2])
    addr=(ipaddr, port)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
    with JoystickHID() as jsio:
        last_p = None
        while True:
            cmd = jsio.button
            axis = jsio.axis
            p = pack('hhhhbbbbbbbbbb' ,*axis[0:4]+cmd[0:10])
            if p != last_p:
                print(cmd[0:10],axis[0:4])
            s.sendto(p, addr)
            time.sleep(0.05) 
            last_p = p

else:
    print("Usage: wifi_joystick.py ip_address port")



