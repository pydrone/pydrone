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
 
class Moter:

    SERVO_MIN = 1000 # 1ms
    SERVO_MAX =  2020 # 2ms
    PWM_PERIOD = 20000 # 20ms
    NUM_CH = 4

    def __init__(self,pwm):
        self.pwm = pwm 
        self.pwm.init_all_ch(Moter.PWM_PERIOD, Moter.SERVO_MIN)
        self.running = False
        self.BLHeli_startup_seq()

    def stop(self):
        self.update([0.0] * Moter.NUM_CH)
        self.running = False

    def soft_start(self, float_list, startup_time=1.0):
        for i in range(1,11):
            output = [f * i/10 for f in float_list]
            self.update_sub(output)
            time.sleep(startup_time/10)

    def BLHeli_startup_seq(self):
        """
        Start up BLHeli ESC
        """
        self.update([0.2] * Moter.NUM_CH)
        time.sleep(1)
        self.update([0] * Moter.NUM_CH)
        

    def update(self, float_list, soft_start=False, startup_time=1.0):
        if soft_start and self.running is False:
            self.soft_start(float_list, startup_time)
            return
        self.update_sub(float_list)
    
    def update_sub(self, float_list):
        self.running = True
        if len(float_list) != Moter.NUM_CH:
            raise AssertionError
        duty = []
        for i in range(Moter.NUM_CH):
            val = float_list[i]
            if val > 1.0:
                val = 1
            if val < 0:
                val = 0 
            duty.append(int((Moter.SERVO_MIN + val * (Moter.SERVO_MAX-Moter.SERVO_MIN) ))) 
        self.pwm.set_duty(duty)

    def __enter__(self):
        return self

    def __exit__(self ,type, value, traceback):
        self.stop()

