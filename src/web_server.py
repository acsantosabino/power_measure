#Import the libraries used
import os
import os.path

#libraries for the web interface
import tornado.options
import tornado.web
import json

from tornado.options import define, options
from datetime import datetime

#Defines the communication between program and webserver
class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html' )
    def post(self):
        self.render('index.html')

class DevInfoHandler(tornado.web.RequestHandler):
    def get(self):
        try:
          with open('../data/devinfo.json', 'r') as file:
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

        with open('../data/devinfo.json', 'w+') as file:
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
          with open(datetime.today().strftime('../data/%Y%m%d.json'), 'r') as file:
              data = json.loads(file.read())
          self.set_header('Cache-Control', 'no-cache')
          self.set_header('Access-Control-Allow-Origin', '*')
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
        result = {};
        try:
          with open('../data/consumeinfo.json', 'r') as file:
              data = json.loads(file.read())
          self.set_header('Cache-Control', 'no-cache')
          self.set_header('Access-Control-Allow-Origin', '*')
          for key in data.keys():
            result[key] = "{:0.3f}".format(data[key])
          self.write(json.dumps(result))
        except:
          self.set_header('Cache-Control', 'no-cache')
          self.set_header('Access-Control-Allow-Origin', '*')
          self.write(json.dumps("[{ current_rms: [], current_mean: [], voltage_rms: [], voltage_mean: [], power_apparent: [], power_active: [], power_factor: []}]"))

