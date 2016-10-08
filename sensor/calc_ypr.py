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
import math
from struct import pack, unpack
from math import atan, atan2, sqrt

def wrap_180(x):
    if x < -180:
        return x+360
    if x > 180:
        return x-360
    else:
        return x

class ComplementaryFilter:
    def __init__(self, rate=0.98):
        self.rate = rate
        self.out = 0.0

    def filter(self, angle, angular_velocity, dt):
        self.out = self.rate * (self.out + angular_velocity * dt) + (1-self.rate) * angle
        return self.out

class CalcYPR:
    RAD_TO_DEG = 180/math.pi
    def __init__(self, rate=0.98):
        self.yaw = 0.0
        self.filter_pitch = ComplementaryFilter()
        self.filter_roll = ComplementaryFilter()
        self.last_time = 0

    def calc_ypr(self, acc, gyro, acq_time):
        ax, ay, az = acc
        gx, gy, gz = gyro
        
        dt = acq_time - self.last_time if self.last_time != 0 else 0 
        self.last_time = acq_time

        pitch, roll = self.pitch_roll(ax, ay, az)
        self.yaw = wrap_180(self.yaw + gz * dt)

        return (self.yaw, self.filter_pitch.filter(pitch, gy, dt), self.filter_roll.filter(roll, gx, dt))
    
    @staticmethod
    def pitch_roll(ax, ay, az):
        RAD_TO_DEG = 180/math.pi
        try:
            roll = atan2(ay, az) * RAD_TO_DEG
        except ZeroDivisionError:
            roll = 90 if ay > 0 else -90
        try:
            pitch = atan(-ax / sqrt(ay * ay + az * az)) * RAD_TO_DEG
        except ZeroDivisionError:
            pitch = 90 if -ax > 0 else -90 
        return (pitch, roll)

if __name__=="__main__":

    datas = '''\
1480593690.3763    0.40    0.48    0.87   80.98 -115.50  -43.17
1480593690.3862    0.40    0.49    0.85   68.94 -110.92  -35.48
1480593690.3960    0.42    0.49    0.84   55.34 -105.25  -27.60
1480593690.4059    0.45    0.49    0.83   40.93  -98.68  -19.50
1480593690.4167    0.48    0.49    0.82   25.74  -91.33  -11.34
1480593690.4266    0.49    0.49    0.81    9.34  -83.47   -3.40
1480593690.4364    0.49    0.48    0.81   -7.84  -75.39    4.08
1480593690.4463    0.48    0.48    0.81  -24.24  -67.31   11.12
1480593690.4561    0.47    0.47    0.80  -39.80  -58.89   18.05
1480593690.4659    0.47    0.47    0.79  -54.86  -49.90   25.05
1480593690.4758    0.49    0.47    0.78  -68.76  -40.62   32.23
1480593690.4866    0.50    0.47    0.78  -80.95  -31.24   39.53
1480593690.4965    0.52    0.46    0.78  -91.58  -21.85   46.83
1480593690.5063    0.53    0.45    0.77 -101.60  -12.72   53.80
1480593690.5162    0.53    0.45    0.77 -111.14   -4.24   60.23
1480593690.5260    0.53    0.44    0.78 -119.79    3.31   65.94
1480593690.5359    0.52    0.43    0.79 -127.89   10.08   70.88
1480593690.5467    0.52    0.41    0.79 -135.71   16.41   74.98
1480593690.5566    0.52    0.38    0.80 -142.69   22.37   78.34'''

    calc_ypr = CalcYPR()
    data_list = datas.split("\n")
    for data in data_list:
        d_list = data.split()
        acq_time, ax, ay, az, gx, gy, gz = [float(x) for x in d_list]
        acc = (ax, ay, az)
        gyro = (gx, gy, gz)
        ypr = calc_ypr.calc_ypr(acc, gyro, acq_time)
        print("{:7.2f} {:7.2f} {:7.2f}".format(*ypr))
