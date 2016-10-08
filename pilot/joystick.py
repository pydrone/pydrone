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

import time

#from . pilot.Pilot import CMD_START as CMD_START
#from . pilot.Pilot import CMD_STOP as CMD_STOP
#from . pilot.Pilot import CMD_EMERGENCY as CMD_EMERGENCY

AXIS_YAW = 0
AXIS_PITCH = 3
AXIS_ROLL = 2
AXIS_THROTTLE = 1
DIR_YAW = -1
DIR_PITCH = -1
DIR_ROLL = 1
DIR_THROTTLE = -1

BUTTON_START = 8
BUTTON_TRIM_UP = 5 
BUTTON_TRIM_DOWN = 4
BUTTON_TRIM_RIGHT = 3
BUTTON_TRIM_LEFT = 0
BUTTON_TRIM_FORWARD = 1
BUTTON_TRIM_BACK = 2

class WatchDog:
    def __init__(self, is_alive_func, check_interval_sec):
        self.last_result = True
        self.last_check_time = None
        self.check_interval_sec = check_interval_sec
        self.is_alive_func = is_alive_func

    def is_alive(self):
        ''' return False if watchdog find fail.'''
        current_time = time.time()

        # at 1st time just return True
        if(self.last_check_time is None):
            self.last_check_time = current_time
            self.last_result = True
            return self.last_result

        # Return last_reslult if elapsed time is not reach to check_interval
        if(current_time - self.last_check_time < self.check_interval_sec):
            return self.last_result
        
        self.last_check_time = current_time
        self.last_result = self.is_alive_func()
        return self.last_result

class Joystick:
    
    def __init__(self, js_io):
       self.js_io = js_io
       self.watch_dog = WatchDog(js_io.is_alive, 1.0)
       self.last_cmd = None

    def is_all_zero(data_list):
        for x in data_list:
            if x != 0:
                return False
        return True

    def cmd(self):
        from . pilot import Pilot
        if not self.watch_dog.is_alive():
            return Pilot.CMD_EMERGENCY
        b = self.js_io.button
        throttle = DIR_THROTTLE * self.js_io.axis[AXIS_THROTTLE] / float(0x7fff)
        if throttle == -1:
            cmd = Pilot.CMD_THROTTLE_ZERO
        elif b[BUTTON_TRIM_UP]:
            cmd = Pilot.CMD_TRIM_UP
        elif b[BUTTON_TRIM_DOWN]:
            cmd = Pilot.CMD_TRIM_DOWN
        elif b[BUTTON_TRIM_LEFT]:
            cmd = Pilot.CMD_TRIM_LEFT
        elif b[BUTTON_TRIM_RIGHT]:
            cmd = Pilot.CMD_TRIM_RIGHT
        elif b[BUTTON_TRIM_FORWARD]:
            cmd = Pilot.CMD_TRIM_FORWARD
        elif b[BUTTON_TRIM_BACK]:
            cmd = Pilot.CMD_TRIM_BACK
        else:
            cmd = Pilot.CMD_NOP
        is_new_cmd = self.last_cmd != cmd
        self.last_cmd = cmd
        if(is_new_cmd):
            return cmd
        else:
            return Pilot.CMD_NOP
            
        


    def axis(self):
        yaw = self.js_io.axis[AXIS_YAW] / 0x7fff * DIR_YAW
        pitch = self.js_io.axis[AXIS_PITCH] / 0x7fff * DIR_PITCH
        roll = self.js_io.axis[AXIS_ROLL] / 0x7fff * DIR_ROLL
        throttle = DIR_THROTTLE * self.js_io.axis[AXIS_THROTTLE] / float(0x7fff) 
        return [yaw, pitch, roll], throttle


if __name__=="__main__":
    import time
    from joystick_udp import JoystickUDP
    js = Joystick(JoystickUDP())
    while True:
        ypr,t = js.axis() 
        cmd = js.cmd()
        print("{0:.2f},{1:.3f},{2:.3f},{3:.3f},{4}".format(ypr[0], ypr[1], ypr[2], t, cmd))
        time.sleep(0.1)
