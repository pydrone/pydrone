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


import math
import json

def limit(value, limit):
    if value > limit:
        return limit
    if value < -limit:
        return -limit
    return value
        
def dot(in_a,in_b):
    out = []
    for x in in_a:
        v_sum = 0
        for a,b in zip(x, in_b):
            v_sum += a*b
        out.append(v_sum)
    return out

class BodyCoefficient:
    M = [[1,1,1,1],[1,-1,1,-1],[1,1,-1,-1],[1,-1,-1,1]]

    def __init__(self,mass, L, Ixx, Iyy, Izz, moter):
        self.mass = mass
        self.L = L
        self.Ixx = Ixx
        self.Iyy = Iyy
        self.Izz = Izz
        self.moter_coefficient = moter

    def tau2force_kg(self, thrust, tau):
        tau_yaw, tau_pitch, tau_roll = tau
        f_thrust = self.mass * thrust / 4
        f_pitch = limit(self.Ixx * tau_pitch / self.L / 4, f_thrust * 0.5)
        f_roll = limit(self.Iyy * tau_roll / self.L / 4, f_thrust * 0.5)
        f_yaw = limit(self.Izz * tau_yaw / 4, f_thrust *0.5)
        out = dot(self.M, [f_thrust, f_yaw, f_pitch, f_roll])
        return out

    def force2esc(self, ch, force_kg):
        '''
        force_kg 力の強さkg
        return escに出力する0~1の値    
        '''
        a,b,c = self.moter_coefficient[ch]
        x = b**2 -4 * a * (c - force_kg * 1000)
        if x <= 0:
            return 0
        return (-b + math.sqrt(x))/(2 * a)


class BodyCoefficient_from_file(BodyCoefficient):
    def __init__(self, filename = "_body_coefficient.json"):
        f = open(filename, "rt")
        dic = json.load(f)
        f.close()
        BodyCoefficient.__init__(self,  **dic)

