Communication Protocols
=====================================

***********************************
SPI - Serial Peripheral Interface
***********************************

SPI is a full-duplex serial communication protocol that was created by Motorola in the
1980’s for high-speed communication in embedded systems [18]_. The SPI protocol consists of a
single master device and one or many slave devices. For a simple two device system, A clock
(SCLK), a chip select (CS), and two data lines (MOSI, MISO) are employed. MOSI is the data
transmitted from the master device, while MISO is the data received from the master device.

.. figure:: theremin_images/image004.png
  :align: center

  Figure 1: SPI configuration for a two-device system [18]_.

SPI can incorporate multiple slave devices by connecting data and clock lines,
individually accessing a slave device by using a dedicated chip select line for each device as seen
in figure 2. This can become GPIO intensive as the number of pins needed on the master device
will increase with each additional slave device. Alternatively, SPI devices can work
cooperatively by tying all chip selects to the same line as seen in figure 3. This works well if data
does not need to be returned from the slave devices and the slave devices are intended to have
the same output.


..  |fig5| image:: theremin_images/image005.png
           :width: 320


..  |fig6| image:: theremin_images/image006.png
           :width: 320

.. list-table::
   :header-rows: 0

   * - |fig5|
     - |fig6|
   * - *Figure 2: SPI independent configuration* [18]_.
     - *Figure 3: SPI daisy-chained configuration* [18]_.



SPI transmits and receives data simultaneously in both directions, making the
communication full duplex in design. SPI also uses GPIO for addressing a chip instead of
transmitting addresses over the data lines commonly seen in I2C. Because of the full duplex data
transmission and GPIO addressing, SPI has very high transmission speeds, but can become
GPIO intensive. In practice, the maximum clock speeds of a SPI configuration depend highly on
the connected devices and their method of connection. Finally, the SPI protocol is highly
configurable in that the clock polarity and phase can be configured. This is also highly dependent
on connected devices and should be considered when creating a two-device or multi-device
system. In terms of using SPI on the Pico, A clock at or below 1MHz is best for breadboarding
and flywire use.


**References**


.. [18] “Serial peripheral interface,” Wikipedia, 27-Sep-2022. [Online]. Available:
    https://en.wikipedia.org/wiki/Serial_Peripheral_Interface. [Accessed: 19-Oct-2022].


