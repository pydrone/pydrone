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

from thrust.moter import Moter
from thrust.pwm_rpio import PwmRPIO

def main():
    import time
    import sys

    m = Moter(PwmRPIO([23,24,25,8]))

    for i in range(4):
        for j in range(0,80,2):
            out = [0]*4
            out[i] = j/100
            m.update(out) 
            print ("ch={}, power = {}".format(i,out[i]))
            input("---hit Enber key to next")

    m.update([0, 0, 0, 0]) 

main()
