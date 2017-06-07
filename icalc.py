#!/dev/python

import rrdtool
import os

#--- x is the amount of data points per package to take the average from ---#
x = 5
inactive_hns = 0
active_hns = 0
tot_cpu_sec = 0
tot_hns = 0
print "All files with an average of CPU seconds above a second:"

for files in os.walk(r'/home/aboukema/rp2/data/machines'):
 #print "\nNumber of files in the directory = %i " %len(files[2])

 #--- for each package in the package directory compute the average cpu seconds ---#
 for filename in files[2]:
  filename = str(filename)

  if filename.startswith('i') and filename.endswith('cpu.rrd'):
   tot_hns += 1
   total = 0
   info = rrdtool.fetch('/home/aboukema/rp2/data/machines/%s' % filename,
	'AVERAGE',
	 '-r', '1',
	 '--start', '1495550400',
	 '--end', '1495558200')

   #--- the cpu seconds are stored at index i ---#
   if isinstance(info[2][2][0], float): #--- make sure to only use non-empty data ---#
    for i in range(x):
     total += info[2][i][0]

    average = total/x
    if average > 1:
	print filename, average
    #print "%s \t %f" %(filename, average)
    active_hns += 1
    tot_cpu_sec += average
   else:
    #print "empty host package rrd file"
    inactive_hns += 1


print "Number of empty host packages = %i" %inactive_hns

#--- there are 12 harware devices which have 2x8 CPU cores ---#
max_cpu_sec =  12 * 16
print "max CPU seconds available = %i \n" %max_cpu_sec

print "All %d active hosting nodes used %f seconds of CPU" %(active_hns, tot_cpu_sec)

total_used = tot_cpu_sec/max_cpu_sec*100
print "Which is %f%% of total available CPU seconds \n" %total_used

