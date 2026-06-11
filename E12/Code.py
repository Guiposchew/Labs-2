import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit 

#Gaussian function
def Gauss(x, a, x0, sigma):
    return a * np.exp(-(x - x0)**2 / (2 * sigma**2))

#Constants
r1 = 220 #Ohms +- 5%
r2 = 10 #Ohms +- 5%
L = 1.5e-3 #Henry


#data import
data1_pd = pd.read_csv('Series_R1.csv')
data1 = data1_pd.to_numpy()

data2_pd = pd.read_csv('Series_R2.csv')
data2 = data2_pd.to_numpy()

datap_pd = pd.read_csv('Parallel_R1.csv')
datap = datap_pd.to_numpy()

A1 = data1[:,1].astype(float)
f_1 = data1[:,2].astype(float) 

A2 = data2[:,1].astype(float)
f_2 = data2[:,2].astype(float) 

Ap = datap[:,1].astype(float)
f_p = datap[:,2].astype(float)


#noise filtering
noise1 = A1 > 0.01
noise2 = A2 > 0.07
noisep = Ap > 0.01

A1 = A1[noise1]
A2 = A2[noise2]
Ap = Ap[noisep]
f_1 = f_1[noise1]
f_2 = f_2[noise2]
f_p = f_p[noisep]


#frequency range around f_r
low1 = f_1 >= 1600
high1 = f_1 <= 9000

f_1 = f_1[low1*high1]
A1 = A1[low1*high1]

low2 = f_2 >= 1600
high2 = f_2 <= 9000

f_2 = f_2[low2*high2]
A2 = A2[low2*high2]

#Calculations

#Curve fitting
mean1 = sum(f_1 * A1) / sum(A1)
sigma1 = np.sqrt(sum(A1 * (f_1 - mean1)**2) / sum(A1))

mean2 = sum(f_2 * A2) / sum(A2)
sigma2 = np.sqrt(sum(A2 * (f_2 - mean2)**2) / sum(A2))

popt1,pcov1 = curve_fit(Gauss, f_1, A1, p0=[max(A1), mean1, sigma1])
popt2,pcov2 = curve_fit(Gauss, f_2, A2, p0=[max(A2), mean2, sigma2])

fit1 = Gauss(f_1, *popt1)
fit2 = Gauss(f_2, *popt2)

#PLotting
plt.figure(1)
plt.xlabel('Frequency [kHz]')
plt.ylabel('Amplitude [mV]')

plt.plot(f_1/1000,A1*1000,'.', color='red', label = f'R1 = {r1} Ohms')
plt.plot(f_1/1000, fit1*1000, 'blue', label='fit')
plt.plot(f_2/1000,A2*1000,'.', color='red', label = f'R2 = {r2} Ohms')
plt.plot(f_2/1000, fit2*1000, 'blue', label='fit')
plt.legend(loc = 'upper left')

plt.figure(2)

plt.xlabel('Frequency [kHz]')
plt.ylabel('Amplitude [mV]')

plt.plot(f_p/1000,Ap*1000, '.', color = 'red', label = 'Parallel')

plt.show()

#finding the resonant frequency
f_r = (f_1[fit1 == fit1.max()] + f_2[fit2 == fit2.max()])*0.5

#Task 2
FWHM1 = 2*np.sqrt(2*np.log(2))*sigma1
delta1 = np.pi*FWHM1
Q1 = f_r/FWHM1

FWHM2 = 2*np.sqrt(2*np.log(2))*sigma2
delta2 = np.pi*FWHM2
Q2 = f_r/FWHM2

C = 1/(L*(4*(np.pi**2)*(f_r**2)))


print(f'd_1 = {delta1}, d_2 = {delta2} , q1 = {Q1}, q2 = {Q2}, FWHM1 = {FWHM1}, FWHM2 = {FWHM2}, f = {f_r/1000}kHz, C = {C*1e9} nF')