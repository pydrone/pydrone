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

class Led:
    flag = None

    @classmethod
    def change(cls, flag):
        ''' change led status. if flag is True led is ON'''
        if cls.flag is None:
            ''' it is first time'''
            cls.clear_trigger()

        cls.flag = flag
        if flag:
            val = "0"
        else:
            val = "1" 
        with open("/sys/class/leds/led0/brightness", 'w') as f:
            f.write(val)
    
    @classmethod
    def toggle(cls):
        cls.change(not cls.flag)
        
    @staticmethod
    def clear_trigger():
        with open("/sys/class/leds/led0/trigger", "w") as f:
            f.write("none")

