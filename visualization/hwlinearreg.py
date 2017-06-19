
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import glob

sns.set(style="whitegrid", color_codes=True)
os.chdir('/Users/anoukboukema/Desktop/SaNE/rp2/git/rp2/data')
cpu=np.load('306_*cpu_user*.npy')
watt = np.load('306_hw*.npy')
print cpu.size , watt.size
itterate = watt

# file_list = glob.glob('305*')
# print file_list
# for filename in file_list:
#     if re.search('\d{3}..cpu', filename)
#         cpu=np.load('filename)
#     elif re.search('\d{3}..mem', filename)
# x = 0
# for i in range(0, itterate.size):
#     #print itterate[i]
#     if itterate[i] > 8.23954693487:
#         print "deleted value ", itterate[i], " at index ", i, "current size: ", cpu.size
#         #mem = np.delete(mem, x)
#         watt = np.delete(watt, x)
#         cpu = np.delete(cpu, x)
#     else:
#         x += 1


data = pd.DataFrame({'cpu' : cpu, 'watt' : watt})

#g = sns.FacetGrid()
sns.lmplot(x="cpu", y="watt", data=data)

plt.show()
