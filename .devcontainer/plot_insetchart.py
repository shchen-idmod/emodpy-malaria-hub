# This script is used to plot the InsetChart data from a JSON file for selected simulation.
# Drop this file under job_directory/suite directory. and replace experiment/simulation directory names in line 14 to plot InsetChart.json for selected simulation.

# Import necessary libraries
import json
import pandas as pd
import os
import sys
import matplotlib.pyplot as plt

# Load JSON data from file
CURRENT_DIRECTORY = os.path.dirname(__file__)  # drop this file under suite directory
if "params" not in globals():
    params = {
        "dataset": os.path.join(
            CURRENT_DIRECTORY,
            "all_reports_example_97357c05-fbba-4f72-9506-6b9daca29cc9",
            "994ead91-cd2b-4808-b162-d03743da7a68",
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