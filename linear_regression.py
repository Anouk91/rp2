#!dev/python

import numpy as np
import os
from numpy import arange,array,ones,linalg
from pylab import plot,show


hn_i, hw =np.loadtxt('hn_i.out')

xi = arange(0,len(hw)-1)
w = linalg.lstsq(hn_i.T,hw)[0] # obtaining the parameters

# plotting the line
line = w[0]*xi+w[1] # regression line
plot(xi,line,'r-',xi,hw,'o')
show()
