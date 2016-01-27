
#yocto bluetooth setup

#https://communities.intel.com/message/309869#309869
#https://communities.intel.com/thread/55602?tstart=0

RUN AS ROOT

#pair
$ rfkill unblock bluetooth
$ bluetoothctl
$ scan on
$ agent KeyboardDisplay
$ default-agent
$ pair 00:04:48:10:7E:36
$ 6000
$ reboot

#send an image(does not work, incomplete obex support)
$ rfkill unblock bluetooth
$ export DBUS_SESSION_BUS_ADDRESS=unix:path=/var/run/dbus/system_bus_socket
$ systemctl start obex
$ rfcomm bind rfcomm0 00:04:48:10:7E:36
$ obexctl
$ connect 00:04:48:10:7E:36 OPP
$ send image.jpg #fails
