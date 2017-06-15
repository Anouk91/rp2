#!dev/python

import numpy as np


hn_i, hw =np.loadtxt('data6days')
hn_vps = list(hn_i)
highest = 0 
tot_value = 0
tot_amount = 0

for i in range(0, len(hn_vps)):
	if hn_vps[i] > highest:
		highest = hn_vps[i]
	tot_value += hn_vps[i]
	tot_amount += 1

print "highest amount of CPU seconds = ", highest, "which is ", (highest/192)*100, "%"

print "average aamount of CPU seconds = ", tot_value/tot_amount, "which is ", ((tot_value/tot_amount)/192)*100, "%"
