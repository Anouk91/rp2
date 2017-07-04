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
            data= concatinate(rrdfile[2], data, interval, key)
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


  

def concatinate(rrdFile, complete, time, key):
    a = list(rrdFile)
    complete.append(0)
    if key == 'us*':
        complete[-1] += a[time][0]
    else:
        complete[-1] += a[time][1]
    return complete 


#--- Creating the data lists, by giving a key string to find the right rrdfiles, giving the interval underwhich it is collected, and under wich directory it should be found---#
pack1 = read_rrd('usage*',1,pwd3)
pack10 = read_rrd('usage*',10,pwd3)
pack20 = read_rrd('usage*',20,pwd3)
mem1 = read_rrd('us*',1,pwd3)
mem10 = read_rrd('us*',10,pwd3)
mem20 = read_rrd('us*',20,pwd3)
print pack1


os.chdir('/home/aboukema/rp2/data/git/data')
used_files = (total_files - not_used_files)
percent = (float(used_files) /float(total_files))*100
print "all files: \t", total_files, "\n removed files \t", not_used_files , "\ngives \t%.2f "  %percent, "% useable files"
np.save('pack1', (pack1, mem1))
np.save('pack10', (pack10, mem10))
np.save('pack20', (pack20, mem20))
