import pandas as pd
import numpy as np
import numpy.fft as nf
import matplotlib.pyplot as plt
import scipy.signal as sp
from scipy.ndimage import gaussian_filter1d
from collections import defaultdict

#New camera
pixel_width = 14e-6

#Used functions
def label_m(arr):
    arr = np.asarray(arr)
    labels = np.zeros_like(arr, dtype=int)

    # Get indices of negative and non-negative values
    neg_indices = np.where(arr < 0)[0]
    pos_indices = np.where(arr >= 0)[0]

    # Sort each group by closeness to zero
    neg_sorted = neg_indices[np.argsort(np.abs(arr[neg_indices]))]
    pos_sorted = pos_indices[np.argsort(np.abs(arr[pos_indices]))]

    # Assign -1, -2, -3, ... to negatives
    for i, idx in enumerate(neg_sorted):
        labels[idx] = -(i + 1)

    # Assign 1, 2, 3, ... to positives
    for i, idx in enumerate(pos_sorted):
        labels[idx] = i + 1

    return labels.tolist()

def group_by_index(data):
    grouped = defaultdict(list)
    for item in data:
        a, b = item
        grouped[b].append(item)
    return dict(grouped)

#excel data
data0 = pd.read_excel('Data/meas.xlsx', sheet_name='Fraunhofer-Task1')
lamb = 636e-9
focal_length = data0['f (mm)'][0]*1e-3
LD_fh = data0['Lens distance (mm)'][0]*1e-3
SL_fh = data0['Slit distance camera (mm)'][0]*1e-3
b_exp = data0['slit width (mm)'][0]*1e-3

data0 = pd.read_excel('Data/meas.xlsx', sheet_name='Fresnel-Task1')
SL_fn = data0['Actual'].to_numpy()*1e-3

#data importing
data1 = pd.read_csv(f'Data/Task1/Fraunhofer/Task1-1.csv', sep=',', header=None)
id_Fh = data1[0].to_numpy()
Fh = data1[1].to_numpy()

Fn_list = []
id_list = []

for i in range(1,4):
    data1 = pd.read_csv(f'Data/Task1/Fresnel/Task1-{i}.csv', sep=',', header=None)
    index = data1[0].to_numpy()
    y = data1[1].to_numpy()
    Fn_list.append(y)
    id_list.append(index)

Fn = np.vstack(Fn_list)
id_Fn = np.vstack(id_list)
Fh -= np.min(Fh)

ind_dff_Fn =[]
for i in range(0,3):
    Fn[i] -= np.min(Fn[i])

    #noise filtering
    Fn[i] = gaussian_filter1d(Fn[i], sigma=1)

    #centering of the functions
    ind_dff = np.where(Fn[i] == max(Fn[i]))
    id_Fn[i] -= ind_dff[0]
    ind_dff_Fn.append(ind_dff[0][0])

#removing ambient light interference


#smoothing out noise
Fh = gaussian_filter1d(Fh, sigma=1)

#centralizing the function
ind_dff_Fh = np.where(Fh == max(Fh))[0]
id_Fh -= ind_dff_Fh

#Minima of light intensity 
ind0_Fn,_ = sp.find_peaks(-Fn[0],distance=10)
minima0_Fn = Fn[0][ind0_Fn]
ind1_Fn,_ = sp.find_peaks(-Fn[1],distance=10)
minima1_Fn = Fn[1][ind1_Fn]
ind2_Fn,_ = sp.find_peaks(-Fn[2],distance=10)
minima2_Fn = Fn[2][ind2_Fn]

ind_Fh,_ = sp.find_peaks(-Fh,distance=10)
minima_Fh = Fh[ind_Fh]

minima_list = [minima0_Fn,minima1_Fn,minima2_Fn]
minima_ind_list = [ind0_Fn,ind1_Fn,ind2_Fn]

#calculations
a = []         # stores b1 values
weights = []   # stores weights

n = label_m(minima_Fh - ind_dff_Fh)

for i in range(len(minima_Fh)):
    order = n[i]

    delta_x = (minima_Fh[i] - ind_dff_Fh) * pixel_width
    b1 = (order * lamb * focal_length) / delta_x
    a.append(np.abs(b1))
    weights.append(1 / abs(order))  # weight based on order distance

a = np.array(a)
weights = np.array(weights)

b1_weighted_avg = np.sum(weights * a) / np.sum(weights)

b1 = b1_weighted_avg

b2_weighted_avg = []
for j in range(0, 3):
    n = label_m(minima_ind_list[j] - ind_dff_Fn[j])
    a = []
    weights = []

    for i in range(len(minima_ind_list[j])):
        delta_x = (minima_ind_list[j][i] - ind_dff_Fn[j]) * pixel_width
        order = n[i]
        if order == 0:
            continue  # skip center (not a minimum)

        b2 = (order * lamb * SL_fn[j]) / delta_x
        a.append(np.abs(b2))
        weights.append(1 / abs(order))  # or use 1 / (order**2) if preferred

    a = np.array(a)
    weights = np.array(weights)

    weighted_avg = np.sum(weights * a) / np.sum(weights)
    b2_weighted_avg.append(weighted_avg)

#calculated slit width for each distance
b2 = np.array(b2_weighted_avg)

slit_widths =[]

I_fft = np.fft.fft(Fh)
freqs = np.fft.fftfreq(len(Fh), d=pixel_width)  # spatial frequency (1/m)
fft_mag = np.abs(I_fft)

# Find central FFT peak
center_idx = np.argmax(fft_mag)
half_max = fft_mag[center_idx] / 2

# Find left and right indices where FFT falls below half max
left = center_idx
while left > 0 and fft_mag[left] > half_max:
    left -= 1

right = center_idx
while right < len(fft_mag) and fft_mag[right] > half_max:
    right += 1

# Frequency difference (FWHM)
delta_f = np.abs(freqs[right] - freqs[left])
b1_FFT = 1 / delta_f

print(b1_FFT)

print(b1,b2)



#plot
plt.figure(4)
plt.xlim(-2,2)
plt.title(f'Fn[j]ntensity of light in the Fraunhofer regime; D = {"%.2f"%(SL_fh*1e3)} mm')
plt.ylabel('Intensity')
plt.xlabel('Distance (mm)')
plt.plot(id_Fh*pixel_width*1e3, Fh, label='Ligh intensity')
plt.plot(id_Fh[ind_Fh]*pixel_width*1e3, minima_Fh, 'x', label = 'Detected minima')
plt.legend(loc='upper right')

for i in range(0,3):
    plt.figure(i)
    plt.title(f'Intensity of light in the Fresnel regime; D = {"%.2f"%(SL_fn[i]*1e3)} mm')
    plt.ylabel('Intensity')
    plt.xlabel('Distance (mm)')
    plt.xlim(-2,2)
    plt.plot(id_Fn[i]*pixel_width*1e3, Fn[i], label='Ligh intensity')
    plt.plot(id_Fn[i][minima_ind_list[i]]*pixel_width*1e3, minima_list[i], 'x', label = 'Detected minima')
    plt.legend(loc='upper right')

plt.show()