
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error
import matplotlib.cm as cm

os.chdir('/Users/anoukboukema/Desktop/SaNE/rp2/git/rp2/data')

x= np.load('cpu_pack_all.npy')
y = np.load('cpu_hn_all.npy')
#t= x[1]
#cpu = data[1] + data[2] + data[3]
#data = np.vstack((data[0], cpu))


A = np.vstack([x, np.ones(len(x))]).T
t = x[1].T
y = y.T
print A.shape
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




#--- Test matrix and vectors ---#
#x = np.array([[0,1,2,3,4,5,],[10,11,12,13,14,15],[100,101,102,103,104,105]])
#A = np.vstack([x, np.ones(len(x[0]))]).T
#w = np.array([[2],[2],[2],[1]])
#y = np.array([[ 222, 225, 235, 240, 245, 250]]).T
#print A.shape, y.shape
#
#indices = np.random.permutation(A.shape[0])
#training_id, test_id = indices[:4], indices[4:]
#
##print indices , "\n"
#print "training id x = ", training_id, "test id x = ", test_id
##print "y shape", y.shape
#
#trainingx, testx = A[training_id,:], A[test_id,:]
#trainingy, testy = y[training_id], y[test_id]
#print 'train x \n',  trainingx, '\n test x \n', testx  , '\n train y \n',  trainingy, '\n test y \n', testy
##print x, x.shape, "\n"
#
##print w, w.shape
#y_pred = np.dot(testx,w)
##print dot.shape
#
#mean = mean_squared_error(testy, y_pred, multioutput='raw_values')
#print mean



#--- Making plot out of train data ---#

trainx = trainingx.T[0].reshape(-1, 1)
#traint = trainingt.T[0].reshape(-1, 1)
trainy = trainingy

regr = linear_model.LinearRegression()
regr.fit(trainx, trainy)
print trainx.shape, trainy.shape
plt.scatter(trainx, trainy)#, c=trainingt, cmap = 'bwr')
plt.plot(trainx, regr.predict(trainx), color='blue', linewidth=3)

plt.xlabel('CPU (%)')
plt.ylabel('Power (W)')

plt.grid()
#plt.colorbar()

plt.show()



