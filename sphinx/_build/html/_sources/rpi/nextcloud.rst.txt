Nextcloud Personal Cloud Storage
====================================================

*******************
Preface
*******************


Setup Materials
------------------

* Raspberry Pi 4 8GB
* WD Passport 2TB
* sandisk 32 GB micro SD
* peripherals mouse/keyboard/monitor + cables
* A separate computer
* Ethernet Cable for Pi

Imager Software
------------------

* Raspberry Pi Imager 1.4 (older version for compatibility)
* Raspberry Pi Imager 1.7 (newest at time of writing, has bootloader images)
* Imager software like Etcher or win32DiskImager (backup image of drive for after install)


Notes
------------------
A straightforward setup would be a large microSD card or an USB mass storage device.
If you choose to use mass storage, you will need to get the USB bootloader from the official
Raspberry Pi Imager. After imaging a SD card with the bootloader, entering it into the pi and powering
on will update the boot priority then make the existing monitor display green when finished.
I had a hard time getting the Raspberry Pi OS to boot correctly on my 2TB HDD when imaging from
the Raspberry Pi Imager ver.1.7. I remembered I had an older Imager on my other computer (ver1.4)
that has the (2021-05-07) release. This had solved my issue, your mileage may vary.

.. warning::

    If using a non-system running (external) drive such as a USB Mass storage device
    alongside a micro SD system drive, there are instructions on mounting an external drive
    at the end of this install tutorial. `However, I do not recommend this method.
    <https://help.nextcloud.com/t/external-storage-app-extremely-slow-down-the-system/96636>`_
    Using an external drive for storage produced lackluster speeds for me and others.
    This could be due to bottlenecks on the pi or limitations from my HDD. From what I have seen on forums,
    the slowdown is consistent across hardware and associated with the external storage app
    on nextcloud. It took days to sync 90GB of data and still did not sync certain files.
    I caution against taking this route.


The raspberry pi also does not support php7.4 or higher, which is required for the
latest releases of nextcloud. There is a workaround for this seen later.
If you are not using a Pi then you can probably install the php8.0 packages directly.
If you are using a pi and wish to avoid this altogether, there is an older build that
can be installed for ease of use.

.. tip:: For out-of-home use, I recommend using a VPN to tunnel into the Pi's network. I Have a separate Raspberry Pi
    using piVPN and piHole for secure network access.


Useful Links
------------------

* `Nextcloud Docs <https://docs.nextcloud.com/>`_
* `Manual Install Help <https://pimylifeup.com/raspberry-pi-nextcloud-server/>`_
* `mySQL Setup <https://pimylifeup.com/raspberry-pi-mysql/>`_
* `Pi Nextcloud Image <https://ownyourbits.com/nextcloudpi/>`_
* `Nextcloud Image Install Help <https://www.makeuseof.com/raspberry-pi-nextcloud/>`_
* `Image or Manual Install Help <https://raspberrytips.com/install-nextcloud-raspberry-pi/>`_

******************
Installation
******************

you can install all of this while using the raspberry pi as your desktop,
however I recommend using an app like PuTTy to secure shell (SSH) into the pi.
This allows you to remote into the pi from another computer on the network using the
Pi's Local IP address.


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


Installing Packages
--------------------

Install apache, once installed if you go to the pi's IP you will see the default apache webpage.

.. code-block:: console

    sudo apt install apache2 mariadb-server libapache2-mod-php


.. list-table::

   * - **Easy and Compatible Method**
   * - install php7.3, raspberry pi OS does not support higher than 7.3

       .. code-block:: console

          sudo apt install php-gd php-json php-mysql php-curl php-mbstring php-intl php-imagick php-xml php-zip

   * - **Latest Version Method**
   * - download the GPG key and add the PHP repo. **You may need to update the Pi again.**

       .. code-block:: console

          sudo wget -qO /etc/apt/trusted.gpg.d/php.gpg https://packages.sury.org/php/apt.gpg
          echo "deb https://packages.sury.org/php/ $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/php.list

       Now install php now with our workaround.

       .. code-block:: console

          sudo apt install php8.0 php8.0-gd php8.0-curl php8.0-zip php8.0-xml php8.0-mbstring php8.0-mysql php8.0-bz2 php8.0-intl php-smbclient php8.0-imap php8.0-gmp libapache2-mod-php8.0


Restart apache now. The pi's IP should display the default apache webpage after restart.

.. code-block:: console

    sudo service apache2 restart


Nextcloud installation
----------------------

go to the html directory apache webfolder and install the latest version of nextcloud.
note, this puts the nextcloud web software in html, directory needs to be refernenced later.

.. code-block:: console

      cd /var/www/html


.. list-table::

   * - **Easy and Compatible Method**
   * - An older version of nextcloud if you did not do the php workaround.

       .. code-block:: console

          sudo wget https://download.nextcloud.com/server/releases/nextcloud-15.0.8.zip
          sudo unzip nextcloud-15.0.8.zip

   * - **Latest Version Method**
   * - Download and extract the latest release. Extracts all files in current directory.

       .. code-block:: console

          sudo wget https://download.nextcloud.com/server/releases/latest.tar.bz2
          sudo tar -xvf latest.tar.bz2


Nextcloud Permissions
----------------------

Create a data directory for nextcloud to operate in, this is where all cloud data is stored.

.. code-block:: console

   sudo mkdir -p /var/www/nextcloud/data

Give the (www-data) user and group control over the nextcloud data folder using chown.

.. code-block:: console

   sudo chown -R www-data:www-data /var/www/nextcloud/

Give permissions to the (www-data) user using chmod.

.. code-block:: console

   sudo chmod 750 /var/www/nextcloud/data


mySQL database
----------------------

create a mySQL database for the data to be stored in. follow all prompts in installation.
sudo apt install mariadb-server # done when installing apache at beginning.

.. code-block:: console

    sudo mysql_secure_installation
    sudo mysql -u root -p

.. code-block:: console

    CREATE USER 'picloud' IDENTIFIED BY 'password';

    CREATE DATABASE piclouddb;

    GRANT ALL PRIVILEGES ON piclouddb.* TO 'picloud';

.. note:: If the above GRANT ALL PRIVILEGES did not work you can try this too.

    .. code-block:: console

         GRANT ALL PRIVILEGES ON piclouddb.* TO 'root'@localhost;


Save and quit.

.. code-block:: console

    FLUSH PRIVILEGES;
    quit


Have Apache find Nextcloud
---------------------------

create a file with all of our changes for apache access to nextcloud.

.. code-block:: console

    sudo nano /etc/apache2/sites-avacdilable/nextcloud.conf

This is where you have to be mindful of the nextcloud service directory.
The Alias /nextcloud is wherever the service directory is. Write the following in the file.

.. code-block:: console

    Alias /nextcloud "/var/www/html/nextcloud/"

    <Directory /var/www/nextcloud/>
      Require all granted
      AllowOverride All
      Options FollowSymLinks MultiViews

      <IfModule mod_dav.c>
        Dav off
      </IfModule>

    </Directory>


Then we can have apache make use of the configuration file.
After reloading apache, the nextcloud page should be available.

.. code-block:: console

    sudo a2ensite nextcloud.conf
    sudo systemctl reload apache2

******************
Enter Nextcloud
******************

Go to http://IP/nextcloud to see service's webpage.

Create an admin account.

point the data directory to the directory we made earlier. **/var/www/nextcloud/data** if you did not change it.

sign into the database using the database, user, and password specified
earlier in the mySQL section

Viola!


Add External Storage
----------------------

`mounting drives <https://forum.endeavouros.com/t/tutorial-how-to-permanently-mount-external-internal-drives-in-linux/18688>`_

Using the above link, mount the drive to the device. Give permissions to the storage device using the following.

.. code-block:: console

    sudo chown -R www-data:www-data /path/to/localdir
    sudo chmod -R 0750 /path/to/localdir

    sudo -u www-data bash
    cd /path/to/localdir
    mkdir data

Install the external storage app on the nextcloud webpage.

.. note:: External drive speed is considerably slower than primary drive speed. See the warning at the top of the page
    for more information.


Remove Warnings in Nextcloud Security
-------------------------------------

Change the php memory limit and output buffering.

.. code-block:: console

    navigate to /etc/php/<version/>apache2/
    sudo nano php.ini

ctrl+W to search both terms
raise mem limit above 512M and turn output buffering off
repeat in /etc/php/<version/>cli/

******************
Troubleshooting
******************

Do you see the apache webpage on the IP?
If not restart apache service or reinstall.

**403 Error - Forbidden:**

    * Redo 'Nextcloud data directory and permissions' section.
    * Change ownership of the service files and the data files.
    * Change modification privileges of the service files and the data files.
    * restart apache.

**404 Error - Not Found:**

    * redo 'Pointing to nextcloud via apache' section
    * make sure that the alias points to the service in the var/www/html section
    * restart apache

**Nextcloud splash error when in 'Enter Nextcloud' section:**

    * Make sure there are no errors in the Nextcloud data directory and permissions' section
    * I had copied a comment into sudo nano /etc/apache2/sites-avacdilable/nextcloud.conf and it threw this error.
    * restart apache



