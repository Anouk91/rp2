#!/dev/python

import rrdtool
import os

# x is the amount of data points per package to take into account
x = 5
i = 0
y = 5.

for filename in os.walk(r'/home/aboukema/rp2/data/packages'):
 #print filename
 pass

tot = 0

info = rrdtool.fetch('/home/aboukema/rp2/data/packages/usage_3476_N241.rrd',
	'AVERAGE',
	 '-r', '1',
	 '--start', '1484652900',
	 '--end', '1484659500')

print info
for i in range(x):
  print info[2][i][1]
  tot += info[2][i][1]
  #print tot

average = tot/y
print "average = %f" % average

