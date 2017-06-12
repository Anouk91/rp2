#!/dev/python
import rrdtool
import os
import numpy as np

x = 5 		#x = the amount of data points per package to take the average from
hn_i = []
hw = []
t1 = '1495550400'
t2 = '1495749000'
t = []
i = 0
inode = 0
hnnode = 0

for y in range(5):
 hw.append(0)

for y in range(5):
 hn_i.append(0)

for files in os.walk(r'/home/aboukema/rp2/data/machines'):

 for filename in files[2]:
  filename = str(filename)
 # print filename
  #--- add HN CPU seconds to hn_i ---#
  if filename.startswith('hn') and filename.endswith('cpu.rrd'):
   info = rrdtool.fetch('/home/aboukema/rp2/data/machines/%s' % filename,
	'AVERAGE',
	 '-r', '1',
	 '--start', t1,
	 '--end', t2)

#   if isinstance(info[2][2][0], float):
#    for i in range(x):
   i = 0
   print len(info[2])
   for z in range(1, len(info[2])):
    if isinstance(info[2][i][0], float):
     if not isinstance(hn_i[i], float):
      hn_i.append(0)
     hn_i[i] += info[2][i][0]
     i += 1


  #--- add i CPU seconds to hn_i ---#
  if filename.startswith('i') and filename.endswith('cpu.rrd'):
   print hnnode
   info = rrdtool.fetch('/home/aboukema/rp2/data/machines/%s' % filename,
        'AVERAGE',
         '-r', '1',
         '--start', t1,
         '--end', t2)

   i = 0
   while isinstance(info[2][i][0], float):
    if not isinstance(hn_i[i], float):
     hn_i.append(0)
    hn_i[i] += info[2][i][0]
    i += 1
    if i > inode:
     inode = i

  #--- add HW wattage to hw ---#
  if filename.startswith('hw'):
#   print "length hw_i = %i" %inode
   info = rrdtool.fetch('/home/aboukema/rp2/data/machines/%s' % filename,
        'AVERAGE',
         '-r', '1',
         '--start', t1,
         '--end', t2)

   i = 0
   while isinstance(info[2][i][0], float):
    if not isinstance(hw[i], float):
      hw.append(0)
    hw[i] += info[2][i][0]
    i += 1
   print len(hw)

print hn_i
print hw

np.savetxt('hn_i.out', (hn_i, hw))
