# -----------------------------------------
#                 NOTES 
# -----------------------------------------

# Dieter Steinhauser
# 10/2023
# I2C Device, Register, and field objects for driver implementation

# -----------------------------------------
#               IMPORTS
# -----------------------------------------

# from pico_power_management.helpers import check_range, check_type, check_str, check_list, read_modify
from src.pico_power_management.helpers import *
# from helpers import *
import time

# -----------------------------------------
#               CLASS
# -----------------------------------------

_RW_TYPE = ['R', 'W', 'R/W']
_READ = ['R', 'R/W']
_WRITE = ['W', 'R/W']


class Device:

    def __init__(self, name:str, address:int, i2c_bus, description = None, width=8, endian='big', *args, **kwargs) -> None: 

        """
        Creation of an I2C Device.

        :param name: Device name.
        :type name: str
        :param address: device i2c address
        :type address: int
        :param i2c_bus: I2C Bus object for communication
        :type i2c_bus: i2c_bus
        :param description: Short Description of the device, defaults to None
        :type description: str, optional
        :param width: register bit width must be a power of 2 between 8 and 64, defaults to 8
        :type width: int, optional
        :param endian: endian structure of device, either big or little, defaults to 'big'
        :type endian: str, optional
        """

        # Check inputs for errors
        check_type(name, 'name', str)
        check_type(address, 'address', int)
        check_type(width, 'width', int)
        check_list(width, 'width', [8, 16, 32, 64])
        check_type(endian, 'endian', str)
        check_str(endian, 'endian', ('big', 'little'))

        self.name = name
        self.addr = address
        self.description = description
        self.registers= {}
        self.endian = endian
        self.width = width
        self.reg_bytes = int(width / 8)

        if i2c_bus is not None:
            self.i2c_bus = i2c_bus

            devices = i2c_bus.scan()
            # hex_addr = [hex(x) for x in devices]

            if address not in devices:
                raise ValueError(f'Cannot find device address {address} upon instantiation of I2C device. \nFound Device addresses: {devices} ')

 
    def read(self):
        """
        Read data from the device. 
        
        Primarily used when the I2C device does not employ a memory system or a register set.

        :param register: Register object to read from.
        :type register: Register
        :return: Data read from the register.
        """
        if not self.i2c_bus:
            raise ValueError("I2C bus not initialized.")
        
        read_data = self.i2c_bus.readfrom(self.addr, 1)
        return int.from_bytes(read_data, self.endian) # type: ignore

    def write(self, data):
        """
        Write data to the device.

        Primarily used when the I2C device does not employ a memory system or a register set.

        :param data: Data to write to the device.
        :type data: int
        """
        
        # Write the data to the bus
        self.i2c_bus.writeto(self.addr, data.to_bytes(self.reg_bytes, self.endian))
        
        # Confirm the write by reading and comparing the data
        read_data = self.read()
        if read_data != data:
            raise ValueError(f"Write confirmation failed.\nRead Data: {read_data} \nWritten Data: {data}")


    def add_register(self, name:str, address:int, *args, **kwargs) -> None:
        """
        Register addition to the device.

        :param name: Name of the Register
        :type name: str
        :param address: Address of the Register.
        :type address: int
        """

        register = Register(self, name, address, *args, **kwargs)
        self.registers[name] = register
        setattr(self, name, register)

    def reg_read(self, register):
        """
        Read data from a specific register in the device's memory.

        :param register: Register object to read from.
        :type register: Register
        :return: Data read from the register.
        """
        if not self.i2c_bus:
            raise ValueError("I2C bus not initialized.")
        
        read_data = self.i2c_bus.readfrom_mem(self.addr, register.addr, self.reg_bytes)
        return int.from_bytes(read_data, self.endian)  # type: ignore
            

    def reg_write(self, register, data):
        """
        Write data to a specific register in the device's memory.

        :param register: Register object to write to.
        :type register: Register
        :param data: Data to write to the register.
        :type data: int
        """
        
        # Write the data to the bus
        self.i2c_bus.writeto_mem(self.addr, register.addr, data.to_bytes(self.reg_bytes, self.endian))
        
        # If possible, confirm that we correctly edited the field.
        if register.r_w in _READ:

            # Confirm the write by reading and comparing the data
            read_data = self.reg_read(register)
            if read_data != data:
                raise ValueError(f"Write confirmation failed.\nRead Data: {read_data} \nWritten Data: {data}")





class Register:

    def __init__(self, device, name : str, address : int, r_w:str = "R/W", description = None, *args, **kwargs) -> None:
        """
        Register creation

        :param name: Name of the Register
        :type name: str
        :param address: Address of the Register.
        :type address: int
        """
        # Check inputs for errors
        check_type(name, 'name', str)
        check_type(address, 'address', int)

        self.name = name
        self.addr = address
        self.r_w = r_w
        self.description = description
        self.device = device
        self.endian = device.endian
        self.width = device.width
        self.reg_bytes = int(self.width / 8)
        self.fields= {}
        self.i2c_bus = device.i2c_bus

    def add_field(self, name:str, bit_offset:int, *args, **kwargs):
        """
        Field addition to the register.

        :param name: Name of field.
        :type name: str
        :param bit_offset: offset of the bits
        :type bit_offset: int
        :param size: size of the fields bits, defaults to 1
        :type size: _type_, optional
        :param r_w: Read/Write permissions for the field, can be 'R', 'W', 'R/W', defaults to "R/W"
        :type r_w: str, optional
        :param description: description of the field and how it operates, defaults to None
        :type description: str, optional
        """
        field = Field(self, name, bit_offset, *args, **kwargs)
        self.fields[name] = field
        setattr(self, name, field)

    def read(self):
        """
        Read from the register.

        :return: Returns the value of the read register.
        :rtype: int
        """
        # Throw an error if the I2C bus object does not exist.
        if not self.i2c_bus:
            raise ValueError("I2C bus not initialized.")
        
        # Throw an error if not readable.
        if self.r_w not in _READ:
            raise ValueError(f"Error writing to register, Permission is {self.r_w} 'Write Only'.")

        read_byte = self.i2c_bus.readfrom_mem(self.device.addr, self.addr, self.reg_bytes)
        return int.from_bytes(read_byte, self.endian)
    
         
    def write(self, value):
        """
        Write data to a register.

        :param value: integer value for the data to be written.
        :type value: int
        """

        # Throw an error if the I2C bus object does not exist.
        if not self.i2c_bus:
            raise ValueError("I2C bus not initialized.")

        # Throw an error if the field cannot be written.
        if self.r_w not in _WRITE:
            raise ValueError(f"Error writing to register, Permission is {self.r_w} 'Read Only'.")

        # Throw an error if the value is larger than the field width
        if value > (2**self.width - 1):
            raise ValueError(f"Error writing to register, Value {value} is too large for {self.width}-bit register size ")
        
        # Write the data to the bus
        self.i2c_bus.writeto_mem(self.device.addr, self.addr, value.to_bytes(self.reg_bytes, self.endian))

        # let the device settle, avoids EIO error
        # time.sleep_us(10)
        
        # If possible, confirm that we correctly edited the field.
        if self.r_w in _READ:

            # Confirm the write by reading and comparing the data
            read_data = self.read()
            if read_data != value:
                raise ValueError(f"Write confirmation failed.\nRead Data: {read_data} \nWritten Data: {value}")



class Field:

    def __init__(self, register, name:str, bit_offset:int, width:int = 1, r_w:str = "R/W", description = None, *args, **kwargs) -> None:
        """
        Field creation.

        :param name: Name of field.
        :type name: str
        :param name: Name of field.
        :type name: str
        :param bit_offset: offset of the bits
        :type bit_offset: int
        :param width: Width of the fields bits, defaults to 1
        :type width: _type_, optional
        :param r_w: Read/Write permissions for the field, can be 'R', 'W', 'R/W', defaults to "R/W"
        :type r_w: str, optional
        :param description: description of the field and how it operates, defaults to None
        :type description: str, optional
        """

        # Check inputs for errors
        check_type(name, 'name', str)
        check_type(bit_offset, 'bit_offset', int)
        check_range(bit_offset, 'bit_offset', 0, (register.width - 1))
        check_type(width, 'width', int)
        check_range(width, 'width', 1, register.width)
        
        if not isinstance(r_w, str) or r_w not in _RW_TYPE:
            raise ValueError(f" Incorrect value for r_w: {r_w}. Input should be in {_RW_TYPE}")
        
        self.name = name
        self.bit_offset = bit_offset
        self.width = width
        self.r_w = r_w
        self.description = description
        self.register = register
        self.device = register.device
        self.endian = register.endian
        self.reg_bytes = register.reg_bytes
        self.i2c_bus = register.i2c_bus
        
    def read(self):
        """
        Read from the field.

        :return: Returns the value of the read field.
        :rtype: int
        """
        # Throw an error if the I2C bus object does not exist.
        if not self.i2c_bus:
            raise ValueError("I2C bus not initialized.")
        
        # Throw an error if not readable.
        if self.r_w not in _READ:
            raise ValueError(f"Error writing to field, Permission is {self.r_w} 'Write Only'.")
        
        read_byte = self.i2c_bus.readfrom_mem(self.device.addr, self.register.addr, self.reg_bytes)
        
        read_data = int.from_bytes(read_byte, self.endian)
        field =  (read_data >> self.bit_offset) & ((2**self.width) - 1)
        return field
            
    def write(self, value):
        """
        Write data to a field.

        :param value: integer value for the data to be written.
        :type value: int
        """

        # Throw an error if the I2C bus object does not exist.
        if not self.i2c_bus:
            raise ValueError("I2C bus not initialized.")

        # Throw an error if the field cannot be written.
        if self.r_w not in _WRITE:
            raise ValueError(f"Error writing to field, Permission is {self.r_w} 'Read Only'.")

        # Throw an error if the value is larger than the field width
        if value > (2**self.width - 1):
            raise ValueError(f"Error writing to field, Value {value} is too large for {self.width}-bit field size ")
        
        # Perform a Read Modify Write Cycle.
        write_data = read_modify(read_data = self.register.read(), modify_data = (value << self.bit_offset), bit_mask = (((2**self.width)-1) << self.bit_offset))
        
        # Write the data to the bus
        self.i2c_bus.writeto_mem(self.device.addr, self.register.addr, write_data.to_bytes(self.reg_bytes, self.endian))

        # let the device settle, avoids EIO error
        # time.sleep_us(10)
        
        # Confirm the write by reading and comparing the data
        read_data = self.read()
        if read_data != value:
            raise ValueError(f"Write confirmation failed.\nRead Data: {read_data} \nWritten Data: {value}")
        

# -----------------------------------------
#               END OF FILE
# -----------------------------------------
   
