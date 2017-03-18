import time
import RPi.GPIO as GPIO
from threading import Event
import statistics
from collections import deque

class T13A_READ:
    def __init__(self, ss_pin=37, clk_pin=33, data_pin=35):
        self.ss_pin = ss_pin
        self.clk_pin = clk_pin
        self.data_pin = data_pin
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.ss_pin, GPIO.OUT)
        GPIO.output(self.ss_pin, True)
        GPIO.setup(self.clk_pin, GPIO.OUT)
        GPIO.output(self.clk_pin, False)
        GPIO.setup(self.data_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    def get(self):
        if(GPIO.input(self.data_pin)==0):
            return(0,0) # no data
        GPIO.output(self.clk_pin,False)
        GPIO.output(self.ss_pin,False)
        bit=1
        data = 0
        for i in range(16):
            GPIO.output(self.clk_pin,(i%2)==0)
            if(GPIO.input(self.data_pin)):
                data |= bit
            bit <<= 1                
        bit=1
        sens_time = 0
        sens_bits = 0 # 0 to disable sens
        for i in range(sens_bits):
            GPIO.output(self.clk_pin,(i%2)==0)
            if(GPIO.input(self.data_pin)):
                sens_time |= bit
            bit <<= 1                
        GPIO.output(self.ss_pin,True)
        GPIO.output(self.clk_pin,False)
        return (data, sens_time)


class HC_SR04:
    event = Event()
    def __init__(self):
        self.t13a_read = T13A_READ()
        self.y1 = 0
        self.x1 = 0
        self.t1 = 0
        self.result_queue = deque([0,0,0,0,0,0,0], 7)

    def mesure_distance(self):
        t1, t2 = self.t13a_read.get()
        if t1 != 0:
            self.result_queue.append(t1/1200000*340/2)
            x0 = statistics.median(self.result_queue)
            y0 = (self.y1*2 + x0 + self.x1)/4
            self.y1 = y0
            self.x1 = x0
            self.t1 = time.time() - t2/1200000
        #return y0, self.t1
        return self.y1, self.t1
        #return t1,measure_time
if __name__ == "__main__":
    sensor = HC_SR04()
    last = 0
    for i in range(1000000):
        l, t = sensor.mesure_distance()
        if(l!=0):
            print("{:6.3f} {}".format(l,time.time()-t))
        #if(l-last >256 or l-last <-256):
        #    print("******")
        time.sleep(0.01)
        last = l
