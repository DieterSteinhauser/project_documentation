Linear Power Supply
====================================================

Date: 3/2023

Revision: 1

.. figure:: power_supply/power_supply.jpg
  :align: center

  Figure 1: Finished Linear power supply.

*******************
Introduction
*******************

The purpose and goals of this project are to become familiar with linear power supply design, prepare engineers to
transform, regulate, and rectify power for future projects, and create a critical tool for any engineer’s lab.
Power transformation, AC to DC rectification, and voltage regulation are key components for practically every
electrical project. With this project, we aim to design a 20V/3A linear power supply with adjustable voltage
and current limiting capability. We also aim to create a precise voltmeter and ammeter to relay status of the supply.

******************
Methods
******************

.. seealso:: This project draws from numerous engineering concepts. For general reference and theory, concepts and
    components from the pages below are employed. Topics that required greater detail for clarification
    are revisited.

    * :ref:`Transformers`
    * :ref:`Full-Bridge Rectifier`
    * :ref:`Decoupling and Bypass`
    * :ref:`Application Note: Rectification Filtering`
    * :ref:`Zener Regulation`
    * :ref:`Linear Regulators`
    * :ref:`Instrumentation Amplifiers`
    * :ref:`Charge Pumps`
    * :ref:`Voltage Reference - VBE Multiplier`
    * :ref:`Raspberry Pico Microcontroller`
    * :ref:`Data Conversion: ADC and DAC Theory`
    * :ref:`16x2 LCD Display`


Project Overview
------------------

This linear power supply aims to provide up to 20 volts at 3 amps. The design employs linear regulators to minimize
noise of the output, adjust voltage, and a current limit for the device. The power supply will need to be monitored
for the output current and voltage. A Raspberry Pico will be employed for taking voltage and current measurements and
displaying them on an LCD for the user. LED indicators, reverse polarity protection, and output enable switch are also
added for a better user interface. A fuse will also be used for the safety of the user and the device.


Introduction to AC/DC Linear Power Supply
----------------------------------------------

.. figure:: power_supply/supply_abstract.png
  :align: center

  Figure 2: Fig 7-35 of Circuit Analysis and Design [1]_. Block diagram of a basic AC-DC linear power supply.


An AC to DC converter can be broken up into multiple stages. An AC input usually needs transformation of the existing
power to step up or down voltage to the desired range of operation. In our case, 120V wall power needs to be stepped
down by a factor of six to eight before use in the rest of our circuit. This will bring the AC voltage of the
secondary between 15 and 20V, ready for rectification from AC to DC. A full bridge rectifier is employed to have
current flow in the same direction for each half cycle of AC wave. A rectified wave would then require filter
components for reducing voltage swing. Capacitors are employed to store change and mitigate this voltage swing
but a separate step for regulation is required. Regulation can be accomplished using multiple methods, primarily
using voltage regulator IC’s or Zener diodes in reverse breakdown.

.. figure:: power_supply/simple_supply_circuit.png
  :align: center

  Figure 3: Fig 7-40 of Circuit Analysis and Design [1]_.  A complete circuit of a basic power supply. This design
  employs a Zener diode regulator.


Power Supply Circuit Design
------------------------------

.. figure:: power_supply/block_diagram_drawio.png
  :align: center

  Figure 4: Hardware Block Diagram of the Linear Power Supply.

The circuit implements the general systems shown in the block diagram. From the AC outlet, a fuse and switch connect
mains voltage to the device for operation. The Flat-Pak 16V transformer (FP16-3000) which can deliver 48VA of power.
This device is perhaps one of the most limiting factors of the supply. I anticipate 22.6V peak-to-peak voltage from a
115V AC circuit, which may not be enough for a 20V output after regulation. This will be followed by a RS603M full
bridge rectifier, with a forward voltage drop of 1.1V. Two 2200uF capacitors follow the rectifier for filtering,
providing a raw DC voltage around 21.5V to the following circuit stages.

.. figure:: power_supply/input_stage.png
  :align: center

  Figure 5: Input voltage conditioning Stage.

The rectified voltage is passed into the Constant Current Constant Voltage (CCCV) stage for output conditioning.
Both stages center around a LD1085 linear regulator IC, which has a 30V rating a can supply 3A of current. The constant
current stage uses a selection of switchable series resistances to determine the current limit of following stage.
Both output and adjust pins are bypassed for better noise performance but comes at the cost of storing and possibly
supplying more energy during a transient spike from the load.


The constant voltage stage allows for switching between a selection of fixed voltage outputs and an adjustable output.
Given there is no current limiting occurring, the device should provide 1.25V to about 20V. The output’s upper
boundary is limited by the dropout voltage over both linear regulators, forward voltage of the rectifier, output of
the transformer, and the AC voltage seen at the plug. The supply should comfortably hit
20V on the output under moderate loads, however bottlenecks may be encountered for worst case scenarios. Again, each
terminal of the LD1085 is bypassed for noise performance. Diodes are incorporated for protection purposes on each
regulator and will provide a discharge path for capacitors on the adjust and output pins when the device is turned off.
An output enable switch, reverse polarity diode, and a LED is employed for output safety and interaction.

.. figure:: power_supply/cccv_stage.png
  :align: center

  Figure 5: Constant Current-Constant Voltage Stage with reverse polarity protection.

.. Warning:: There are some flaws with the constant current circuit as depicted. Decoupling capacitors on the output and
   adjust pins of the constant current regulator cause current spikes from various operations. the short circuit
   implemented originally was removed in favor of a 0.33ohm resistor providing the same effect as before. Finally, to
   reduce transient uncertainty when switching between Rlim resistors, A 10kOhm resistor was added in parallel to Rlim.

   If you attempt to recreate this constant current circuit, remove the decoupling capacitors, short circuit condition,
   and add a high resistance in parallel to Rlim.

The output of the CCCV then feeds into the measurement circuitry for observation and user interaction.
A 0.1 Ohm shunt resistor is added for high side current sensing. This was done with the INA128 which should have
no problem observing the dynamic range of the power supply. The current can be no more than 3 amps as set by
both the transformer and the regulators. This circuit observe currents in the full operation range and imposes
minimal voltage loss on the output. A 100W rated shunt is used for safety during a short circuit condition. A gain
of 10 is applied to make the output voltage functionally equivalent to the observed current over the shunt resistor.
This means that a 0-3V output can easily be read by a 3.3V ADC. The output voltage is observed through a resistor
divider that similarly creates a 0-3V output for ADC readings. The ratio of loss from the divider is inverted and
applied back to the sensed ADC value in software to relay the correct output voltage.

.. figure:: power_supply/monitor_stage.png
  :align: center

  Figure 5: Input voltage conditioning Stage.

The INA128 used for current readings has a 36V operation range and requires about 2V of offset from each rail to
operate effectively. The device will be supplied by both the rectified voltage and a negative reference voltage.
This is because the rectified voltage should be approximately 2 to 3V higher than the output of the voltage regulator,
giving enough room for higher voltage measurements. However, the device must also output on the 0-3V range.
To do this effectively, a negative voltage reference must be made to supply an offset from the lower rail of
operation. A negative voltage rail around -3 to -7V is sufficient. This was done using a negative voltage charge
pump that feeds a VBE multiplier, giving a nice output reference. The INA128 will only draw about 1mA of current
from this rail, so a charge pump is fine for this purpose.

.. figure:: power_supply/negative_ref.png
  :align: center

  Figure 5: Negative voltage charge pump with Vbe multiplier output.

Pico Setup
------------------------------

To supply power to the measurement devices, I chose a combination of regulators power the sensor devices.
This provided a smooth 5V and 3.3V source for most components, with local decoupling capacitors where needed.
The LM7805 is a prime candidate for 5V regulation as its implementation is simple, only requiring two capacitors
on the Vin and Vout. The 7805 is also tolerant to the range of voltage seen after rectification.

.. figure:: reference/fixed_out_app.png
  :align: center

  Figure 1: Fixed Output Regulator configuration for an LM7805.

In addition to the 5V source, I powered the Raspberry Pico via 3.3V regulators. Two 3.3V rails were also developed
using LT1086 regulators, also in a fixed configuration. One regulator was connected directly to the 3.3V rail,
while the other was connected to the ADC reference.


.. figure:: theremin_images/figure18.png
  :align: center

  Figure 2: Pico Power-chain.


ADC Configuration
------------------------------

.. figure:: devboard/adc_ref.png
  :align: center

  Figure 18: Pico ADC reference circuit.

For this project, I did everything I could to isolate the ADC reference for the best possible readings. Essentially,
I have added a separate 3.3V linear regulator specifically for the ADC reference. To use this reference voltage
without digital operation or SMPS noise, I have removed the R7 resistor that connects the Pico’s 3.3V source to the
ADC reference. This method heavily isolates the ADC reference. It is potentially overkill, but I was interested in
seeing how the device would perform.

Pico Software
------------------------------

.. figure:: power_supply/microcontroller_software_drawio.png
  :align: center

  Figure 4: Hardware Block Diagram of the Linear Power Supply.

The Pico has a relatively simple program loop, A few systems such as the LCD and ADC are initialized on startup,
then continuous readings from both ADC channels are taken for interpretation. Each channel has offset removed,
becomes averaged over several samples, and scaled if necessary. Then the data is printed onto the LCD screen for
interpretation. There are a few edge cases regarding the output being off, an open circuit, and a short circuit.
In these situations, the LCD relays the situation to the user based on interpreted ADC data.

Schematic and PCB Design
-------------------------

All previously mentioned components must be compiled into a schematic design for wiring structure and PCB design.
Bypass and decoupling capacitors are added to the board for several reasons. First, capacitors can be used on power
headers to avoid voltage spikes and removing AC ripple on DC power. Small ceramic caps offer low series resistance and
react fast but have a difficult time dealing with substantial amounts of charge over long periods. Polarized
electrolytic capacitors usually have a much higher capacitance, and in conjunction with smaller ceramic capacitors,
effectively clean DC voltage. In larger schematics and PCB’s, we are not always able to position circuits
near bypass capacitors. Therefore, small decoupling capacitors are recommended for placement near a circuit
subsection to help clean AC ripple from DC voltages.

Once the schematic was populated with all necessary circuit components, the PCB was updated with all schematic
components for board layout. A general layout of parts was done before resizing the board outline to find the most
effective use of space. When all components have found their relative placement, routing traces for components using
auto-routing tools or manually is required. I chose to auto-route, followed with manual edits to correct some trace
routes. I found 100mil routes were sufficient for this circuit. Copper pours are also recommended for adding a
ground layer to the PCB, further simplifying routing design.

.. figure:: power_supply/schematic1.png
  :align: center

  Figure 22: Power Supply schematic page 1 of 2.

.. figure:: power_supply/schematic2.png
  :align: center

  Figure 23: Power Supply schematic page 2 of 2.

.. figure:: power_supply/altium_pcb_top.png
  :align: center

  Figure 24: Top side of Power Supply PCB layout.

.. figure:: power_supply/altium_pcb_bottom.png
  :align: center

  Figure 24: Bottom side of Power Supply PCB layout.

Bill Of Materials
---------------------

.. csv-table:: Bill Of Materials
   :file: power_supply/BillOfMaterials.csv


******************
Results
******************

The schematic of the circuit and PCB turned out fine, with a few errors that were fixable. The
assembled PCB was easy to debug because of its plentiful headers employed in the diagram. Thankfully,
there were no design breaking errors in this circuit, and most components worked immediately after installation.

.. figure:: power_supply/assembled_board.jpg
  :align: center

  Figure 42: Power Supply Board.

Flaws and Oversights
---------------------

There were a few things that I messed up in designing the board, but acknowledging them is a good practice as lessons
are learned and further revisions could be optimized. In terms of some minor design issues, I went overkill on a
series of parts. the Raspberry Pico's powerchain is excessive but works wonderfully. I could have easily removed one
of the 3.3V regulators and relied on the Pico's internal SMPS fed from the 7805 for operation. This doesn't affect the
ADC since the reference is isolated from removing the R7 resistor. Using a linear regulator for an ADC reference was
also overkill, and a LM385, TL431, or some other voltage reference could have been used to cut costs a bit. That being
said, this powerchain worked wonderfully and provided very clean measurements.

In addition, I completely over-specified the shunt resistor needed for current sensing. I employed a 100W resistor
thinking that the total power of the device could deliver 20V/3A = 60W during a short circuit condition. However, I
neglected to see that the entire short circuit wire would act as a resistor and that the power dissipated on a
resistance is equal to I*I*R or about 1W in my design. this is without mentioning any limiting or thermal shutdown that
would occur.

Some more serious design errors included incorrectly wiring the instrumentation amplifier. This caused the device to
read negative values and therefore send useless data to the ADC for current readings. Since I chose to use an IC riser,
This was easily worked around using some wire wrapping. Some header ports were also too small for wires and made
connecting the front panel difficult. The most egregious error was from designing the constant current regulator with
decoupling capacitors and without a parallel limit resistor. These too factors led to the destruction of a handful of
regulator IC's from current spikes.


Conclusion
---------------------

Overall, This project has been insightful and a useful addition to my workbench. While there were some design faults,
all errors were fixable and operation has not been impacted. Creating a linear power supply is a great way to introduce
power electronics to engineers and provide utility to the engineer for future projects. This device performed well at
providing power and realistic measurements to the user.


******************
Appendix
******************

LCD.py
---------------------

    .. literalinclude:: power_supply/LCD.py
       :language: python
       :linenos:

main.py
---------------------

    .. literalinclude:: power_supply/test.py
       :language: python
       :linenos:

******************
References
******************

.. [1] F. T. Ulaby, M. M. Maharbiz, and C. Furse, “7-12 Application Note: Power-Supply Circuits,” in Circuit analysis
   and Design, Ann Arbor, MI: Michigan Publishing, 2018, pp. 432–437.

