# This script is used to plot each channel with dropdown for InsetChart.json for selected simulation.
# Drop this file under the result's job_directory/suite/experiment directory. 
# and replace the simulation id with your simulation id.

# Import necessary libraries
import json
import pandas as pd
import os
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display, clear_output

# Define the path to the JSON file
# CURRENT_DIRECTORY is the result's path: job_directory/suite/experiment
CURRENT_DIRECTORY = os.path.dirname(__file__)
if "params" not in globals():
    params = {
        "dataset": os.path.join(
            CURRENT_DIRECTORY,
            "994ead91-cd2b-4808-b162-d03743da7a68", # replace with your simulation_id 
            "output",
            "InsetChart.json"
        )
    }  # fallback for debugging

# Load the JSON data
file_path = params["dataset"]
with open(file_path) as f:
    data = json.load(f)

# Normalize header and channels
header = data["Header"]
channels = data["Channels"]

# Dropdown widget for channel selection
channel_names = list(channels.keys())
dropdown = widgets.Dropdown(
    options=channel_names,
    description='Channel:',
    layout=widgets.Layout(width='50%')
)


# Plotting function
def plot_channel(channel_name):
    clear_output(wait=True)
    display(dropdown)

    channel_data = channels[channel_name]
    units = channel_data["Units"]
    values = channel_data["Data"]
    timesteps = range(len(values))

    plt.figure(figsize=(10, 6))
    plt.plot(timesteps, values, label=channel_name)
    plt.title(f'{channel_name} ({units})')
    plt.xlabel('Timesteps')
    plt.ylabel(units)
    plt.grid(True)
    plt.legend()
    plt.show()


# Bind dropdown to plotting function
dropdown.observe(lambda change: plot_channel(change.new), names='value')

# Display the dropdown and initial plot
display(dropdown)
plot_channel(channel_names[0])
