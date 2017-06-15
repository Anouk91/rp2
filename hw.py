#!/dev/python
import rrdtool
import os
import numpy as np
import re
import glob

#    ''''a script to create a text file containin all CPU seconds and wattage at the same time''''
t1 = '1497491820' #2017-06-08 00:00
t2 = '1497521760' #2017-06-13 12:00
tot = 0
empty = 0
pwd = '/home/aboukema/rp2/hardware_nodes'


def init_list(x):
    empty_array = []
    for x in range(x):
        empty_array.append(0)
    print "type if epty array", type(empty_array)
    return empty_array


def read_rrd(key):
    global tot
    a = 0
    os.chdir(pwd)
    file_list = glob.glob(key)    
    print file_list
    for filename in file_list:
        file = rrdtool.fetch('/home/aboukema/rp2/hardware_nodes/%s' % filename, 'AVERAGE',
        '-r', '1', '--start', t1, '--end', t2)
        print filename
        if a == 0:
            print "length of file = ", len(file[2])
            a = init_list(len(file[2]))
            b = init_list(len(file[2]))
            empty = 1
        a, b = sum_lists(file, a, b)
        tot += 1
        #print "\n empty indexes", filename,  b
    return a, b


def sum_lists(a, b, empty_values = 0):
    a = list(a)   
# print "index 0 of array = ", array[0]
#    print type(info), type(array)
    for i in range(0, len(a[2])):
        if isinstance(a[2][i][0], float): #eigenlijk moet bij een none het hele datapunt worden verwijderd
            b[i] += a[2][i][0]
        else:
            empty_values[i] += 1
    return b, empty_values 

def sum_lists1(a, b):
    l = init_list(len(a))
    for i in range(0, len(a)):
        l[i] = b[i] + a[i]
    return l 


cpu, empty_cpu = read_rrd('*cpu_user*')
mem, empty_mem = read_rrd('*total*')
watt, empty_watt = read_rrd('hw_*')
print cpu, empty_cpu, tot
print mem, empty_mem
print watt



#print empty_hn_i,empty_hw, "tot =", tot
np.save('x-as', (cpu, mem))
np.save('y-as', (watt))
