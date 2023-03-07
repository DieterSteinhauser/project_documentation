Ultrasonic Sensors
=====================================

The HC-SR04 is an Ultrasonic sensor module that uses sonar to determine distance of
objects similar to echolocation seen in animals like bats or dolphins [1]_. It is rated for distances
of 2cm to 400cm and can provide high accuracy within this range. The sensors have four
connections, VCC, Trig, Echo, and GND. The device operates with a 5V supply, while the
trigger and echo are used to communicate digital data between the sensor and a microcontroller.

From the microcontroller, the Trig pin is set high for 10uS then brought low. This tells
the sensor to send eight 40kHz bursts from the transmitter. The microcontroller should then poll
the Echo pin, waiting for a high signal from the receiver, indicating the return of the bursts echo.
The time between the rising and falling edge of the Echo pin can be used to calculate distance
based on the speed of sound, 343 m/s. Based on the distances calculated from each sensor, we
can modify output sound data.

.. figure:: theremin_images/image028.png
  :align: center

  Figure 19: Ultrasonic sensor timing diagram [1]_.


**References**

.. [1] “HC-SR04 User Manual,” Scribd. [Online]. Available:
    https://www.scribd.com/document/363064776/HC-SR04-User-Manual. [Accessed: 14-
    Nov-2022].