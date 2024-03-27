import os
import csv
import math
import numpy as np
import matplotlib.pyplot as plt

def read_txt(file_path):
    with open(file_path, 'r') as file:
        integers = []
        for line in file:
            clean_line = line.strip()
            first_part = int(clean_line[0:4], 16)
            second_part = int(clean_line[4:8], 16)
            integers.extend([first_part, second_part])
        return np.array(integers)

csv_file = "raster_0.5_32k_PID.csv"
txt_file = "raster_hexadecimal_0.5.txt"
cutoff = 2

actual_data = np.genfromtxt(csv_file, delimiter=',')[cutoff:]
target_data = read_txt(txt_file)

actual_data = (actual_data - 32768) * 15 / 32768
target_data = (target_data - 32768) * 15 / 32768
actual_data = actual_data[:, :-1]

actual_data_x = actual_data[:, ::2]
actual_data_y = actual_data[:, 1::2]
target_data_x = target_data[::2]
target_data_y = target_data[1::2]

print(actual_data_x.shape, actual_data_x[0][0])
print(actual_data_y.shape, actual_data_y[0][0])
print(target_data_x.shape, target_data_x[0])
print(target_data_y.shape, target_data_y[0])

error_data_x = actual_data_x - np.expand_dims(target_data_x, axis=0)
error_data_y = actual_data_y - np.expand_dims(target_data_y, axis=0)

error_data_x_rms = np.sqrt(np.mean(error_data_x**2, axis=1))
error_data_x_mean_abs = np.mean(np.abs(error_data_x), axis=1)
error_data_x_max_abs = np.max(np.abs(error_data_x), axis=1)

error_data_y_rms = np.sqrt(np.mean(error_data_y**2, axis=1))
error_data_y_mean_abs = np.mean(np.abs(error_data_y), axis=1)
error_data_y_max_abs = np.max(np.abs(error_data_y), axis=1)
 
print("Mean of every trial's X RMS : ", np.mean(error_data_x_rms), "Y RMS : ", np.mean(error_data_y_rms))
print("Mean of every trial's X MAE : ", np.mean(error_data_x_mean_abs), "Y MAE : ", np.mean(error_data_y_mean_abs))
print("Mean of every trial's X MME : ", np.mean(error_data_x_max_abs), "Y MME : ", np.mean(error_data_y_max_abs))

error_distance = np.sqrt(error_data_x**2 + error_data_y**2)
error_data_rms = np.sqrt(np.mean(error_distance**2, axis=1))
error_data_mean_abs = np.mean(np.abs(error_distance), axis=1)
error_data_max_abs = np.max(np.abs(error_distance), axis=1)
 
print("Mean of every trial's Error Distance RMS : ", np.mean(error_data_rms))
print("Mean of every trial's Error Distance MAE : ", np.mean(error_data_mean_abs))
print("Mean of every trial's Error Distance MME : ", np.mean(error_data_max_abs))

error_distance.shape

lesser_count = np.sum(error_distance < 0.0322)
lesser_count/(error_distance.shape[0] * error_distance.shape[1])

Trial = 30
t_values = [1/48 * i for i in range(len(error_distance[Trial]))]
plt.plot(t_values, error_distance[Trial])
plt.title('error distance according to time')
plt.axhline(y=0.0322, color='red') 
plt.xlabel('Time(ms)')
plt.ylabel('Error')
plt.grid(True)
plt.show()
