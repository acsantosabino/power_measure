#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Import the libraries used
import os
import os.path

#libraries for the web interface
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import json
from src.fake_measure import *

from tornado.options import define, options
from datetime import datetime

#define the port in which the website will be running
define("port", default=8000, help="run on the given port", type=int)

#Defines the communication between program and webserver
class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html' )
    def post(self):
        self.render('index.html')

class DevInfoHandler(tornado.web.RequestHandler):
    def get(self):
        try:
          with open('./data/devinfo.json', 'r') as file:
              data = json.loads(file.read())
          self.set_header('Cache-Control', 'no-cache')
          self.set_header('Access-Control-Allow-Origin', '*')
          self.write(json.dumps(data))
        except:
          self.set_header('Cache-Control', 'no-cache')
          self.set_header('Access-Control-Allow-Origin', '*')
          self.write(json.dumps("{ dev_name: [], power: [] , consume_class: [A] }"))
          

    def post(self):
        data = self.request.body_arguments

        with open('./data/devinfo.json', 'w+') as file:
            file.write(json.dumps(data, indent=4, separators=(',', ': ')))
        self.set_header('Cache-Control', 'no-cache')
        self.set_header('Access-Control-Allow-Origin', '*')
        self.write(json.dumps(data))

class HistoryHandler(tornado.web.RequestHandler):
    def get(self):
        elem = {}
        data = {}
        result = []
        try:
          with open(datetime.today().strftime('./data/%Y%m%d.json'), 'r') as file:
              data = json.loads(file.read())
          self.set_header('Cache-Control', 'no-cache')
          self.set_header('Access-Control-Allow-Origin', '*')
          data = data["current"]
          j=0
          for i in data[data.keys()[0]]:
              for key, value in data.items():
                  elem[key] = "{:0.3f}".format(value[j])
              result.append(elem)
              elem = {}
              j+=1
          self.write(json.dumps(result))
        except:
          self.set_header('Cache-Control', 'no-cache')
          self.set_header('Access-Control-Allow-Origin', '*')
          self.write(json.dumps("[{rms: [], mean: []}]"))

class ConsumeHistoryHandler(tornado.web.RequestHandler):
    def get(self):
        try:
          with open('./data/consumeinfo.json', 'r') as file:
              data = json.loads(file.read())
          self.set_header('Cache-Control', 'no-cache')
          self.set_header('Access-Control-Allow-Origin', '*')
          self.write(json.dumps(data))
        except:
          self.set_header('Cache-Control', 'no-cache')
          self.set_header('Access-Control-Allow-Origin', '*')
          self.write(json.dumps("[{ current_rms: [], current_mean: [], voltage_rms: [], voltage_mean: [], power_apparent: [], power_active: [], power_factor: []}]"))

#Configures the threads ans how the website should interpret requisitions from the website
if __name__ == '__main__':

    voltage = Measure("voltage", 0, 0, size=100)
    current = Measure("current", 0, 0, size=100)
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[(r'/', IndexHandler),
                  (r'/api/devinfo', DevInfoHandler),
                  (r'/api/history', HistoryHandler),
                  (r'/api/consumehistory', ConsumeHistoryHandler),
                  (r"/fig/(.*\.png)", tornado.web.StaticFileHandler,{'path': os.path.join(os.path.dirname(__file__), "fig")}),
                  (r'/css/(.*\.css)',tornado.web.StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), "templates/css")},),
                  (r'/js/(.*\.js)',tornado.web.StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), "templates/js")},)],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    server = tornado.ioloop.IOLoop.instance()
    tornado.ioloop.PeriodicCallback(lambda: threadRead(voltage, current),2000).start()
    server.start()
