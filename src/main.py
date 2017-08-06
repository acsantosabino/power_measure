#!/usr/bin/python
# -*- coding: utf-8 -*-

#Import the libraries used
import os, os.path

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

    opt = parser.parse_args()
    if opt.fake_measure :
        from fake_measure import *
    else :
        from measure import *

    buffersize = (1200) #Tamanho do buffer
    voltage = Measure('voltage', "AIN0", 7,buffersize) #Variavel de tensao
    current = Measure('current', "AIN1", 8, buffersize) #Variavel de corrente
    voltage.amp = 235.4
    current.amp = 7.6

    if opt.fake_measure : current.form = 'hwr'

    app = tornado.web.Application(
        handlers=[(r'/', IndexHandler),
                  (r'/api/devinfo', DevInfoHandler),
                  (r'/api/history', HistoryHandler),
                  (r'/api/consumehistory', ConsumeHistoryHandler),
                  (r"/fig/(.*\.png)", tornado.web.StaticFileHandler,{'path': os.path.join(os.path.dirname(__file__), "../fig")}),
                  (r"/fig/(.*\.svg)", tornado.web.StaticFileHandler,{'path': os.path.join(os.path.dirname(__file__), "../fig")}),
                  (r'/css/(.*\.css)',tornado.web.StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), "../templates/css")},),
                  (r'/js/(.*\.js)',tornado.web.StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), "../templates/js")},)],
        template_path=os.path.join(os.path.dirname(__file__), "../templates"), debug=True
    )

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(opt.port_num)
    server = tornado.ioloop.IOLoop.instance()
    tornado.ioloop.PeriodicCallback(lambda: threadRead(voltage, current),5000).start()
    server.start()

