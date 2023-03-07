PiHole Ad Blocking and PiVPN Remote Network Access
==================================================

*******************
Preface
*******************


Setup Materials
------------------

* Raspberry Pi 4 8GB
* sandisk 32 GB micro SD
* peripherals mouse/keyboard/monitor + cables
* A separate computer
* Ethernet Cable for Pi

Imager Software
------------------

* Raspberry Pi Imager
* Imager software like Etcher or win32DiskImager (backup image of drive for after install)

Notes
------------------

I install both of these programs onto the same Pi for safe browsing from anywhere in the world.
This also allow for greater home network usage expanding utility of network attached storage, Plex Servers,
and secure communication to remote desktops and devices.


Pi First time Setup
--------------------

Turn on and follow the prompts. Connect the pi to over ethernet if possible,
otherwise connect to wifi. skip updates and go to the terminal.

Update the Raspberry Pi.

.. code-block:: console

    sudo apt-get update
    sudo apt-get upgrade -y

Enable SSH on the Pi, either with the following line or by changing the IO settings in the desktop.

.. code-block:: console

    sudo service ssh start

Find the Pi's local IP Address.

.. code-block:: console

    sudo ifconfig

If this the first time that you have booted up the pi hardware, consider a firmware update.

.. code-block:: console

    sudo rpi-update

Restart the machine after these changes.

.. code-block:: console

    sudo reboot


.. Note:: **Network Settings**

    At this point you will want to go to your routers settings and configure a Static IP address
    for your Pi. The IP should be something like 192.168.X.Y where X is a number (0-255)
    intrinsic to the router settings, while Y is a number (0-255) that is reserved for the device
    the pi's IP currently will show you what X is set to on your router.

    **For example:**

        * PI:	192.168.80.77
        * Router: 192.168.80.1 or 192.168.1.1
        * alice's phone:  192.168.80.24
        * bob's   phone:  192.168.80.32

    Go to your routers IP using your browser to change it's settings, this is highly
    dependent on your Router but look for DCHP settings or Static IP.

.. Note:: **Port Forwarding**

    Setup your router to port forward on the device's static IP using the the port 1194.

    Now you want to setup a domain that masks your public IP, and a DDNS service to
    dynamically point to your network even if you ISP changes your Public IP.

    Go to DuckDNS (or any other DDNS provider) and create a domain and have it point to your public IP.
    try to access the server again using the DDNS domain name. You can stop here if you desire.
    Alternatively you can have a custom domain that you own point to the DDNS domain you created to
    add a layer of protection and uniqueness.

    Useful links for port forwarding:
        * `What is port forwarding? <https://portforward.com/>`_
        * `How to forward a port <https://www.howtogeek.com/66214/how-to-forward-ports-on-your-router/>`_


*******************
PiHole Setup
*******************

PiHole is a relatively easy setup, I recommend doing it with an attached display.

.. code-block:: console

    curl -sSL https://install.pi-hole.net | bash

*******************
PiVPN Setup
*******************

PiVPN is slightly more difficult to setup than the PiHole, but is mostly complex due to the networking involved.

.. tip:: Make sure to follow the networking notes in the preface before attempting this setup.

.. code-block:: console

    curl -L https://install.pivpn.io | bash