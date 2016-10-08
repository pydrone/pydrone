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

from .threading_w_stop import ThreadWStop
from .joystick_hid import JoystickHID
from .joystick_udp import JoystickUDP
from .joystick import Joystick

def wrap_180(x):
    if x < -180:
        return x+360
    if x > 180:
        return x-360
    else:
        return x

class Pilot:
    METHOD_UDP=1
    METHOD_HID=2
    CMD_NOP = 0
    CMD_THROTTLE_ZERO = 1
    CMD_EMERGENCY = 2
    CMD_TRIM_UP = 3
    CMD_TRIM_DOWN = 4
    CMD_TRIM_LEFT = 5
    CMD_TRIM_RIGHT = 6
    CMD_TRIM_FORWARD = 7
    CMD_TRIM_BACK = 8
    
    def __init__(self, controll_method=METHOD_UDP, throttle_base = 0.8, startup_time = 5.0):
        self.trim_forward = 0
        self.trim_right = 0
        self.trim_up = 0
        self.throttle_base = 0
        self.throttle_base_target = throttle_base
        self.startup_time = startup_time
        if controll_method == Pilot.METHOD_UDP:
            js_io = JoystickUDP()
        else:
            js_io = JoystickHID()
        self._js = Joystick(js_io)
        self.initialize()

    def initialize(self):
        self.last_yaw_setpoint = None
        self.startup_done = False
        self.start_time = time.time()

    def linear_throttle_up(self):
        if self.startup_done:
            return
        rate = (time.time() - self.start_time) / self.startup_time
        if(rate>=1):
            self.startup_done = True
            rate = 1
        self.throttle_base =  self.throttle_base_target * rate

    def trim_cmd(self, cmd):
        if cmd == Pilot.CMD_TRIM_UP:
            self.throttle_base += 0.01
        elif cmd == Pilot.CMD_TRIM_DOWN:
            self.throttle_base += -0.01
        elif cmd == Pilot.CMD_TRIM_LEFT:
            self.trim_right += -0.02
        elif cmd == Pilot.CMD_TRIM_RIGHT:
            self.trim_right += 0.02
        elif cmd == Pilot.CMD_TRIM_FORWARD:
            self.trim_forward += 0.02
        elif cmd == Pilot.CMD_TRIM_BACK:
            self.trim_forward += -0.02
        else:
            return
        print("trim_throttle/forward/right ={:7.3f} / {:7.3f} / {:7.3f}".format(self.throttle_base, self.trim_forward, self.trim_right))
            
    def get_setpoint(self, angle, angular_velocity, acc):
        self.linear_throttle_up()
        ypr, throttle_js = self._js.axis()
        yaw = self.yaw_ctrl(ypr[0], angle[0])
        pitch, roll = self.pitch_roll_ctrl(ypr[1],ypr[2])
        throttle = self.throttle_ctrl(throttle_js) 
        return (throttle, [yaw, pitch, roll])
        
    def get_cmd(self):
        cmd = self._js.cmd()
        self.trim_cmd(cmd)
        return cmd

    def throttle_ctrl(self, throttle):
        return self.throttle_base + throttle * 0.6

    def pitch_roll_ctrl(self, pitch, roll):
        roll += self.trim_right
        pitch += self.trim_forward
        # -20 degree to 20 degree
        return [pitch*20, roll*20]

    def yaw_ctrl(self, joystick_val, angle):
        # if last value is not known use current value
        if self.last_yaw_setpoint == None:
            self.last_yaw_setpoint = angle

        JOYSTICK_DEAD = 0.05  
        if abs(joystick_val) < JOYSTICK_DEAD:
            #no need change setpoint
            setpoint = self.last_yaw_setpoint
        else:
            #update setpoint
            if joystick_val < 0:
                joystick_val += JOYSTICK_DEAD 
            else:
                joystick_val -= JOYSTICK_DEAD 
            # move setpoint to joystick direction
            # maximaum speed is 30deg/sec
            setpoint = self.last_yaw_setpoint + joystick_val * 30 / 100 # 100 update per sec 
            setpoint = wrap_180(setpoint)
        self.last_yaw_setpoint = setpoint
        return setpoint
            
