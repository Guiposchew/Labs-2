import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def parabola(x,a,b,c):
    return a*(x**2)+b*x+c

data1 = pd.read_excel('O11.xlsx', sheet_name='Task1')

V_0 = data1['Voltage (V)']*1e3
V_30 = data1['Voltage (V).1']*1e3
V_45 = data1['Voltage (V).2']*1e3

D_Angle_0 = data1['Delta Angle (°)']
D_Angle_30 = data1['Delta Angle (°).1']
D_Angle_45 = data1['Delta Angle (°).2']

popt0,_ = curve_fit(parabola, D_Angle_0, V_0)
x0 = np.linspace(min(D_Angle_0),max(D_Angle_0),1000)
model0 = parabola(x0, *popt0)

popt30,_ = curve_fit(parabola, D_Angle_30, V_30)
x30 = np.linspace(min(D_Angle_30),max(D_Angle_30),1000)
model30 = parabola(x30, *popt30)

popt45,_ = curve_fit(parabola, D_Angle_45, V_45)
x45 = np.linspace(min(D_Angle_45),max(D_Angle_45),1000)
model45 = parabola(x45, *popt45)

plt.figure(1)
plt.title('Intensity per angle difference \n'r'$\theta_0$ = 0°')
plt.xlabel('Angle (°)')
plt.ylabel('Light intensity')
plt.plot(D_Angle_0,V_0, 'x', label = 'Measured intensity')
plt.plot(x0, model0, label = f'Fitted curve: y = {"%.3f"%popt0[0]}*x²+{"%.3f"%popt0[1]}*x+{"%.3f"%popt0[2]}')
plt.legend(loc = 'lower left')

plt.figure(2)
plt.title('Intensity per angle difference \n'r'$\theta_0$ = 30°')
plt.plot(D_Angle_30,V_30, 'x', label = 'Measured intensity')
plt.plot(x30, model30, label = f'Fitted curve: y = {"%.3f"%popt30[0]}*x²+{"%.3f"%popt30[1]}*x+{"%.3f"%popt30[2]}')
plt.legend(loc = 'lower left')

plt.figure(3)
plt.title('Intensity per angle difference \n'r'$\theta_0$ = 45°')
plt.plot(D_Angle_45,V_45, 'x', label = 'Measured intensity')
plt.plot(x45, model45, label = f'Fitted curve: y = {"%.3f"%popt45[0]}*x²+{"%.3f"%popt45[1]}*x+{"%.3f"%popt45[2]}')
plt.legend(loc = 'lower left')

plt.show()