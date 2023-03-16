Circuit Applications
=====================================

Charge Pumps
--------------------------

.. figure:: reference/pos_charge_pump.png
  :align: center

  Figure 1: Positive voltage charge pump.

A charge pump is a circuit that uses a periodic signal and diodes to force charge buildup on a capacitor.
While this is an effective way to store an energy potential, the voltage will approach the peak-to-peak voltage
unless dissipated on a load or regulated. The size of the capacitors and the frequency of the input waveform
will determine the time it takes for the circuit to charge.


.. figure:: reference/neg_charge_pump.png
  :align: center

  Figure 2: Negative voltage charge pump.

Negative voltage rails are often needed for reference voltages and are a useful addition to many circuit designs.
An easy approach for low current applications could rely on a negative charge pump.

**References**



