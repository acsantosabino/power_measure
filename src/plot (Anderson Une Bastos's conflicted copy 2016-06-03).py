import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import os
from datetime import datetime

plotly.tools.set_credentials_file(username='TCC2016', api_key='wfo2kqaa3f')

# Create random data with numpy
import numpy as np
import json

with open(os.path.join(os.path.dirname(__file__),datetime.today().strftime('../data/%Y%m%d.json')), 'r') as datafile:
    dataraw = json.load(datafile)

data = []
i = 0

for key in dataraw.keys():
    data.append( go.Scatter(
        y = dataraw[key],
        x = np.linspace(0,len(dataraw[key]),len(dataraw[key])),
        name = key
    ))
    
with open(os.path.join(os.path.dirname(__file__).datetime.today()('../data/consume.info.json')), 'r') as filedata:
          filedata = json.load(filedata)
          
# Plot and embed in ipython notebook!
py.iplot(data, filename='History_test')




# or plot with: plot_url = py.plot(data, filename='basic-line')