#Import the libraries used
import os, os.path
from collections import deque
import numpy as np
import time, json
from datetime import datetime
import sys
import plotly
import plotly.plotly as py
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.graph_objs as go
import json

plotly.tools.set_credentials_file(username='TCC2016', api_key='wfo2kqaa3f')

historyurl = "https://plot.ly/~TCC2016/6.embed"

#Criacao da classe de leitura dos pinos analogicos
class Measure(deque):
  num_elem = 0
  freq = 60
  amp = 5
  
#Inicializacao da porta analogica
  def __init__(self, name, adcPort, gpioPort, size=0):
    super(Measure, self).__init__(maxlen=size)
    self.name = name
    self.ts = (10**6)*(1.0/(size*60.0))
  
#Realiza a media da variavel
  @property
  def average(self):
    return sum(self)/len(self)

#Realiza o rms
  @property
  def rms(self):
    sum_sqr = 0
    for a in list(self) :
      sum_sqr = (sum_sqr + a*a )
    return np.sqrt(sum_sqr/len(self))

#Funcao de concatenacao das amostras
  def add(self, value):
    self.num_elem += 1
    self.append(value)

#Funcao de leitura das portas analogicas
  def readPort(self):
    if(self.num_elem >= self.maxlen):
      print "full", datetime.today()
      self.num_elem = 0
      dataraw = {}
      try:
        datafile = open(os.path.join(os.path.dirname(__file__),datetime.today().strftime('../data/%Y%m%d.json')), 'r+')
        dataraw = json.load(datafile)
        datafile.close()

        if dataraw.has_key(self.name + '_rms'):
          dataraw[self.name + '_rms'].append(self.rms)
          dataraw[self.name + '_mean'].append(self.average)

        else :
          dataraw[self.name + '_rms'] = [self.rms]
          dataraw[self.name + '_mean'] = [self.average]

      except:
        dataraw[self.name + '_rms'] = [self.rms]
        dataraw[self.name + '_mean'] = [self.average]

      datafile = open(os.path.join(os.path.dirname(__file__),datetime.today().strftime('../data/%Y%m%d.json')), 'w+')
      datafile.write(json.dumps(dataraw))
      return 1
    value = self.amp * np.sin(2 * np.pi * self.freq * (self.num_elem%self.maxlen) * self.ts/(10**6))
    self.num_elem += 1
    self.append(value)
    return 0

#Realiza o rms da potencia
def power_apparent(buffer1, buffer2):
  return buffer1.rms * buffer2.rms

#Realiza o calculo da potencia ativa
def power_active(buffer1, buffer2):
  sum_power = sum(np.array(buffer1) * np.array(buffer2))
  if len(buffer1) > len(buffer2):
    return sum_power/len(buffer2)
  else:
    return sum_power/len(buffer1)

def ConsumeCalc(voltage,current):
  data = {
    "current_rms": current.rms,
    "current_mean": current.average,
    "voltage_rms": voltage.rms,
    "voltage_mean": voltage.average,
    "power_apparent": power_apparent(voltage,current),
    "power_active": power_active(current,voltage),
    "power_factor": power_active(current,voltage)/power_apparent(current,voltage)
  }
  return data

def usleep(delay):
  mdelay = delay / 1000.0
  now = time.time()
  while now + mdelay > time.time():
    pass
  return None


#Thread de leitura da tensao e da corrente
def threadRead(voltage, current):
  run_flag = 0
  print "start read", datetime.today()
  while(~run_flag):
    usleep(voltage.ts)
    run_flag = voltage.readPort()
    run_flag = current.readPort()
    if (run_flag) :
        dataraw = {}
        datacalc = ConsumeCalc(voltage,current)

        with open(os.path.join(os.path.dirname(__file__),datetime.today().strftime('../data/%Y%m%d.json')), 'r+') as datafile:
          dataraw = json.load(datafile)
          datafile.close()
          if dataraw.has_key('power_apparent'):
            dataraw['power_apparent'].append(datacalc['power_apparent'])
            dataraw['power_active'].append(datacalc['power_active'])
            dataraw['power_factor'].append(datacalc['power_factor'])
          else :
            dataraw['power_apparent'] = [datacalc['power_apparent']]
            dataraw['power_active'] = [datacalc['power_active']]
            dataraw['power_factor'] = [datacalc['power_factor']]
        with open(os.path.join(os.path.dirname(__file__),datetime.today().strftime('../data/%Y%m%d.json')), 'w+') as datafile:
          datafile.write(json.dumps(dataraw))

        with open(os.path.join(os.path.dirname(__file__),datetime.today().strftime('../data/consumeinfo.json')), 'w+') as datafile:
          datafile.write(json.dumps(datacalc))

        print "PLOT", datetime.today()
        t = np.arange(0,voltage.maxlen)*voltage.ts
        voltage_trace = go.Scatter(
          x = t,
          y = list(voltage),
          name = 'Voltage'
        )
        
        current_trace = go.Scatter(
          x = t,
          y = list(current),
          name = 'Current',
          yaxis = 'y2' 
        )
        
        plot = [voltage_trace, current_trace]
        
        # Edit the layout
        layout = dict(title = 'Instant Consumption',
              xaxis = dict(title = 'Time in microseconds'),
              yaxis = dict(title = 'Voltage[V]'),
              yaxis2 = dict(title = 'Current[A]',
                  overlaying='y',
                  side='right',
                  range = [-10,10]),
              paper_bgcolor='rgba(0,0,0,0)',
              plot_bgcolor='rgba(0,0,0,0)'
        )
        
        # Plot and embed in ipython notebook!
        fig = dict(data=plot, layout=layout)
        py.image.save_as(fig, filename=os.path.join(os.path.dirname(__file__),'../fig/ConsumeInfo.png'))
        data = []
        
        for key in dataraw.keys():
          data.append( go.Scatter(
            y = dataraw[key],
            x = np.linspace(0,len(dataraw[key]),len(dataraw[key])),
            name = key
          ))
        
        layout2 = dict(title = 'Consumption History',
              xaxis = dict(title = 'Samples'),
              yaxis = dict(title = 'Power, Voltage, Current'),
              paper_bgcolor='rgba(0,0,0,0)',
              plot_bgcolor='rgba(0,0,0,0)'
        )
        fig = dict(data=data, layout=layout2)
        historyurl = py.image.save_as(fig, filename=os.path.join(os.path.dirname(__file__),'../fig/History_test2.png'))
        print historyurl
        return None
