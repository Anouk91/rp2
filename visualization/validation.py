
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error
import matplotlib.cm as cm

os.chdir('/Users/anoukboukema/Desktop/SaNE/rp2/git/rp2/data')

cpu_pack, cpu_vps, mem_hw = np.load('predict_paramaters.npy')
true_cpu_hn, true_cpu_hw, watt = np.load('true.npy')

x = np.concatenate(true_cpu_hw, mem_hw)

A = np.vstack([true_cpu_hw, np.ones(len(true_cpu_hw))]).T
#t = x[1].T
y = watt.T
print x.shape, A.shape
percentTT = 0.2*y.size
indices = np.random.permutation(A.shape[0])
training_id, test_id = indices[percentTT:], indices[:percentTT] #750

trainingx, testx = A[training_id,:], A[test_id,:]
trainingy, testy = y[training_id], y[test_id]
#trainingt, testt = t[training_id], t[test_id]
#print "training id x = ", training_id.shape, "test id x = ", test_id.shape

weights = np.linalg.lstsq(trainingx, trainingy)[0]
weights = weights.reshape(-1,1)
print "Coefficient \t= %.2f \nConstant \t= %.2f"%(weights[0], weights[1])
print weights
y_pred = np.dot(testx, weights)
#print trainingx.shape
mean = mean_squared_error(testy, y_pred, multioutput='raw_values')

print "mean squared error = ", float(mean)


cpu_hn = 0.49 * cpu_pack + 0.05734329*12
cpu_hw = 3.15 *(cpu_hn + cpu_vps) + 186.25
predict_power = 0.26553476 * cpu_hw + 3.07985209 * mem_hw + 90.97268386*12


mean = mean_squared_error(watt, predict_power, multioutput='raw_values')
print "mean squared error = ", float(mean)


#--- Making plot out of train data ---#

trainx = trainingx.T[0].reshape(-1, 1)
#traint = trainingt.T[0].reshape(-1, 1)
trainy = trainingy

regr = linear_model.LinearRegression()
regr.fit(trainx, trainy)
#print trainx.shape, trainy.shape
plt.scatter(trainx, trainy)#, c=trainingt, cmap = 'bwr')
plt.plot(trainx, regr.predict(trainx), color='blue', linewidth=3)

plt.xlabel('CPU (%)')
plt.ylabel('Power (W)')

plt.grid()
#plt.colorbar()

plt.show()



#plt.subplot(221)
#plt.scatter(cpu_hn, true_cpu_hn)
#plt.xlabel('cpu HN predict')
#plt.ylabel('cpu HN true')
##plt.title('CPU part 1')
#plt.grid()
#
#plt.subplot(222)
#plt.scatter(cpu_hw, true_cpu_hw)
#plt.xlabel('cpu HW predict')
#plt.ylabel('cpu HW true')
##plt.title('CPU part 2')
#plt.grid()
#
#plt.subplot(223)
#plt.scatter(predict_power, watt)
#plt.xlabel('power predict')
#plt.ylabel('power true')
##plt.title('power part 3')
#plt.grid()
#
#plt.subplot(224)
#plt.boxplot(cpu_pack)
#plt.show()



