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

from optparse import OptionParser, OptionValueError

# sudo pip3 install pyyaml
import yaml
import math
import time

from debug_tools.attitude_log import AttitudeLog
from thrust.thrust import Thrust
from sensor.sensor import Sensor
from pilot.pilot import Pilot
from controller.controller import Controller
from controller.controller import Controller_h
from time_log import TimeLog
from led_pyzero import Led

def main_loop(conf_file, log_path, controll_method):
    Led.change(False)
    pilot = Pilot(controll_method, throttle_base=1.2)
    print("Ready")
    cmd = Pilot.CMD_NOP
    while True:
        last_cmd = cmd
        cmd = pilot.get_cmd()
        if cmd == Pilot.CMD_NOP:
            pass
        elif last_cmd == Pilot.CMD_NOP and cmd == Pilot.CMD_THROTTLE_ZERO:
            # start
            try:
                params = yaml.load(open(conf_file, "rt"))
            except:
                print("ERROR can not read conf file")
                raise
            if log_path is not None:
                # over write log_path if --log option is specifed
                params["log"]["path"] = log_path
            print("ctrl start")
            pilot.initialize()
            alog = AttitudeLog(**params["log"])
            Led.change(True)
            with Thrust(params["body_const"]) as thrust:
                sensor = Sensor()
                dt = sensor.sampling_interval()
                controller = Controller(dt=dt,**params["controller"])
                controller_h = Controller_h(**params["controller_h"])
                control_loop(pilot, sensor, controller, controller_h, thrust, alog)
            print("ctrl end")
            Led.change(False)
            alog.add_info('param', params)
            alog.save() 
            print("seve end")
        time.sleep(0.5) 
        Led.toggle()


            
def throttle_correction(throttle_in, angle):
    DEG_TO_RAD = math.pi/180
    return throttle_in/(math.cos(angle[1] * DEG_TO_RAD) * math.cos(angle[2] * DEG_TO_RAD))

def control_loop(pilot, sensor, controller, controller_h, thrust, alog):
    timelog = TimeLog()
    start_time = None
    startup_done =False
    throttle_ctrl = 0
    last_distance_retrive_time = None
    while True:
        cmd = pilot.get_cmd()
        if cmd==Pilot.CMD_THROTTLE_ZERO:
            if startup_done:
                break
        else:
            startup_done = True
        if cmd==Pilot.CMD_EMERGENCY:
            print("EMERGENCY!")
            break
        timelog.checkpoint_first()
        retrieve_time, angle, angular_velocity, acc, distance, velocity, distance_retrive_time = sensor.get()
        timelog.checkpoint(retrieve_time)
        timelog.checkpoint()
        throttle, setpoint, setpoint_height = \
            pilot.get_setpoint(angle, angular_velocity, acc, distance)
        tau = controller.out(angle, angular_velocity, setpoint)
        if(distance is not None):
            if last_distance_retrive_time is None:
                dt = 0.01
            else:
                dt = distance_retrive_time - last_distance_retrive_time
            last_distance_retrive_time = distance_retrive_time
            throttle_ctrl = controller_h.out(distance, velocity, setpoint_height, dt)
        throttle_out = throttle_correction(throttle, angle) + throttle_ctrl
        thrust.set_thrust(throttle_out, tau)
        time_result = timelog.checkpoint(is_last=True)
        if startup_done == False:
            continue
        if start_time is None:
            start_time = retrieve_time
        alog.append(time = retrieve_time - start_time,
                    time_log = time_result[:],
                    angle_ypr = list(angle), 
                    gyro_ypr = list(angular_velocity),
                    raw_acc = list(acc),
                    out_throttle = throttle_out,
                    out_tau = list(tau),
                    pilot_ypr = list(setpoint),
                    pilot_throttle = throttle,
                    height = list((distance, velocity, distance_retrive_time, setpoint_height))) 
    thrust.set_thrust(0,[0,0,0]) 


if __name__ == "__main__":
    """
    QuadCopter Controller v0.1
    
    """
    usage = "usage: %prog [options] keyword"
    parser = OptionParser(usage)
    parser.add_option(
     "--hid",
     action="store_true", # Trueを保存
                          # store_falseならFalseを保存
     default=False,
     help="use hid joystic"
    )
    parser.add_option(
     "-c", "--conf",
     action="store", type="string", dest="conf_file",
     default="pydrone.conf",
     help="configuration file"
    )
    parser.add_option(
     "-l", "--log",
     action="store", type="string", dest="log_path",
     default=None,
     help="path for log file"
    )
    (options, args) = parser.parse_args()

    Led.change(False)

    if options.hid:
        controll_method=Pilot.METHOD_HID
    else:
        controll_method=Pilot.METHOD_UDP

    main_loop(options.conf_file, options.log_path, controll_method)
