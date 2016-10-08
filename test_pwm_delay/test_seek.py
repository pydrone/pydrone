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

import sys, os
sys.path.append(os.pardir)

#from moter import Moter
#from pwm_rpio import PwmRPIO
from RPIO.PWM import Servo
from RPIO import PWM
import RPi.GPIO as GPIO
import time

trigger_pin = 40

GPIO.setmode(GPIO.BOARD) 
GPIO.setup(trigger_pin, GPIO.OUT)
GPIO.setwarnings(False)

PWM.setup(pulse_incr_us=1)
PWM.init_channel(0, subcycle_time_us=10000)

# Add some pulses to the subcycle
PWM.add_channel_pulse(0, 20, 0, 1000)
PWM.set_loglevel( PWM.LOG_LEVEL_ERRORS)
# Stop PWM for specific GPIO on channel 0
while True:
    GPIO.output(trigger_pin, 0)
    #PWM.cleanup()
    #PWM.set_loglevel( PWM.LOG_LEVEL_ERRORS)
    #PWM.setup(pulse_incr_us=1)
    #PWM.init_channel(0, subcycle_time_us=10000)
    #PWM.clear_channel_gpio(0, 20)
    PWM.add_channel_pulse(0, 20, 0, 1000)
    PWM.seek(0,0)
    time.sleep(0.020)

    GPIO.output(trigger_pin, 1)
    #PWM.cleanup()
    #PWM.set_loglevel( PWM.LOG_LEVEL_ERRORS)
    #PWM.setup(pulse_incr_us=1)
    #PWM.init_channel(0, subcycle_time_us=10000)
    #PWM.clear_channel_gpio(0, 20)
    PWM.add_channel_pulse(0, 20, 0, 2000)
    PWM.seek(0,0)
    time.sleep(0.020)
        

PWM.clear_channel_gpio(0, 17)

# Shutdown all PWM and DMA activity
PWM.cleanup()
