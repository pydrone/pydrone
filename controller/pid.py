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

def guard(value, value_guard):
    if(value_guard is not None):
        if(value > value_guard):
            return value_guard
        if(value < -value_guard):
            return -value_guard
    return value

class PID:
    def __init__(self,Kp, Ki, Kd, guard=None):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.inegration = 0
        self.error_last = None
        self.guard = guard
        if self.Ki != 0:
            self.guard *= self.Kp/self.Ki
    
    def out(self, setpoint, y_value, dt):
        """get pid output.
        setpoint: setpoint
        y_value: feedback value from plant
        dt: delta t"""

        error = setpoint - y_value
        self.inegration = guard(self.inegration + error*dt, self.guard)
        d_error = error - self.error_last if self.error_last is not None else 0 
        u = self.Kp*error + self.Ki*self.inegration + self.Kd*d_error/dt
        self.error_last = error
        return u

        
    