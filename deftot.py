#!/dev/python
import rrdtool
import os
import numpy as np

t1 = '1495550400'
t2 = '1495749000'
itt = 0
def create_array():
  empty_array = []
  for x in range(663):
    empty_array.append(0)
  return empty_array


def read_rrd(array, start, end):
 for files in os.walk(r'/home/aboukema/rp2/data/machines'):
  for filename in files[2]:
     filename = str(filename)
     if filename.startswith(start) and filename.endswith(end):
         info = rrdtool.fetch('/home/aboukema/rp2/data/machines/%s' % filename,
         'AVERAGE',
         '-r', '1',
         '--start', t1,
         '--end', t2)
         for i in range(0, len(info[2])):
            if isinstance(info[2][i][0], float): #eigenlijk moet bij een none het hele datapunt worden verwijderd
               array[i] += info[2][i][0]
	    #else:
	    #   hn_i[i] += 10
            #if i == 20:
	     # print filename, array[i], info[2][i][0]
# print start, "\n" , array
 return array
 array = []


empty = create_array()
#print  "empty \n", empty
hn = read_rrd(empty, 'hn', 'cpu.rrd')
#print "HN \n ", hn , "empty \n", empty
hn_i = read_rrd(hn, 'i', 'cpu.rrd')
empty = create_array()
#print "HN \n ", hn , " HN + i \n", hn_i , "empty \n", empty
hw = read_rrd(empty, 'hw', 'rrd')


print "HN \n ", hn , " HN + i \n", hn_i , "HW \n" , hw, "empty \n", empty
#for i in range(0,10):
 #  print hw[i]

np.savetxt('hn_i.out', (hn_i, hw))
