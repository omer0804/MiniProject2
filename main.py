import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# I use python 3.13 and it have some problem with tkinter so I use this code to avoid it
# Set the Matplotlib backend to 'Agg' to avoid Tkinter issues
plt.switch_backend('Agg')

def calc_mean_erp(trial_points_path, ecog_data_path):
    # Load data
    trial_points = pd.read_csv(trial_points_path, header=None, names=['start', 'peak', 'finger'])
    ecog_data = pd.read_csv(ecog_data_path).squeeze() # Squeeze the data to a 1D array

    # Initialize matrix for brain signals
    fingers_erp_mean = np.zeros((5, 1201))

    for finger in range(1, 6):
        # Extract starting time for each finger
        finger_trials = trial_points[trial_points["finger"] == finger]["start"].values
        finger_data = []

        for start in finger_trials:
            # Ensure indices are within bounds
            start_idx = int(start - 200)
            end_idx = int(start + 1001)
            if start_idx >= 0 and end_idx < len(ecog_data):
                finger_data.append(ecog_data[start_idx:end_idx].values) # Append the data to the list

        # Calculate the mean ERP for the finger if data is available
        if finger_data: # Check if the list is not empty
            fingers_erp_mean[finger - 1] = np.mean(finger_data, axis=0)

    # Plot average brain responses
    plot_mean_erp(fingers_erp_mean)

    return fingers_erp_mean

def plot_mean_erp(fingers_erp_mean):
    # Define time stamps for finger data
    time_axis = np.arange(-200, 1001)  

    plt.figure(figsize=(10, 6))
    for i in range(5):
        plt.plot(time_axis, fingers_erp_mean[i], label=f'Finger {i+1}')

    plt.legend() 
    plt.xlabel('Time (ms)')
    plt.ylabel('Brain Signal (µV)')
    plt.title('Averaged Brain Response by Finger')
    plt.grid(True)
    plt.savefig('Brain finger response.png')  # Save the plot to a file
    

# File paths
trial_points = 'C:/Users/USER/Desktop/Advanced Python Course/Mini_Project2/mini_project_2_data/events_file_ordered.csv'
ecog_data = 'C:/Users/USER/Desktop/Advanced Python Course/Mini_Project2/mini_project_2_data/brain_data_channel_one.csv'

# Run analysis
fingers_erp_mean = calc_mean_erp(trial_points, ecog_data)
