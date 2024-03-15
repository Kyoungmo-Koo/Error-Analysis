import os
csv_file = "data_5020.csv"
txt_file = "raster_hexadecimal_5020.txt"

import csv
file_length = 5020
cutoff = 2

# Example function to read CSV data from a file
def read_csv(file_path):
    with open(file_path, newline='') as csvfile:
        # Create a CSV reader object
        csv_reader = csv.reader(csvfile)
        # Read the CSV data into a 2D list (buffer)
        buffer = [[int(item) for item in row[0:2 * file_length]] for row in csv_reader]
    return buffer

def read_txt(file_path):
    with open(file_path, 'r') as file:
        integers = []
        for line in file:
            # Remove newline and other potential trailing characters
            clean_line = line.strip()
            # Split the line into two parts and convert each to an integer
            first_part = int(clean_line[0:4], 16)
            second_part = int(clean_line[4:8], 16)
            # Add the converted integers to the list
            integers.extend([first_part, second_part])
        return integers
        
actual_data = read_csv(csv_file)[cutoff :]
target_data = read_txt(txt_file)

print("Actual data : Number of rows(trials): ", len(actual_data))
print("Actual data : Number of columns(positions per trial): ", len(actual_data[0]))
print("Target data : Number of positions(positions per trial): ", len(target_data))

actual_data_deg = [[(value - 32768) * 15 / 32768 for value in sublist] for sublist in actual_data]
target_data_deg = [(value - 32768) * 15 / 32768 for value in target_data]
actual_data_deg_x = [[row[i] for i in range(len(row)) if i % 2 == 0] for row in actual_data_deg]
actual_data_deg_y = [[row[i] for i in range(len(row)) if i % 2 != 0] for row in actual_data_deg]
target_data_deg_x = [target_data_deg[i] for i in range(len(target_data_deg)) if i % 2 == 0]
target_data_deg_y = [target_data_deg[i] for i in range(len(target_data_deg)) if i % 2 != 0]

print(len(actual_data_deg_x[0]))
print(len(actual_data_deg_y[0]))
print(len(target_data_deg_x))
print(len(target_data_deg_y))

def subtract_lists(Actual_data, Target_data):
    result = []
    for row in Actual_data :
        # Subtract the corresponding element in list_1d from each element in the row
        result_row = [row_element - Target_data[i] for i, row_element in enumerate(row)]
        result.append(result_row)
    return result

def calculate_rms(buffer):
    rms_values = []
    for row in buffer:
        # Calculate the mean of the squares of the elements in the row
        mean_of_squares = sum(x**2 for x in row) / len(row)
        # Take the square root of the mean of squares to get the RMS
        rms = math.sqrt(mean_of_squares)
        rms_values.append(rms)
    return rms_values

def calculate_mean_abs(buffer):
    mean_abs_values = []
    for row in buffer:
        # Calculate the mean of the absolute values of the elements in the row
        mean_abs = sum(abs(x) for x in row) / len(row)
        mean_abs_values.append(mean_abs)
    return mean_abs_values

def calculate_max_abs(buffer):
    max_abs_values = []
    for row in buffer:
        # Find the maximum absolute value in the row
        max_abs = max(abs(x) for x in row)
        max_abs_values.append(max_abs)
    return max_abs_values

import math
import numpy as np
time_shift_x = 8
time_shift_y = 8
actual_data_deg_x_shift = [row[time_shift_x:] for row in actual_data_deg_x]
actual_data_deg_y_shift = [row[time_shift_y:] for row in actual_data_deg_y]

target_data_deg_x_shift = target_data_deg_x[0:-time_shift_x]
target_data_deg_y_shift = target_data_deg_y[0:-time_shift_y]

error_data_deg_x = subtract_lists(actual_data_deg_x_shift, target_data_deg_x_shift)
error_data_deg_y = subtract_lists(actual_data_deg_y_shift, target_data_deg_y_shift)

error_data_deg_x_rms = calculate_rms(error_data_deg_x)
error_data_deg_x_mean_abs = calculate_mean_abs(error_data_deg_x)
error_data_deg_x_max_abs = calculate_max_abs(error_data_deg_x)

error_data_deg_y_rms = calculate_rms(error_data_deg_y)
error_data_deg_y_mean_abs = calculate_mean_abs(error_data_deg_y)
error_data_deg_y_max_abs = calculate_max_abs(error_data_deg_y)

print(np.mean(error_data_deg_x_mean_abs))
print(np.mean(error_data_deg_y_mean_abs))
print(np.mean(error_data_deg_x_max_abs))
print(np.mean(error_data_deg_y_max_abs))

error_data_deg_x = subtract_lists(actual_data_deg_x, target_data_deg_x)
error_data_deg_y = subtract_lists(actual_data_deg_y, target_data_deg_y)

error_data_deg_x_rms = calculate_rms(error_data_deg_x)
error_data_deg_x_mean_abs = calculate_mean_abs(error_data_deg_x)
error_data_deg_x_max_abs = calculate_max_abs(error_data_deg_x)

error_data_deg_y_rms = calculate_rms(error_data_deg_y)
error_data_deg_y_mean_abs = calculate_mean_abs(error_data_deg_y)
error_data_deg_y_max_abs = calculate_max_abs(error_data_deg_y)

print(np.mean(error_data_deg_x_mean_abs))
print(np.mean(error_data_deg_y_mean_abs))
print(np.mean(error_data_deg_x_max_abs))
print(np.mean(error_data_deg_y_max_abs))

import matplotlib.pyplot as plt

freq = 48000
trial_num = 10
error_data_deg_x = subtract_lists(actual_data_deg_x_shift, target_data_deg_x_shift)
error_data_deg_y = subtract_lists(actual_data_deg_y_shift, target_data_deg_y_shift)
#t_values = [1000/freq * i for i in range(len(error_data_deg_x[trial_num]))]
t_values = [1000/freq * i for i in range(420)]

plt.figure(figsize = (10, 6))
#plt.plot(t_values, error_data_deg_y[trial_num], marker = 'o')
plt.plot(t_values, error_data_deg_y[trial_num][80:500], marker = 'o')

np.mean(error_data_deg_y[trial_num])
len(error_data_deg_y[trial_num])
len(result_buffer)


# Parameters
period = 500
amplitude = 0.055
offset = 0.016
buffer_size = len(error_data_deg_y[trial_num])  # Adjust the size as needed

# Generate buffer with sinusoidal pattern
buffer = [amplitude * math.sin(2 * math.pi * i / period) for i in range(buffer_size)]
result_buffer = [x + y for x, y in zip(buffer, error_data_deg_y[trial_num])]

t_values = [1000/freq * i for i in range(len(error_data_deg_y[trial_num]))]

plt.figure(figsize = (10, 6))
plt.plot(t_values, result_buffer, marker = 'o')

for i in range(len(error_data_deg_y[trial_num])):
    error_data_deg_y[trial_num][i] -= 0.016
np.mean(np.absolute(error_data_deg_y[trial_num]))
