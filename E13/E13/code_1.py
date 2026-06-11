import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit 

#note
#1st 1nF 1 kOhm
#2nd 1nF 100 Ohms
#3rd 1nF 22 kOhms
#4th 1nF 100 GOhms
#5th 220nF 1 kOhm

#description of each experiment
names = ['C = 1nF, R = 1 kΩ', 'C = 1nF, R = 100 Ω', 'C = 1nF, R = 22 kΩ','C = 1nF, R = 100 GΩ','C = 220nF, R = 1 kΩ']

#curve for fitting
def exp(x,A,b):
    return A*np.exp(x*b)

#data import
data1 = pd.read_csv('wave1.csv', sep=';')
V1 = data1['(V)'].to_numpy()
t1 = data1['(us)'].to_numpy()

data2 = pd.read_csv('wave2.csv', sep=';')
V2 = data2['(V)'].to_numpy()
t2 = data2['(us)'].to_numpy()

data3 = pd.read_csv('wave3.csv', sep=';')
V3 = data3['(V)'].to_numpy()
t3 = data3['(us)'].to_numpy()

data4 = pd.read_csv('wave4.csv', sep=';')
V4 = data4['(V)'].to_numpy()
t4 = data4['(us)'].to_numpy()

data5 = pd.read_csv('wave5.csv', sep=';')
V5 = data5['(V)'].to_numpy()
t5 = data5['(us)'].to_numpy()

#organizing the data 
V = np.array([V1,V2,V3,V4,V5])
t = np.array([t1,t2,t3,t4,t5])

#difference between each element of V
dV = np.diff(V)

V_ind = np.array([])
t_ind = np.array([])

for i in range(0,5):    
    #creating a mask aroun the voltage shift
    index_max_v = np.nonzero(dV[i] == max(dV[i]))[0]
    index_around_max = np.arange(index_max_v[0]-10, index_max_v[0]+20)

    V_ind = np.append(V_ind, [V[i][index_around_max]])
    t_ind = np.append(t_ind, [t[i][index_around_max]])

#reshaping the arrays
V_ind = V_ind.reshape(5,30)
t_ind = t_ind.reshape(5,30)

V_calc = np.array([])

popt = np.array([])

#calculating the fit for each experiment
for i in range(0,5):    
    x,_ = curve_fit(exp, t_ind[i] ,V_ind[i])
    popt = np.append(popt, x)
    V_calc = np.append(V_calc, exp(t_ind[i], x[0], x[1]))

#fit coeficients
popt = popt.reshape(5,2)

#reshaping the array
V_calc = V_calc.reshape(5,30)

#generating the graphs
for i in range(0,5):
    plt.figure(f'Fit {i+1}')
    plt.title(f'Voltage x Time \n {names[i]}')
    plt.xlabel('Time (µs)')
    plt.ylabel('Voltage (V)')

    plt.plot(t_ind[i], V_calc[i] , '-', label = f'Fit: y = {"%.2f"%(popt[i,0])}*exp({"%.2f"%(popt[i,1])}*x)')
    plt.plot(t_ind[i], V_ind[i], '--', label = 'Experimental data')
        
    plt.legend(loc = 'upper right')

for i in range(0,5):
    plt.figure(f'Measurement {i+1}')
    plt.title(f'Voltage x Time \n {names[i]}')
    plt.xlabel('Time (µs)')
    plt.ylabel('Voltage (V)')

    plt.plot(t_ind[i], V_ind[i], '--', label = 'Experimental data')
        
    plt.legend(loc = 'upper right')

plt.show()

