Ultrasonic Sensors
=====================================

.. figure:: reference/SR04.png
  :align: center

  Figure 1: HC-SR04 Ultrasonic Sensor module.

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

  Figure 2: Ultrasonic sensor timing diagram [1]_.


.. code-block:: python
   :caption: Ultrasonic Sensor Driver

    # -----------------------------------------
    #           ULTRASONIC SENSORS
    # -----------------------------------------


    from machine import Pin
    from utime import ticks_us, sleep_us

    # Ultrasonic sensor pins
    # ----------------------------
    us0_trig = Pin(6, Pin.OUT)
    us0_echo = Pin(7, Pin.IN)
    us1_trig = Pin(8, Pin.OUT)
    us1_echo = Pin(9, Pin.IN)

    def get_distance_u0():

        # send the trigger wave
        us0_trig(1)
        sleep_us(10)
        us0_trig(0)

        # listen for the return echo
        while us0_echo.value() == 0:
            start = ticks_us()
        while us0_echo.value() == 1:
            stop = ticks_us()

        return ((stop - start) * 0.0343) / 2

    def get_distance_u1():
        global us1_distance

        # send the trigger wave
        us1_trig(1)
        sleep_us(10)
        us1_trig(0)

        # listen for the return echo
        while us1_echo.value() == 0:
            start = ticks_us()
        while us1_echo.value() == 1:
            stop = ticks_us()

        return ((stop - start) * 0.0343) / 2


**References**

.. [1] “HC-SR04 User Manual,” Scribd. [Online]. Available:
    https://www.scribd.com/document/363064776/HC-SR04-User-Manual. [Accessed: 14-
    Nov-2022].