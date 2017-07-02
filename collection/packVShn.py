#!/dev/python
import rrdtool
import os
import numpy as np
import re
import glob

#--- a script to create a text file containin all CPU seconds and wattage at the same time ---#

#--- Variables ---#
t1 = '1498482000' #2017-06-26 15:00
t2 = '1498732140' #2017-06-29 12:29
#t1 = '1497628800'  # 2017-06-16 18:00
#t2 = '1498230000'  # 2017-06-23 17:00 
not_used_files = 0
total_files = 0
rangeHN = range(181,246)

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
    st = str(interval)
    for i in rangeHN: #--- Per HostingNode ---#
        newHN = True

        for filename in file_list: #--- Itterate through all files in directory ---#
#        if pwd == pwd1: #--- uncomment if you want to TUNE the data in pwd1---#
#            rrdtool.tune('%s/%s' % (pwd,filename), 'DELRRA:2') # add extra fill up first RRA with 4320 data points
            rrdfile = rrdtool.fetch( '%s/%s' % (pwd,filename), 'AVERAGE',
               '-r', '5m', '--start', t1, '--end', t2)
            
            match =".*n%i.*" %i
            if re.search(match,filename, re.IGNORECASE): 
                if newHN == True: 
                    empty = init_list(len(rrdfile[2]))
                    missing = concatinate(empty, missing)
                    newHN = False
                    data = concatinate(empty, data)
                if isinstance(rrdfile[2][2][0], float): #--- Exclude empty rrdfiles---#
                    data, missing= add_rrd(rrdfile[2], data, missing, pwd)
                else:  
                     not_used_files += 1
                     print "not used file = " ,filename, type(rrdfile[2][2][0])
                total_files += 1    
#                if pwd == pwd3: #data of the package is derive (counter) so should be devided by 300 to get average of 5 min
#                    for i in range(len(data)):
#                        data[i] = data[i]/300

    if pwd == pwd1:
        data = make_half(data, interval)
    if pwd == pwd3:
        for i in range(len(data)):
            data [i] = data[i]/10000

#    half = make_half(data, interval)
#    del data[-1]
    print "lengths of ",key,  len(data)
    return data, missing

def save(x, i):
    os.chdir('/home/aboukema/rp2/data/git/data')
    np.save(i,(x))


def add_rrd(rrd, data, empty, pwd):
    length = len(data) - len(rrd)
    if pwd == pwd3: #cpu data of packages is stored at index 1, all other have it stored at index 0
         index = 1 
    else:
         index = 0
    rrd = list(rrd)
    for t in range(0, len(rrd)): #itterate through time points within rrd file and add to data at same (t)
        if isinstance(rrd[t][index], float): 
            data[length + t] += rrd[t][index]
        else:
           empty[length + t] += 1
    return data, empty 

#---used to interpolate ---#
def make_half(a, interval):
    half =[0] 
    new_interval = 0
    count = 1 
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
    return half
  

def concatinate(rrdFile, complete):
    a = list(rrdFile)
    empty_values = init_list(len(a))
    length = len(complete) 
    for i in range(0, len(a)):
        complete.append(0)
        complete[length] += a[i]
        length += 1
    return complete 

def sum_lists(a, b):
    l = init_list(len(a))
    for i in range(0, len(a)):
        l[i] = b[i] + a[i]
    return l 


#--- remove the data points which contain 1 or more empty values---#
def gen_indexes(e1, l1, e2, l2):
    removed = 0
    index = 0 
    for i in range(len(e1)-10):
        if e1[i] > 0 or e2[i] > 0:
            removed += 1
            del l1[index]
            del l2[index]
        else: 
            index += 1
    print "removed amount of time points = " , removed


#--- Creating the data lists, by giving a key string to find the right rrdfiles, giving the interval underwhich it is collected, and under wich directory it should be found---#
#cpu_system, e1 = read_rrd('*cpu_system*',5)
#cpu_softirq, e2 = read_rrd('*cpu_softirq*',5)
#cpu_user, e3 = read_rrd('*cpu_user*',5)
cpu_hn, e4= read_rrd('hn*_cpu.rrd',6,pwd2)
cpu_pack, e6 = read_rrd('usage*',1,pwd3)
#cpu_vps, e5 = read_rrd('i*_cpu.rrd',6,pwd2)

#--- Add lists together ---#
#cpu_hw = sum_lists(cpu_system, cpu_softirq)
#cpu_hw = sum_lists(cpu_hw, cpu_user)
#e_hw = sum_lists(e1, e2)
#e_hw = sum_lists(e_hw, e3)
#cpu_vis = sum_lists(cpu_hn, cpu_vps)
#e_vis = sum_lists(e4, e5)

#--- remove the data points which contain 1 or more empty values---#
print "length before ", len(cpu_pack), len(e6)
gen_indexes(e4, cpu_pack, e6, cpu_hn)
print "length after ", len(cpu_pack)



os.chdir('/home/aboukema/rp2/data/git/data')
used_files = ((total_files - not_used_files)/total_files)*100    
print "all files: \t", total_files, "\n removed files \t", not_used_files , "\ngives \t" ,used_files, "% useable files"
np.save('newdata_newscript_pack', (cpu_pack))
np.save('newdata_newscript_hn', (cpu_hn))
