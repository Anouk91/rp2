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
rangehn = range(181,246)
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
    missing = []
    st = str(interval)
    for i in rangehn:
        b = 0 
        for filename in file_list:
#        if pwd == pwd1:
 #           rrdtool.tune('%s/%s' % (pwd,filename), 'DELRRA:2') # add extra fill up first RRA with 4320 data points
            rrdfile = rrdtool.fetch( '%s/%s' % (pwd,filename), 'AVERAGE',
               '-r', '5m', '--start', t1, '--end', t2)
            match =".*n%i.*" %i

            if re.search(match,filename, re.IGNORECASE): 
                if a == 0:           
                    data =[] 
                    a = 1
                if b==0: 
                    empty = init_list(len(rrdfile[2]))
                    missing = concatinate(empty, missing)
                    b = 1
                    data = concatinate(empty, data)
              #  print filename, a, b, rrdfile[2][2][0], float
              #  print "len data",len(data), "len missing", len(missing)          
                if isinstance(rrdfile[2][2][0], float):
                    data, missing= add_rrd(rrdfile[2], data, missing)
                    tot += 1
                    print rrdfile[2][2][0]
                else: #if not isinstance(rrdfile[2][2][0], float): 
                    print "not used file = " ,filename, type(rrdfile[2][2][0])
                    totall += 1    
#                if pwd == pwd3:
 #                   for i in range(len(data)):
  #                      data[i] = data[i]/10000

        if pwd == pwd1:
            data = make_half(data, interval)   

    
    #half = make_half(data, interval)
 #   del data[-1]
    print "lengths of ",key,  len(data)
    return data, missing

def save(x, i):
    os.chdir('/home/aboukema/rp2/data/git/data')
    np.save(i,(x))


def add_rrd(rrd, data, empty):
    length = len(data) - len(rrd)
    rrd = list(rrd)
    for i in range(0, len(rrd)):
        if isinstance(rrd[i][0], float): #eigenlijk moet bij een none het hele datapunt worden verwijderd
            data[length + i] += rrd[i][0]
        else:
           empty[length + i] += 1
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
    for i in range(0, len(a)):
#        if isinstance(a[2][i][0], float): #eigenlijk moet bij een none het hele datapunt worden verwijderd
        complete.append(0)
        complete[length] += a[i]
        length += 1
      #  else:
      #       pass
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
        if e1[i] > 0 or e2[i] > 0:
    #        print e1[i],"&", e2[i], " at index ",i, "with value", l1[index], l2[index] 
            removed += 1
            del l1[index]
            del l2[index]
        else: 
            index += 1

    print "removed amount = " , removed

#cpu_idle = read_rrd('*cpu_idle*',5)
#cpu_system, e1 = read_rrd('*cpu_system*',5)
#cpu_softirq, e2 = read_rrd('*cpu_softirq*',5)
#mem = read_rrd('*mem_free*',5)
#cpu_user, e3 = read_rrd('*cpu_user*',5)
#watt = read_rrd('hw*',6)
#usage_2142_N236.rrd

cpu_hn, e4= read_rrd('hn*_cpu.rrd',6,pwd2)
cpu_pack, e6 = read_rrd('usage*',1,pwd3)
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
#gen_indexes(e4, cpu_pack, e6, cpu_hn)
print "length after ", len(cpu_pack)
#print "packages:\n ",e4,"\n Hosting nodes \n", e6
os.chdir('/home/aboukema/rp2/data/git/data')



print "used files: ", tot, " all files: ", totall, " gives ", totall - tot , " deleted files"
#print empty_hn_i,empty_hw, "tot =", tot
np.save('cpu_pack_all', (cpu_pack))
np.save('cpu_hn_all', (cpu_hn))
