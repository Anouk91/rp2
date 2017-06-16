#!/dev/python
import rrdtool
import os
import numpy as np
import re
import glob

#    ''''a script to create a text file containin all CPU seconds and wattage at the same time''''
t1 = '1497279600' #2017-06-12 17:00 
t2 = '1497520800' #2017-06-15 12:00
tot = 0
empty = 0
pwd = '/home/aboukema/rp2/hardware_nodes'


def init_list(x):
    empty_array = []
    for x in range(x):
        empty_array.append(0)
    return empty_array


def read_rrd(key, interval):
    global tot
    a = 0
    os.chdir(pwd)
    file_list = glob.glob(key)    
    #print file_list
    for filename in file_list:
        file = rrdtool.fetch( '%s/%s' % (pwd,filename), 'AVERAGE',
                '-r', '6m', '--start', t1, '--end', t2)
       #   qq print filename
        if a == 0:
            #print "length of file = ", len(file[2])
            a = init_list(len(file[2]))
            b = init_list(len(file[2]))
            empty = 1
             
        a, b = sum_lists(file, a, b)
        tot += 1
        #print "\n empty indexes", filename,  b

    half = make_half(a, interval)
    print half
    return half, b


def make_half(a, interval):
    length = len(a)/interval +1
    half = init_list(length)
    new_interval = 0
    count = 1
    for i in range(0, len(a)):
        if count != interval:
            half[new_interval] += a[i]
            count += 1
        else:
            half[new_interval] = half[new_interval]/interval
            new_interval += 1
            count = 1
    print "length of file = ", len(half)
    return half
  

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


cpu, empty_cpu = read_rrd('*cpu_user*',5)
mem, empty_mem = read_rrd('*total*',5)
watt, empty_watt = read_rrd('hw_*',6)
#print cpu, empty_cpu, tot
#print mem, empty_mem
#print watt

os.chdir('/home/aboukema/rp2/data/git')


#print empty_hn_i,empty_hw, "tot =", tot
np.save('x', (cpu, mem))
np.save('y', (watt))
