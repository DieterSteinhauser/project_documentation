16x2 LCD Display
=====================================

.. figure:: reference/lcd_i2c.png
  :align: center

  Figure 1: 16x2 LCD Display with I2C Driver.


LCD Displays can be configured for I2C or Parallel communication with a microcontroller.
When configured with an I2C driver, much of the following is abstracted away for the user. Contrast, brightness, and
pinouts are much less complicated in this approach at the cost of price and speed.

.. figure:: reference/lcd.png
  :align: center

  Figure 1: 16x2 LCD Display without I2C Driver.

Using parallel communication, the LCD is wired to the microcontroller with either four-bit or
eight bit communication [1]_. A potentiometer should be connected for contrast control of the LCD, and a 500 ohm
resistor for brightness control. If the user desires adaptive brightness control, a photoresistor and 1k-ohm
resistor can be connected in parallel.

.. figure:: reference/lcd_pinout.png
  :align: center

  Figure 1: 16x2 LCD Display Pinout

Using 4-bit parallel communication, a nibble of data is sent to the display simultaneously. 8-bit parallel will
communicate a full byte simultaneously. Regardless of method, a full byte of data is then sent to the device
in a process called bit-banging. This splits a byte of data to send two nibbles in series for 4-bit communication,
ordered by the upper four bits and then the lower four bits.

.. figure:: reference/lcd_nibble_wiring.png
  :align: center

  Figure 1: Wiring for parallel nibble communication.

.. code-block:: python
   :caption: LCD Class for Parallel Communication.

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
   import utime

   # -----------------------------------------
   #          CONSTANTS AND VARIABLES
   # -----------------------------------------

   # CONSTANTS
   # ----------------------

   LCD_CMD = 0
   LCD_DATA = 1

   # -----------------------------------------
   #                 LCD Class:
   # -----------------------------------------


   class LCD:
       """The LCD class is meant to abstract the LCD driver further and streamline development."""

       CMD_MODE = 0
       DATA_MODE = 1

       def __init__(self, enable_pin: int, reg_select_pin: int, data_pins: list) -> None:
           """Object initialization"""

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
           """Flashes the enable line and provides wait period."""

           self.enable_pin.value(1)
           utime.sleep_ms(1)

           self.enable_pin.value(0)
           utime.sleep_ms(1)

       # -----------------------------------------

       def write(self, command, mode):
           """Sends data to the LCD module. """

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
           """Clear the LCD Screen."""

           self.write(0x01, 0)
           utime.sleep_ms(5)

       # -----------------------------------------

       def home(self):
           """Return the Cursor to the starting position."""

           self.write(0x02, 0)
           utime.sleep_ms(5)

       # -----------------------------------------


       def blink(self):
           """Have the cursor start blinking."""

           self.write(0x0D, 0)
           utime.sleep_ms(1)

       # -----------------------------------------

       def cursor_on(self):
           """Have the cursor on, Good for debugging."""

           self.write(0x0E, 0)
           utime.sleep_ms(1)

       # -----------------------------------------

       def cursor_off(self):
           """Turn the cursor off."""

           self.write(0x0C, 0)
           utime.sleep_ms(1)

       # -----------------------------------------

       def print(self, string):
           """Write a string on to the LCD."""

           for element in string:
               self._putch(element)

       # -----------------------------------------

       def _putch(self, c):
           """Write a character on to the LCD."""
           self.write(c, 1)

       # -----------------------------------------

       def _puts(self, string):
           """Write a string on to the LCD."""

           for element in string:
               self._putch(element)


       # -----------------------------------------
       def go_to(self, column, row):


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

.. code-block:: python
   :caption: Parallel Nibble LCD Driver without class.

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
   import utime

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

   EN = Pin(0, Pin.OUT) # Enable Pin
   RS = Pin(1, Pin.OUT) # Register Select

   PINS = [2, 3, 4, 5]
   # Pin numbers for the upper nibble, does the below assignment in configure method.
   # D4 = Pin(2, Pin.OUT)
   # D5 = Pin(3, Pin.OUT)
   # D6 = Pin(4, Pin.OUT)
   # D7 = Pin(5, Pin.OUT)

   # list that gets populated with pinout objects for data line.
   DATA_BUS = []

   # -----------------------------------------
   #                 METHODS
   # -----------------------------------------

   def Configure():
       """Creates the data bus object from the pin list"""

       for index in range(4):
          DATA_BUS.append(Pin(PINS[index], Pin.OUT))

   # -----------------------------------------

   def lcd_strobe():
       """Flashes the enable line and provides wait period."""

       EN.value(1)
       utime.sleep_ms(1)

       EN.value(0)
       utime.sleep_ms(1)

   # -----------------------------------------

   def lcd_write(command, mode):
       """Sends data to the LCD module. """

       # determine if writing a command or data
       data = command if mode == 0 else ord(command)

       # need upper nibble for first loop. lower nibble can use data directly.
       upper = data >> 4

       # write the upper nibble
       for index in range(4):
           bit = upper & 1
           DATA_BUS[index].value(bit)
           upper = upper >> 1

       # strobe the LCD, sending the nibble
       RS.value(mode)
       lcd_strobe()

       # write the lower nibble
       for index in range(4):
           bit = data & 1
           DATA_BUS[index].value(bit)
           data = data >> 1

       # Strobe the LCD, sending the nibble
       RS.value(mode)
       lcd_strobe()
       utime.sleep_ms(1)
       RS.value(1)

   # -----------------------------------------

   def lcd_clear():
       """Clear the LCD Screen."""

       lcd_write(0x01, 0)
       utime.sleep_ms(5)

   # -----------------------------------------

   def lcd_home():
       """Return the Cursor to the starting position."""

       lcd_write(0x02, 0)
       utime.sleep_ms(5)

   # -----------------------------------------


   def lcd_cursor_blink():
       """Have the cursor start blinking."""

       lcd_write(0x0D, 0)
       utime.sleep_ms(1)

   # -----------------------------------------

   def lcd_cursor_on():
       """Have the cursor on, Good for debugging."""

       lcd_write(0x0E, 0)
       utime.sleep_ms(1)

   # -----------------------------------------

   def lcd_cursor_off():
       """Turn the cursor off."""

       lcd_write(0x0C, 0)
       utime.sleep_ms(1)

   # -----------------------------------------

   def lcd_puts(string):
       """Write a string on to the LCD."""

       for element in string:
          lcd_putch(element)

   # -----------------------------------------

   def lcd_putch(c):
       """Write a character on to the LCD."""
       lcd_write(c, 1)

   # -----------------------------------------

   def lcd_goto(column, row):


       if row == 0:
           address = 0

       if row == 1:
           address = 0x40

       if row == 2:
           address = 0x14

       if row == 3:
           address = 0x54

       address = address + column
       lcd_write(0x80 | address, 0)

   # -----------------------------------------

   def lcd_init():

       # Configure the pins of the device.
       Configure()
       utime.sleep_ms(120)

       # clear values on data bus.
       for index in range(4):
           DATA_BUS[index].value(0)
       utime.sleep_ms(50)

       # initialization sequence.
       DATA_BUS[0].value(1)
       DATA_BUS[1].value(1)
       lcd_strobe()
       utime.sleep_ms(10)

       lcd_strobe()
       utime.sleep_ms(10)

       lcd_strobe()
       utime.sleep_ms(10)

       DATA_BUS[0].value(0)
       lcd_strobe()
       utime.sleep_ms(5)

       lcd_write(0x28, 0)
       utime.sleep_ms(1)

       lcd_write(0x08, 0)
       utime.sleep_ms(1)

       lcd_write(0x01, 0)
       utime.sleep_ms(10)

       lcd_write(0x06, 0)
       utime.sleep_ms(5)

       lcd_write(0x0C, 0)
       utime.sleep_ms(10)

**References**


.. [1] “Sitronix ST7066U - Crystalfontz,” crystalfontz. [Online]. Available:
    https://www.crystalfontz.com/controllers/Sitronix/ST7066U/438. [Accessed: 03-Oct2022].

