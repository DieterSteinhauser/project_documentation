16x2 LCD Display
=====================================

.. figure:: reference/lcd_i2c.png
  :align: center

  16x2 LCD Display with I2C Driver.


LCD Displays can be configured for I2C or Parallel communication with a microcontroller.
When configured with an I2C driver, much of the following is abstracted away for the user. Contrast, brightness, and
pinouts are much less complicated in this approach at the cost of price and speed.

.. figure:: reference/lcd.png
  :align: center

  16x2 LCD Display without I2C Driver.

Using parallel communication, the LCD is wired to the microcontroller with either four-bit or
eight bit communication [1]_. A potentiometer should be connected for contrast control of the LCD, and a 500 ohm
resistor for brightness control. If the user desires adaptive brightness control, a photoresistor and 1k-ohm
resistor can be connected in parallel.

.. figure:: reference/lcd_pinout.png
  :align: center

  16x2 LCD Display Pinout

Using 4-bit parallel communication, a nibble of data is sent to the display simultaneously. 8-bit parallel will
communicate a full byte simultaneously. Regardless of method, a full byte of data is then sent to the device
in a process called bit-banging. This splits a byte of data to send two nibbles in series for 4-bit communication,
ordered by the upper four bits and then the lower four bits.

.. figure:: reference/lcd_nibble_wiring.png
  :align: center

  Wiring for parallel nibble communication.

.. autoclass:: src.pico_devboard.LCD.LCD
   :members:
   :undoc-members:


Code
--------------------------

.. literalinclude:: ../../src/pico_devboard/LCD.py
   :language: python
   :linenos:


**References**


.. [1] “Sitronix ST7066U - Crystalfontz,” crystalfontz. [Online]. Available:
    https://www.crystalfontz.com/controllers/Sitronix/ST7066U/438. [Accessed: 03-Oct2022].

