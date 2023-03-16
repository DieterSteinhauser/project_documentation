BJTs Bipolar Junction Transistors
=====================================

*******************
Theory
*******************

*******************
Applications
*******************

Voltage Reference - VBE Multiplier
-------------------------------------

.. figure:: reference/vbe_multiplier.png
  :align: center

  Figure 1: Rubber Diode VBE multiplier.

For a simple reference voltage, a VBE multiplier (or rubber diode) can be implemented to regulate the output voltage
to a consistent level for voltage reference. A Zener regulator or negative linear regulator could also be implemented.
However, I found this circuit to be a good middle ground between linear performance and operating configurability.
The rubber diode exploits a BJT’s VBE drop and voltage divider properties to set a voltage reference for small
loads. This circuit is nice because it is both simple like a Zener regulator but configurable in its voltage
output, similar to a linear regulator IC.




**References**

.. [1] A. S. Sedra, K. C. Smith, T. C. Carusone, and V. Gaudet, “Chapter 6: Bipolar Junction
    Transistors (BJTs),” in Microelectronic circuits, New York, NY: Oxford University Press, 2021,
    pp. 60–73.

.. [2] P. Horowitz and W. Hill, “Chapter 2: Bipolar Transistors,” in The Art of Electronics, New York:
    Cambridge University Press, 2022.

