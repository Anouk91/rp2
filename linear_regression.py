#!dev/python

import numpy as np
import os
from numpy import arange,array,ones,linalg
import matplotlib.pyplot as plt


hn_i, hw =np.loadtxt('hn_i.out')

A = np.vstack([hn_i, np.ones(len(hn_i))]).T
print A


m, c = np.linalg.lstsq(A, hw)[0]

print(m, c)
#plt.plot(hw, label='Watt')
plt.plot(hn_i, hw, 'o')
#plt.plot(hn_i, hw, 'o', label='Original data', markersize=10)
#plt.plot(hn_i, m*hn_i + c, 'r', label='Fitted line')
plt.legend()
plt.show()
