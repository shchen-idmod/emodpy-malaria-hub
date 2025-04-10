# This is the script to plot CSV data with a dropdown menu to select the column to plot.
# Put this script in the same directory as your CSV file or adjust the path accordingly.
# Change the CSV file name as needed.
import pandas as pd
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display, clear_output

# === Load CSV ===
df = pd.read_csv("ReportVectorStats.csv")  # Replace with your CSV file

# === Determine x-axis column (first column) ===
x_col = df.columns[0]
x = df[x_col]

# === Detect numeric columns for plotting ===
numeric_columns = df.select_dtypes(include='number').columns.tolist()
if x_col in numeric_columns:
    numeric_columns.remove(x_col)  # Don't plot index column

# === Create dropdown widget ===
dropdown = widgets.Dropdown(
    options=numeric_columns,
    description="Column:",
    layout=widgets.Layout(width="50%")
)

# === Plotting function ===
def plot_column(col_name):
    clear_output(wait=True)
    display(dropdown)

    plt.figure(figsize=(8, 4))
    plt.plot(x, df[col_name], marker='o')
    plt.title(f"{col_name} over {x_col}")
    plt.xlabel(x_col)
    plt.ylabel(col_name)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# === Bind dropdown to plot function ===
dropdown.observe(lambda change: plot_column(change.new), names='value')

# === Show dropdown and initial plot ===
display(dropdown)
plot_column(numeric_columns[0])
