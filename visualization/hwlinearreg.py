
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import glob
from sklearn import datasets, linear_model

sns.set(style="whitegrid", color_codes=True)
os.chdir('/Users/anoukboukema/Desktop/SaNE/rp2/git/rp2/data')

#mem, cpu_idle, cpu_system, cpu_softirq, cpu_user =np.load('mem_idle_sys_irq_usr.npy')
#
#watt = np.load('y_watt.npy')

#cpu = cpu_softirq



#for i in range(0,cpu.size):
#    cpu[i] = 1600 - cpu[i]


#for i in range(0,cpu.size):
#    cpu[i] += cpu_user[i] + cpu_softirq[i]


#print cpu.size , watt.size


x = np.load('cpu_vis.npy')
y = np.load('cpu_hw.npy')

itterate = x

index = 0
deleted_values = 0
for i in range(0, len(itterate)):
    if itterate[i] < 50:
        print "deleted value ", x[index], i
        x = np.delete( x, index)
        y = np.delete( y, index)
        deleted_values += 1
    else:
        index += 1


# Create linear regression object
regr = linear_model.LinearRegression()

x = x.reshape(-1, 1)
# watt.reshape((940, 1))
print x.shape, y.shape
regr.fit(x, y)

# The coefficients
Coefficient = regr.coef_[0]
print "Coefficient = ", Coefficient



# Plot outputs
plt.scatter(x, y,  color='black')
plt.plot(x, regr.predict(x), color='blue', linewidth=3)

# plt.xticks(())
# plt.yticks(())
plt.xlabel('Visualization Layer (s)')
plt.ylabel('Hardware Layer (%)')
plt.title('CPU')
#data = pd.DataFrame({'cpu' : cpu, 'mem' : mem, 'watt' : watt})

#g = sns.FacetGrid()
#sns.lmplot(x="cpu", y="watt", data=data)

plt.show()
