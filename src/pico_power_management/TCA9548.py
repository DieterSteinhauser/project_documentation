# -----------------------------------------
#                 NOTES 
# -----------------------------------------
# 
# Dieter Steinhauser
# 11/2023
# TCA9548 I2C Driver

# -----------------------------------------
#               IMPORTS
# -----------------------------------------

desc = r"""
The TCA9548A device has eight bidirectional translating switches that can be controlled throughthe I2C bus. The SCL/SDA upstream pair fans out to
eight downstream pairs, or channels. Any individual SCn/SDn channel or combination of channels can be selected, determined by the contents of the
programmable control register. These downstream channels can be used to resolve I2C slave address conflicts. For example, if eight identical digital
temperature sensors are needed in the application, one sensor can be connected at each channel: 0-7.

The TCA9548A has a standard bidirectional I2C interface that is controlled by a master device in order to beconfigured or read the status of this device. Each slave on the I2C 
bus has a specific device address to differentiate between other slave devices that are on the same I2C bus. Many slave devices require configuration upon startup to set the 
behavior of the device. This is typically done when the master accesses internal register maps of the slave, which have unique register addresses. 
A device can have one or multiple registers where data is stored, written, or read.

"""

from machine import Pin, I2C
from src.pico_power_management.i2c_device import Device
from src.pico_power_management.helpers import *
# from i2c_device import Device
# from helpers import *
# -----------------------------------------
#                Class:
# -----------------------------------------

class TCA9548(Device):

    I2C_MIN_FREQ = 100_000
    I2C_MAX_FREQ = 400_000
    DEFAULT_ADDR = 0x70 # The address is determined by the A2-A0 external pins, allowing 8 different addresses. All are grounded in our circuit.
    # ALT_ADDR = 0x75 # The address is determined by the A2-A0 external pins, allowing 8 different addresses.
    CHANNELS = tuple(range(0, 8))
    NUM_CHANNELS = len(CHANNELS)
    
    def __init__(self, name:str, address:int, i2c_bus, description = None, *args, **kwargs) -> None:
        """Object initialization for TCA9548. Follow device initialization and adds register information to object"""
        description = desc if desc is None else description
        super().__init__(name, address, i2c_bus, description, *args, **kwargs)

        
    def enable_channel(self, channel):
        """
        Turn the specified channel on.

        :param channel: Channel number, must be within 0 and 7.
        :type channel: int
        """
        # Throw an error for incorrect channel value
        check_type(channel, 'channel', int)
        check_range(channel, 'channel', 0, 7)

        # perform a read modify write cycle
        write_data = read_modify(read_data=self.read(), modify_data= (1 << channel), bit_mask= (1 << channel))

        # write to the device
        self.write(write_data)


    def disable_channel(self, channel):
        """
        Turn the specified channel off.

        :param channel: Channel number, must be within 0 and 7.
        :type channel: int
        """

        # Throw an error for incorrect channel value
        check_type(channel, 'channel', int)
        check_range(channel, 'channel', 0, 7)

        # perform a read modify write cycle
        write_data = read_modify(read_data=self.read(), modify_data= (0 << channel), bit_mask= (1 << channel))

        # write to the device
        self.write(write_data)


    def channel_status(self, channel):
        """
        Query the status of a channel.

        :param channel: Channel number, must be within 0 and 7.
        :type channel: int
        """
        # Throw an error for incorrect channel value
        check_type(channel, 'channel', int)
        check_range(channel, 'channel', 0, 7)

        # read the status of the channel
        status = (self.read() >> channel ) & 1
        return status


    def enable_all_channels(self):
        """
        Turn all channels on.
        """
        # write to the device
        self.write(0xFF)


    def disable_all_channels(self):
        """
        Turn all channels off.
        """
        # write to the device
        self.write(0x00)


    def all_channels_status(self):
        """Query the status of all channels"""
        return_dict = {}
        read_data = self.read()
        return_dict['CH7'] = (read_data >> 7) & 1
        return_dict['CH6'] = (read_data >> 6) & 1
        return_dict['CH5'] = (read_data >> 5) & 1
        return_dict['CH4'] = (read_data >> 4) & 1
        return_dict['CH3'] = (read_data >> 3) & 1
        return_dict['CH2'] = (read_data >> 2) & 1
        return_dict['CH1'] = (read_data >> 1) & 1
        return_dict['CH0'] = (read_data >> 0) & 1
        return return_dict


if __name__ == '__main__':
    i2c_bus =  I2C(1, sda=Pin(14), scl=Pin(15), freq=100_000)
    tca =  TCA9548(name="TCA9548", address=0x70, i2c_bus=i2c_bus)
    devices = tca.i2c_bus.scan()
    hex_addr = [hex(x) for x in devices]
    print(f"Seen device addresses: {hex_addr}")
    
    test = True
    if test:
        
        print(f"Channels Status: {tca.all_channels_status()}")
        tca.enable_all_channels()
        print(f"Channels Status: {tca.all_channels_status()}")
        tca.disable_all_channels()
        print(f"Channels Status: {tca.all_channels_status()}")
        
        tca.enable_channel(0)
        print(f"Channels Status: {tca.all_channels_status()}")
        print(f"Channel Status: {tca.channel_status(0)}")
        tca.disable_channel(0)
        
        tca.enable_channel(1)
        print(f"Channels Status: {tca.all_channels_status()}")
        print(f"Channel Status: {tca.channel_status(1)}")
        tca.disable_channel(1)
        
        tca.enable_channel(2)
        print(f"Channels Status: {tca.all_channels_status()}")
        print(f"Channel Status: {tca.channel_status(2)}")
        tca.disable_channel(2)
        
        

        

# -----------------------------------------
#              END OF FILE
# -----------------------------------------