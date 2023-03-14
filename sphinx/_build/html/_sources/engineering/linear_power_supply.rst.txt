Linear Power Supply
====================================================

Date: 3/2023

Revision: 1

.. figure:: power_supply/power_supply.jpg
  :align: center

  Figure 42: Finished Linear power supply.



*******************
Introduction
*******************

The Raspberry Pico is a powerful and inexpensive microcontroller that can be used for a variety of projects.
However, the Raspberry Pi Foundation prioritized factors of size, efficiency, and cost when creating the board.
This leaves certain drawbacks of the microcontroller that are well documented in the Pico datasheet [15]_.
In this project, I aim to solve a few minor inconveniences of the Pico's design and create a development board better
suited to approaching projects. Fixes include a reset button, an off switch for the onboard SMPS,
LDO voltage regulators, and better ADC performance. Additionally, Parallel 16x2 LCD display, two 10-bit DAC channels,
and SD card R/W capability are added to allow the development board to act as a drop in test bench for relaying or saving
information.

******************
Methods
******************

.. seealso:: This project draws from numerous engineering concepts. For general reference and theory, concepts and
    components from the pages below are employed. Topics that required greater detail for clarification
    are revisited.

    * :ref:`Transformers`
    * :ref:`Full-Bridge Rectifier`
    * :ref:`Application Note: Rectification Filtering`
    * :ref:`Linear Regulators`
    * :ref:`Raspberry Pico Microcontroller`
    * :ref:`Data Conversion: ADC and DAC Theory`
    * :ref:`Instrumentation Amplifiers`
    * :ref:`16x2 LCD Display`


ADC Configuration
------------------

Since the ADC in on the Raspberry Pico, initial setup of the ADC can easily be achieved using the ADC section of the
Pico Software Development Kit (SDK) [16]. This provides the engineer with a simple and straightforward introduction
on taking ADC readings. However, the 12-bit ADC onboard the Pico is not great by any means. This is due to the
switching power regulator on the Pico. As a result of switching signal noise, the onboard voltage reference for
the ADC is setup in poor conditions. The ADC has a 30mV offset and its signal is quite noisy [15]. The datasheet
gives suggestions on improvement of the ADC readings. An External reference voltage may be used, the R7 resistor
can be removed, or issues can be mitigated in averaging and offset code. I chose a different route entirely, by
adding bypass capacitors to the reference voltage and ADC input pins for filtering and smoothing. Adding bypass
capacitors to the reference voltage and ADC input pins can also improve filtering and smoothing at the cost of
a larger circuit footprint.

.. figure:: devboard/adc_ref.png
  :align: center

  Figure 18: Pico ADC reference circuit [13]_.


For this project, I did everything I could to isolate the ADC reference for the best possible readings.
Essentially, I have added a separate 3.3V linear regulator specifically for the ADC reference. To use this reference
voltage without digital operation or SMPS noise, I have removed the R7 resistor that connects the Pico’s 3.3V source
to the ADC reference. This method heavily isolates the ADC reference. It is potentially overkill, but I was interested
in seeing how the device would perform. Driving the Pico via a 3.3V LDO feeds the ADC reference through a lowpass
filter onboard. This creates a significant improvement from ADC SMPS measurements.

Power Regulation and Filtering
--------------------------------

To supply power to the system, I chose to use the LDL1117 5V and 3.3V low-dropout regulators.
This allows for a 9-12V DC source to supply the devices without much overhead. This provided
a smooth 5V and 3.3V source for most components, with local decoupling capacitors where needed.

In addition to the 5V source, I powered the Raspberry Pico via the VSYS node to activate
the device and use the 3.3V Switching Mode Power Supply (SMPS). This was done using a
Schottky diode from 5V to VSYS to avoid backflow when the Pico is plugged in via USB [13]_.
The Pico power-chain is good because the SMPS is efficient, but noise on the output causes
problems with other systems like the ADC [13]_, [14]_. As a result, I byapassed the SMPS entirely by incorporating a
shutoff switch for the SMPS.

.. figure:: theremin_images/figure18.png
  :align: center

  Figure 18: Pico Power-chain and the implemented method of external supply [8]_.

SD Card Reader
------------------

An SD card reader has been added via SPI [16]_. This permits the user to incorporate data collection over time via
sensors and ADC readings. These data readings can be written to text or csv files on a SD card for post test analysis.

Inputs and Outputs
---------------------

A physical reset button was added to the development board to interrupt the RUN pin on the Pico. When this pin is
connected to ground, the device will shut off. To insure proper reset, hold the reset button for 3 seconds. This will
guarantee that the Pico has been discharged. The Pico has a full array of female headers for easy pinout access and
another for seating the pico onboard. Pinout names have been added to the silkscreen simplify development.


Schematic and PCB Design
-------------------------

.. figure:: devboard/devboard_schematic1.png
  :align: center

  Figure 22: Devboard schematic page 1 of 2.

.. figure:: devboard/devboard_schematic2.png
  :align: center

  Figure 23: Devboard schematic page 2 of 2.

.. figure:: devboard/dev_board_top_altium.png
  :align: center

  Figure 24: Top side of Devboard PCB layout.

.. figure:: devboard/dev_board_bottom_altium.png
  :align: center

  Figure 24: Bottom side of Devboard PCB layout.

Bill Of Materials
---------------------

.. csv-table:: Bill Of Materials
   :file: devboard/BillOfMaterials.csv


******************
Results
******************

The schematic of the circuit and PCB turned out well, with minimal errors. The
assembled PCB was easy to debug because of its plentiful headers employed in the diagram.
Also, using female headers for the ultrasonic sensors, LCD, DIP packages, and potentiometers
aided debug and ensured that any errors in design could be more easily fixed if the PCB was
routed wrong. Thankfully, there were no design breaking errors in this circuit, and most
components worked immediately after installation.

.. figure:: devboard/dev_board_assembled.jpg
  :align: center

  Figure 42: Raspberry Pico Development Board


Power
---------------------

The power regulation and filtering produced a 5V and 3.3V source with minimal noise, observed
with as little as 10mV ripple on both sources.

.. figure:: devboard/powerchain.jpg
  :align: center

  Figure 27: Power regulation system on the PCB

.. figure:: devboard/scope_power.png
  :align: center

  Figure 28: 5V and 3.3V source observed on the oscilloscope.

.. figure:: devboard/scope_power_zoom.png
  :align: center

  Figure 29: 5V and 3.3V source observed on the oscilloscope, both from a 20mV div.



******************
Appendix
******************

LCD.py
---------------------

    .. literalinclude:: devboard/LCD.py
       :language: python
       :linenos:

sdcard.py
---------------------

    .. literalinclude:: devboard/sdcard.py
       :language: python
       :linenos:

test.py
---------------------

    .. literalinclude:: devboard/test.py
       :language: python
       :linenos:

******************
References
******************


.. [2] “What is a bypass capacitor? tutorial: Applications,” Electronics Hub, 14-Sep-2021.
    [Online]. Available: https://www.electronicshub.org/bypass-capacitor-tutorial/. [Accessed:
    27-Aug-2022].

.. [10] “Ltc1661 – micropower dual 10-bit DAC in MSOP - Analog Devices.” [Online]. Available:
    https://www.analog.com/media/en/technical-documentation/data-sheets/1661fb.pdf.
    [Accessed: 17-Oct-2022].

.. [13] “Raspberry Pico Datasheet,” raspberrypi.com. [Online]. Available:
    https://datasheets.raspberrypi.com/pico/pico-datasheet.pdf. [Accessed: 15-Nov-2022].

.. [14] “Raspberry Pico python SDK,” raspberrypi.com. [Online]. Available:
    https://datasheets.raspberrypi.com/pico/raspberry-pi-pico-python-sdk.pdf. [Accessed: 15-
    Nov-2022].

.. [15] “RP2040 Datasheet,” raspberrypi.com. [Online]. Available:
    https://datasheets.raspberrypi.com/rp2040/rp2040-datasheet.pdf. [Accessed: 14-Nov-2022].

.. [16] “Serial peripheral interface,” Wikipedia, 27-Sep-2022. [Online]. Available:
    https://en.wikipedia.org/wiki/Serial_Peripheral_Interface. [Accessed: 19-Oct-2022].

.. [17] “Sitronix ST7066U - Crystalfontz,” crystalfontz. [Online]. Available:
    https://www.crystalfontz.com/controllers/Sitronix/ST7066U/438. [Accessed: 03-Oct2022].

.. [18] “What is a Bypass Capacitor?,” What is a bypass capacitor? [Online]. Available:
    http://www.learningaboutelectronics.com/Articles/What-is-a-bypass-capacitor.html.
    [Accessed: 27-Aug-2022].






