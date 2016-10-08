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

from .i2c_device import I2CDevice
from struct import unpack, pack
import time
import statistics

from .mpu6050_reg import MPU6050Reg as Reg

class ReadTimmingHelper:
    def __init__(self, interval):
        self.interval = interval
        self.a_bit_short = self.interval * 0.995
        self.adjust = (self.interval-self.a_bit_short) * 10
        self.next_sampling = time.time()

    def post_get(self, sync_time = False):
        if(sync_time):
            self.next_sampling = time.time()    
        # forward nxt_sampling time in fiture
        while True:
            if(self.next_sampling > time.time()):
                break
            self.next_sampling += self.a_bit_short
        # return last sampling time
        return self.next_sampling - self.a_bit_short

    def pre_get(self):
        wait_time = self.next_sampling - time.time()
        if wait_time > 0:
            time.sleep(wait_time)

    def sleep(self):
        time.sleep(self.adjust)

class AccGyro:
    Reg_Rate = 9
    SamplingInterval = 1/1000 * (1+Reg_Rate)
    def __init__(self):
        # Sensor initialization
        self._mpu = MPU6050()
        self.offset_acc = [0,0,0]
        self.offset_gyro = [0,0,0]
        self.setup_mpu()
    def setup_mpu(self):
        if not self._mpu.testConnection():
            print("MPU not found")
            raise Exception("Hardware error")
        self._mpu.intialize(AccGyro.Reg_Rate, 6)
        interval = self.calibration(100)
        interval = self.calibration(100)
        if AccGyro.SamplingInterval*0.9 < interval < AccGyro.SamplingInterval*1.1:
            pass
        else:
            interval = AccGyro.SamplingInterval
        self.read_timming_helper = ReadTimmingHelper(interval)

    def get(self):
        resync = False
        self.read_timming_helper.pre_get()
        while True:
            try:
                acc, gyro = self._mpu.get_last_one()
                break
            except NoDataError:
                self.read_timming_helper.sleep()
                resync = True
        get_time = self.read_timming_helper.post_get(resync)
        acc = [val - offset for val,offset in zip(acc[:], self.offset_acc)]
        gyro = [val - offset for val,offset in zip(gyro[:], self.offset_gyro)]
        return (acc, gyro, get_time)

    def calibration(self,N=200):
        time_start = time.time()
        buf = self._mpu.gets(N)
        time_end = time.time()
        avarage = []
        for i in range(6):
            avarage.append(statistics.mean((x[i] for x in buf)))
        self.offset_acc = avarage[0:3]
        self.offset_acc[2] -= 1.0
        self.offset_gyro = avarage[3:6]
        self.estimate_interval = (time_end - time_start)/N
        return self.estimate_interval

class NoDataError(Exception):
    """Exception """
    pass

class MPU6050:

    def __init__(self, address = Reg.DEFAULT_ADDRESS):
        self.i2c = I2CDevice(address)
        self.offset_ax, self.offset_ay, self.offset_az, self.offset_gx, self.offset_gy, self.offset_gz = (0, 0, 0, 0, 0, 0)
        self.estimate_interval = None
    
    def reset(self):
        self.i2c.writeBit(Reg.RA_PWR_MGMT_1, Reg.PWR1_DEVICE_RESET_BIT, True)       

    def resetFIFO(self):
        self.i2c.writeBit(Reg.RA_USER_CTRL, Reg.USERCTRL_FIFO_RESET_BIT, True)

    def enableFIFO(self):      
        self.i2c.writeBit(Reg.RA_USER_CTRL, Reg.USERCTRL_FIFO_EN_BIT, 1)

    def disableFIFO(self):      
        self.i2c.writeBit(Reg.RA_USER_CTRL, Reg.USERCTRL_FIFO_EN_BIT, 0)

    def getDeviceID(self):
        return self.i2c.readBits(Reg.RA_WHO_AM_I, Reg.WHO_AM_I_BIT, Reg.WHO_AM_I_LENGTH)

    def testConnection(self):
        return self.getDeviceID() == 0x34

    def intialize(self, rate_div, bw):
        self.reset()
        time.sleep(0.1)

        # Disable device sleep
        self.i2c.writeBit(Reg.RA_PWR_MGMT_1, Reg.PWR1_SLEEP_BIT, False)    
        # set clock Source CLOCK_PLL_XGYRO
        self.i2c.writeBits(Reg.RA_PWR_MGMT_1,
            Reg.PWR1_CLKSEL_BIT, Reg.PWR1_CLKSEL_LENGTH, Reg.CLOCK_PLL_XGYRO)

        #   bw            bandwidth  delay
        # 0 DLPF_BW_256   256Hz       0.98ms
        # 1 DLPF_BW_188   188Hz       1.9ms
        # 2 DLPF_BW_98     98Hz       2.8ms
        # 3 DLPF_BW_42     42Hz       4.8ms
        # 4 DLPF_BW_20     20Hz       8.3ms
        # 5 DLPF_BW_10     10Hz      13.4ms
        # 6 DLPF_BW_5       5Hz      18.6ms
        self.i2c.writeBits(Reg.RA_CONFIG,
            Reg.CFG_DLPF_CFG_BIT, Reg.CFG_DLPF_CFG_LENGTH,bw)
        # set rate 1kHz/(1+rate_div)
        self.i2c.write8(Reg.RA_SMPLRT_DIV, rate_div)
        # set gyro full scale 250deg/sec
        self.i2c.writeBits(Reg.RA_GYRO_CONFIG,
            Reg.GCONFIG_FS_SEL_BIT, Reg.GCONFIG_FS_SEL_LENGTH, Reg.GYRO_FS_250)
        # set accel full scale 2g
        self.i2c.writeBits(Reg.RA_ACCEL_CONFIG,
            Reg.ACONFIG_AFS_SEL_BIT, Reg.ACONFIG_AFS_SEL_LENGTH, Reg.ACCEL_FS_2)

        self.disableFIFO()
        self.resetFIFO()
        # Enable Xgyro, Ygyro Zgyro FIFO
        self.i2c.writeBit(Reg.RA_FIFO_EN, Reg.XG_FIFO_EN_BIT, 1)
        self.i2c.writeBit(Reg.RA_FIFO_EN, Reg.YG_FIFO_EN_BIT, 1)
        self.i2c.writeBit(Reg.RA_FIFO_EN, Reg.ZG_FIFO_EN_BIT, 1)
        # Enable Accel FIOF
        self.i2c.writeBit(Reg.RA_FIFO_EN, Reg.ACCEL_FIFO_EN_BIT, 1)
        self.enableFIFO()

    def getFIFOCount(self):
        return self.i2c.readU16(Reg.RA_FIFO_COUNTH)

    def getFIFOBytes(self,length):
        return self.i2c.readBytes(Reg.RA_FIFO_R_W, length)

    def setOffset(self, offset_accel, offset_gyro):
        for val, reg in zip(offset_accel, [Reg.RA_XA_OFFS_H, Reg.RA_YA_OFFS_H, Reg.RA_ZA_OFFS_H]):
            self.i2c.writeS16(reg, val)
        for val, reg in zip(offset_gyro, [Reg.RA_XG_OFFS_USRH, Reg.RA_YG_OFFS_USRH, Reg.RA_ZG_OFFS_USRH]):
            self.i2c.writeS16(reg, val)

    def get_count(self):
        return self.getFIFOCount() // 12
            
    def is_arrived(self):
        return self.get_count() > 0

    def get_last_one(self):
        n = self.get_count()
        if(n==2):
            # drop old one
            self.getFIFOBytes(12)
            n -= 1
        if(n>2):
            # lot of data in fifo. clear all
            self.disableFIFO()
            self.resetFIFO()
            self.enableFIFO()
            n = 0
        if(n==0):
            raise NoDataError()
        return self.get()

    def get(self):
        value = self.getFIFOBytes(12)
        value_int16 = unpack('>hhhhhh', value)
        acc = [v/16384 for v in value_int16[0:3]]
        gyro = [v/131.0 for v in value_int16[3:6]]
        return (acc, gyro)

    def gets(self,n):
        buf = []
        self.disableFIFO()
        self.resetFIFO()
        self.enableFIFO()
        for i in range(n):
            while not self.is_arrived():
                time.sleep(0.001)
            acc, gyro = self.get()
            buf.append(acc+gyro)
        return buf


