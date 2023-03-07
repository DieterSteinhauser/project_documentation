LTC1661 DAC
=====================================


The LTC1661 from Linear Technology hosts two 10-bit DAC’s that are addressable via
SPI [1]_. Communication is configured with the SPI clock idling low and capturing data on the
rising edge of the clock.  The maximum baud rate of the LTC1661 is 10MHz [2]_.

.. figure:: theremin_images/image008.png
  :align: center

  Figure 1: Timing Diagram of LTC1661 SPI communication [2]_

Communication with this DAC is slightly more complicated due to the 10-bit resolution
associated with the device. Commanding the device to write to its internal register and Update is
the primary functionality desired for this module. Knowing this, the commands 0x9 or 0xA
would be applicable for continuously changing voltage on output A and B respectively [2]_

.. figure:: theremin_images/image009.png
  :align: center

  Figure 2: SPI communication Sequence for the LTC1661 [2]_.

In our program, we must parse the data for every transmission so that a word packet sent will
have the format seen in figure 2. The LTC1661 sends the command, then splits the data bits
between the two bytes, followed by don’t cares to fill the word packet. In an 8-, 12-, or 16-bit
DAC, less bit manipulation is required.



**References**


.. [1] “Serial peripheral interface,” Wikipedia, 27-Sep-2022. [Online]. Available:
    https://en.wikipedia.org/wiki/Serial_Peripheral_Interface. [Accessed: 19-Oct-2022].

.. [2] “Ltc1661 – micropower dual 10-bit DAC in MSOP - Analog Devices.” [Online]. Available:
    https://www.analog.com/media/en/technical-documentation/data-sheets/1661fb.pdf.
    [Accessed: 17-Oct-2022].

