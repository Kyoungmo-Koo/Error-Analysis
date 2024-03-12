import os
import csv
import math
import matplotlib.pyplot as plt

csv_file = "data.csv"
txt_file = "raster_hexadecimal.txt"

# Example function to read CSV data from a file
def read_csv(file_path):
    with open(file_path, newline='') as csvfile:
        # Create a CSV reader object
        csv_reader = csv.reader(csvfile)
        # Read the CSV data into a 2D list (buffer)
        buffer = [[int(item) for item in row[0:10000]] for row in csv_reader]
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

        
actual_data = read_csv('data.csv')
target_data = read_txt('raster_hexadecimal.txt')

print("Actual data : Number of rows(trials): ", len(actual_data))
print("Actual data : Number of columns(positions per trial): ", len(actual_data[0]))
print("Target data : Number of positions(positions per trial): ", len(target_data))

error_data = subtract_lists(actual_data, target_data)

print("Error data : Number of rows(trials): ", len(error_data))
print("Error data : Number of columns(positions per trial): ", len(error_data[0]))

error_data_deg= [[value * 15 / 32768 for value in sublist] for sublist in error_data]
error_data_rms = calculate_rms(error_data_deg)
error_data_mean_abs = calculate_mean_abs(error_data_deg)
error_data_max_abs = calculate_max_abs(error_data_deg)

###################################PLOT####################################################################

Trial_num =99

# Generating X values. Nth data point's X value will be 0.02 * (N - 1)
x_values = [0.01 * i for i in range(len(error_data_deg[Trial_num]))]

# Creating the plot
plt.figure(figsize=(10, 6))
plt.plot(x_values, error_data_deg[Trial_num], marker='o')

# Setting the title and labels
plt.title("Plot of the trial " + str(Trial_num))
plt.xlabel("X axis ms")
plt.ylabel("Y axis degree")

#plt.ylim(-65535, 65535)

# Showing the plot
plt.grid(True)
plt.show()

###########################################################################################

# Creating the plot
plt.figure(figsize=(10, 6))
plt.plot(error_data_rms[2:100], marker='o')  # Plotting the values with circle markers

# Setting the title and labels
plt.title("Plot of the Error RMS of each trial")
plt.xlabel("Trial number")
plt.ylabel("Error RMS")
plt. ylim(0, 1)

# Showing the plot with grid
plt.grid(True)
plt.show()

###########################################################################################

# Creating the plot
plt.figure(figsize=(10, 6))
plt.plot(error_data_mean_abs[2:100], marker='o')  # Plotting the values with circle markers

# Setting the title and labels
plt.title("Plot of the Error Mean Absolute of each trial")
plt.xlabel("Trial number")
plt.ylabel("Error Mean Absolute")
plt. ylim(0, 1)

# Showing the plot with grid
plt.grid(True)
plt.show()

############################################################################################

# Creating the plot
plt.figure(figsize=(10, 6))
plt.plot(error_data_max_abs[2:100], marker='o')  # Plotting the values with circle markers

# Setting the title and labels
plt.title("Plot of the Error Max Absolute of each trial")
plt.xlabel("Trial number")
plt.ylabel("Error Max Absolute")
plt. ylim(0, 3)

# Showing the plot with grid
plt.grid(True)
plt.show()
