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

from .pid import PID

class Controller:
    def __init__(self, dt, pid_stable_const, pid_angle_const):
        self.pid_stable = {}
        self.pid_angle = {}
        for key in ["yaw", "pitch", "roll"]:
            self.pid_stable[key] = PID(**pid_stable_const[key])
            self.pid_angle[key] = PID(**pid_angle_const[key])
        self.dt = dt
    def out(self, angle, angular_velocity, setpoint):
        angle_control = {}
        control = {}
        for i, key in enumerate(["yaw", "pitch", "roll"]):
            angle_control[key] = self.pid_angle[key].out(setpoint[i], angle[i], self.dt)
            if key == "yaw":
                control[key] = angle_control[key]
            else:
                control[key] = self.pid_stable[key].out(angle_control[key], angular_velocity[i], self.dt)

        return [control["yaw"], control["pitch"], control["roll"]]
   
