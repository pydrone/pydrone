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

from moter.Moter import NUM_CH 

class PwmACME:
    PWM_DISABLE = 0
    PWM_ENABLE = 1
    PWM_SCALE = 500 # 1countup = 500us

    def __init__(self, devname_base = "/sys/class/pwm/pwmchip0"):
        self.devname_base = devname_base

    def write_digit(self, path, val):
        with open(self.devname_base + path , "wt") as f:
            f.write(str(val))

    def set_pwm_val(self, ch, path, val):
        self.write_digit("/pwm%d/%s" % (ch, path), val)

    def export_ch(self, ch):
        try:
            self.write_digit("/export", ch)
        except IOError:
            pass

    def init_ch(self, ch, period, duty):
        self.export_ch(ch)
        self.set_pwm_val(ch, "enable", PwmACME.PWM_DISABLE)
        self.set_pwm_val(ch, "period", period * PwmACME.PWM_SCALE)
        self.set_pwm_val(ch, "duty_cycle", duty * PwmACME.PWM_SCALE)
        self.set_pwm_val(ch, "enable", Pwm.PWM_ENABLE)

    def init_all_ch(self,period, duty):
        for i in range(NUM_CH):
            self.init_ch(i,period, duty)

    def set_duty(self, duty):
        for ch, val in enumerate(duty):
            self.set_pwm_val(ch, "duty_cycle", val * Pwm.PWM_SCALE)

    def stop(self):
        for ch in range(NUM_CH):
            self.set_pwm_val(ch, "enable", Pwm.PWM_DISABLE)


