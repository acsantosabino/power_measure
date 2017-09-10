#Import the libraries used
import os, os.path
from collections import deque
import numpy as np
import time, json
from datetime import datetime
import sys

import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import json

forms = deque([ 'sin', 'hwr', 'fwr', 'sqr'])

#Criacao da classe de leitura dos pinos analogicos
class Measure(deque):
  num_elem = 0
  freq = 60
  amp = 5
  
#Inicializacao da porta analogica
  def __init__(self, name, adcPort, gpioPort, size=0):
    super(Measure, self).__init__(maxlen=size)
    self.name = name
    self.form = 'sin'
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

  def signal_gen(self):
    sinus = np.sin(2 * np.pi * self.freq * (self.num_elem%self.maxlen) * self.ts/(10**6))
    return {
      'sin' : self.amp * sinus,
      'hwr' : self.amp * (sinus if sinus >0 else 0),
      'fwr' : self.amp * np.abs(sinus),
      'sqr' : self.amp * ( 1.0 if self.num_elem < self.maxlen/2 else -1.0)
    }.get(self.form)

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
    value = self.signal_gen()
    self.num_elem += 1
    self.append(value)
    return 0

#Realiza o rms da potencia
def power_apparent(buffer1, buffer2):
  return buffer1.rms * buffer2.rms

#Realiza o calculo da potencia ativa
def power_active(buffer1, buffer2):
  sum_power = sum(np.array(buffer1) * np.array(buffer2))
  print "sum_power: ", sum_power
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

        #current.form = forms[0]
        forms.rotate(1)

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
        # Plot 1
        fig, ax1 = plt.subplots()
        ax1.grid(True)
        ax1.plot(t, list(voltage))
        ax1.set_xlabel('Time in microseconds')
        # Make the y-axis label, ticks and tick labels match the line color.
        ax1.set_ylabel('Voltage[V]', color='b')
        ax1.tick_params('y', colors='b')
        ax2 = ax1.twinx()
        ax2.plot(t, list(current), 'r')
        ax2.set_ylabel('Current[A]', color='r')
        ax2.tick_params('y', colors='r')

        plt.title('Instant Consuption')
        plt.axis('tight')
        ax1.set_ylim([1.2*min(voltage), 1.2*max(voltage)])
        ax2.set_ylim([1.2*min(current) if min(current)!=0 else -0.2*max(current), 1.2*max(current)])

        fig.savefig(os.path.join(os.path.dirname(__file__),'../fig/ConsumeInfo.svg'), transparent=True)
        plt.close(fig)
        legend = []
        ymax = 0

        # Plot 2
        fig = plt.figure()
        plt.title('Consumption History')
        plt.grid(True)

        for key in dataraw.keys():
          y = dataraw[key]
          x = np.linspace(0,len(dataraw[key]),len(dataraw[key]))
          legend.append(key.replace('_',' ').title())
          ymax = max(ymax, max(y))
          plt.plot(x, y)

        plt.axis('tight')
        plt.ylim(0,ymax*1.2)
        lgd = plt.legend(legend, loc='center left', bbox_to_anchor=(1, 0.5))
        fig.savefig(os.path.join(os.path.dirname(__file__),'../fig/History_test2.svg'), transparent=True, bbox_extra_artists=(lgd,), bbox_inches='tight')
        plt.close(fig)
        return None

