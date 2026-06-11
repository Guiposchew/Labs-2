import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit 


#functions
def line(x, a, b):
    return a*x+b

def tan_phase_shift(omega, R):
    return ((omega**2)*L*C - 1)/((omega * C)*R)


#data import
data_1 = pd.read_excel('Data.xlsx', sheet_name='RLC')
data_2 = pd.read_excel('Data.xlsx', sheet_name='RL')
data_3 = pd.read_excel('Data.xlsx', sheet_name='RC')
data_4 = pd.read_excel('Data.xlsx', sheet_name='things')

data_RLC = data_1.to_numpy()
data_RL = data_2.to_numpy()
data_RC = data_3.to_numpy()
data_m = data_4.to_numpy()


#asserting variables
L , C , R_c, R_r = data_m[0,0]*1e-3, data_m[0,1]*1e-6, data_m[0,2], data_m[0,3]
f_RLC, dt_RLC, rs_f = data_RLC[:,0]*1e3 , data_RLC[:,1]*1e-6,  data_RLC[0,3]*1e3
f_RL, dt_RL= data_RL[:,0]*1e3 , data_RL[:,1]*1e-6
f_RC, dt_RC = data_RC[:,0]*1e3 , data_RC[:,1]*1e-6


#calculating the phase shift and omega
omega_RC = 2*np.pi*f_RC
phi_RC = omega_RC*dt_RC

omega_RLC = 2*np.pi*f_RLC
phi_RLC = omega_RLC*dt_RLC

omega_RL = 2*np.pi*f_RL
phi_RL = omega_RL*dt_RL


#fitting a line around the resonance frequency
mask1 = (f_RLC < 3000)&(f_RLC > 2000)

p,c = curve_fit(line, f_RLC[mask1] , phi_RLC[mask1])

x = np.arange(min(f_RLC), max(f_RLC), 100)
fit1 = line(x, *p)

rs_f_fit = -p[1]/p[0] #calculated resonance frequency


#finding the inductance

L_fit_RLC = 1/(C*((2*np.pi*rs_f_fit)**2))

L_fit_RL = np.mean(np.tan(phi_RL)*(R_r/omega_RL))

print(f'{L_fit_RL*1e3}, {L_fit_RLC*1e3}, mH')

#resistance RC circuit
R_RC = 1/(np.tan(np.abs(phi_RC))*omega_RC*C)

#Curve fitting for RLC circuit

p2,_ = curve_fit(tan_phase_shift, omega_RLC, np.tan(phi_RLC), p0 = [1])

fit2 = tan_phase_shift(x, *p2)

plt.figure(1)
plt.title('Phase shift of different circuits')
plt.xlim((0.5,10))
plt.xlabel('Frequency [kHz]')
plt.ylabel('Phase shift [rad]')
plt.grid(True)

plt.plot(f_RLC*1e-3, phi_RLC, '--', label='RLC circuit')
plt.plot(f_RL*1e-3, phi_RL, '--', label='RL circuit')
plt.plot(f_RC*1e-3, phi_RC, '--', label='RC circuit')

plt.legend(loc = 'upper right')


plt.figure(2)
plt.title('RLC Circuit fit around the resonace frequency')
plt.xlabel('Frequency [kHz]')
plt.ylabel('Phase shift [rad]')
plt.grid(True)

plt.plot(f_RLC*1e-3, phi_RLC, '.', label='Measured data')
plt.plot(x*1e-3, fit1, '-' , label = f'Fit around the resonace frequency:\n y = {"%.3f"%(p[0]*1e3)}x + {"%.3f"%(p[1])}')

plt.legend(loc = 'upper right')

plt.figure(3)

plt.xlabel('Frequency [kHz]')
plt.ylabel('Resistance [Ohms]')
plt.title('RLC circuit')
plt.grid(True)

#plt.plot(phi_RC*1e-3, R_RC, '.' ,label='Calculated resistance')
plt.plot(f_RLC*1e-3, np.tan(phi_RLC), '.')
plt.plot(x*1e-3, fit2, '-' ,label='fit')

print(np.tan(phi_RLC),fit2)

plt.show()

