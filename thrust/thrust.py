from .moter import Moter
from .body_coefficient import BodyCoefficient
from .pwm_rpio import PwmRPIO
import copy

class Thrust:
    def __init__(self,body_const):
        body_const_copy = copy.copy(body_const)
        try:
            pwm_pin_list = body_const_copy.pop("pwm_pin_list")
        except KeyError:
            pwm_pin_list = [23,24,25,8]
        self.moter = Moter(PwmRPIO(pwm_pin_list))
        self.body = BodyCoefficient(**body_const_copy)
    def __enter__(self):
        return self
    def __exit__(self ,type, value, traceback):
        self.moter.stop()

    def set_thrust(self, thrust, tau):
        moter_kg = self.body.tau2force_kg(thrust, tau)
            
        out = [self.body.force2esc(i, force) for i,force in enumerate(moter_kg[:])]
        self.moter.update(out)
