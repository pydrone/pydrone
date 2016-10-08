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

from threading import Thread
from threading import Event

class ThreadWStop(Thread):
    MAGIC_KEY = "_ThreadStopEvent_"
    def __init__(self, group = None, target = None, name = None, args = (), kwargs = {}, *, daemon=None):
        self._stop_event = Event()
        kwargs[ThreadWStop.MAGIC_KEY] = self._stop_event
        Thread.__init__(self, group, target, name, args, kwargs, daemon = daemon)

    def start(self):
        self._stop_event.clear()
        Thread.start(self)

    def stop(self):
        self._stop_event.set()
        if Thread.is_alive(self):
            Thread.join(self)

    def recive_exit_request(kwargs):
        return kwargs[ThreadWStop.MAGIC_KEY].is_set()

if __name__=="__main__":
    import time
    def loop(**kwargs):
        i=0
        while not ThreadWStop.recive_exit_request(kwargs):
            print(i, end=" ")
            i += 1
        print("End of thread")
    th = ThreadWStop(target = loop, daemon = True)
    print("start")
    th.start();
    time.sleep(3)
    print("stop")
    th.stop()
    time.sleep(3)
    print("end")
    

       
