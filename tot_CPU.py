#!/dev/python
import rrdtool
import os
import numpy as np

x = 5 		#x = the amount of data points per package to take the average from
hn_i = []
hw = []
t1 = '1495550400'
t2 = '1495558200'

for i in range(5):
 hw.append(0)

for i in range(5):
 hn_i.append(0)

for files in os.walk(r'/home/aboukema/rp2/data/machines'):

 for filename in files[2]:
  filename = str(filename)
  #--- add HN CPU seconds to hn_i ---#
  if filename.startswith('hn') and filename.endswith('cpu.rrd'):
   info = rrdtool.fetch('/home/aboukema/rp2/data/machines/%s' % filename,
	'AVERAGE',
	 '-r', '1',
	 '--start', t1,
	 '--end', t2)

   if isinstance(info[2][2][0], float):
    for i in range(x):
     hn_i[i] += info[2][i][0]

  #--- add i CPU seconds to hn_i ---#
  if filename.startswith('i') and filename.endswith('cpu.rrd'):
   info = rrdtool.fetch('/home/aboukema/rp2/data/machines/%s' % filename,
        'AVERAGE',
         '-r', '1',
         '--start', t1,
         '--end', t2)

   if isinstance(info[2][2][0], float):
    for i in range(x):
     hn_i[i] += info[2][i][0]

  #--- add HW wattage to hw ---#
  if filename.startswith('hw'):
   info = rrdtool.fetch('/home/aboukema/rp2/data/machines/%s' % filename,
        'AVERAGE',
         '-r', '1',
         '--start', t1,
         '--end', t2)

   if isinstance(info[2][2][0], float):
    for i in range(x):
     hw[i] += info[2][i][0]



print hn_i
print hw

np.savetxt('hn_i.out', (hn_i, hw))
