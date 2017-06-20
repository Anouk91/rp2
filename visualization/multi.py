
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from sklearn import datasets, linear_model #, mean_squared_error


os.chdir('/Users/anoukboukema/Desktop/SaNE/rp2/git/rp2/data')

cpu=np.load('mem_idle_sys_irq_usr.npy')


watt = np.load('y_watt.npy')


print cpu.size , watt.size


A = np.vstack([cpu  , np.ones(len(cpu[0]))]).T
a1, a2, a3, a4, a5, b= np.linalg.lstsq(A, watt)[0]


types = ['mem', 'cpu_idle', 'cpu_system', 'cpu_softirq', 'cpu_user']

mem = cpu[0]*a1 + b


print mem.size

