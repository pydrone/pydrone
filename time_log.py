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

class TimeLog:
    def __init__(self):
        self.last = 0
    
    def checkpoint_first(self):
        self.result = []
        if self.last == 0:
            self.last = time.time()

    def checkpoint(self, logtime=None, is_last=False):
        if logtime is None:
            logtime = time.time()
        self.result.append(logtime - self.last)
        if is_last:
            self.last = logtime
            return self.result
        else:
            return None
       
