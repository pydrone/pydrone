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

from .mpu6050_lib import AccGyro
from .calc_ypr import CalcYPR


class Sensor:
    def __init__(self):
        self.calc_ypr = CalcYPR()
        self.acc_gyro = AccGyro()
    def get(self):
        acc, gyro, retrieve_time = self.acc_gyro.get()
        angle_ypr = self.calc_ypr.calc_ypr(acc, gyro, retrieve_time)
        angular_velocity_ypr = (gyro[2], gyro[1], gyro[0])
        return (retrieve_time,angle_ypr ,angular_velocity_ypr, acc)
    def sampling_interval(self):
        return self.acc_gyro.SamplingInterval
