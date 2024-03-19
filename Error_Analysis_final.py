import os
import csv
import math
import numpy as np
import matplotlib.pyplot as plt

def read_csv(file_path):
    with open(file_path, newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        buffer = [[int(item) for item in row[0:2 * file_length]] for row in csv_reader]
    return buffer

def read_txt(file_path):
    with open(file_path, 'r') as file:
        integers = []
        for line in file:
            clean_line = line.strip()
            first_part = int(clean_line[0:4], 16)
            second_part = int(clean_line[4:8], 16)
            integers.extend([first_part, second_part])
        return integers

def subtract_lists(Actual_data, Target_data):
    result = []
    for row in Actual_data :
        result_row = [row_element - Target_data[i] for i, row_element in enumerate(row)]
        result.append(result_row)
    return result

def calculate_rms(buffer):
    rms_values = []
    for row in buffer:
        mean_of_squares = sum(x**2 for x in row) / len(row)
        rms = math.sqrt(mean_of_squares)
        rms_values.append(rms)
    return rms_values

def calculate_mean_abs(buffer):
    mean_abs_values = []
    for row in buffer:
        mean_abs = sum(abs(x) for x in row) / len(row)
        mean_abs_values.append(mean_abs)
    return mean_abs_values

def calculate_max_abs(buffer):
    max_abs_values = []
    for row in buffer:
        max_abs = max(abs(x) for x in row)
        max_abs_values.append(max_abs)
    return max_abs_values

csv_file = "data_5020_half_32k.csv"
txt_file = "raster_hexadecimal_5020_half.txt"
file_length = 5020
cutoff = 2

actual_data = read_csv(csv_file)[cutoff :]
target_data = read_txt(txt_file)

actual_data = [[(value - 32768) * 15 / 32768 for value in sublist] for sublist in actual_data]
target_data = [(value - 32768) * 15 / 32768 for value in target_data]
actual_data_x = [[row[i] for i in range(len(row)) if i % 2 == 0] for row in actual_data]
actual_data_y = [[row[i] for i in range(len(row)) if i % 2 != 0] for row in actual_data]
target_data_x = [target_data[i] for i in range(len(target_data)) if i % 2 == 0]
target_data_y = [target_data[i] for i in range(len(target_data)) if i % 2 != 0]

def Time_Shift_Error_Print(actual_data_x, actual_data_y, target_data_x, target_data_y, time_shift):
    actual_data_x_shift = [row[time_shift:] for row in actual_data_x]
    actual_data_y_shift = [row[time_shift:] for row in actual_data_y]

    target_data_x_shift = target_data_x[0:-time_shift]
    target_data_y_shift = target_data_y[0:-time_shift]

    error_data_x_shift = subtract_lists(actual_data_x_shift, target_data_x_shift)
    error_data_y_shift = subtract_lists(actual_data_y_shift, target_data_y_shift)

    error_data_x_rms_shift = calculate_rms(error_data_x_shift)
    error_data_x_mean_abs_shift = calculate_mean_abs(error_data_x_shift)
    error_data_x_max_abs_shift = calculate_max_abs(error_data_x_shift)

    error_data_y_rms_shift = calculate_rms(error_data_y_shift)
    error_data_y_mean_abs_shift = calculate_mean_abs(error_data_y_shift)
    error_data_y_max_abs_shift = calculate_max_abs(error_data_y_shift)
    
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

#Error_Of_Shifts_Print(error_of_shifts)

def Error_in_time_domain(actual_data_x, actual_data_y, target_data_x, target_data_y, time_shift, trial_num, freq, start, data_num):
    actual_data_x_shift = [row[time_shift:] for row in actual_data_x]
    actual_data_y_shift = [row[time_shift:] for row in actual_data_y]

    target_data_x_shift = target_data_x[0:-time_shift]
    target_data_y_shift = target_data_y[0:-time_shift]

    error_data_x_shift = subtract_lists(actual_data_x_shift, target_data_x_shift)
    error_data_y_shift = subtract_lists(actual_data_y_shift, target_data_y_shift)
    
    t_values = [1/freq * i for i in range(data_num)]
    plt.figure(figsize = (5, 3))
    plt.plot(t_values, actual_data_x_shift[trial_num][start : start + data_num], marker = 'o', markersize = 0.1)
    plt.plot(t_values, target_data_x[start: start + data_num], marker = 'o', markersize = 0.1)

    plt.figure(figsize = (5, 3))
    plt.plot(t_values, actual_data_y_shift[trial_num][start : start + data_num], marker = 'o', markersize = 0.1)
    plt.plot(t_values, target_data_y[start: start + data_num], marker = 'o', markersize = 0.1)    
    
    plt.figure(figsize = (5, 3))
    plt.plot(t_values, error_data_x_shift[trial_num][start: start + data_num], marker = 'o', markersize = 0.1)

    plt.figure(figsize = (5, 3))
    plt.plot(t_values, error_data_y_shift[trial_num][start: start + data_num], marker = 'o', markersize = 0.1)

#Error_in_time_domain(actual_data_x, actual_data_y, target_data_x, target_data_y, 6, 10, 48, 0, 500)
