# -----------------------------------------
#                 NOTES 
# -----------------------------------------
"""
Dieter Steinhauser
5/2023
Parallel LCD functions, Configured for 4-bit communication.
"""

# -----------------------------------------
#               IMPORTS
# -----------------------------------------

from machine import Pin
import time
utime = time

# -----------------------------------------
#          CONSTANTS AND VARIABLES
# -----------------------------------------

# CONSTANTS
# ----------------------

LCD_CMD = 0
LCD_DATA = 1

# ----------------------
# GPIO Wiring: Legacy Structure
# ----------------------

# EN = Pin(0, Pin.OUT) # Enable Pin
# RS = Pin(1, Pin.OUT) # Register Select

# PINS = [2, 3, 4, 5]  
# Pin numbers for the upper nibble, does the below assignment in configure method.
# D4 = Pin(2, Pin.OUT)
# D5 = Pin(3, Pin.OUT)
# D6 = Pin(4, Pin.OUT)
# D7 = Pin(5, Pin.OUT)
 
# list that gets populated with pinout objects for data line.
# DATA_BUS = []

# -----------------------------------------
#                 METHODS
# -----------------------------------------

# def Configure():
#     """Creates the data bus object from the pin list"""

#     for index in range(4):
#        DATA_BUS.append(Pin(PINS[index], Pin.OUT))

# # -----------------------------------------

# def lcd_strobe():
#     """Flashes the enable line and provides wait period."""

#     EN.value(1)
#     utime.sleep_ms(1)

#     EN.value(0)
#     utime.sleep_ms(1)

# # -----------------------------------------
 
# def lcd_write(command, mode):
#     """Sends data to the LCD module. """

#     # determine if writing a command or data
#     data = command if mode == 0 else ord(command)

#     # need upper nibble for first loop. lower nibble can use data directly.
#     upper = data >> 4
    
#     # write the upper nibble
#     for index in range(4):
#         bit = upper & 1
#         DATA_BUS[index].value(bit)
#         upper = upper >> 1

#     # strobe the LCD, sending the nibble
#     RS.value(mode)
#     lcd_strobe()

#     # write the lower nibble
#     for index in range(4):
#         bit = data & 1
#         DATA_BUS[index].value(bit)
#         data = data >> 1

#     # Strobe the LCD, sending the nibble 
#     RS.value(mode)
#     lcd_strobe()
#     utime.sleep_ms(1)
#     RS.value(1)

# # -----------------------------------------

# def lcd_clear():
#     """Clear the LCD Screen."""

#     lcd_write(0x01, 0)
#     utime.sleep_ms(5)

# # -----------------------------------------

# def lcd_home():
#     """Return the Cursor to the starting position."""

#     lcd_write(0x02, 0)
#     utime.sleep_ms(5)

# # -----------------------------------------


# def lcd_cursor_blink():
#     """Have the cursor start blinking."""

#     lcd_write(0x0D, 0)
#     utime.sleep_ms(1)

# # -----------------------------------------

# def lcd_cursor_on():
#     """Have the cursor on, Good for debugging."""

#     lcd_write(0x0E, 0)
#     utime.sleep_ms(1)

# # -----------------------------------------

# def lcd_cursor_off():
#     """Turn the cursor off."""

#     lcd_write(0x0C, 0)
#     utime.sleep_ms(1)

# # -----------------------------------------

# def lcd_puts(string):
#     """Write a string on to the LCD."""

#     for element in string:
#        lcd_putch(element)

# # -----------------------------------------

# def lcd_putch(c):
#     """Write a character on to the LCD."""
#     lcd_write(c, 1)

# # -----------------------------------------

# def lcd_goto(column, row):
    
    
#     if row == 0:
#         address = 0

#     if row == 1:
#         address = 0x40

#     if row == 2:
#         address = 0x14

#     if row == 3:
#         address = 0x54

#     address = address + column
#     lcd_write(0x80 | address, 0)

# # -----------------------------------------

# def lcd_init():
    
#     # Configure the pins of the device.
#     Configure()
#     utime.sleep_ms(120)

#     # clear values on data bus.
#     for index in range(4):
#         DATA_BUS[index].value(0)
#     utime.sleep_ms(50)

#     # initialization sequence.
#     DATA_BUS[0].value(1)
#     DATA_BUS[1].value(1)
#     lcd_strobe()
#     utime.sleep_ms(10)

#     lcd_strobe()
#     utime.sleep_ms(10)

#     lcd_strobe()
#     utime.sleep_ms(10)

#     DATA_BUS[0].value(0)
#     lcd_strobe()
#     utime.sleep_ms(5)

#     lcd_write(0x28, 0)
#     utime.sleep_ms(1)

#     lcd_write(0x08, 0)
#     utime.sleep_ms(1)

#     lcd_write(0x01, 0)
#     utime.sleep_ms(10)

#     lcd_write(0x06, 0)
#     utime.sleep_ms(5)

#     lcd_write(0x0C, 0)
#     utime.sleep_ms(10)


# -----------------------------------------
#                 LCD Class:
# -----------------------------------------


class LCD:
    """The LCD class is meant to abstract the LCD driver further and streamline development."""

    CMD_MODE = 0
    DATA_MODE = 1

    def __init__(self, enable_pin: int, reg_select_pin: int, data_pins: list) -> None:
        """
        Object initialization.

        :param enable_pin: integer value of the enable pin desired.
        :type enable_pin: int
        :param reg_select_pin: integer value of the reg_select pin desired.
        :type reg_select_pin: int
        :param data_pins: list of integer values for the data pins desired in communication.
        :type data_pins: list[int]
        """

        self.enable_pin = Pin(enable_pin, Pin.OUT)
        self.reg_select_pin = Pin(reg_select_pin, Pin.OUT)
        self._data_pins = data_pins
        self.data_bus = []
        
        # Configure the pins of the device.
        self._configure()
        utime.sleep_ms(120)

    # -----------------------------------------    

    def _configure(self):
        """Creates the data bus object from the pin list. """

        # Configure the pins of the device.
        for element in self._data_pins:
            self.data_bus.append(Pin(element, Pin.OUT))

    # -----------------------------------------

    def init(self):
        """Initializes the LCD for communication."""

        # clear values on data bus.
        for index in range(4):
            self.data_bus[index].value(0)
        utime.sleep_ms(50)

        # initialization sequence.
        self.data_bus[0].value(1)
        self.data_bus[1].value(1)
        self.strobe()
        utime.sleep_ms(10)

        self.strobe()
        utime.sleep_ms(10)

        self.strobe()
        utime.sleep_ms(10)

        self.data_bus[0].value(0)
        self.strobe()
        utime.sleep_ms(5)

        self.write(0x28, 0)
        utime.sleep_ms(1)

        self.write(0x08, 0)
        utime.sleep_ms(1)

        self.write(0x01, 0)
        utime.sleep_ms(10)

        self.write(0x06, 0)
        utime.sleep_ms(5)

        self.write(0x0C, 0)
        utime.sleep_ms(10)

    # -----------------------------------------

    def strobe(self):
        """
        Flashes the enable line and provides wait period.
        """

        self.enable_pin.value(1)
        utime.sleep_ms(1)

        self.enable_pin.value(0)
        utime.sleep_ms(1)

    # -----------------------------------------
    
    def write(self, command, mode):
        """
        Sends data to the LCD module.

        :param command: Information packet being sent to the LCD.
        :type command: str
        :param mode: Mode of operation for the LCD, either command mode (1) or data mode (0)
        :type mode: int
        :return: None
        """

        # determine if writing a command or data
        data = command if mode == 0 else ord(command)

        # need upper nibble for first loop. lower nibble can use data directly.
        upper = data >> 4
        
        # write the upper nibble
        for index in range(4):
            bit = upper & 1
            self.data_bus[index].value(bit)
            upper = upper >> 1

        # strobe the LCD, sending the nibble
        self.reg_select_pin.value(mode)
        self.strobe()

        # write the lower nibble
        for index in range(4):
            bit = data & 1
            self.data_bus[index].value(bit)
            data = data >> 1

        # Strobe the LCD, sending the nibble 
        self.reg_select_pin.value(mode)
        self.strobe()
        utime.sleep_ms(1)
        self.reg_select_pin.value(1)

    # -----------------------------------------

    def clear(self):
        """
        Clears the LCD Screen.

        Good to perform on occasion but produces flashing on screen when triggered consistently.
        """

        self.write(0x01, 0)
        utime.sleep_ms(5)

    # -----------------------------------------

    def home(self):
        """
        Return the Cursor to the starting position.

        Functionally the same as using the go_to function and specifying (0, 0) coordinates.
        """

        self.write(0x02, 0)
        utime.sleep_ms(5)

    # -----------------------------------------


    def blink(self):
        """
        Have the cursor start blinking.
        """

        self.write(0x0D, 0)
        utime.sleep_ms(1)

    # -----------------------------------------

    def cursor_on(self):
        """
        Have the cursor on, Good for debugging.
        """

        self.write(0x0E, 0)
        utime.sleep_ms(1)

    # -----------------------------------------

    def cursor_off(self):
        """
        Turn the cursor off.
        """

        self.write(0x0C, 0)
        utime.sleep_ms(1)

    # -----------------------------------------

    def print(self, string):
        """
        Write a string on to the LCD.

        Wrapper of the string function with more descriptive naming.

        :param string: String desired to be written.
        :type string: str

        """

        for element in string:
            self._putch(element)

    # -----------------------------------------

    def _putch(self, c):
        """
        Write a character on to the LCD.

        Protected because the method is less intuitive compared to the print.

        :param c: ASCII character.
        :type c: str
        :return: None
        """
        self.write(c, 1)

    # -----------------------------------------

    def _puts(self, string):
        """
        Write a string on to the LCD.

        :param string: String desired to be written.
        :type string: str
        :return: None
        """

        for element in string:
            self._putch(element)

    # -----------------------------------------
    def go_to(self, column, row):
        """
        Move the cursor to a specific column and row.

        :param column: Column index, 0-15. May be higher on different size LCDs
        :type column: int
        :param row: Row index, 0-1. May be higher on different size LCDs
        :type row: int
        :return: None
        """
        if row == 0:
            address = 0

        if row == 1:
            address = 0x40

        if row == 2:
            address = 0x14

        if row == 3:
            address = 0x54

        address = address + column
        self.write(0x80 | address, 0)

 
# -----------------------------------------
#              END OF FILE
# -----------------------------------------