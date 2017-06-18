
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="whitegrid", color_codes=True)

cpu, mem =np.load('x.npy')
watt = np.load('y.npy')
print cpu.size , mem.size, watt.size
itterate = cpu

# x = 0
# for i in range(0, itterate.size):
#     #print itterate[i]
#     if itterate[i] > 8.23954693487:
#         print "deleted value ", itterate[i], " at index ", i, "current size: ", cpu.size
#         mem = np.delete(mem, x)
#         watt = np.delete(watt, x)
#         cpu = np.delete(cpu, x)
#     else:
#         x += 1


data = pd.DataFrame({'cpu' : cpu, 'mem' : mem, 'watt' : watt})


sns.lmplot(x="mem", y="watt", data=data)

plt.show()
