## Pruio test

from pruio import Pruio
import time

Act = 0xFFFF #0xFFFF=PRUIO_DEF_ACTIVE  #activation mode
Av = 0                  #avaraging for default steps
OpD = 0                 #open delay for default steps (default 0x98, max 0x3FFFF)
SaD = 0                 #sample delay for default steps (defaults to 0)
Stp = 9                 #step index (0=step 0=>charge step, 1=step 1 (=> AIN-0 by default), ...., 17 = idle step)
ChN = 0                 #Channel Number to scan (0 = AIN-0, 1= AIN-1, ....)
Mds = 4                 #modus for output (default to 4 = 16 bit)
samp = 50             #number of samples in the files (per step)
tmr = 1000000000.0/(600.0*60.0) #1ms! sampling rate in ns (10000 -> 100 kHz)


adc = Pruio(Act, Av, OpD, SaD)
print "1 sample test"
adc.config(1, 0x1FE, 0, 4)
ch = adc.read_adc_ch()
print ch


print "rb test 1200"
adc.config(samp, 0b010000100, tmr, Mds)
adc.rb_start()
time.sleep(2)
ch = adc.read_adc_ch()
print ch

for key in ch.keys():
  print key, "length", len(ch[key])
