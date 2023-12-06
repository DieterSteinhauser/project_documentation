# -----------------------------------------
#                 NOTES 
# -----------------------------------------
# 
# Dieter Steinhauser
# 11/2023
# AT24C256 I2C Driver

# -----------------------------------------
#               IMPORTS
# -----------------------------------------

desc = r"""
The AT24C128/256 provides 131,072/262,144 bits of serial electrically erasable and
programmable read only memory (EEPROM) organized as 16,384/32,768 words of 8
bits each. The devices cascadable feature allows up to 4 devices to share a common
Two-wire bus. The device is optimized for use in many industrial and commercial applications
 where low power and low voltage operation are essential.

"""

from machine import Pin, I2C
from src.pico_power_management.i2c_device import Device
from src.pico_power_management.helpers import *
# from i2c_device import Device, Register
# from helpers import *
# -----------------------------------------
#                Class:
# -----------------------------------------

class AT24C256(Device):

    I2C_MIN_FREQ = 100_000
    I2C_MAX_FREQ = 400_000
    I2C_MAX_FREQ_5V = 1_000_000

    # 0b10100_A1_A0_RW -> 0b1010_000X -> 0x50
    DEFAULT_ADDR = 0x50 # The address is determined by the A1-A0 external pins, allowing 4 different addresses. All are grounded in our circuit.

    def __init__(self, name:str, address:int, i2c_bus, description = None, *args, **kwargs) -> None:
        """Object initialization for AT24C256. Follow device initialization and adds register information to object"""
        description = desc if desc is None else description
        super().__init__(name, address, i2c_bus, description, *args, **kwargs)
        
        def write(address, data):
            """
            Write data to the device. Overloads the i2c device method so 16bit addresses are supported

            :param data: Data to write to the device.
            :type data: int
            """
            addr_high = address >> 8
            addr_low = address & 0x00FF
            


if __name__ == '__main__':
    i2c_bus =  I2C(1, sda=Pin(14), scl=Pin(15), freq=100_000)
    at =  AT24C256(name="AT24C256", address=0x50, i2c_bus=i2c_bus)
    devices = at.i2c_bus.scan()
    hex_addr = [hex(x) for x in devices]
    print(f"Seen device addresses: {hex_addr}")
    
    test = True
    if test:
        import time
        at.reg_write(0x0000, 0xA)
        time.sleep_ms(100)
        at.reg_write(0x0002, 0xC)
        time.sleep_ms(100)
        print(at.reg_read(0x0000))
        time.sleep_ms(100)
        print(at.reg_read(0x0002))
        time.sleep_ms(100)
        pass

# -----------------------------------------
#              END OF FILE
# -----------------------------------------