#!/dev/python
import rrdtool
import os
import numpy as np
#	''''a script to create a text file containin all CPU seconds and wattage at the same time''''
t1 = '1495550400'
t2 = '1495749000'
tot = 0

def create_array(x):
	empty_array = []
	for x in range(x):
		empty_array.append(0)
  	return empty_array


def read_rrd(start, end, a = 0, b = 0):
	global tot
	for files in os.walk(r'/home/aboukema/rp2/data/machines'):
		print file
		for filename in files[2]:
			filename = str(filename)
	     		if filename.startswith(start) and filename.endswith(end):
        			file = rrdtool.fetch('/home/aboukema/rp2/data/machines/%s' % filename, 'AVERAGE', '-r', '1', '--start', t1, '--end', t2)
				print "length of file = ", len(file[2])
				if a == 0:
					print "a = empty array"
					a = create_array(len(file[2]))
				if b == 0:
					#print len(file[2])
					b = create_array(len(file[2]))
				a, b = fill_array(file, a, b)
				#print "\n empty indexes", filename,  b
				tot += 1
 			return a, b


def fill_array(info, array, empty_values):
	print "index 0 of array = ", array[0]
	for i in range(0, len(info[2])):
		if isinstance(info[2][i][0], float): #eigenlijk moet bij een none het hele datapunt worden verwijderd
			array[i] += info[2][i][0]
		else:
			empty_values[i] += 1
	return array, empty_values




hn, empty_hn = read_rrd('hn', 'cpu.rrd')
print "HN \n ", hn 
hn_i, empty_hn_i = read_rrd('i', 'cpu.rrd', hn, empty_hn)

hw, empty_hw = read_rrd('hw', 'rrd')


print "HN \n ", hn , "\n HN + i \n", hn_i , " \n HW \n" , hw
print empty_hn_i,empty_hw, "tot =", tot
#np.savetxt('hn_i.out', (hn_i, hw))
