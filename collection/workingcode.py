#!/dev/python
import rrdtool
import os
import numpy as np
#    ''''a script to create a text file containin all CPU seconds and wattage at the same time''''
t1 = '1497270600' #2017-06-12 14:30
t2 = '1497348000' #2017-06-13 12:00
tot = 0

pwd1 = '/home/aboukema/rp2/data/machines'
pwd2 = '/home/aboukema/rp2/hardware_nodes'
 
def init_list(x):
    empty_array = []
    for x in range(x):
        empty_array.append(0)
    print "type if epty array", type(empty_array)
    return empty_array


def read_rrd(start, end):
    global tot
    empty = 0 
    for files in os.walk(r'/home/aboukema/rp2/data/machines'):
        for filename in files[2]:
            if filename.startswith(start) and filename.endswith(end):
                file = rrdtool.fetch('/home/aboukema/rp2/data/machines/%s' % filename, 'AVERAGE',
                '-r', '5', '--start', t1, '--end', t2)
                if empty == 0:
                    #print "length of file = ", len(file[2])
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


hn, empty_hn = read_rrd('hn', 'cpu.rrd')
vps, empty_vps = read_rrd('i', 'cpu.rrd')
hn_vps= sum_lists1(hn, vps)
empty_HNandVPS = sum_lists1(empty_hn, empty_vps)
#hw, empty_hw = read_rrd('hw', 'rrd')


#print "HN \n ", hn , "\n vps \n", vps, "\nHN + VPS\n", hn_vps, "\n empty of both\n", empty_HNandVPS , " \n HW \n" , hw

print len(hn_vps)
print(tot)

os.chdir('/home/aboukema/rp2/data/git/data')
#print empty_hn_i,empty_hw, "tot =", tot
np.savetxt('hn_vps', (hn_vps))