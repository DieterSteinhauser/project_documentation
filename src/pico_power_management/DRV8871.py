# -----------------------------------------
#                 NOTES 
# -----------------------------------------

# Dieter Steinhauser
# 11/2023

# DRV8871 H-Bridge Motor Controller driver.


# -----------------------------------------
#               IMPORTS
# -----------------------------------------

from machine import Pin, PWM
import time
from src.pico_power_management.helpers import *
# from helpers import *
# -----------------------------------------
#                Class:
# -----------------------------------------


desc = r"""
The DRV8871 output consists of four N-channel MOSFETs that are designed to drive high current. They are
controlled by the two logic inputs IN1 and IN2.

IN1 IN2 OUT1, OUT2 DESCRIPTION
0   0   HI-Z  HI-Z  Coast, H=bridge disabled to High-Z
0   1   L     H     Reverse (current OUT2->OUT1)
1   0   H     L     Forward (current OUT1->OUT2)
1   1   L     L     Brake, Low side slow decay.


The inputs can be set to static voltages for 100% duty cycle drive, or they can be pulse-width modulated (PWM)
for variable motor speed. When using PWM, it typically works best to switch between driving and braking. For
example, to drive a motor forward with 50% of its max RPM, IN1 = 1 and IN2 = 0 during the driving period, and
IN1 = 1 and IN2 = 1 during the other period. Alternatively, the coast mode (IN1 = 0, IN2 = 0) for fast current
decay is also available. The input pins can be powered before VM is applied.

"""


class DRV8871:
    
    MAX_PWM_FREQ = 200_000
    HIGH = 65535
    LOW = 0
    
    def __init__(self, name:str, in1, in2, pwm_freq=100_000, description = None, *args, **kwargs) -> None:
        """Object initialization for DRV8871. Follow device initialization and adds register information to object"""
        
        # Throw errors for incorrect values.
        check_type(in1, 'in1', (int, Pin))
        check_type(in2, 'in2', (int, Pin)) 
        check_type(pwm_freq, 'pwm_freq', int)

        if isinstance(in1, int):
            check_range(in1, 'in1', 0, 28)
        if isinstance(in2, int):
            check_range(in2, 'in2', 0, 28)

        check_range(pwm_freq, 'pwm_freq', 0, self.MAX_PWM_FREQ)

        # assign the object variables
        self.name  = name
        self.pwm_freq = pwm_freq
        self.description = desc if description is None else description

        # Create Pin Objects
        self.in1 = Pin(in1, Pin.OUT) if isinstance(in1, int) else in1
        self.in2 = Pin(in2, Pin.OUT) if isinstance(in2, int) else in2

        # Create PWM channels with the Pins
        self.in1_pwm = PWM(self.in1)
        self.in1_pwm.freq(pwm_freq)
        self.in1_pwm.duty_u16(self.LOW)
        self.in2_pwm = PWM(self.in2)
        self.in2_pwm.freq(pwm_freq)
        self.in2_pwm.duty_u16(self.LOW)

    def full_forward(self):
        """Set the device in a full forward state."""

        # Set IN2 Low then IN1 High.
        self.in2_pwm.duty_u16(self.LOW)
        self.in1_pwm.duty_u16(self.HIGH)

    def full_backward(self):
        """Set the device in a full backward state."""

        # Set IN1 Low then IN2 High.
        self.in1_pwm.duty_u16(self.LOW)
        self.in2_pwm.duty_u16(self.HIGH)

    def forward(self, duty = 5, coast=True):
        """
        Set the device in a forward state. 
        Duty Cycle of forward power is controlled by PWM ON time.

        :param duty: Duty Cycle of forward power given on a scale of 0 to 100, defaults to 5.
        :type duty: int | float
        :param coast: Determines the alternate state of operation. Either Coast (True) or Brake (False). Defaults to True.
        :type coast: bool
        """
        # Throw errors for incorrect values
        check_type(duty, 'duty', (int, float))
        check_range(duty, 'duty', 0, 100)
        check_type(coast, 'coast', bool) 

        if coast: # Alternates between forward and coast
            
            # Start PWM at the desired Duty Cycle
            duty = int((duty/100) * 65535)
            self.in2_pwm.duty_u16(self.LOW)
            self.in1_pwm.duty_u16(duty)

        else: # Alternates between forward and Brake

            # Start PWM at the desired Duty Cycle
            duty = int(((100-duty)/100) * 65535)
            self.in2_pwm.duty_u16(duty)
            self.in1_pwm.duty_u16(self.HIGH)

    def backward(self, duty = 5, coast=True):
        """
        Set the device in a backward state. 
        Duty Cycle of backward power is controlled by PWM ON time.

        :param duty: Duty Cycle of backward power given on a scale of 0 to 100, defaults to 5.
        :type duty: int | float
        :param coast: Determines the alternate state of operation. Either Coast (True) or Brake (False). Defaults to True.
        :type coast: bool
        """
        # Throw errors for incorrect values
        check_type(duty, 'duty', (int, float))
        check_range(duty, 'duty', 0, 100)
        check_type(coast, 'coast', bool) 

        if coast: # Alternates between forward and coast
            
            # Start PWM at the desired Duty Cycle
            duty = int((duty/100) * 65535)
            self.in1_pwm.duty_u16(self.LOW)
            self.in2_pwm.duty_u16(duty)

        else: # Alternates between forward and Brake

            # Start PWM at the desired Duty Cycle
            duty = int(((100-duty)/100) * 65535)
            self.in1_pwm.duty_u16(duty)
            self.in2_pwm.duty_u16(self.HIGH)

    def coast(self):
        """Set the device to coast. """

        # Set the device to coast
        self.in1_pwm.duty_u16(self.LOW)
        self.in2_pwm.duty_u16(self.LOW)

    def brake(self):
        """Set the device to stop abruptly. """

        # Set the device to brake
        self.in1_pwm.duty_u16(self.HIGH)
        self.in2_pwm.duty_u16(self.HIGH)

    def status(self):
        """
        Query the status of the H-bridge controls.

        NOTE: we cannot read the H-Bridge's status directly, rather this method returns the status of the associated pins and PWM system.
        """
        return_dict = {}
        in1_duty = self.in1_pwm.duty_u16() 
        in2_duty = self.in2_pwm.duty_u16() 

        # IN1 IN2 OUT1, OUT2 DESCRIPTION
        # 0   0   HI-Z  HI-Z  Coast, H=bridge disabled to High-Z
        # 0   1   L     H     Reverse (current OUT2->OUT1)
        # 1   0   H     L     Forward (current OUT1->OUT2)
        # 1   1   L     L     Brake, Low side slow decay.

        state = None
        off_state = None
        effective_duty = None

        # Based on the Pin setup, determine the status of the system
        if in1_duty == self.HIGH and in2_duty == self.HIGH:
            state = "BRAKE"
            off_state = 'BRAKE'
        
        elif in1_duty == self.LOW and in2_duty == self.LOW:
            state = 'COAST'
            off_state = 'COAST'

        elif self.LOW <= in1_duty <= self.HIGH and in2_duty == self.HIGH:
            state = 'BACKWARD'
            off_state = 'BRAKE'
            effective_duty = 100 - int(100* in1_duty / 65535)

        elif self.LOW <= in2_duty <= self.HIGH and in1_duty == self.LOW:
            state = 'REVERSE'
            off_state = 'COAST'
            effective_duty = int(100* in2_duty / 65535)

        elif self.LOW <= in2_duty <= self.HIGH and in1_duty == self.HIGH:
            state = 'FORWARD'
            off_state = 'BRAKE'
            effective_duty = 100 - int(100* in2_duty / 65535)

        elif self.LOW <= in1_duty <= self.HIGH and in2_duty == self.LOW:
            state = 'FORWARD'
            off_state = 'COAST'
            effective_duty = int(100* in1_duty / 65535)

        in1_pwm = {'FREQ': self.in1_pwm.freq(), 'DUTY': int(100* in1_duty / 65535)}
        in2_pwm = {'FREQ': self.in2_pwm.freq(), 'DUTY': int(100* in2_duty / 65535)}

        return_dict['in1_pwm'] = in1_pwm
        return_dict['in2_pwm'] = in2_pwm
        return_dict['effective_duty'] = effective_duty
        return_dict['state'] = state
        return_dict['off_state'] = off_state
        return return_dict
    

if __name__ == '__main__':

    drv = DRV8871(name='Motor Driver', in1 = Pin(13, Pin.OUT), in2=Pin(12, Pin.OUT))
    
    test = True
    if test:
        print('testing')
        drv.full_forward()
        print(drv.status())
        time.sleep(1)
        drv.brake()
        print(drv.status())
        time.sleep(1)
        drv.forward(80)
        print(drv.status())
        time.sleep(1)
        drv.coast()
        print(drv.status())
        time.sleep(1)
        drv.forward(80, coast=False)
        time.sleep(1)
        drv.brake()
        print(drv.status())
        
        

        

# -----------------------------------------
#              END OF FILE
# -----------------------------------------