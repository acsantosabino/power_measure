#!/usr/bin/python
# -*- coding: utf-8 -*-

#Import the libraries used
import os, os.path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "./ext_libpruio"))

#libraries for the database
import numpy as np
import time
import argparse
import pymongo

parser = argparse.ArgumentParser(description='Run sensor measure')

parser.add_argument('--fake-measure', action='store_true', default=False ,
                    help='simutate measures', dest="fake_measure")
parser.add_argument('-d', '--debug', action='store_true', default=False ,
                    help='debug mode')

if __name__ == '__main__':

    client = pymongo.MongoClient("mongodb://acsantosabino:power1@powermeasure-shard-00-00-0s7q1.mongodb.net:27017,powermeasure-shard-00-01-0s7q1.mongodb.net:27017,powermeasure-shard-00-02-0s7q1.mongodb.net:27017/test?ssl=true&replicaSet=PowerMeasure-shard-0&authSource=admin&retryWrites=true")
    db = client.powermeasure

    buffersize = 1200 #Tamanho do buffer
    opt = parser.parse_args()
    sampleRate = 600.0*60.0
    sensor_delay = 0.2 * 10**(-3) #atraso entre corrente e tensão

    if opt.fake_measure :
        from fake_measure import *
        d = 0
        adc = None
    else :
        from measure import *
        from pruio import Pruio
        Act = 0xFFFF  #activation mode
        Av = 0                  #avaraging for default steps
        OpD = 0                 #open delay for default steps (default 0x98, max 0x3FFFF)
        SaD = 0                 #sample delay for default steps (defaults to 0)
        Mds = 4                 #modus for output (default to 4 = 16 bit)
        tmr = 1000000000.0/sampleRate #1ms! sampling rate in ns (10000 -> 100 kHz)

        d = int(sampleRate * sensor_delay) #atraso em amostras
        adc = Pruio(Act, Av, OpD, SaD)
        adc.config(buffersize+d, 0b010000100, tmr, Mds)
        adc.rb_start()
        time.sleep(0.5)

    voltage = Measure('voltage', "AIN6", buffersize) #Variavel de tensao
    current = Measure('current', "AIN1", buffersize) #Variavel de corrente
    voltage.amp = (311/0.43)
    current.amp = (7/0.61)

    if opt.fake_measure : current.form = 'sin'

    else :
      ch = adc.read_adc_ch()
      voltage.calibrate(ch, d)
      current.calibrate(ch, d)

    threadRead(voltage, current, db, adc, d)
    # while(1):
    #     threadRead(voltage, current, db, adc, d)
    #     print "Measure"
    #     time.sleep(0.5)