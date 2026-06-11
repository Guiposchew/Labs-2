import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

lamb = 546.1e-9

def angle_rad(x):
    return np.array((x['Angle']+ x['Minutes']/60 + x['Seconds']/3600)*np.pi/180)

data1 = pd.read_excel('O12.xlsx', sheet_name='Off_set1')
data2 = pd.read_excel('O12.xlsx', sheet_name='Task1')
data3 = pd.read_excel('O12.xlsx', sheet_name='Off_set2')
data4 = pd.read_excel('O12.xlsx', sheet_name='Doublet1')
data5 = pd.read_excel('O12.xlsx', sheet_name='Doublet2')
data6 = pd.read_excel('O12.xlsx', sheet_name='Doublet3')
data7 = pd.read_excel('O12.xlsx', sheet_name='Doublet4')
index = pd.read_excel('O12.xlsx', sheet_name='Task1')['Lines'].to_numpy()

offset1 = angle_rad(data1)
lines_t1 = angle_rad(data2)
offset2 = angle_rad(data3)

db1 = angle_rad(data4)
db2 = angle_rad(data5)
db3 = angle_rad(data6)
db4 = angle_rad(data7)

db = np.array([db1,db2,db3,db4])

alpha1 = (np.pi - lines_t1[0] + offset1)/2
beta1 = np.pi + offset1 - alpha1 - lines_t1

g = np.nan_to_num(index*lamb/(2*np.pi*(np.sin(alpha1)-np.sin(beta1))))

g = (np.sum(g)/3)*1e9

alpha2 = (np.pi - 70 + offset2)/2
beta2 = np.pi + offset1 - alpha1 - db

print(g*(np.sin(beta2)-np.sin(60/180*np.pi)))