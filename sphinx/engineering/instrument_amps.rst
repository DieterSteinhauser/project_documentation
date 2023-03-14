Instrumentation Amplifiers
=====================================

*******************
Theory
*******************


.. figure:: reference/instrumentation_amp.png
  :align: center

  Figure 1: The classic instrumentation amplifier circuit [2]_.

Instrumentation Amplifiers (INA) are an improvement on the differential amplifier for applications needing high input
impedance, gain, CMRR, and low noise. They work on the principle of taking an existing differential amplifier and
adding non-inverting amplifiers to the differential input. By adding resistor Rg, gain can be applied to the
differential signal. If the gain resistor is omitted, the input amplifiers become voltage followers and the gain
of the system is 1. High CMRR and low noise is only available when a large gain is applied, as Rg scales the signal to
noise ratio of the input stage and diminishes reliance on U3 for common mode rejection.

*******************
Applications
*******************


.. figure:: reference/inst_apps_1.png
  :align: center

  Figure 1: Applications of the INA128 Instrumentation Amplifier [1]_.

Instrumentation amplifiers are fantastic devices for applications requiring observation of a signal without
disturbing it. However, they are costly devices compared to a typical op-amp, and the INA circuit is hard to
recreate off chip without matched pair components. Features such as CMRR and noise reduction would be lost as
a result. ADCs, balanced audio, current sensing, and electrocardiography (ECG) machines are some of the many
applications that utilize the benefits of instrumentation amplifiers.

.. figure:: reference/inst_apps_2.png
  :align: center

  Figure 1: More Instrumentation amplifier circuits [1]_.


**References**

.. [1] “INA128 Datasheet,” Analog | Embedded Processing | Semiconductor Company | ti.com. [Online]. Available:
    https://www.ti.com/lit/ds/symlink/ina128.pdf. [Accessed: 13-Mar-2023].

.. [2] P. Horowitz and W. Hill, “Chapter 5: Precision Circuits,” in The Art of Electronics, New York: Cambridge
    University Press, 2022.
