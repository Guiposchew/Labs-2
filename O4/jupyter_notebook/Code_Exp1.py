import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

#data import and adjusting
data1_pd = pd.read_excel('Data.xlsx',sheet_name=0)
data1 = data1_pd.to_numpy()

data2_pd = pd.read_excel('Data.xlsx',sheet_name=1, header=1)
data2 = data2_pd.to_numpy()

#Task1

#getting the relevant values from the data
g_1 = data1[:,7]
b_1 = data1[:,9]
gamma = data1[:,6]
gamma_inv = 1/gamma

#Plot of 1/gamma vs g'
gT= np.array([])
gT = g_1.reshape((-1,1))

#fitting
model1 = LinearRegression().fit(gT,gamma_inv)

A1 = model1.coef_
B1 = model1.intercept_

# #PLotting
# plt.figure(1)
# plt.xlabel('Distance from the Object to A [mm]')
# plt.ylabel('Inverse of magnification')

# plt.plot(gT,gamma_inv,'.', color='red', label = 'Measured data')
# plt.plot(gT,model1.predict(gT),label = 'Linear fit')
# plt.legend(loc = 'lower right')
# plt.savefig('g_vs_1_mag.png')
# plt.show()

#Plot of gamma vs b'

bT = b_1.reshape((-1,1))

#fitting
model2 = LinearRegression().fit(bT,gamma)

A2 = model2.coef_
B2 = model2.intercept_

# #PLotting
# plt.figure(2)
# plt.xlabel('Distance from the Image to A [mm]')
# plt.ylabel('Magnification')

# plt.plot(bT,gamma,'.', color='red', label = 'Measured data')
# plt.plot(bT,model2.predict(bT),label = 'Linear fit')
# plt.legend(loc = 'lower right')
# plt.savefig('b_vs_mag.png')
# plt.show()

#Calculations
A_mean = (A1+A2)/2

F_sys = 1/A_mean

h = -B1*F_sys
h_p = -B2*F_sys

# print(h, h_p)

#Task2

#data
screen_pos_l1 = data2[:,1]
pos_l1_1 = data2[:,2]
pos_l1_2 = data2[:,3]

screen_pos_l2 = data2[:,6]
pos_l2_1 = data2[:,7]
pos_l2_2 = data2[:,8]

#calculations
a_l1 = pos_l1_2-pos_l1_1
a_l2 = pos_l2_2-pos_l2_1

f_l1 = (screen_pos_l1*screen_pos_l1 - a_l1*a_l1)/(4*screen_pos_l1)
f_l2 = (screen_pos_l2*screen_pos_l2 - a_l2*a_l2)/(4*screen_pos_l2)

#fitting
a_l1T = a_l1.reshape((-1,1))
model3 = LinearRegression().fit(a_l1T,f_l1)

a_l2T = a_l2.reshape((-1,1))
model4 = LinearRegression().fit(a_l2T,f_l2)

# #ploting
# plt.figure(3)
# plt.ylabel('Focal distance [mm]')
# plt.xlabel('Distance between two sharp images [mm]')
# plt.ylim([0,120])

# plt.plot(a_l1,f_l1,'.', color='red', label = 'Measured data')
# plt.plot(a_l1,model3.predict(a_l1T), label = 'Linear fit')
# plt.savefig('focal_length_1.png')

# #ploting
# plt.figure(4)
# plt.ylabel('Focal distance [mm]')
# plt.xlabel('Distance between two sharp images [mm]')
# plt.ylim([0,350])

# plt.plot(a_l2,f_l2,'.', color='red', label = 'Measured data')
# plt.plot(a_l2,model4.predict(a_l2T), label = 'Linear fit')
# plt.savefig('focal_length_2.png')


print(screen_pos_l2, f_l2*4)