#!/usr/bin/python
# -*- coding: utf-8 -*-

#Import the libraries used
import os, os.path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "./ext_libpruio"))


#libraries for the web interface
import numpy as np
from tornado.options import define
import time
from web_server import *
import tornado.httpserver
import tornado.ioloop
import tornado.web
import argparse

parser = argparse.ArgumentParser(description='Run web server')

parser.add_argument('--fake-measure', action='store_true', default=False ,
                    help='simutate measures', dest="fake_measure")
parser.add_argument('-d', '--debug', action='store_true', default=False ,
                    help='debug mode')
parser.add_argument("--port", default=8000, help="run on the given port",
                    dest='port_num', type=int)

if __name__ == '__main__':

    buffersize = 1200 #Tamanho do buffer
    opt = parser.parse_args()
    if opt.fake_measure :
        from fake_measure import *
    else :
        from measure import *
        from pruio import Pruio
        Act = 0xFFFF  #activation mode
        Av = 0                  #avaraging for default steps
        OpD = 0                 #open delay for default steps (default 0x98, max 0x3FFFF)
        SaD = 0                 #sample delay for default steps (defaults to 0)
        Mds = 4                 #modus for output (default to 4 = 16 bit)
        tmr = 1000000000.0/(600.0*60.0) #1ms! sampling rate in ns (10000 -> 100 kHz)
        adc = Pruio(Act, Av, OpD, SaD)
        adc.config(buffersize, 0b010000100, tmr, Mds)
        adc.rb_start()
        time.sleep(0.5)

    voltage = Measure('voltage', "AIN6", buffersize) #Variavel de tensao
    current = Measure('current', "AIN1", buffersize) #Variavel de corrente
    voltage.amp = (311/0.38)  
    current.amp = (5/0.2964)

    if opt.fake_measure : current.form = 'fwr'

    else :
      ch = adc.read_adc_ch()
      voltage.calibrate(ch)
      current.calibrate(ch)

    app = tornado.web.Application(
        handlers=[(r'/', IndexHandler),
                  (r'/api/devinfo', DevInfoHandler),
                  (r'/api/history', HistoryHandler),
                  (r'/api/consumehistory', ConsumeHistoryHandler),
                  (r"/fig/(.*\.png)", NoCacheStaticFileHandler,{'path': os.path.join(os.path.dirname(__file__), "../fig")}),
                  (r"/fig/(.*\.svg)", NoCacheStaticFileHandler,{'path': os.path.join(os.path.dirname(__file__), "../fig")}),
                  (r'/css/(.*\.css)',tornado.web.StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), "../templates/css")},),
                  (r'/js/(.*\.js)',tornado.web.StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), "../templates/js")},)],
        template_path=os.path.join(os.path.dirname(__file__), "../templates"), debug=True
    )

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(opt.port_num)
    server = tornado.ioloop.IOLoop.instance()
    tornado.ioloop.PeriodicCallback(lambda: threadRead(voltage, current, adc),20000).start()
    server.start()
