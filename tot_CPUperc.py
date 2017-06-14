#!dev/python

import numpy as np


hn_i, hw =np.loadtxt('data6days')
hn_vps = list(hn_i)
highest = 0 
print hn_vps
for i in range(0, len(hn_vps)):
	if hn_vps[i] > highest:
		highest = hn_vps[i]



print "highest amount of CPU seconds = ", highest, "which is ", (highest/192)*100, "\%"

