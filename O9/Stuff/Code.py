import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
#note measured distance for task1 starts at the 10th ring

#Data import
data1_pd = pd.read_excel('Data.xlsx', sheet_name='Task1')
data1 = data1_pd.to_numpy()

data2_pd = pd.read_excel('Data.xlsx', sheet_name='Task2')
data2 = data2_pd.to_numpy()

##Task1
#distance of the dark rings
d = data1[:,1].astype(float)*1e-3

#did not use all of the measurements
dr = np.flip(d[0:10]) 
dl = d[10:20]

d = (dl-dr)/2

print(d)

index = np.arange(10,20)
index_T = index.reshape((-1,1))

#wavelength of the light
lamb = data1[2,6]*1e-9

#calculations
d2 = d**2

#linear regression results

model1 = LinearRegression().fit(index_T,d2)

A1 = model1.coef_[0]
B1 = model1.intercept_

#calculated results
R = A1/lamb
d0 = -lamb/4 -B1/(2*R)

#float formating for the graph
A1_graph = "%.3f"%(A1*1e6)
B1_graph = "%.3f"%(B1*1e6)

#plotting
plt.figure(1)
plt.figure(1)
plt.xlabel('Ring number (#)')
plt.ylabel('r squared (mm²)')

plt.plot(index, d2*1e6, '.', color='red', label = 'experimental data')
plt.plot(index, model1.predict(index_T)*1e6, label = f'linear fit: y = {A1_graph}x+{B1_graph}')
plt.legend(loc = 'upper left')

##Task2
#distance of the dark lines

d_Al = data2[:,1]*1e-3
d_Hair = data2[:,2]*1e-3

I_Al = data2[1,4]*1e-2
I_Hair = data2[3,4]*1e-2

index2 = np.arange(0,10)
index2_T = index2.reshape((-1,1))

#linear fit
model2 = LinearRegression().fit(index2_T,d_Al)
model3 = LinearRegression().fit(index2_T,d_Hair)

#linear regression results
A2 = model2.coef_[0]
B2 = model2.intercept_

A3 = model3.coef_[0]
B3 = model3.intercept_

#calculations
D_Al = (I_Al*lamb)/(2*A2)
D_Hair = (I_Hair*lamb)/(2*A3)

#float formating for the graph
A2_graph = "%.3f"%(A2*1e3)
B2_graph = "%.3f"%(B2*1e3)

A3_graph = "%.3f"%(A3*1e3)
B3_graph = "%.3f"%(B3*1e3)


#plotting
plt.figure(2)
plt.xlabel('line number (#)')
plt.ylabel('line position (mm)')

plt.plot(index2, d_Al*1e3, '.', color='red', label = 'experimental data')
plt.plot(index2, model2.predict(index2_T)*1e3, label = f'linear fit: y = {A2_graph}x+{B2_graph}')
plt.legend(loc = 'upper left')


plt.figure(3)
plt.xlabel('line number (#)')
plt.ylabel('line position (mm)')

plt.plot(index2, d_Hair*1e3, '.', color='red', label = 'experimental data')
plt.plot(index2, model3.predict(index2_T)*1e3, label = f'linear fit: y = {A3_graph}x+{B3_graph}')
plt.legend(loc = 'upper left')

plt.show()

print(f'Task 1: R = {"%.3f"%(R)} m, d0 = {"%.3f"%(d0*1e6)} μm,\n Task 2: Thickness Aluminum foil: {"%.3f"%(D_Al*1e6)} μm, Thickness Hair: {"%.3f"%(D_Hair*1e6)} μm')
