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
   :caption: Parallel Nibble LCD Driver

    #--------------------------------------------------
    #       PARALLEL LCD FUNCTIONS
    #       ======================
    #
    # These functions initialize and control the LCD
    #
    # Author: Dogan Ibrahim
    # File  : LCD
    # Date  : August, 2021
    #--------------------------------------------------
    # Modified by Dieter Steinhauser
    #--------------------------------------------------
    from machine import Pin
    import utime

    # ----------------------
    LCD_CMD = 0
    LCD_DATA = 1
    # ----------------------

    # GPIO Wiring
    # ----------------------


    EN = Pin(0, Pin.OUT)
    RS = Pin(1, Pin.OUT)
    D4 = Pin(2, Pin.OUT)
    D5 = Pin(3, Pin.OUT)
    D6 = Pin(4, Pin.OUT)
    D7 = Pin(5, Pin.OUT)
    PORT = [2, 3, 4, 5]
    L = [0,0,0,0]


    # Methods
    # ----------------------

    def Configure():

        for i in range(4):
           L[i] = Pin(PORT[i], Pin.OUT)

    def lcd_strobe():

        EN.value(1)
        utime.sleep_ms(1)
        EN.value(0)
        utime.sleep_ms(1)

    def lcd_write(c, mode):

        if mode == 0:
           d = c
        else:
           d = ord(c)
        d = d >> 4
        for i in range(4):
            b = d & 1
            L[i].value(b)
            d = d >> 1
        RS.value(mode)
        lcd_strobe()

        if mode == 0:
           d = c
        else:
           d = ord(c)
        for i in range(4):
            b = d & 1
            L[i].value(b)
            d = d >> 1
        RS.value(mode)
        lcd_strobe()
        utime.sleep_ms(1)
        RS.value(1)

    def lcd_clear():

        lcd_write(0x01, 0)
        utime.sleep_ms(5)

    def lcd_home():

        lcd_write(0x02, 0)
        utime.sleep_ms(5)

    def lcd_cursor_blink():

        lcd_write(0x0D, 0)
        utime.sleep_ms(1)

    def lcd_cursor_on():

        lcd_write(0x0E, 0)
        utime.sleep_ms(1)

    def lcd_cursor_off():

        lcd_write(0x0C, 0)
        utime.sleep_ms(1)

    def lcd_puts(s):

        l = len(s)
        for i in range(l):
           lcd_putch(s[i])

    def lcd_putch(c):

        lcd_write(c, 1)

    def lcd_goto(col, row):
        c = col + 1
        if row == 0:
            address = 0
        if row == 1:
            address = 0x40
        if row == 2:
            address = 0x14
        if row == 3:
            address = 0x54
        address = address + c - 1
        lcd_write(0x80 | address, 0)

    def lcd_init():

        Configure()
        utime.sleep_ms(120)
        for i in range(4):
            L[i].value(0)
        utime.sleep_ms(50)
        L[0].value(1)
        L[1].value(1)
        lcd_strobe()
        utime.sleep_ms(10)
        lcd_strobe()
        utime.sleep_ms(10)
        lcd_strobe()
        utime.sleep_ms(10)
        L[0].value(0)
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
    #================= END OF LCD FUNCTIONS =======================


**References**


.. [1] “Sitronix ST7066U - Crystalfontz,” crystalfontz. [Online]. Available:
    https://www.crystalfontz.com/controllers/Sitronix/ST7066U/438. [Accessed: 03-Oct2022].

