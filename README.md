**Error_Analysis_Final_Numpy.py** :
Put csv_file and txt_file. We would like to compare actual data of csv_file (position feedback from servo driver) and 
target data of txt_file (Scan pattern) to calculate the error and determine galvo delay in digital interface.

Time_Shift_Optimization generates the list that has error list which each error bundles correspond to time shift. 

Error bundle => (np.mean(error_data_x_rms_shift), np.mean(error_data_x_mean_abs_shift), np.mean(error_data_x_max_abs_shift), 
np.mean(error_data_y_rms_shift), np.mean(error_data_y_mean_abs_shift), np.mean(error_data_y_max_abs_shift)

Error_of_Shifts_Print -> plot each errors using matplotlib

Error_in_time_Domain -> plot graph and print errors in the case of float shifts

Rest of the code is for generating new txt file with optimized float shift



**Error_Analysis_Final.py**  : Same as Error_Analysis_Final_Numpy but without Numpy functions

**Digital_Interface_Error_Analysis.py** : Mainly used for fast check if the data is correct
1. Plot error in time domain for each trial
2. Plot RMS error in Trial domain
3. Plot absolute mean error in Trial domain
4. Plot max error in Trial domain

**Digital_Interface_Error_Analysis_Distance.py** : Used for distance-wise error between target and actual
Print distance error RMS, ABS mean, and Max
And check the percentage of error that is below the resolution limit
