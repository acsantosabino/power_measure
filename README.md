# Power Measure BBB

## Description

This is the project of a eletric power measure device. In this git repository you can find the software project. It was developed for a **BeagleBone Black** using python ,**React.js** and is based on ***libpruio*** library.

The software works by sampling and processing the current and voltage signal. With this data, the rms and average of the current and voltage are calculted as well as the real power, the apparent power and the power factor.

All the data are exposed in a web interface with a graph of two cycles of the voltage and current signals and a graph with all data evolution in a day.

## Installation

### Preparation

#### libpruio

 - Install FreeBasic compiler in BBB
Download and uncompress package from BBB-FBC (fbc für Beaglebone Black)

```bash
wget http://www.freebasic-portal.de/dlfiles/452/BBB_fbc-1.00.tar.bz2
tar xjf BBB_fbc-1.00.tar.bz2
```
Copy files
```bash
cd BBB_fbc-1.00
cp usr/local/bin/fbc /usr/local/bin/
cp -R usr/local/lib/freebasic /usr/local/lib/
```
Test compiler
```bash
fbc -version
```
should result in
```bash
FreeBASIC Compiler - Version 1.01.0 (10-14-2014), built for linux-arm (32bit)
Copyright (C) 2004-2014 The FreeBASIC development team.
```
 - Install pruss driver kit.

Install original am335x-pru-package
```bash
apt-get install am335x-pru-package
```
Download and uncompress FB package from FB prussdrv Kit (BBB)
```bash
wget http://www.freebasic-portal.de/dlfiles/539/FB_prussdrv-0.0.tar.bz2
tar xjf FB_prussdrv-0.0.tar.bz2
```
Copy files
```bash
cd FB_prussdrv-0.0
mkdir /usr/local/include/freebasic/BBB
cp include/* /usr/local/include/freebasic/BBB
cp bin/pasm /usr/local/bin
```

 - Install libpruio

Download and uncompress package from libpruio (D/A - I/O schnell und einfach)
```bash
wget https://www.freebasic-portal.de/dlfiles/592/libpruio-0.2.tar.bz2
tar xjf libpruio-0.2.tar.bz2
```
Copy files
```bash
cd libpruio-0.2
cp src/c_wrapper/libpruio.so /usr/local/lib
```
ldconfig
```bash
cp src/c_wrapper/pruio*.h* /usr/local/include
cp src/config/libpruio-0A00.dtbo /lib/firmware
cp src/pruio/pruio*.bi /usr/local/include/freebasic/BBB
cp src/pruio/pruio.hp /usr/local/include/freebasic/BBB
```

#### Python preparation

```bash
apt-get install  python-matplotlib
pip install Cython tornado 
```
### Power Measure installation

 - Clone repository
```bash
apt-get install  git
git clone https://github.com/acsantosabino/power_mesure.git
```
 - Compile Pruio.py
```bash
cd power_mesure/src/ext_libpruio
python setup.py build_ext -i
cd ../../
```
 - Make scripts executable and create data and fig diretory
```bash
chmod 777 power_measure.sh
chmod 777 src/main.py
mkdir data fig
```
 - Run
```bash
./power_measure.sh
```
 - Prepare to autorun on system start
```bash
cp power_mesure/power_measure.sh /etc/init.d
sudo update-rc.d power_measure.sh defaults
```