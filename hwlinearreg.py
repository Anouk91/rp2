
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="whitegrid", color_codes=True)

cpu, mem =np.load('x-as.npy')
watt = np.load('y-as.npy')
print cpu.size , mem.size, watt.size
# hn_itterate = list(hn_i)
# hn_vps = list(hn_i)
# hw = list(hw)
# length = len(list(hn_i))
# print "length before deletion = ", length
# deleted_values = 0
# x = 0
# for i in range(0, len(hn_itterate)):
#     if hn_itterate[i] < 50:
#         print "deleted value ", hn_vps[x], i
#         del hn_vps[x]
#         del hw[x]
#         deleted_values += 1
#     else:
#         x += 1

# print "length before deletion = ", len(hn_vps)
# print "deleted values ", deleted_values

# ========================
# Model for Original Data
# ========================
data = pd.DataFrame({'cpu' : hn_vps, 'watt' : hw})
# # create another data frame of log values
# data_log = np.log(data)
#
# # Get the linear models
# lm_original = np.polyfit(data.cpu, data.watt, 1)
#
# # calculate the y values based on the co-efficients from the model
# r_x, r_y = zip(*((i, i*lm_original[0] + lm_original[1]) for i in data.cpu))
#
# # Put in to a data frame, to keep is all nice
# lm_original_plot = pd.DataFrame({
# 'cpu' : r_x,
# 'watt' : r_y
# })
# print type(lm_original_plot)
# r_x, r_y = zip(*((i, i*lm_original[0] + lm_original[1]) for i in data.cpu))
#
# # ========================
# # Model for Log Data
# # ========================
#
# # Get the linear models
# lm_log = np.polyfit(data_log.cpu, data_log.watt, 1)
#
# # calculate the y values based on the co-efficients from the model
# r_x, r_y = zip(*((i, i*lm_log[0] + lm_log[1]) for i in data_log.cpu))
#
# # Put in to a data frame, to keep is all nice
# lm_log_plot = pd.DataFrame({
# 'cpu' : r_x,
# 'watt' : r_y
# })
#
# # ========================
# # Plot the data
# # ========================

sns.regplot(x="cpu", y="watt", data=data) # ,robust=True, ci=None, scatter_kws={"s": 80});
# fig, axes = plt.subplots(nrows=1)
#
# # Plot the original data and model
# data.plot(kind='scatter', color='Blue', x='cpu', y='watt', ax=axes[0], title='Original Values')
# lm_original_plot.plot(kind='line', color='Red', x='cpu', y='watt', ax=axes[0])

# # Plot the log transformed data and model
# data_log.plot(kind='scatter', color='Blue', x='cpu', y='watt', ax=axes[1], title='Log Values')
# lm_log_plot.plot(kind='line', color='Red', x='cpu', y='watt', ax=axes[1])

plt.show()
