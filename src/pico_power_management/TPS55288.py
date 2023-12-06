# -----------------------------------------
#                 NOTES 
# -----------------------------------------
# 
# Dieter Steinhauser
# 10/2023
# TPS55288 I2C Driver


# -----------------------------------------
#               IMPORTS
# -----------------------------------------

desc = r"""
The TPS55288 uses I2C interface for flexible converter parameter programming. I2C is a bi-directional 2-wire
serial interface. Only two bus lines are required: a serial data line (SDA) and a serial clock line (SCL). I2C
devices can be considered as masters or slaves when performing data transfers. A master is the device that
initiates a data transfer on the bus and generates the clock signals to permit that transfer. At that time, any
device addressed is considered a slave.
The TPS55288 operates as a slave device with address 74h and 75h set by a different resistor at the MODE pin.
Receiving control inputs from the master device like a microcontroller or a digital signal processor reads and
writes the internal registers 00h through 07h. The I2C interface of the TPS55288 supports both standard mode
(up to 100 kbit/s) and fast mode plus (up to 1000 kbit/s). Both SDA and SCL must be connected to the positive
supply voltage through current sources or pullup resistors. When the bus is free, both lines are in high voltage.
"""


from machine import Pin, I2C
from time import sleep
from src.pico_power_management.i2c_device import Device, Register, Field
from src.pico_power_management.helpers import *
# from i2c_device import Device, Register, Field
# from helpers import *
# -----------------------------------------
#                Class:
# -----------------------------------------

class TPS55288(Device):

    I2C_MIN_FREQ = 100_000
    I2C_MAX_FREQ = 1_000_000
    DEFAULT_ADDR = 0x74
    ALT_ADDR = 0x75

    VREF_LOW: Register
    VREF_HIGH: Register
    IOUT_LIMIT: Register
    VOUT_SR: Register
    VOUT_FS: Register
    CDC: Register
    VOUT_FS: Register
    MODE: Register
    STATUS: Register


    def __init__(self, name:str, address:int, i2c_bus, description = None, *args, **kwargs) -> None:
        """Object initialization for TPS55288. Follow device initialization and adds register information to object"""
        description = desc if desc is None else description
        super().__init__(name, address, i2c_bus, description, *args, **kwargs)

        # Add device registers
        self.add_register("VREF_LOW", 0x0, r_w = "R/W", description='Low byte of internal reference voltage')
        self.add_register("VREF_HIGH", 0x1, r_w = "R/W", description='high byte of internal reference voltage')
        self.add_register("IOUT_LIMIT", 0x2, r_w = "R/W", description='Current Limit Setting')
        self.add_register("VOUT_SR", 0x3, r_w = "R/W", description='Slew Rate ')
        self.add_register("VOUT_FS", 0x4, r_w = "R/W", description='Feedback Selection')
        self.add_register("CDC", 0x5, r_w = "R/W", description='Cable Compensation')
        self.add_register("MODE", 0x6, r_w = "R/W", description='Mode Control')
        self.add_register("STATUS", 0x7, r_w = "R", description='Operating Status')

        # Add fields to each register
        self.VREF_LOW.add_field(name='REF_LSB', bit_offset=0, width=8, r_w="R/W", description="VREF Lower byte. 10 bits total.")

        self.VREF_HIGH.add_field(name='REF_MSB', bit_offset=0, width=2, r_w="R/W", description="VREF higher bits. 10 bits total.")

        self.IOUT_LIMIT.add_field(name='CURR_LIMIT', bit_offset=0, width=7, r_w="R/W", description="Current Limit, setting the target voltage between ISP and ISN.")
        self.IOUT_LIMIT.add_field(name='CURR_LIMIT_EN', bit_offset=7, width=1, r_w="R/W", description="Current Limit Enable, Active High and on by default")

        self.VOUT_SR.add_field(name='SR', bit_offset=0, width=2, r_w="R/W", description="Sets slew rate for output voltage change.")
        self.VOUT_SR.add_field(name='OCP_DELAY', bit_offset=4, width=2, r_w="R/W", description="Sets the response time of the device when the output overcurrent is reached.")

        self.VOUT_FS.add_field(name='INTFB', bit_offset=0, width=2, r_w="R/W", description="Internal Feedback ratio")
        self.VOUT_FS.add_field(name='FB', bit_offset=7, width=1, r_w="R/W", description="Output feedback voltage.")

        self.CDC.add_field(name='CDC', bit_offset=0, width=3, r_w="R/W", description="Compensation for voltage droop over cable")
        self.CDC.add_field(name='CDC_OPTION', bit_offset=3, width=1, r_w="R/W", description="Select the cable voltage droop compensation approach")
        self.CDC.add_field(name='OVP_MASK', bit_offset=5, width=1, r_w="R/W", description="Overvoltage Mask")
        self.CDC.add_field(name='OCP_MASK', bit_offset=6, width=1, r_w="R/W", description="Overcurrent Mask")
        self.CDC.add_field(name='SC_MASK', bit_offset=7, width=1, r_w="R/W", description="Short Circuit Mask")

        self.MODE.add_field(name='MODE', bit_offset=0, width=1, r_w="R/W", description="Mode Control Approach")
        self.MODE.add_field(name='PFM', bit_offset=1, width=1, r_w="R/W", description="Select operating mode at light load condition")
        self.MODE.add_field(name='I2CADD', bit_offset=2, width=1, r_w="R/W", description="I2C address")
        self.MODE.add_field(name='VCC', bit_offset=3, width=1, r_w="R/W", description="VCC option")
        self.MODE.add_field(name='DISCHG', bit_offset=4, width=1, r_w="R/W", description="Output discharge")
        self.MODE.add_field(name='HICCUP', bit_offset=5, width=1, r_w="R/W", description="Hiccup mode")
        self.MODE.add_field(name='FSWDBL', bit_offset=6, width=1, r_w="R/W", description="Switching frequency doubling in buck-boost mode")
        self.MODE.add_field(name='OE', bit_offset=7, width=1, r_w="R/W", description="Output enable")

        self.STATUS.add_field(name='STATUS', bit_offset=0, width=2, r_w="R", description="Operating status")
        self.STATUS.add_field(name='OVP', bit_offset=5, width=1, r_w="R", description="Overvoltage protection")
        self.STATUS.add_field(name='OCP', bit_offset=6, width=1, r_w="R", description="Overcurrent protection")
        self.STATUS.add_field(name='SCP', bit_offset=7, width=1, r_w="R", description="Short circuit protection")

        
    def voltage(self, value=None):
        """
        method for setting the voltage on the device, if no value is given, returns the device set voltage.

        :param value: Voltage value, defaults to None
        :type value: int, optional
        """

        # read back the voltage on the device
        if value is None:
            
            # Throw Error if external feedback is being used.
            if self.feedback_select() == 1:
                raise ValueError("Cannot determine state of output voltage digitally because the system is utilizing an external feedback for voltage selection")
            
            # Check the internal feedback ratio
            ratio_int = self.feedback_ratio() # 0 = 5mV, 1 = 10mV, 2 = 15mV, 3 = 20mV
            ratio = (ratio_int+1) * 0.00520833
             
            # check the reference voltage
            low = self.VREF_LOW.REF_LSB.read()
            high = self.VREF_HIGH.REF_MSB.read()
            ref_value = (high << 8) | low
            
            # multiply the reference voltage by the feedback ratio to give the output value.
            voltage = ratio * ref_value
            return voltage
        
        # Throw errors for incorrect values given
        check_type(value, 'value', (int, float))
        check_range(value, 'value', 0.8, 21)

        # Determine the smallest step size required to produce the desired value
        if (0 <= value < 5.31):
            ratio_int = 0
        elif (5.31 <= value < 10.64):
            ratio_int = 1
        elif (10.64 <= value < 15.97):
            ratio_int = 2
        else:
            ratio_int = 3

        # calculate the ratio and reference value required.
        ratio = (ratio_int+1) * 0.00520833
        ref_value = 0.045 + int(value/ratio) * 0.001129

        # set the feedback ratio and reference value
        self.feedback_ratio(ratio_int) # 0 = 5mV, 1 = 10mV, 2 = 15mV, 3 = 20mV
        self.reference_voltage(ref_value)
        
        

    def reference_voltage(self, value=None):
        """
        method for setting reference voltage on the device, if no value is given, returns the device set reference voltage.

        :param value: Voltage value, defaults to None
        :type value: int, optional
        """

        # read back the reference voltage on the device
        if value is None:
            low = self.VREF_LOW.REF_LSB.read()
            high = self.VREF_HIGH.REF_MSB.read()
            ref_value = (high << 8) | low

            # Reference voltage starts at 45mV and goes in 1.129mV increments
            ref_voltage = 0.045 + ref_value * 0.001129
            return ref_voltage
        
        # Throw errors for incorrect values given
        check_type(value, 'value', (int, float))
        check_range(value, 'value', 0.045, 1.2)

        # make voltage value into clean byte for data transfer
        ref_value =  int(round((value - 0.045) / 0.001129))
        ref_low = ref_value & 0x0FF
        ref_high = (ref_value & 0x300) >> 8

        # write to the registers
        self.VREF_LOW.write(ref_low)
        self.VREF_HIGH.write(ref_high)
        

    def status(self):
        """
        method to query the status register on the device. Reset's the STATUS register after reading.
        """
        return_dict = {}
        status_vals = ['BOOST', 'BUCK', 'BUCK_BOOST']
        status_ovp = ['NONE', 'OVP']
        status_ocp = ['NONE', 'OCP']
        status_scp = ['NONE', 'SCP']

        # read back the reference voltage on the device
        read_data = self.STATUS.read()
        status = (read_data & 0x03)
        ovp = (read_data & 0x20) >> 5
        ocp = (read_data & 0x40) >> 6
        scp = (read_data & 0x80) >> 7

        # format the returned data
        return_dict['STATUS'] = status_vals[status]
        return_dict['OVP'] = status_ovp[ovp]
        return_dict['OCP'] = status_ocp[ocp]
        return_dict['SCP'] = status_scp[scp]
        return return_dict
    

    def output_enable(self, value=None):
        """
        Query or Command the output enable status. if no value is given, return the current status.

        :param value: Enable value, active high, defaults to None
        :type value: int, optional
        """

        if value is None:
            return self.MODE.OE.read()
        
        check_type(value, 'output_en', int)
        check_range(value, 'output_en', 0, 1)

        self.MODE.OE.write(value)


    def current_limit(self, current_limit=None, enable=None):
        """
        Query or Command the output current limit and enable status. if no value is given, return the status of the current limit system.

        :param value: Enable value, active high, defaults to None
        :type value: int, optional
        """

        if all (val is None for val in [current_limit, enable]):
            return_dict = {}
            register = self.IOUT_LIMIT.read()
            return_dict['current_limit'] = (register & 0x7F) * 0.0005
            return_dict['enable'] = (register >> 7) & 1
            return register
        
        check_type(current_limit, 'current_limit', (int, float))
        check_range(current_limit, 'current_limit', 0, 0.0635)
                
        check_type(enable, 'enable', int)
        check_range(enable, 'enable', 0, 1)

        if current_limit is not None:
            self.IOUT_LIMIT.CURR_LIMIT.write(int(current_limit/0.0005))

        if enable is not None: 
            self.IOUT_LIMIT.CURR_LIMIT_EN.write(enable)


    def feedback_ratio(self, feedback_ratio=None):
        """
        Command and Query the internal feedback ratio. Changes the step size of voltage increments.

        0 = 5mV, 1 = 10mV, 2 = 15mV, 3 = 20mV 

        :param value: _description_, defaults to None
        :type value: _type_, optional
        :return: Returns the feedback ratio integer
        :rtype: int
        """
        if feedback_ratio is None:
            return self.VOUT_FS.INTFB.read()
        
        check_type(feedback_ratio, 'feedback_ratio', int)
        check_range(feedback_ratio, 'feedback_ratio', 0, 3)

        self.VOUT_FS.INTFB.write(feedback_ratio)


    def feedback_select(self, select=None):
        """
        Command and Query the output feedback voltage location. Defaults to internal.

        :param select: Feedback Select Either external (1) or internal (0), defaults to None
        :type select: int, optional
        :return: Returns the current feedback select setting.
        :rtype: int
        """

        if select is None:
            return self.VOUT_FS.FB.read()
        
        check_type(select, 'feedback_ratio', int)
        check_range(select, 'feedback_ratio', 0, 1)

        self.VOUT_FS.FB.write(select)


    def mode(self, output_en=None, freq_doubling=None, hiccup=None, discharge=None, vcc=None, i2c_addr=None, pfm=None, mode=None):
        """
        Command or Query the operation mode of the device.

        :param output_en: Output enable 0 = off, 1 = on, defaults to None
        :type output_en: int, optional
        :param freq_doubling: Switching frequency doubling in buck-boost mode, 0 = off, 1 = on, defaults to None
        :type freq_doubling: int, optional
        :param hiccup: Hiccup mode, 0 = off, 1 = on, defaults to None
        :type hiccup: int, optional
        :param discharge: Output discharged through 100mA current sink when active, 0 = off, 1 = on, defaults to None
        :type discharge: int, optional
        :param vcc: Choose between internal LDO (0, default) or external 5V power supply (1), defaults to None
        :type vcc: int, optional
        :param i2c_addr: Swap between 0x74 (0, default) and 0x75 (1), defaults to None
        :type i2c_addr: int, optional
        :param pfm: Select operating mode at light load condition PFM (0, default) or FPWM (1), defaults to None
        :type pfm: int, optional
        :param mode:  Mode control approach set VCC, I2CADD, and PFM either through external resistor(0) or internal register (1), defaults to None
        :type mode: int, optional
        """
        inputs = [output_en, freq_doubling, hiccup, discharge, vcc, i2c_addr, pfm, mode]
        # if all are none, read back the state of the device
        if all (val is None for val in inputs):

            return_dict = {}
            register = self.MODE.read()
            return_dict['output_en'] = (register >> 7) & 1
            return_dict['freq_doubling'] = (register >> 6) & 1
            return_dict['hiccup'] = (register >> 5) & 1
            return_dict['discharge'] = (register >> 4) & 1
            return_dict['vcc'] = (register >> 3) & 1
            return_dict['i2c_addr'] = (register >> 2) & 1
            return_dict['pfm'] = (register >> 1) & 1
            return_dict['mode'] = (register >> 0) & 1
            return return_dict
        
        # check the types of the input
        check_type(output_en, 'output_en', int)
        check_type(freq_doubling, 'freq_doubling', int)
        check_type(hiccup, 'hiccup', int)
        check_type(discharge, 'discharge', int)
        check_type(vcc, 'vcc', int)
        check_type(i2c_addr, 'i2c_addr', int)
        check_type(pfm, 'pfm', int)
        check_type(mode, 'mode', int)
        
        # check the range of the inputs
        check_range(output_en, 'output_en', 0, 1)
        check_range(freq_doubling, 'freq_doubling', 0, 1)
        check_range(hiccup, 'hiccup', 0, 1)
        check_range(discharge, 'discharge', 0, 1)
        check_range(vcc, 'vcc', 0, 1)
        check_range(i2c_addr, 'i2c_addr', 0, 1)
        check_range(pfm, 'pfm', 0, 1)
        check_range(mode, 'mode', 0, 1)

        # read the current controls of the device
        register = self.MODE.read()

        # Have the inputs as binary values
        bin_list = [0 if value is None else value for value in inputs]
        
        # create the field mask from the changed inputs and data to be written
        field_mask = 0x00
        write_data = 0x00

        for index in range (7, -1, -1):
            if inputs[index] is not None:

                # Place a 1 in the position desired for editing.
                field_mask |= (1 << index)

                # make the write data equivalent to the inputs given
                # write_command = (output_en << 7) | (freq_doubling << 6) |  (hiccup << 5) |  (discharge << 4) |  (vcc << 3) |  (i2c_addr << 2) |  (pfm << 1) |  (mode << 0)
                write_data |= inputs[index] << (7-index)

            else:
                write_data |= 0 << index

        # clear the field bits we are writing to while leaving the others untouched
        register &= ~field_mask

        # Make changes to the register
        register |= write_data

        # write the register
        self.MODE.write(register)

    def initialize_rail(self, voltage, current_limit):
        """
        Startup Sequence for a TPS voltage rail.

        :param voltage: Output voltage desired for the rail
        :type voltage: int | float
        :param current_limit: Current limit boundary for the voltage rail
        :type current_limit: int | float
        """
        # set the output enable low.
        self.output_enable(0)

        # check the current status of the rail, if protection has been tripped then throw errors.
        status_dict = self.status()
        status_dict.pop("STATUS")
        msg = ''
        for key, value in status_dict.items():
            if value != "NONE":
                msg += f'Protection field {key} is in effect. Device status is reset and output is off. \n'

        if len(msg) > 0:
            raise ValueError(msg)


        # Throw an error for incorrect voltage or current values
        check_type(current_limit, 'current_limit', (int, float))
        check_range(current_limit, 'current_limit', 0, 6.35)

        # calculate the acceptable voltage drop between the ISP and ISN rails, a 10m ohm resistor on the EVM
        v_drop = current_limit / 100

        # write the voltage and current limit
        self.voltage(voltage)
        self.current_limit(v_drop)

        # set the output enable high
        self.output_enable(1)

    # TODO Implement CDC Method for CDC controls

    # TODO Implement Slew Rate method for slew controls


if __name__ == '__main__':
    i2c_bus =  I2C(1, sda=Pin(14), scl=Pin(15), freq=100_000)
    tps =  TPS55288(name="TPS_rail", address=0x74, i2c_bus=i2c_bus)
    devices = tps.i2c_bus.scan()
    hex_addr = [hex(x) for x in devices]
    print(f"Seen device addresses: {hex_addr}")

# -----------------------------------------
#              END OF FILE
# -----------------------------------------