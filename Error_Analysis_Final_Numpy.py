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

csv_file = "radial_0.5_32k.csv"
txt_file = "radial_hexadecimal_0.5.txt"
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

def Time_Shift_Error_Print(actual_data_x, actual_data_y, target_data_x, target_data_y, time_shift):
    actual_data_x_shift = actual_data_x[:, time_shift:]
    actual_data_y_shift = actual_data_y[:, time_shift:]
    target_data_x_shift = target_data_x[:-time_shift]
    target_data_y_shift = target_data_y[:-time_shift]

    error_data_x_shift = actual_data_x_shift - np.expand_dims(target_data_x_shift, axis=0)
    error_data_y_shift = actual_data_y_shift - np.expand_dims(target_data_y_shift, axis=0)

    error_data_x_rms_shift = np.sqrt(np.mean(error_data_x_shift**2, axis=1))
    error_data_x_mean_abs_shift = np.mean(np.abs(error_data_x_shift), axis=1)
    error_data_x_max_abs_shift = np.max(np.abs(error_data_x_shift), axis=1)

    error_data_y_rms_shift = np.sqrt(np.mean(error_data_y_shift**2, axis=1))
    error_data_y_mean_abs_shift = np.mean(np.abs(error_data_y_shift), axis=1)
    error_data_y_max_abs_shift = np.max(np.abs(error_data_y_shift), axis=1)
    
    print("Shift : ", time_shift)
    print("Mean of every trial's X RMS : ", np.mean(error_data_x_rms_shift), "Y RMS : ", np.mean(error_data_y_rms_shift))
    print("Mean of every trial's X MAE : ", np.mean(error_data_x_mean_abs_shift), "Y MAE : ", np.mean(error_data_y_mean_abs_shift))
    print("Mean of every trial's X MME : ", np.mean(error_data_x_max_abs_shift), "Y MME : ", np.mean(error_data_y_max_abs_shift))
    
    return [np.mean(error_data_x_rms_shift), np.mean(error_data_x_mean_abs_shift), np.mean(error_data_x_max_abs_shift), np.mean(error_data_y_rms_shift), np.mean(error_data_y_mean_abs_shift), np.mean(error_data_y_max_abs_shift)]

def Time_Shift_Optimization(actual_data_x, actual_data_y, target_data_x, target_data_y, time_shift_max):
    error_of_shifts = []
    for i in range(1, time_shift_max):
        error_of_shifts.append(Time_Shift_Error_Print(actual_data_x, actual_data_y, target_data_x, target_data_y, i))
    return error_of_shifts

#error_of_shifts = Time_Shift_Optimization(actual_data_x, actual_data_y, target_data_x, target_data_y, 15)

def Error_Of_Shifts_Print(error_of_shifts):
    y_labels = ["X RMS", "X MAE", "X MME", "Y RMS", "Y MAE", "Y MME"]

    for i in range(len(error_of_shifts[0])):
        element_values = [lst[i] for lst in error_of_shifts]
        plt.figure()
        plt.plot(range(len(element_values)), element_values, marker='o', linestyle='-')
    
    
        plt.xlabel('Index')
        plt.ylabel(y_labels[i])
        plt.title('{} of Each Shift'.format(y_labels[i]))

    plt.show()

Error_Of_Shifts_Print(error_of_shifts)

def arctan_function(theta, K):
    return 2 * np.degrees(np.arctan(K / (2 + K * np.tan(np.radians(np.abs(theta))))))

# Define the range of theta values (-15 degrees to 15 degrees)
theta_values = np.linspace(-15, 15, 1000)

# Define K value
K = 27 / 48000

# Calculate the function values
function_values = arctan_function(theta_values, K)

# Plot the graph
plt.plot(theta_values, function_values)
plt.title('Graph of arctan[K / (2 + K*tan(theta))]')
plt.xlabel('Theta (degrees)')
plt.ylabel('arctan[K / (2 + K*tan(theta))]')
plt.ylim(0.0322, 0.03223)
plt.grid(True)
plt.show()

def Float_Shift(row, time_shift, float_shift):
    new_row = np.zeros(len(row))
    for i in range(len(row)):
        left = i + time_shift
        right = i + time_shift + 1
        if(left > len(row) - 1):
            left = left - len(row)
        if(right > len(row) - 1):
            right = right - len(row)
        new_row[i] = row[left] * (1 - float_shift) + row[right] * float_shift
    return new_row

def Error_in_time_domain(actual_data_x, actual_data_y, target_data_x, target_data_y, time_shift, float_shift, trial_num, freq, start, data_num):
    actual_data_x_shift = [Float_Shift(row, time_shift, float_shift) for row in actual_data_x]
    actual_data_y_shift = [Float_Shift(row, time_shift, float_shift) for row in actual_data_y]

    target_data_x_shift = target_data_x
    target_data_y_shift = target_data_y

    error_data_x_shift = actual_data_x_shift - np.expand_dims(target_data_x_shift, axis=0)
    error_data_y_shift = actual_data_y_shift - np.expand_dims(target_data_y_shift, axis=0)

    error_data_x_rms_shift = np.sqrt(np.mean(error_data_x_shift**2, axis=1))
    error_data_x_mean_abs_shift = np.mean(np.abs(error_data_x_shift), axis=1)
    error_data_x_max_abs_shift = np.max(np.abs(error_data_x_shift), axis=1)

    error_data_y_rms_shift = np.sqrt(np.mean(error_data_y_shift**2, axis=1))
    error_data_y_mean_abs_shift = np.mean(np.abs(error_data_y_shift), axis=1)
    error_data_y_max_abs_shift = np.max(np.abs(error_data_y_shift), axis=1)
    
    print("Shift : ", time_shift)
    print("Mean of every trial's X RMS : ", np.mean(error_data_x_rms_shift), "Y RMS : ", np.mean(error_data_y_rms_shift))
    print("Mean of every trial's X MAE : ", np.mean(error_data_x_mean_abs_shift), "Y MAE : ", np.mean(error_data_y_mean_abs_shift))
    print("Mean of every trial's X MME : ", np.mean(error_data_x_max_abs_shift), "Y MME : ", np.mean(error_data_y_max_abs_shift))
    
    t_values = [1/freq * i for i in range(data_num)]
    
    fig, axs = plt.subplots(2, 2, figsize=(10, 6))
    

    axs[0, 0].plot(t_values, actual_data_x_shift[trial_num][start : start + data_num], marker = 'o', markersize = 0.1)
    axs[0, 0].plot(t_values, target_data_x[start: start + data_num], marker = 'o', markersize = 0.1)

    axs[0, 1].plot(t_values, actual_data_y_shift[trial_num][start : start + data_num], marker = 'o', markersize = 0.1)
    axs[0, 1].plot(t_values, target_data_y[start: start + data_num], marker = 'o', markersize = 0.1)    
 
    axs[1, 0].plot(t_values, error_data_x_shift[trial_num][start: start + data_num], marker = 'o', markersize = 0.1)
    axs[1, 0].axhline(y=0.0322, color='red')
    axs[1, 0].axhline(y=-0.0322, color='red') 

    axs[1, 1].plot(t_values, error_data_y_shift[trial_num][start: start + data_num], marker = 'o', markersize = 0.1)
    axs[1, 1].axhline(y=0.0322, color='red')
    axs[1, 1].axhline(y=-0.0322, color='red') 

Error_in_time_domain(actual_data_x, actual_data_y, target_data_x, target_data_y, 6, 0.6, 10, 48, 0, 5000)

target_data_x_new = Float_Shift(target_data_x, 6, 0.6)
target_data_y_new = Float_Shift(target_data_y, 6, 0.6)

hex_list1 = [format(int(32768 + num * 1/15 * 32768), 'X') for num in target_data_x_new]
hex_list2 = [format(int(32768 + num * 1/15 * 32768), 'X') for num in target_data_y_new]
target_data_new = [hex_list1[i] + hex_list2[i] for i in range(len(target_data_x_new))]

write_file = "new_radial_hexadecimal_0.5_32k.txt"
with open(write_file, "w") as file:
        for element in target_data_new:
            file.write(str(element) + "\n")
