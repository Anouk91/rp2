#!/dev/python

import rrdtool
import os
#for i in range(5):
for files in os.walk(r'/home/aboukema/rp2/data/packages'):
   for filename in files:
      print filename

info = rrdtool.fetch('/home/aboukema/rp2/data/packages/usage_1701_N243.rrd',
	'AVERAGE',
	 '-r', '1',
	 '--start', '1484652900',
	 '--end', '1484659500')

print info
