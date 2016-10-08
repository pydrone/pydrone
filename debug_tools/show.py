# coding: utf-8
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

from optparse import OptionParser, OptionValueError
from datetime import datetime
import matplotlib.pyplot as plt
import json
import sys
from attitude_log import AttitudeLog

def load_log(filename, start, end):
    if start is None:
        time_start = 0
    else:
        time_start = float(start)
    if end is None:
        time_end = None
    else:
        time_end = float(end)
    log = AttitudeLog()
    log.load(filename)
    log.show_info()
    d = log.get_log()
    for i, e in enumerate(d):
        t = e['time']
        if t >= time_start:
            break
    point_s = i
    if time_end is not None:
        for i, e in enumerate(d[point_s:]):
            t = e['time']
            if t >= time_end:
                break
        point_e = point_s + i + 1
    else:
        point_e = len(d)
    
    return d[point_s:point_e]

def show_ypr(d):
    title_list = ["yaw", "pitch", "roll"]
    label_list = ["angle", "setpoint"] 
    style_list = ["-r", "-g"] 

    x = [e['time'] for e in d]
    for i in range(3):
        y_list = []
        y_list.append([e['angle_ypr'][i] for e in d])
        y_list.append([e['pilot_ypr'][i] for e in d])
        plt.subplot(3, 1, i+1)                    
        for y, label, style in zip(y_list, label_list, style_list):
            plt.plot(x, y,style, label=label)
            plt.legend()
        plt.grid(True)
        plt.title(title_list[i])
        plt.xlim(left = x[0], right= x[-1])
        plt.legend(loc="upper left")
    plt.show()

def show_time(d):
    title_list = ["time"]
    label_list = ["samping", "get", "out"]
    style_list = ["-r", "-g", "-b"] 

    x = [e['time'] for e in d]
    N = len(title_list)
    for i in range(N):
        y_list = []
        y_list.append([e['time_log'][0] for e in d])
        y_list.append([e['time_log'][1] for e in d])
        y_list.append([e['time_log'][2] for e in d])
        plt.subplot(N, 1, i+1)                    
        for y, label, style in zip(y_list, label_list, style_list):
            plt.plot(x, y,style, label=label)
            plt.legend()
        plt.grid(True)
        plt.title(title_list[i])
        plt.ylim(0,0.02)
        plt.xlim(left = x[0], right= x[-1])
        plt.legend(loc="upper left")
    plt.show()

def show_sensor(d):
    title_list = ["angle","gyro","accel"]
    label_list = ["yaw", "pitch", "roll"]
    style_list = ["-r", "-g", "-b"] 
    d_key = ["angle_ypr", "gyro_ypr", "raw_acc"]

    x = [e['time'] for e in d]
    N = len(title_list)
    for i in range(N):
        
        y_list = []
        y_list.append([e[d_key[i]][0] for e in d])
        y_list.append([e[d_key[i]][1] for e in d])
        y_list.append([e[d_key[i]][2] for e in d])
        plt.subplot(N, 1, i+1)                    
        for y, label, style in zip(y_list, label_list, style_list):
            plt.plot(x, y,style, label=label)
            plt.legend()
        plt.grid(True)
        plt.title(title_list[i])
        plt.xlim(left = x[0], right= x[-1])
        plt.legend(loc="upper left")
    plt.show()

def show_pidout(d):
    title_list = ["angle","dot_angle","tau"]
    label_list = ["yaw", "pitch", "roll"]
    style_list = ["-r", "-g", "-b"] 
    d_key = ["angle_ypr", "gyro_ypr", "out_tau"]
    ymax_list = [20, 100, 300]

    x = [e['time'] for e in d]
    N = len(title_list)
    for i in range(N):
        
        y_list = []
        y_list.append([e[d_key[i]][0] for e in d])
        y_list.append([e[d_key[i]][1] for e in d])
        y_list.append([e[d_key[i]][2] for e in d])
        plt.subplot(N, 1, i+1)                    
        for y, label, style in zip(y_list, label_list, style_list):
            plt.plot(x, y,style, label=label)
            plt.legend()
        plt.grid(True)
        plt.title(title_list[i])
        plt.xlim(left = x[0], right= x[-1])
        plt.ylim(-ymax_list[i], ymax_list[i])
        plt.legend(loc="upper left")
    plt.show()

def show_throttle(d):
    title_list = ["throttle"]
    label_list = ["pilot", "out"]
    style_list = ["-r", "-g"] 
    d_key = ["pilot_throttle", "out_throttle"]

    x = [e['time'] for e in d]
    N = len(title_list)
    for i in range(N):
        
        y_list = []
        y_list.append([e[d_key[0]] for e in d])
        y_list.append([e[d_key[1]] for e in d])
        plt.subplot(N, 1, i+1)                    
        for y, label, style in zip(y_list, label_list, style_list):
            plt.plot(x, y,style, label=label)
            plt.legend()
        plt.grid(True)
        plt.title(title_list[i])
        plt.xlim(left = x[0], right= x[-1])
        #plt.ylim(-ymax_list[i], ymax_list[i])
        plt.legend(loc="upper left")
    plt.show()


if __name__ == "__main__":
    function_table = {
        "pid": show_ypr,
        "time": show_time,
        "sensor": show_sensor,
        "pid_out": show_pidout,
        "throttle": show_throttle,
    }
    usage = "usage: %prog [options] cmd file_name"
    parser = OptionParser(usage)
    parser.add_option(
     "-s", "--start",
     action="store", type="string", dest="start",
     default=None,
     help="start time")
    parser.add_option(
     "-e", "--end",
     action="store", type="string", dest="end",
     default=None,
     help="end time")
    (options, args) = parser.parse_args()
    data = load_log(args[1], options.start, options.end)
    print(args[0])
    func = function_table[args[0]]
    func(data)


