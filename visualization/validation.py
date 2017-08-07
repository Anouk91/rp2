
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error
import matplotlib.cm as cm

os.chdir('/Users/anoukboukema/Desktop/rp2/data')






#---part 3---#
#x = np.load('cpu_mem_hw.npy')
#y = np.load('power_hw.npy')

#---part 2---#
#x = np.load('cpu_vis.npy')
#y = np.load('cpu_hw.npy')

#---part 1---#
x = np.load('cpu_pack_concat.npy')
y = np.load('cpu_hn_concat.npy')

#---validating---#
#cpu_pack, cpu_vps, mem_hw = np.load('predict_paramaters.npy')
#true_cpu_hn, true_cpu_hw, watt = np.load('true.npy')
#x = cpu_pack
#y = true_cpu_hn

#--- Linear Regression on Train and mean squared error on Test ---#
A = np.vstack([x, np.ones(len(x))]).T
#t = x[1].T             #--part 3
y = y.T
print x.shape, A.shape
percentTT = 0.2*y.size
indices = np.random.permutation(A.shape[0])
training_id, test_id = indices[percentTT:], indices[:percentTT] #750

trainingx, testx = A[training_id,:], A[test_id,:]
trainingy, testy = y[training_id], y[test_id]
#trainingt, testt = t[training_id], t[test_id]  #--part 3
#print "training id x = ", training_id.shape, "test id x = ", test_id.shape

weights = np.linalg.lstsq(trainingx, trainingy)[0]
weights = weights.reshape(-1,1)
print "Coefficient \t= %.2f \nConstant \t= %.2f"%(weights[0], weights[1])
print weights
y_pred = np.dot(testx, weights)
#print trainingx.shape
meanTest = mean_squared_error(testy, y_pred, multioutput='raw_values')
print "mean squared error comparison plot = ", float(meanTest)
print testy.shape, trainingy.shape
meanTrain = mean_squared_error(trainingy, y_pred, multioutput='raw_values')
print "mean squared error comparison plot = ", float(meanTrain)


#--- Making plot out of train data ---#


trainx = trainingx.T[0].reshape(-1, 1)
#traint = trainingt.T[0].reshape(-1, 1)  #--part 3
trainy = trainingy

regr = linear_model.LinearRegression()
regr.fit(trainx, trainy)
print trainx.shape, trainy.shape
plt.scatter(trainx, trainy)
#plt.scatter(trainx, trainy, c=trainingt, cmap = 'bwr') #--part 3
plt.plot(trainx, regr.predict(trainx), linewidth=3, color="red")

#print trainingx.shape
meanTest = mean_squared_error(testy, y_pred, multioutput='raw_values')


##---part 3---#
#plt.xlabel('CPU Hardware Node (%)')
#plt.ylabel('Power Hardware Node (W)')
#plt.colorbar()  #--part 3
##
##--- part 2---#
#plt.xlabel('Virtualization (HN + VPS) (s)')
#plt.ylabel('Hardware Nodes (%)')
#
#less = 0
#more = 0
#for i in range(y.size):
#    if x[0][i] < 10:
# 
#        less += 1
#    else:
#        more += 1
#
#
#
#print less, more, float(less)/(float(less +more))
#plt.grid()
#plt.show()
##



#--- Calculating the Energy usage of a package---#
#packcpu, packmem = np.load('pack1.npy')
#packcpu = np.load('cpu_pack_concat.npy')
#packmem = np.load('cpu_pack_mem_concat.npy')
#pack10 = np.load('pack10.npy')
#pack20 = np.load('pack20.npy')#x = data[0]
#z = data[1]
#y = np.load('cpu_hn_concat.npy')
#cpu_average = np.average(packcpu)
#cpu_min = np.min(packcpu)
#cpu_max = np.max(packcpu)
#print "cpu average\t", cpu_average
#print "cpu min\t",cpu_min
#print "cpu max\t",cpu_max
##
#mem_average = np.average(packmem)/1000000  #
#mem_min = np.min(packmem)/1000000
#mem_max = np.max(packmem)/1000000
#print "mem average\t", mem_average
#print "mem min\t", mem_min
#print "mem max\t",mem_max
#
#power_min = 00.867663 * cpu_min + 3.30113 * mem_min +  (0.11*1118.6)/8162
#power_average = 0.867663 * cpu_average + 3.30113 * mem_average +  (0.11*1118.6)/8162
#power_max =0.867663 * cpu_max + 3.30113 * mem_max +  (0.11*1118.6)/8162
#
#print "power min\t", power_min
#print "power average\t", power_average
#print "power max\t", power_max

#
##---Validating final formula---#
#cpu_hn = 0.96935176 * cpu_pack +  0.05486263 * 48
#cpu_hw = 2.81565561 *(cpu_hn + cpu_vps) + 219.80571215
#predict_power = 0.31789973 * cpu_hw + 3.30112601 * mem_hw + 87.34456914 * 12


#mean = mean_squared_error(watt, predict_power, multioutput='raw_values')
#print "mean squared error pack to power = ", float(mean)




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
#plt.xlabel('Predicted Power (W)')
#plt.ylabel('Measured Power (W)')
#plt.axis('equal')
#plt.title('power part 3')
plt.grid()
###
###plt.subplot(224)
###plt.boxplot(cpu_pack)
plt.show()



