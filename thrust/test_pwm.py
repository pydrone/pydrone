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
import time
import sys


def main():
    if len(sys.argv)!=2:
        return
    PWM.set_loglevel(PWM.LOG_LEVEL_ERRORS)
    servo = Servo(subcycle_time_us = 10000, pulse_incr_us = 1)
    servo.set_servo(23, int(sys.argv[1]))
    servo.set_servo(24, int(sys.argv[1]))
    servo.set_servo(25, int(sys.argv[1]))
    servo.set_servo(8, int(sys.argv[1]))
    input("hit Enber key")
    servo.set_servo(23, int(1000))
    servo.set_servo(24, int(1000))
    servo.set_servo(25, int(1000))
    servo.set_servo(8, int(1000))
    input("hit Enber key")

main()
