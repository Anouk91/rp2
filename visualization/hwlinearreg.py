
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import glob
from sklearn import datasets, linear_model

sns.set(style="whitegrid", color_codes=True)
os.chdir('/Users/anoukboukema/Desktop/SaNE/rp2/git/rp2/data')

cpu=np.load('x_idle_sys_irq_usr.npy')
#cpu_idle, cpu_system, cpu_softirq, cpu_user =np.load('x_idle_sys_irq_usr.npy')

watt = np.load('y_watt.npy')

#cpu = cpu_system

print


#for i in range(0,cpu.size):
#    cpu[i] = 1600 - cpu[i]


#for i in range(0,cpu.size):
#    cpu[i] += cpu_user[i] + cpu_softirq[i]


print cpu.size , watt.size

weg = cpu[0].size -1

watt = np.delete(watt, weg)
for i in range(0,4):
    cpu[i] = np.delete(cpu[i], weg)
    print cpu[i]

A = np.vstack([cpu  , np.ones(len(cpu[0]))]).T
x= np.linalg.lstsq(A, watt)


print x
#
#
#print cpu.size , watt.size

#x = 0
#itterate = cpu
#for i in range(0, itterate.size):
#     #print itterate[i]
#     if itterate[i] > 2500:
#         print "deleted value ", itterate[i], " at index ", i, "current size: ", cpu.size
#         #mem = np.delete(mem, x)
#         watt = np.delete(watt, x)
#         cpu = np.delete(cpu, x)
#     else:
#         x += 1

## Create linear regression object
#regr = linear_model.LinearRegression()
#
#cpu = cpu.reshape(-1, 1)
## watt.reshape((940, 1))
#print cpu.shape, watt.shape
#regr.fit(cpu, watt)
#
## The coefficients
#Coefficient = regr.coef_[0]
#print "Coefficient = ", Coefficient
## # The mean squared error
##mean = np.mean((regr.predict(cpu.reshape(940, )) - watt) ** 2 #"Mean squared error: ",
## print mean
## # Explained variance score: 1 is perfect prediction
#print int(regr.score(cpu, watt)) #'Variance score: ' ,
#
## Plot outputs
#plt.scatter(cpu, watt,  color='black')
#plt.plot(cpu, regr.predict(cpu), color='blue', linewidth=3)
#
## plt.xticks(())
## plt.yticks(())
#plt.xlabel('CPU')
#plt.ylabel('Watt')
##data = pd.DataFrame({'cpu' : cpu, 'mem' : mem, 'watt' : watt})
#
##g = sns.FacetGrid()
##sns.lmplot(x="cpu", y="watt", data=data)
#
#plt.show()
