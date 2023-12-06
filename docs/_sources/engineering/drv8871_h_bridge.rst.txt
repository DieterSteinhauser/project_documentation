DRV8871 H-Bridge
=====================================

.. figure:: reference/drv8871.jpg
  :align: center

  DRV8871 Breakout Board from Adafruit


The DRV8871 is a CMOS H-Bridge Driver IC manufactured by Texas Instruments. These boards are commonly available in
Breakouts by Adafruit and other manufacturers. The DRV8871 is a versatile H-Bridge driver that can operate between
6.5V and 45V and supply up to 3.6A [1]_. Control of the DRV8871 can occur with both 3.3V and 5V logic with static
and PWM control schemes [5]. Current limiting is determined by an external resistor, enabling overcurrent protection
on the device. This specification proves useful for a wide variety of circuits and particularly motor controls.

.. figure:: reference/h_bridge_control.png
  :align: center

  DRV8871 H-Bridge Control Table [1]_.

.. figure:: reference/h_bridge_control.png
  :align: center

  DRV8871 H-Bridge current paths [1]_.

I developed a micro python driver for the DRV8871 that allows for PWM control of the H-bridge using two GPIO pins
from a micropython enabled microprocessor such as the raspberry pico. Given correct wiring, the microprocessor can
control the flow of current and the duty cycle to which it is pulsed. As a result, a developer can easily command
the H-bridge into a forward, reverse, coast, or brake state. Users can also determine the duty cycle for which the
system should be active and if the H-bridge reverts to a braking or coasting state when off.


.. autoclass:: src.pico_power_management.DRV8871.DRV8871
   :members:
   :undoc-members:

Code
--------------------------

.. literalinclude:: ../../src/pico_power_management/drv8871.py
   :language: python
   :linenos:



.. [1] Texas Instruments. "DRV8871 3.6-A Brushed DC Motor Driver with Internal Current." [Online].
       Available: [www.ti.com/lit/ds/symlink/drv8871.pdf].

