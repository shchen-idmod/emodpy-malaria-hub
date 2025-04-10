# This script is used to plot each channel for InsetChart.json for selected simulation.
# Drop this file under the result's job_directory/suite/experiment directory. 
# and replace the simulation id with your simulation id.

# Import necessary libraries
import json
import pandas as pd
import os
import sys
import matplotlib.pyplot as plt

# Load JSON data from file
# CURRENT_DIRECTORY is the result's path: job_directory/suite/experiment
CURRENT_DIRECTORY = os.path.dirname(__file__)  
if "params" not in globals():
    params = {
        "dataset": os.path.join(
            CURRENT_DIRECTORY,
            "994ead91-cd2b-4808-b162-d03743da7a68",  # replace with your simulation_id 
            "output",
            "InsetChart.json"
        )
    }
file = params["dataset"]
with open(params["dataset"]) as f:
    data = json.load(f)

# Convert JSON to a Pandas DataFrame
df = pd.json_normalize(data)

# Extract the header and channels
header = data['Header']
channels = data['Channels']

# Create a plot for each channel
for channel_name, channel_data in channels.items():
    # Extract the data and units
    units = channel_data['Units']
    values = channel_data['Data']
    
    # Create a time axis based on the number of timesteps
    timesteps = range(len(values))
    
    # Plot the data
    plt.figure(figsize=(10, 6))
    plt.plot(timesteps, values, label=channel_name)
    plt.title(f'{channel_name} ({units})')
    plt.xlabel('Timesteps')
    plt.ylabel(units)
    plt.legend()
    plt.grid(True)
    plt.show()

# Display the chart
#fig.show()