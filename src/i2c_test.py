import mraa as m
import time
import plotly
import matplotlib.pyplot as plt
ts = (1/1200.0)


adc = m.I2c(0)
adc.address(0x48)
x = []
y1 = []
y2 = []

adc.writeByte(0x30)
print 'Start read'
for i in range(20):
  rd = adc.read(4)
  print rd
  y1.append(rd[0])
  x.append(i)
  time.sleep(ts)

print 'Plot'
plt.plot(x,y1)
plt.savefig('ADC_test.png')
