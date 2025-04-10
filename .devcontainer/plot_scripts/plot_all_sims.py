# plot all simulations insetchart for a given channel in dropdown
# Put this under result's job_directory (for example, DEST/)
import os
import json
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display, clear_output

# === CONFIGURATION ===
Experiment_folder = "Campaign_Sweep__SpaceSpraying_e18f3f17-4c5d-4bc9-a0d5-b41f12aef4b9"  # Change this to your experiment folder name
Suite_folder = "Suite_8824c5d3-a45d-4d6f-8c33-f9561fd9249d"  # Change this to your suite folder name

# === Resolve simulation paths ===
BASE_PATH = os.path.join(os.getcwd(), Suite_folder, Experiment_folder)
# === Step 1: Collect All Simulations ===
def get_sim_paths(base_path):
    sim_paths = {}
    for sim_id in os.listdir(base_path):
        inset_path = os.path.join(base_path, sim_id, "output", "InsetChart.json")
        if os.path.isfile(inset_path):
            sim_paths[sim_id] = inset_path
    return sim_paths

simulation_paths = get_sim_paths(BASE_PATH)
if not simulation_paths:
    raise FileNotFoundError(f"No valid simulations found under: {BASE_PATH}")

# === Step 2: Load Channel Names from the First Simulation ===
with open(next(iter(simulation_paths.values()))) as f:
    first_data = json.load(f)

channel_names = list(first_data["Channels"].keys())

# === Step 3: Build Dropdown ===
channel_dropdown = widgets.Dropdown(
    options=channel_names,
    description="Channel:",
    layout=widgets.Layout(width='60%')
)

# === Step 4: Plotting Function ===
def plot_channel_across_sims(channel_name):
    clear_output(wait=True)
    display(channel_dropdown)

    plt.figure(figsize=(10, 6))
    for sim_id, path in simulation_paths.items():
        try:
            with open(path) as f:
                data = json.load(f)

            channel = data["Channels"].get(channel_name)
            if not channel:
                print(f"⚠️ Channel '{channel_name}' not found in simulation {sim_id}")
                continue

            values = channel["Data"]
            units = channel["Units"]
            timesteps = list(range(len(values)))

            plt.plot(timesteps, values, label=sim_id)

        except Exception as e:
            print(f"❌ Failed to process {sim_id}: {e}")

    plt.title(f"{channel_name} across simulations")
    plt.xlabel("Timesteps")
    plt.ylabel(units)
    #plt.legend(loc='best', fontsize='small')  # this is legend (the little box that shows which line is which simulation)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# === Step 5: Bind and Display ===
channel_dropdown.observe(lambda change: plot_channel_across_sims(change.new), names='value')
display(channel_dropdown)
plot_channel_across_sims(channel_names[0])
