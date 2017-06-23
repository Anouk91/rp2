#!/dev/python
import rrdtool
import os
import numpy as np
import re
import glob

#    ''''a script to create a text file containin all CPU seconds and wattage at the same time''''
t1 = '1496836800' #2017-06-06 14:00 
t2 = '1497347700' #2017-06-13 12:00
tot = 0
totall = 0
empty = 0

pwd3 = '/home/aboukema/rp2/data/packages'
pwd2 = '/home/aboukema/rp2/data/machines' 
pwd1 = '/home/aboukema/rp2/hardware_nodes' 

def init_list(x):
    empty_array = []
    for x in range(x):
        empty_array.append(0)
    return empty_array


def read_rrd(key, interval, pwd = pwd1):
    global tot, totall
    a = 0
    os.chdir(pwd)
    file_list = glob.glob(key)    
    complete = []
    st = str(interval)
    for filename in file_list:
#        if pwd == pwd1:
 #           rrdtool.tune('%s/%s' % (pwd,filename), 'DELRRA:2') # add extra fill up first RRA with 4320 data points
        rrdfile = rrdtool.fetch( '%s/%s' % (pwd,filename), 'AVERAGE',
                '-r', '5m', '--start', t1, '--end', t2)
        if re.search('30[2-8]',filename) or re.search('.*.rrd',key): 

            if a == 0:
                data = init_list(len(rrdfile[2]))
                empty = init_list(len(rrdfile[2]))
                a = 1
            #print filename
            if isinstance(rrdfile[2][2][0], float):
                data, empty= add_rrd(rrdfile, data, empty)
                tot += 1
            else: # isinstance(rrdfile[2][2][0], float): 
				print "not used file = " ,filename, type(rrdfile[2][2][0])
            totall += 1      
    if pwd == pwd1:
        data = make_half(data, interval)   
    #half = make_half(data, interval)
    del data[-1]
    print "lengths of ",key,  len(data)
    return data, empty

def save(x, i):
    os.chdir('/home/aboukema/rp2/data/git/data')
    np.save(i,(x))


def add_rrd(rrd, data, empty):
    rrd = list(rrd)
    for i in range(0, len(rrd[2])):

        if isinstance(rrd[2][i][0], float): #eigenlijk moet bij een none het hele datapunt worden verwijderd
            data[i] += rrd[2][i][0]
        else:
           empty[i] += 1
    return data, empty 

def make_half(a, interval):
    half =[0] 
    new_interval = 0
    count = 1 
   # print "old length of file = ", len(a)
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
   # print "new length of file = ", len(half)
    return half
  

def concatinate(rrdFile, complete):
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

def sum_lists(a, b):
    l = init_list(len(a))
    for i in range(0, len(a)):
        l[i] = b[i] + a[i]
    return l 



def gen_indexes(e1, l1, e2, l2):
    removed = 0
    index = 0 
    for i in range(len(e1)-10):
        if e1[i] > 7 or e2[i] > 7:
            print "removed value ",e1[i],"&", e2[i], " at index ",i
            removed += 1
            del l1[index]
            del l2[index]
        else: 
            index += 1

    print "removed amoun = " , removed

#cpu_idle = read_rrd('*cpu_idle*',5)
#cpu_system, e1 = read_rrd('*cpu_system*',5)
#cpu_softirq, e2 = read_rrd('*cpu_softirq*',5)
#mem = read_rrd('*mem_free*',5)
#cpu_user, e3 = read_rrd('*cpu_user*',5)
#watt = read_rrd('hw*',6)

cpu_pack, e6 = read_rrd('usage*',1,pwd3)
cpu_hn, e4= read_rrd('hn*_cpu.rrd',6,pwd2)
#cpu_vps, e5 = read_rrd('i*_cpu.rrd',6,pwd2)

#cpu_hw = sum_lists(cpu_system, cpu_softirq)
#cpu_hw = sum_lists(cpu_hw, cpu_user)
#e_hw = sum_lists(e1, e2)
#e_hw = sum_lists(e_hw, e3)


#cpu_vis = sum_lists(cpu_hn, cpu_vps)
#e_vis = sum_lists(e4, e5)
#print cpu, empty_cpu, tot

#print mem, empty_mem
#print watt
print "length before ", len(cpu_pack), len(e6)
gen_indexes(e4, cpu_pack, e6, cpu_hn)
print "length after ", len(cpu_pack)
#print "packages:\n ",e4,"\n Hosting nodes \n", e6
os.chdir('/home/aboukema/rp2/data/git/data')



print "used files: ", tot, " all files: ", totall, " gives ", totall - tot , " deleted files"
#print empty_hn_i,empty_hw, "tot =", tot
np.save('cpu_pack', (cpu_pack))
np.save('cpu_hn', (cpu_hn))
