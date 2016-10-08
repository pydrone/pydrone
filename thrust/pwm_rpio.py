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

from RPIO.PWM import Servo
from RPIO import PWM

class PwmRPIO:
    def __init__(self,pin_list):
        self.NUM_CH = len(pin_list)
        self._pin_list = pin_list
        self._servo = None
        PWM.set_loglevel(PWM.LOG_LEVEL_ERRORS)

    def _set_ch_duty(self, ch, duty):
        self._servo.set_servo(self._pin_list[ch], duty)
 
    def init_all_ch(self,period, duty):
        self._servo = Servo(subcycle_time_us = period, pulse_incr_us = 1)
        self.set_duty([duty]*self.NUM_CH)

    def set_duty(self, duty):
        for ch, val in enumerate(duty):
            self._set_ch_duty(ch, val)
        PWM.seek(0,0)

    def stop(self):
        if self._servo != None:
            for ch in range(self.NUM_CH):
                self.stop_servo(self._pin_list[ch])

if __name__=="__main__":
    import time
    import sys
    from moter import Moter

    m = Moter(PwmRPIO([17,18,27,22]))
    if len(sys.argv)!=5:
        m.update([0, 0, 0, 0]) 
    else:
        output =[float(x) for x in sys.argv[1:5]]
        m.update(output) 
    input("hit any key to stop")
    m.update([0, 0, 0, 0]) 
