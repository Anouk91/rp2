#!/dev/python
import rrdtool
import os


#--- x is the amount of data points per package to take the average from ---#
  x = 5
inactive_hns = 0
active_hns = 0
tot_cpu_sec = 0
tot_hns = 0
hn_i = []

for i in range(5):
 hn_i.append(0)

print "All files with an average of CPU seconds above a second:"

for files in os.walk(r'/home/aboukema/rp2/data/machines'):
 #print "\nNumber of files in the directory = %i " %len(files[2])

 #--- for each package in the package directory compute the average cpu seconds ---#
 for filename in files[2]:
  filename = str(filename)

  if filename.startswith('hw'):
   tot_hns += 1
   info = rrdtool.fetch('/home/aboukema/rp2/data/machines/%s' % filename,
	'AVERAGE',
	 '-r', '1',
	 '--start', '1495550400',
	 '--end', '1495558200')
 
 print info
   #--- the cpu seconds are stored at index i ---#
   if isinstance(info[2][2][0], float): #--- make sure to only use non-empty data ---#
    for i in range(x):
     hn_i[i] += info[2][i][0]

    active_hns += 1
    print hn_i
   else:
    #print "empty host package rrd file"
    inactive_hns += 1


print hn_i
print "Number of empty host packages = %i" %inactive_hns


