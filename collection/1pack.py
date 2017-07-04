#!/dev/python
import rrdtool
import os
import numpy as np
import re
import glob

#--- a script to create a text file containin all CPU seconds and wattage at the same time ---#

#--- Variables ---#
t1 = '1498775400' #2017-06-30 00:30 '1498420800' #2017-06-25 22:00
t2 = '1499021940' #2017-07-02 21:00
not_used_files = 0
total_files = 0
pwd3 = '/home/aboukema/rp2/data/packages'
pwd2 = '/home/aboukema/rp2/data/machines' 
pwd1 = '/home/aboukema/rp2/data/hardware_nodes' 

def init_list(x):
    empty_array = []
    for x in range(x):
        empty_array.append(0)
    return empty_array


def read_rrd(key, interval, pwd = pwd1):
    global not_used_files, total_files
    os.chdir(pwd)
    file_list = glob.glob(key)    
    missing = []
    data = []
    total_notused = not_used_files
    total_total_files = total_files
    new = True
    st = str(interval)
    for filename in file_list: #--- Itterate through all files in directory ---#
        rrdfile = rrdtool.fetch( '%s/%s' % (pwd,filename), 'AVERAGE',
           '-r', '5m', '--start', t1, '--end', t2)

        if isinstance(rrdfile[2][2][0], float): #--- Exclude empty rrdfiles---#
            data= concatinate(rrdfile[2], data, interval)
#            print filename
        else:  
             not_used_files += 1
#             print "not used file = " ,filename, type(rrdfile[2][2][0])
        total_files += 1    
#        print filename, len(data), len(missing)
    if pwd == pwd1:
        data = make_half(data, interval)
        missing = make_half(missing, interval)
    usedrrds = total_files - total_total_files
    notusedrrds = not_used_files - total_notused
    print "lengths of ",key,  len(data), "\ntotal files ", usedrrds, "\nnot used ", notusedrrds
    return data


def add_rrd(rrd, data, empty, pwd):
    indexsum = 0
    length = len(data) - len(rrd)
    if pwd == pwd3: #cpu data of packages is stored at index 1, all other have it stored at index 0
         index = 1 
    else:
         index = 0
    rrd = list(rrd)
    for t in range(0, len(rrd)): #itterate through time points within rrd file and add to data at same (t)
        if isinstance(rrd[t][index], float) or isinstance(rrd[t][index], int): 
            data[length + t] += rrd[t][index]
        else:
           empty[length + t] += 1
           indexsum += t
    return data, empty 

#---used to interpolate ---#
def make_half(a, interval):
    half =[0] 
    new_interval = 0
    count = 0 
    for i in range(0, len(a)):
        if count != interval:
            half[new_interval] += a[i]
            count += 1
        else:
            half.append(0)
            half[new_interval] =float(half[new_interval])/float(interval)
            new_interval += 1
            half[new_interval] += a[i]
            count = 1
    half[new_interval] =float(half[new_interval])/float(interval)
    if len(half) != len(a)/interval:
         del half[-1]
    return half
  

def concatinate(rrdFile, complete, time):
    a = list(rrdFile)
    complete.append(0)
    #length = len(complete)
    complete[-1] += a[time][1]
    return complete 

def sum_lists(a, b):
    l = init_list(len(a))
    for i in range(0, len(a)):
        l[i] = b[i] + a[i]
    return l 


#--- remove the data points which contain 1 or more empty values---#
def gen_indexes(e1, l1, e2, l2, e3, l3, e4, l4, e5, l5, e6, l6 ):
    removed = 0
    index = 0 
    print e1, e2, e3, e4, e5, e6
    if e3 == []:
        e3 = init_list(len(e1))
        l3 = init_list(len(e1))
        e4 = init_list(len(e1))
        l4 = init_list(len(e1))
    for i in range(len(e1)):
        if e1[i] > 0 or e2[i] > 0 or e3[i] > 0 or e4[i] > 0 or e5[i] > 0 or e6[i] > 0:
            removed += 1
            del l1[index]
            del l2[index]
            del l3[index]
            del l4[index]
            del l5[index]
            del l6[index]
        else: 
            index += 1
    print "removed amount of time points = " , removed


#--- Creating the data lists, by giving a key string to find the right rrdfiles, giving the interval underwhich it is collected, and under wich directory it should be found---#
pack1 = read_rrd('usage*',1,pwd3)
pack10 = read_rrd('usage*',10,pwd3)
pack20 = read_rrd('usage*',20,pwd3)

print pack1


os.chdir('/home/aboukema/rp2/data/git/data')
used_files = (total_files - not_used_files)
percent = (float(used_files) /float(total_files))*100
print "all files: \t", total_files, "\n removed files \t", not_used_files , "\ngives \t%.2f "  %percent, "% useable files"
np.save('packages', (pack1, pack10, pack20))
