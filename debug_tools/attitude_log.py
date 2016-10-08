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


from datetime import datetime
import json
from collections import deque
from subprocess import check_output

class AttitudeLog:
    def __init__(self, path=".", nlimit=0, disable=False):
        self.path = path
        self.info = {} 
        self.disable = disable
        self.counter = 0
        self.nlimit = nlimit
        if nlimit < 0:
            maxlen = -nlimit
        else:
            maxlen = None
        self.log = deque(maxlen=maxlen)

    def add_info(self, key, value):
        self.info[key] = value

    def append(self, **kwargs):
        if self.disable == True:
            return
        if self.nlimit > 0 and self.nlimit <= len(self.log):
            return
        self.log.append(kwargs)

    def git_hash(self):
        try:
            hash = str(check_output(["git", "rev-parse", "HEAD"]))[2:-3]
        except:
            hash = None
        return hash

    def save(self, save_git_hash = True):
        if self.disable == True:
            return
        git_hash = self.git_hash()
        if git_hash != None:
            self.add_info('git_hash', git_hash)
        while True:
            filename = self.path +"/log{:04d}".format(self.counter)
            self.counter += 1
            try:
                f = open(filename, "xt")
                break
            except FileExistsError:
                if self.counter >= 10000:
                    self.disable = True
                    return
                continue
        d = {'info':self.info, 'attitude':list(self.log)}
        json.dump(d, f)
        f.close()

    def load(self, filename):
        f = open(filename, "rt")
        d = json.load(f)
        self.log = d['attitude']
        self.info = d['info']

    def get_log(self):
        return self.log

    def show_info(self):
        print(self.info)

if __name__ == "__main__":
    log = AttitudeLog()
    for i in range(100):
        alog_e = {}
        alog_e['time'] = i
        alog_e['acc'] = [i*1.1, i*1.2, i*1.3]
        alog_e['gyro'] = [i+10, i+15, i+20]
        log.append(alog_e)
    log.save("save.log")
    del log
    log = AttitudeLog()
    log.load("save.log")
    gf_list = [0]*4
    gf_list[0] = lambda a: a['acc'][0]
    gf_list[1] = lambda a: a['acc'][1]
    gf_list[2] = lambda a: a['acc'][2]
    gf_list[3] = lambda a: a['gyro'][2]
    label_list = ["acc_x", "acc_y", "acc_z", "gyro_z"]
    log.show(gf_list,label_list)
