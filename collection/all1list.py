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
    complete = []
    st = str(interval)
    for filename in file_list:
        rrdfile = rrdtool.fetch( '%s/%s' % (pwd,filename), 'AVERAGE',
                '-r', st, 'm', '--start', t1, '--end', t2)
        if re.search('30[2-8]',filename): 
            print filename
            complete = sum_lists(rrdfile, complete)
            tot += 1

    half = make_half(complete, interval)
    print key, len(half)
    return half

def save(x, i):
    os.chdir('/home/aboukema/rp2/data/git/data')
    np.save(i,(x))
    

def make_half(a, interval):
    half =[0] 
    new_interval = 0
    count = 1 
    print "old length of file = ", len(a)
    for i in range(0, len(a)):
        if count != interval:
            half[new_interval] += a[i]
            count += 1
        else:
            half.append(0)
            half[new_interval] = half[new_interval]/interval
            new_interval += 1
            half[new_interval] += a[i]
            count = 1
    print "new length of file = ", len(half)
    return half
  

def sum_lists(rrdFile, complete):
    a = list(rrdFile)  
    empty_values = init_list(len(a))
    length = len(complete) 
    for i in range(0, len(a[2])):
        if isinstance(a[2][i][0], float): #eigenlijk moet bij een none het hele datapunt worden verwijderd
            complete.append(0)
            complete[length] += a[2][i][0]
            length += 1
        else:
             pass
    return complete 

def sum_lists1(a, b):
    l = init_list(len(a))
    for i in range(0, len(a)):
        l[i] = b[i] + a[i]
    return l 


cpu = read_rrd('*cpu_idle*',5)
mem = read_rrd('*mem_free*',5)
watt = read_rrd('hw*',6)
#print cpu, empty_cpu, tot
#print mem, empty_mem
#print watt

os.chdir('/home/aboukema/rp2/data/git/data')


#print empty_hn_i,empty_hw, "tot =", tot
np.save('x_idle', (cpu, mem))
np.save('y_watt', (watt))
