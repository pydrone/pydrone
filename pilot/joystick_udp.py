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

import struct
import socket
import time

from .threading_w_stop import ThreadWStop

MAX_AXIS = 4
MAX_BUTTON = 10
JS_EVENT_BUTTON = 0x01 
JS_EVENT_AXIS = 0x02 
JS_EVENT_INIT = 0x80 
PACKET_LEN = 19

class JoystickUDP:
    button = [0] * MAX_BUTTON
    axis = [0] * MAX_AXIS 

    def __init__(self, LISTEN_ADDR =("0.0.0.0", 8000)):
        self.watch_dog = False
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        self.udp_socket.bind(LISTEN_ADDR)
        self.__start_thread()

    def is_alive(self):
        if self.watch_dog == False:
            return False
        self.watch_dog = False
        return True

    def __enter__(self):
        return self 

    def __start_thread(self):
        self.th = ThreadWStop(target = self.update_loop) 
        self.th.start()
        return self

    def __exit__(self, type, value, traceback): 
        self.th.stop()

    def update_loop(self,**kwargs):
        while not ThreadWStop.recive_exit_request(kwargs):
            self.update() 

    def update(self):
        """
        """
        data, addr = self.udp_socket.recvfrom(PACKET_LEN)
        d = struct.unpack('hhhhbbbbbbbbbb', data)
        self.axis[0:4] = d[0:4]
        self.button[0:10] = d[4:14]
        self.watch_dog = True

if __name__ == "__main__":

    with JoystickUDP() as jsio:
        while True:
          print(jsio.axis, jsio.button)
          time.sleep(0.1)
 

