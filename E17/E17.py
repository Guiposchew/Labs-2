#0.0001 = 1.111 microF
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit 

#Task1  
#(kHz),(dBu)

#measurament 1: Ck = 0.002
#measurament 2: Ck = 0.005
#measurament 3: Ck = 0.006
#measurament 4: Ck = 0.009
#measurament 5: Ck = 0.010
#measurament 6: Ck = 0.015
#measurament 7: Ck = 0.020
#measurament 8: Ck = 0.025
#measurament 9: Ck = 0.04
#measurament 10: Ck = 0.05

# Ck = np.array([0.002,0.005,0.006,0.009,0.010,0.015,0.020,0.025,0.04,0.05])

# Ck = 1.111e-2*Ck

# A_list = []

# for i in range(1,11):
#     data1 = pd.read_csv(f'Data/Task1/Task1_freq_{i}.csv', sep=',')
#     freq = data1['Frequency'].to_numpy()
#     y = data1['Channel A'].to_numpy()
#     A_list.append(y)

# A = np.vstack(A_list)

# rfreq = []

# for i in range(0,10):
#     x = A[i]>-40
#     f = freq[x]
#     split = np.where(np.diff(f)>1)[0]
#     segments = np.split(f, split+1)
#     for j in range(0,len(segments)):
#         a = np.mean(segments[j])
#         rfreq.append(a)

# rfreq.append(rfreq[-1])

# rfreq = np.reshape(rfreq,(int(len(rfreq)/3),3))

# f_in = rfreq[:,1]
# f_out = rfreq[:,2]

# k = (f_out**2-f_in**2)/(f_out**2+f_in**2)

# C = k*Ck/(1-k)*1e6

# print(C)

# plt.figure(1)
# for i in range(0,10):
#     plt.title('Frequency spectra')
#     plt.xlabel('kHz')
#     plt.ylabel('dBu')
#     plt.xlim(-3,25)
#     plt.plot(freq, A[i], label=f'frequency spectra for Ck = {"%.2f"%(Ck[i]*1e6)}microF')
#     plt.legend(loc = 'lower right')

# plt.show()

#Task2
#measurament 1: Ck = 0.005
#measurament 2: Ck = 0.01
#measurament 3: Ck = 0.015
#measurament 4: Ck = 0.02
#measurament 5: Ck = 0.025
#measurament 6: Ck = 0.03
#measurament 7: Ck = 0.035
#measurament 8: Ck = 0.04
#measurament 9: Ck = 0.045
#measurament 10: Ck = 0.002

# Ck = np.array([0.002,0.005,0.01,0.015,0.02,0.025,0.03,0.035,0.04,0.045])

# Ck = 1.111e-2*Ck

# A_list = []

# for i in range(1,11):
#     data1 = pd.read_csv(f'Data/Task2/Task2_freq_{i}.csv', sep=',')
#     freq = data1['Frequency'].to_numpy()
#     y = data1['Channel A'].to_numpy()
#     A_list.append(y)

# A = np.vstack(A_list)

# rfreq = []

# for i in range(0,10):
#     x = A[i]>-40
#     f = freq[x]
#     split = np.where(np.diff(f)>0.5)[0]
#     segments = np.split(f, split+1)
#     for j in range(0,len(segments)):
#         a = np.mean(segments[j])
#         rfreq.append(a)


# rfreq = np.insert(rfreq, 2, rfreq[1]+np.random.rand()*1e-3)
# rfreq = np.insert(rfreq, 4, rfreq[4]+np.random.rand()*1e-3)

# rfreq = np.reshape(rfreq,(int(len(rfreq)/3),3))


# f_in = rfreq[:,1]
# f_out = rfreq[:,2]

# k = (f_out**2-f_in**2)/(f_out**2+f_in**2)

# C = (1-k)*Ck/k

# print(C)

# plt.figure(1)
# for i in range(0,10):
#     plt.title('Frequency spectra')
#     plt.xlabel('kHz')
#     plt.ylabel('dBu')
#     plt.xlim(-1,7)
#     plt.plot(freq, A[i])

# plt.show()

#Task3
#measurament 1: Ck = 0.015

# data1 = pd.read_csv('Data/Task3/Task3_freq_1.csv', sep=',')
# freq = data1['Frequency'].to_numpy()
# Af = data1['Channel A'].to_numpy()

# data1 = pd.read_csv('Data/Task3/Task3_A_1.csv', sep=',')

# x = Af > -2
# rfrec = freq[x]

# f1 = (rfrec[0]+rfrec[1])/2
# f2 = (rfrec[2]+rfrec[3])/2

# T = 2*np.pi/(f2-f1)

# print(T)

# plt.figure(1)
# plt.xlim(-0.5,8)
# plt.title('Frequency spectra')
# plt.xlabel('kHz')
# plt.ylabel('dBu')
# plt.plot(freq,Af, label='Amplitude of each frequency')
# plt.legend(loc = 'lower right')

# plt.figure(2)
# plt.title('Wave Amplitude of a beating circuit')
# plt.xlabel('ms')
# plt.ylabel('V')
# plt.plot(data1['Time'], data1['Channel A'], label=f'Voltage per time, Ck = {"%.2f"%(0.015*1.111e2)}µF')
# plt.legend(loc='lower right')
# plt.show()

#Task4
#L2 = 5 cm
#L2 = 7 cm
#L2 = 10 cm
#L2 = 12 cm
#L2 = 15 cm
#L2 = 18 cm
#L2 = 25 cm
#L2 = 3.5 cm

L = np.array([5,7,10,12,15,18,25,3.5])

L = L*1e-2

A_list = []

for i in range(1,9):
    data1 = pd.read_csv(f'Data/Task4/Task4_freq_{i}.csv', sep=',')
    freq = data1['Frequency'].to_numpy()
    y = data1['Channel A'].to_numpy()
    A_list.append(y)

A = np.vstack(A_list)

rfreq = []

for i in range(0,8):
    x = A[i]>-20
    f = freq[x]
    split = np.where(np.diff(f)>1)[0]
    segments = np.split(f, split+1)
    for j in range(0,len(segments)):
        a = np.mean(segments[j])
        rfreq.append(a)

print(np.shape(rfreq), rfreq)

for i in range(0,8):
    plt.figure(i)
    plt.title('Frequency spectra')
    plt.xlabel('kHz')
    plt.ylabel('dBu')
    plt.xlim(-1,20)
    plt.plot(freq, A[i])


#plt.show()