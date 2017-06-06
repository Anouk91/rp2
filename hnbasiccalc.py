#!/dev/python

import rrdtool
import os

# x is the amount of data points per package to take into account
x = 5
i = 0
y = 5.


tot = 0.

info = rrdtool.fetch('/home/aboukema/rp2/data/machines/hn244_cpu.rrd',
	'AVERAGE',
	 '-r', '1',
	 '--start', '1495550400',
	 '--end', '1495557900')

for i in range(x):
  tot += info[2][i][0]
  print info[2][i][0]

average = tot/y
print "average = %f" % average

