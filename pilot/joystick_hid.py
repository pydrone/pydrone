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
import time

from .threading_w_stop import ThreadWStop

MAX_AXIS = 4
MAX_BUTTON = 10
JS_EVENT_BUTTON = 0x01 
JS_EVENT_AXIS = 0x02 
JS_EVENT_INIT = 0x80 

class JoystickHID:
    button = [0] * MAX_BUTTON
    axis = [0] * MAX_AXIS 

    def __init__(self, devname="/dev/input/js0"):
        self.devname = devname
        self.watch_dog = False
        self.f = None
        self.open_js()
        self.__start_thread()

    def is_alive(self):
        if self.watch_dog == False:
            return False
        self.watch_dog = False
        return True

    def open_js(self):
        if self.f is not None:
            if not self.f.closed:
                self.f.close()
        while True:
            try:
                self.f = open(self.devname,"rb")
            except FileNotFoundError:
                print("device {} not found".format(self.devname))
                time.sleep(1)
            else:
                return
            
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
        unpack js_event data and store to array
          #struct js_event {
          #  __u32 time;     /* event timestamp in milliseconds */
          #  __s16 value;    /* value */
          #  __u8 type;      /* event type */
          #  __u8 number;    /* axis/button number */
          #};
        """
        try:
            buf = self.f.read(8) # sizeof(struct js_event)==8
        except (OSError, ValueError):
            self.open_js()
            return
        time, value, type, number = struct.unpack('IhBB', buf)
        self.watch_dog = True
        #print(time, value, type, number)
        if type == JS_EVENT_BUTTON:
            if number < MAX_BUTTON: 
                self.button[number] = value
        elif type == JS_EVENT_AXIS:
            if number < MAX_AXIS:
                self.axis[number] = value

if __name__ == "__main__":

    with JoystickHID() as jsio:
        while True:
          print(jsio.axis, jsio.button)
          time.sleep(0.1)
 

