import os
import csv
import math
import numpy as np
import matplotlib.pyplot as plt

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


csv_file = "data_5020_half_32k.csv"
txt_file = "raster_hexadecimal_5020_half.txt"
file_length = 5020
cutoff = 2

def Error_Analysis_Function (csv_file, txt_file, file_length, cutoff, time_shift_x, time_shift_y):
    actual_data = read_csv(csv_file)[cutoff :]
    target_data = read_txt(txt_file)

    actual_data_deg = [[(value - 32768) * 15 / 32768 for value in sublist] for sublist in actual_data]
    target_data_deg = [(value - 32768) * 15 / 32768 for value in target_data]
    actual_data_deg_x = [[row[i] for i in range(len(row)) if i % 2 == 0] for row in actual_data_deg]
    actual_data_deg_y = [[row[i] for i in range(len(row)) if i % 2 != 0] for row in actual_data_deg]
    target_data_deg_x = [target_data_deg[i] for i in range(len(target_data_deg)) if i % 2 == 0]
    target_data_deg_y = [target_data_deg[i] for i in range(len(target_data_deg)) if i % 2 != 0]

    actual_data_deg_x_shift = [row[time_shift_x:] for row in actual_data_deg_x]
    actual_data_deg_y_shift = [row[time_shift_y:] for row in actual_data_deg_y]

    target_data_deg_x_shift = target_data_deg_x[0:-time_shift_x]
    target_data_deg_y_shift = target_data_deg_y[0:-time_shift_y]

    error_data_deg_x_shift = subtract_lists(actual_data_deg_x_shift, target_data_deg_x_shift)
    error_data_deg_y_shift = subtract_lists(actual_data_deg_y_shift, target_data_deg_y_shift)

    error_data_deg_x_rms_shift = calculate_rms(error_data_deg_x_shift)
    error_data_deg_x_mean_abs_shift = calculate_mean_abs(error_data_deg_x_shift)
    error_data_deg_x_max_abs_shift = calculate_max_abs(error_data_deg_x_shift)

    error_data_deg_y_rms_shift = calculate_rms(error_data_deg_y_shift)
    error_data_deg_y_mean_abs_shift = calculate_mean_abs(error_data_deg_y_shift)
    error_data_deg_y_max_abs_shift = calculate_max_abs(error_data_deg_y_shift)

    error_data_deg_x = subtract_lists(actual_data_deg_x, target_data_deg_x)
    error_data_deg_y = subtract_lists(actual_data_deg_y, target_data_deg_y)

    error_data_deg_x_rms = calculate_rms(error_data_deg_x)
    error_data_deg_x_mean_abs = calculate_mean_abs(error_data_deg_x)
    error_data_deg_x_max_abs = calculate_max_abs(error_data_deg_x)

    error_data_deg_y_rms = calculate_rms(error_data_deg_y)
    error_data_deg_y_mean_abs = calculate_mean_abs(error_data_deg_y)
    error_data_deg_y_max_abs = calculate_max_abs(error_data_deg_y)
    print("Shift : ", time_shift_x, time_shift_y)
    print("Mean of every trial's X RMS : ", np.mean(error_data_deg_x_rms_shift), "Y RMS : ", np.mean(error_data_deg_y_rms_shift))
    print("Mean of every trial's X MAE : ", np.mean(error_data_deg_x_mean_abs_shift), "Y MAE : ", np.mean(error_data_deg_y_mean_abs_shift))
    print("Mean of every trial's X MME : ", np.mean(error_data_deg_x_max_abs_shift), "Y MME : ", np.mean(error_data_deg_y_max_abs_shift))
    
    return [np.mean(error_data_deg_x_rms_shift), np.mean(error_data_deg_x_mean_abs_shift), np.mean(error_data_deg_x_max_abs_shift), np.mean(error_data_deg_y_rms_shift), np.mean(error_data_deg_y_mean_abs_shift), np.mean(error_data_deg_y_max_abs_shift)]

error_of_shifts = []
for i in range(1, 15):
    error_of_shifts.append(Error_Analysis_Function(csv_file, txt_file, file_length, cutoff, i, i))

y_labels = ["X RMS", "X MAE", "X MME", "Y RMS", "Y MAE", "Y MME"]

for i in range(len(error_of_shifts[0])):
    element_values = [lst[i] for lst in error_of_shifts]
    plt.figure()
    plt.plot(range(len(element_values)), element_values, marker='o', linestyle='-')
    
    
    plt.xlabel('Index')
    plt.ylabel(y_labels[i])
    plt.title('{} of Each Shift'.format(y_labels[i]))

plt.show()

def Error_in_time_domain(csv_file, txt_file, file_length, cutoff, time_shift_x, time_shift_y, trial_num, freq):
    actual_data = read_csv(csv_file)[cutoff :]
    target_data = read_txt(txt_file)

    actual_data_deg = [[(value - 32768) * 15 / 32768 for value in sublist] for sublist in actual_data]
    target_data_deg = [(value - 32768) * 15 / 32768 for value in target_data]
    actual_data_deg_x = [[row[i] for i in range(len(row)) if i % 2 == 0] for row in actual_data_deg]
    actual_data_deg_y = [[row[i] for i in range(len(row)) if i % 2 != 0] for row in actual_data_deg]
    target_data_deg_x = [target_data_deg[i] for i in range(len(target_data_deg)) if i % 2 == 0]
    target_data_deg_y = [target_data_deg[i] for i in range(len(target_data_deg)) if i % 2 != 0]

    actual_data_deg_x_shift = [row[time_shift_x:] for row in actual_data_deg_x]
    actual_data_deg_y_shift = [row[time_shift_y:] for row in actual_data_deg_y]

    target_data_deg_x_shift = target_data_deg_x[0:-time_shift_x]
    target_data_deg_y_shift = target_data_deg_y[0:-time_shift_y]

    error_data_deg_x_shift = subtract_lists(actual_data_deg_x_shift, target_data_deg_x_shift)
    error_data_deg_y_shift = subtract_lists(actual_data_deg_y_shift, target_data_deg_y_shift)

    t_values = [1/freq * i for i in range(len(error_data_deg_y_shift[trial_num]))]
    #t_values = [1000/freq * i for i in range(420)]

    plt.figure(figsize = (5, 3))
    plt.plot(t_values, error_data_deg_x_shift[trial_num], marker = 'o', markersize = 0.1)
    #plt.plot(t_values, error_data_deg_y[trial_num][80:500], marker = 'o')

    plt.figure(figsize = (5, 3))
    plt.plot(t_values, error_data_deg_y_shift[trial_num], marker = 'o', markersize = 0.1)

Error_in_time_domain("data_5020.csv", "raster_hexadecimal_5020.txt", file_length, cutoff, 8, 8, 12, 48)

def txt_shift (read_file, write_file, shift):
    with open(read_file, 'r') as file:
        original_buffer = []
        buffer = []
        float_buffer = []
        for line in file:
            buffer.append(line)
            original_buffer.append(line)
    for _ in range(8):
        buffer.insert(0, buffer.pop())
    
    with open(write_file, "w") as file:
        for element in buffer:
            file.write(str(element))

txt_shift(txt_file, "shifted_5020.txt", 8)

def Plot_in_time_domain(csv_file, txt_file, file_length, cutoff, time_shift_x, time_shift_y, trial_num):
    actual_data = read_csv(csv_file)[cutoff :]
    target_data = read_txt(txt_file)

    actual_data_deg = [[(value - 32768) * 15 / 32768 for value in sublist] for sublist in actual_data]
    target_data_deg = [(value - 32768) * 15 / 32768 for value in target_data]
    actual_data_deg_x = [[row[i] for i in range(len(row)) if i % 2 == 0] for row in actual_data_deg]
    actual_data_deg_y = [[row[i] for i in range(len(row)) if i % 2 != 0] for row in actual_data_deg]
    target_data_deg_x = [target_data_deg[i] for i in range(len(target_data_deg)) if i % 2 == 0]
    target_data_deg_y = [target_data_deg[i] for i in range(len(target_data_deg)) if i % 2 != 0]
    
    actual_data_deg_x_shift = [row[time_shift_x:] for row in actual_data_deg_x]
    actual_data_deg_y_shift = [row[time_shift_y:] for row in actual_data_deg_y]

    target_data_deg_x_shift = target_data_deg_x[0:-time_shift_x]
    target_data_deg_y_shift = target_data_deg_y[0:-time_shift_y]
    
    t_values = [1/48 * i for i in range(len(actual_data_deg_y_shift[trial_num]))]
    plt.figure(figsize = (5, 3))
    plt.plot(t_values, actual_data_deg_x_shift[trial_num], label = 'Actual Data', marker = 'o', markersize = 0.1)
    plt.plot(t_values, target_data_deg_x_shift, label = 'Target Data', marker = 'x', markersize = 0.1)
    
    plt.xlabel('Time')
    plt.ylabel('Angle')
    plt.legend()

    plt.figure(figsize = (5, 3))
    plt.plot(t_values, actual_data_deg_y_shift[trial_num], label = 'Actual Data', marker = 'o', markersize = 0.1)
    plt.plot(t_values, target_data_deg_y_shift, label = 'Target Data', marker = 'x', markersize = 0.1)
    
    plt.xlabel('Time')
    plt.ylabel('Angle')
    plt.legend()
Plot_in_time_domain("data_5020.csv", "raster_hexadecimal_5020.txt", file_length, cutoff, 8, 8, 10)

def Plot_in_time_domain2(csv_file, txt_file, file_length, cutoff, trial_num, start, size, c):
    actual_data = read_csv(csv_file)[cutoff :]
    target_data = read_txt(txt_file)

    actual_data_deg = [[(value - 32768) * 15 / 32768 for value in sublist] for sublist in actual_data]
    target_data_deg = [(value - 32768) * 15 / 32768 for value in target_data]
    actual_data_deg_x = [[row[i] for i in range(len(row)) if i % 2 == 0] for row in actual_data_deg]
    actual_data_deg_y = [[row[i] for i in range(len(row)) if i % 2 != 0] for row in actual_data_deg]
    target_data_deg_x = [target_data_deg[i] for i in range(len(target_data_deg)) if i % 2 == 0]
    target_data_deg_y = [target_data_deg[i] for i in range(len(target_data_deg)) if i % 2 != 0]
    
    target_data_deg_x_float = []
    target_data_deg_y_float = []
    
    end = len(target_data_deg_x)
    target_data_deg_x_float.append(c * target_data_deg_x[0] + (1-c) * target_data_deg_x[end - 1])
    target_data_deg_y_float.append(c * target_data_deg_y[0] + (1-c) * target_data_deg_y[end - 1])
    for i in range(1, end):
        target_data_deg_x_float.append(c * target_data_deg_x[i] + (1-c) * target_data_deg_x[i - 1])
        target_data_deg_y_float.append(c * target_data_deg_y[i] + (1-c) * target_data_deg_y[i - 1])

    error_data_deg_x = subtract_lists(actual_data_deg_x, target_data_deg_x_float)
    error_data_deg_y = subtract_lists(actual_data_deg_y, target_data_deg_y_float)

    error_data_deg_x_rms = calculate_rms(error_data_deg_x)
    error_data_deg_x_mean_abs = calculate_mean_abs(error_data_deg_x)
    error_data_deg_x_max_abs = calculate_max_abs(error_data_deg_x)

    error_data_deg_y_rms = calculate_rms(error_data_deg_y)
    error_data_deg_y_mean_abs = calculate_mean_abs(error_data_deg_y)
    error_data_deg_y_max_abs = calculate_max_abs(error_data_deg_y)

    print("Mean of every trial's X RMS : ", np.mean(error_data_deg_x_rms), "Y RMS : ", np.mean(error_data_deg_y_rms))
    print("Mean of every trial's X MAE : ", np.mean(error_data_deg_x_mean_abs), "Y MAE : ", np.mean(error_data_deg_y_mean_abs))
    print("Mean of every trial's X MME : ", np.mean(error_data_deg_x_max_abs), "Y MME : ", np.mean(error_data_deg_y_max_abs))
    
    
    t_values = [1/48 * i for i in range(len(actual_data_deg_y[trial_num][start:start + size]))]
    plt.figure(figsize = (5, 3))
    plt.plot(t_values, actual_data_deg_x[trial_num][start:start + size], label = 'Actual Data', marker = 'o', markersize = 0.1)
    plt.plot(t_values, target_data_deg_x_float[start:start + size], label = 'Target Data', marker = 'x', markersize = 0.1)
    
    plt.xlabel('Time')
    plt.ylabel('Angle')
    plt.legend()

    plt.figure(figsize = (5, 3))
    plt.plot(t_values, actual_data_deg_y[trial_num][start:start + size], label = 'Actual Data', marker = 'o', markersize = 0.1)
    plt.plot(t_values, target_data_deg_y_float[start:start + size], label = 'Target Data', marker = 'x', markersize = 0.1)
    
    plt.xlabel('Time')
    plt.ylabel('Angle')
    plt.legend()
txt_shift("raster_hexadecimal_5020.txt", "shifted_5020.txt", 8)
Plot_in_time_domain2("data_5020.csv", "shifted_5020.txt", 5020, 2, 10, 3300, 10, 0.6)

def Error_Analysis_Function2 (csv_file, txt_file, file_length, cutoff):
    actual_data = read_csv(csv_file)[cutoff :]
    target_data = read_txt(txt_file)

    actual_data_deg = [[(value - 32768) * 15 / 32768 for value in sublist] for sublist in actual_data]
    target_data_deg = [(value - 32768) * 15 / 32768 for value in target_data]
    actual_data_deg_x = [[row[i] for i in range(len(row)) if i % 2 == 0] for row in actual_data_deg]
    actual_data_deg_y = [[row[i] for i in range(len(row)) if i % 2 != 0] for row in actual_data_deg]
    target_data_deg_x = [target_data_deg[i] for i in range(len(target_data_deg)) if i % 2 == 0]
    target_data_deg_y = [target_data_deg[i] for i in range(len(target_data_deg)) if i % 2 != 0]
     
    error_data_deg_x = subtract_lists(actual_data_deg_x, target_data_deg_x)
    error_data_deg_y = subtract_lists(actual_data_deg_y, target_data_deg_y)

    error_data_deg_x_rms = calculate_rms(error_data_deg_x)
    error_data_deg_x_mean_abs = calculate_mean_abs(error_data_deg_x)
    error_data_deg_x_max_abs = calculate_max_abs(error_data_deg_x)

    error_data_deg_y_rms = calculate_rms(error_data_deg_y)
    error_data_deg_y_mean_abs = calculate_mean_abs(error_data_deg_y)
    error_data_deg_y_max_abs = calculate_max_abs(error_data_deg_y)
 
    print("Mean of every trial's X RMS : ", np.mean(error_data_deg_x_rms), "Y RMS : ", np.mean(error_data_deg_y_rms))
    print("Mean of every trial's X MAE : ", np.mean(error_data_deg_x_mean_abs), "Y MAE : ", np.mean(error_data_deg_y_mean_abs))
    print("Mean of every trial's X MME : ", np.mean(error_data_deg_x_max_abs), "Y MME : ", np.mean(error_data_deg_y_max_abs))

txt_shift("raster_hexadecimal_5020.txt", "shifted_5020.txt", 8)
Error_Analysis_Function2("data_5020.csv", "shifted_5020.txt", 5020, 2)

