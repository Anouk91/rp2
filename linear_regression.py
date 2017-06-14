#!dev/python

import numpy as np
import os
from numpy import arange,array,ones,linalg
import matplotlib.pyplot as plt
from pylab import plot,show
from scipy import stats


hn_i, hw =np.loadtxt('6days')
hn_itterate = list(hn_i)
hn_vps = list(hn_i)
hw = list(hw)
length = len(list(hn_i))
print "length before deletion = ", length
deleted_values = 0
x = 0
for i in range(0, len(hn_itterate)):
    if hn_itterate[i] < 50:
        print "deleted value ", hn_vps[x], i
        del hn_vps[x]
        del hw[x]
        deleted_values += 1
    else:
        x += 1

print "length before deletion = ", len(hn_vps)
print "deleted values ", deleted_values
hn_vps = np.array(hn_vps)
hw = np.array(hw)
#A = np.vstack([hn_vps, np.ones(len(hn_vps))]).T

slope, intercept, r_value, p_value, std_err = stats.linregress(hn_vps,hw)

print 'r value', r_value
print  'p_value', p_value
print 'standard deviation', std_err
print 'length x', len(hn_vps)
print 'length y', len(hw)


line = slope*hn_vps+intercept
plot(hn_vps,line,'r-',hn_vps,hw,'o')
show()
