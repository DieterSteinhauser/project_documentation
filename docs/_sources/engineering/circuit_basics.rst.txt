Circuit Foundations
=====================================

Ohms Law
------------

In any given circuit, there are values that we want to observe change over time. All of circuits revolves around the
relationships between these three values.

    * **Voltage** (*V*) - The difference in electric potential between two points. It is derived from a joule of work
      needed to move a coulomb of charge through a potential difference of 1 volt. [1]_ Voltage is measured **across**
      components. Voltages can be generated from energy sources, and applying voltages across devices create a current.

    * **Current** (*I*) - The rate of electron flow through a point. 1 Amp is a speed derived from flow of 1 coulomb
      of charge per second. From a practical perspective, current is thought to flow from the higher potential to
      the lower potential. However, electron flow occurs from the more negative (lower) potential to the positive
      (higher) potential. Current is measured **through** components.

    * **Resistance** (*Ω*) - Resistance is the opposition to flow of electric current. Resistivity is inverse to
      conductivity. Resistance is measured in Ohms and defined with the omega (Ω) symbol. Ohm's Law says that 1Ω of
      resistance is equivalent to 1 volt supplying 1 Amp of current.


The relationship between these three values creates Ohm's Law.

.. math:: R = V/I
.. math:: V = IR



KCL: Kirchhoff's current law
------------------------------

.. figure:: reference/kcl.png
  :align: center

  KCL in a circuit node.


The sum of currents into a point is equal to the sum of currents out of the point. KCL can be used for
`Nodal Analysis <https://en.wikipedia.org/wiki/Nodal_analysis>`_, observing the current in and out of a node to
find voltage drops or resistor values.




KVL: Kirchhoff's voltage law
------------------------------

.. figure:: reference/kvl.png
  :align: center

  KVL seen in a circuit.


The sum of voltage differences around a closed circuit is zero. Any parallel circuit will see the same potential
difference between two points. In the above figure, the two points are seen as the top and bottom rails. KVL can be
used to perform `Mesh Analysis <https://en.wikipedia.org/wiki/Mesh_analysis>`_ by observing closed circuits in
parallel and finding the current based on equivalent voltage drops.



Power
------------

The power supplied or consumed by a circuit is equivalent to the Voltage applied times the Current created. This is
(Energy / charge) * (charge / time). Power is measured in Watts (W) and is equivalent to 1 Joule per second.

.. math:: P = VI = \frac{V^2}{R} = I^2R


Series and Parallel
--------------------

.. figure:: reference/series_and_parallel.png
  :align: center

  Series and Parallel resistors [1]_.



Resistors when placed in series effectively combine their resistance. Series

.. math:: R= R_1 + R_2

Whereas Parallel or Shunt resistors will effectively create a smaller resistor.

.. math:: R= \frac{R_1 * R_2}{R_1 + R_2}


Voltage Dividers
-----------------

Voltage dividers are a commonly used circuit takes a voltage input and create a voltage output that is a fraction of
original size. Voltage dividers do this predictably and consistently.


.. figure:: reference/voltage_divider.png
  :align: center

  A voltage divider circuit [1]_.



Thevenin and Norton Equivalent
--------------------------------

Thevenin’s theorem states that any two terminal network of resistors and voltage sources can be represented as an
equivalent single resistor and voltage source in **series**. This can be found by finding the open circuit voltage
across the two nodes, and the short circuit current that would occur if you shorted the two nodes. From these values,
Kirchhoff's laws, and ohm's law, you can deduce the Thevenin equivalent circuit.

.. math:: V_T= V_{oc}
.. math:: R_T= \frac{V_{oc}}{I_{sc}}

.. figure:: reference/thevenin_equivalent.png
  :align: center

  A Thevenin equivalent circuit for a voltage divider circuit.


Norton’s theorem states that any two terminal network of resistors and voltage sources can be represented as an
equivalent single resistor and current source in **parallel**. This can be found by finding the open circuit voltage
across the two nodes, and the short circuit current that would occur if you shorted the two nodes. From these values,
Kirchhoff's laws, and ohm's law, you can deduce the Norton equivalent circuit.

.. math:: I_N= I_{sc}
.. math:: R_N= \frac{V_{oc}}{I_{sc}}

.. figure:: reference/norton_equivalent.png
  :align: center

  A Norton equivalent circuit for a voltage divider circuit.


Decibel Representation
--------------------------------

Relative amplitude of signals are often measured on a logarithmic scale of Decibels (*dB*). Power in decibel notation
can be found using the following. Decibel notation is convenient because a difference in 10dB expresses a magnitude of
change in power. Thus, a 30dBW difference is equivalent to 1000W difference.

.. math:: dB = 10\log_{10}{P}

.. math:: \Delta dB = 10\log_{10}{\frac{P_2}{P_1}}

When representing voltage in decibel notation, the following equations are used.

.. math:: dB = 20\log_{10}{V}

.. math:: \Delta dB = 20\log_{10}{\frac{V_2}{V_1}}


**References**


.. [1]  P. Horowitz and W. Hill, “Chapter 1: Foundations,” in The Art of Electronics,
        New York: Cambridge University Press, 2022.
