Spigot Minecraft Server
====================================================

*********************
Downloads and Install
*********************

* `Download Java. <https://www.java.com/download/ie_manual.jsp>`_
* `Download the Java Development Kit. <https://www.oracle.com/java/technologies/downloads/>`_
* `Download the BuildTools GUI. <https://github.com/0uti/BuildToolsGUI/releases>`_
* `Installation Help <https://minecraft.fandom.com/wiki/Tutorials/Setting_up_a_Spigot_server>`_

Create a folder that you wish to store your minecraft server in. Store the BuildTools folder in it.
Run BuildTools. Once it is done, move all newly created files/folders into the base minecraft server folder.


Server Edits
--------------

* Open up eula.txt and change false to true.
* Open up server.properties.
* Make sure the query.port = 25565
* make the server ip the same local IP of the server computer.
* Change motd to the flavortext your heart desires.
* examine for any other changes you may want to make.


Batch file edits and starting the server
------------------------------------------

Create the following batch file in the same directory as the spigot<ver>.jar file.

.. code-block:: batch

    ::--------------------------------------------------------
    :: This file starts the spigot server
    ::--------------------------------------------------------
    ::NOTES
    ::--------------------------------------------------------
    ::Java options should be added between the java and the -jar on the command line, or in your startup script.
    ::If you don't want a GUI for typing commands, add a space and --nogui to the command.
    :: XMS is initial memory, XMX is Server memory. Java doesn't like heap size changes, so make them the same
    ::A "soft max heap size" (-XX:SoftMaxHeapSize=8G). The JRE will try to only use that much memory, but will go over to a maximum of -Xmx if necessary.
    ::Use -d64 if your server is on a 64-bit Solaris system using 64-bit Java.

    :: https://aikar.co/2018/07/02/tuning-the-jvm-g1gc-garbage-collector-flags-for-minecraft/
    :: https://minecraft.fandom.com/wiki/Tutorials/Setting_up_a_server
    ::--------------------------------------------------------

    @ECHO ON
    :SpigotStart
    java -server -Xms16G -Xmx16G -XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200 -XX:+UnlockExperimentalVMOptions -XX:+DisableExplicitGC -XX:-OmitStackTraceInFastThrow -XX:+AlwaysPreTouch  -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 -XX:G1HeapRegionSize=8M -XX:G1ReservePercent=20 -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=8 -XX:InitiatingHeapOccupancyPercent=15 -XX:G1MixedGCLiveThresholdPercent=90 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:MaxTenuringThreshold=1 -Dusing.aikars.flags=true -Daikars.new.flags=true -jar spigot-1.18.1.jar -o false
    PAUSE

Scroll to the end and edit the spigot<ver>.jar command to match the file created earlier by BuildTools.

Change Xmx and Xms to the amount of RAM you want to allocate to the game.
This highly depends on your machine and amount of users, allocate 1G to start and increase as you please.
I think about it as roughly ~512MB/person minimum and ~1GB/person reccomended.
other commands in this prompt are for optimization.

Run SpigotStart.bat. Files will be created on start of the server in the same folder.


Connecting
-------------

Players can now put in the local IP of the computer running the server to connect
192.168.yyy.zzz:25565

In the GUI or terminal of the server computer, write the command op 'minecraftusernamehere'
to give 'minecraftusernamehere' admin privileges on the server.

*********************
Networking
*********************

.. Note:: **Network Settings**

    You will want to go to your routers settings and configure a Static IP address for the device you are running
    the server on. The IP should be something like 192.168.X.Y where X is a number (0-255)
    intrinsic to the router settings, while Y is a number (0-255) that is reserved for the device
    the device's IP currently will show you what X is set to on your router.

    **For example:**

        * device:	192.168.80.77
        * Router: 192.168.80.1 or 192.168.1.1
        * alice's phone:  192.168.80.24
        * bob's   phone:  192.168.80.32

    Go to your routers IP using your browser to change it's settings, this is highly
    dependent on your Router but look for DCHP settings or Static IP.

.. Note:: **Port Forwarding**

    Setup your router to port forward on the device's static IP using the the port 25565.

    Now you want to setup a domain that masks your public IP, and a DDNS service to
    dynamically point to your network even if you ISP changes your Public IP.

    Go to DuckDNS (or any other DDNS provider) and create a domain and have it point to your public IP.
    try to access the server again using the DDNS domain name. You can stop here if you desire.
    Alternatively you can have a custom domain that you own point to the DDNS domain you created to
    add a layer of protection and uniqueness.

    Useful links for port forwarding:
        * `What is port forwarding? <https://portforward.com/>`_
        * `How to forward a port <https://www.howtogeek.com/66214/how-to-forward-ports-on-your-router/>`_
