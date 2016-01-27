RUN ALL STEPS AS ROOT

#####Setup Bluetooth
$ apt-get install libusb-dev libdbus-1-dev libglib2.0-dev automake libudev-dev libical-dev libreadline-dev rfkill
$ wget http://www.kernel.org/pub/linux/bluetooth/bluez-5.24.tar.xz
$ tar xf bluez-5.24.tar.xz
$ cd bluez-5.24
$ ./configure –-disable-systemd
$ make -j 2
$ make install
$ reboot

This next section of steps seems outdated but I will keep it here for troubleshooting
Then from the original image (files in repo) you should copy the following folder and files to your Edison ubilinux filesystem:
/etc/bluetooth/
/usr/sbin/bluetooth_rfkill_event
/usr/sbin/brcm_patchram_plus
As the original files from the Yocto image are looking for the bluetooth firmware in the etc folder (instead that from the /lib/firmware) from your Edison ubilinux run:
$ mkdir /etc/firmware
$ cp /lib/firmware/bcm43341.* /etc/firmware/
now from your Edison ubilinux run the bluetooth_rfkill_event in background:
$ bluetooth_rfkill_event &
$ rfkill unblock bluetooth
now you should see the BT device
$ hciconfig dev
and scan for other devices
$ hcitool scan
Enable changes
$ reboot


####Pair the printer
Turn on bluetooth(only run once at startup)
$ rfkill unblock bluetooth

Get the BDAddress of the adapter denoted as XX:XX:XX:XX:XX:XX
$ hciconfig dev

Get the  BDAddress of the device denoted as YY:YY:YY:YY:YY:YY
$ hcitool scan

Create this file…
/var/lib/bluetooth/XX:XX:XX:XX:XX:XX/pincodes
…where XX:XX:XX:XX:XX:XX is the bdaddr of your bluetooth adapter

Now in that file we write a line for our particular device we’re trying to pair with a PIN using the format…
YY:YY:YY:YY:YY:YY 6000

Enable changes
$ reboot


####Connect to printer
Turn on bluetooth(only run once at startup)
$ rfkill unblock bluetooth

Connect to device
$ rfcomm unbind /dev/rfcomm0 YY:YY:YY:YY:YY:YY
$ rfcomm bind /dev/rfcomm0 YY:YY:YY:YY:YY:YY

####Print image
ussp-push /dev/rfcomm0 SoureFile.jpg image.jpg
