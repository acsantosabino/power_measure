#! /bin/sh
# /etc/init.d/power_measure
#

#run noip to update real ip dns
noip2

#Mount pru module
echo BB-BONE-PRU-01 > /sys/devices/bone_capemgr.9/slots

#Make power_measure executable
chmod 777 /home/debian/power_mesure/src/main.py

#Start power_measure
sudo /home/debian/power_mesure/src/main.py
