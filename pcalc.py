#!/dev/python

import rrdtool
import os

#--- x is the amount of data points per package to take the average from ---#
x = 5
deel = 5.
inactive_packages = 0
active_packages = 0
tot_cpu_sec = 0
print "\n" + "All files with an average of CPU seconds above a second:"

for files in os.walk(r'/home/aboukema/rp2/data/packages'):
 #print "\nNumber of files in the directory = %i " %len(files[2])

 #--- for each package in the package directory compute the average cpu seconds ---#
 for filename in files[2]:
  filename = str(filename)

  if filename.startswith('us'):
   total = 0
   info = rrdtool.fetch('/home/aboukema/rp2/data/packages/%s' % filename,
	'AVERAGE',
	 '-r', '1',
	 '--start', '1484652900',
	 '--end', '1484658900')

   #--- the cpu seconds are stored at index i ---#
   if isinstance(info[2][2][1], float):
    for i in range(x):
     total += info[2][i][1]

    average = total/deel
    if average > 1:
	print filename, average
    #print "%s \t %f" %(filename, average)
    active_packages += 1
    tot_cpu_sec += average
   else:
    #print "empty host package rrd file"
    inactive_packages += 1


print "Number of empty host packages = %i" %inactive_packages

#--- there are 12 harware devices which have 2x8 CPU cores ---#
max_cpu = 60 * 5 * 12 * 16
print "max CPU seconds available = %i \n" %max_cpu

print "All %d active host packages used %f seconds of CPU" %(active_packages, tot_cpu_sec)

total_used = (tot_cpu_sec/max_cpu)*100
print "Which is %i%% of total available CPU \n" %total_used
