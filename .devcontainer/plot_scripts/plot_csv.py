# This script reads a CSV file and generates line plots for each numeric column against the first column.
# Put this script in the same directory as your CSV file or adjust the path accordingly.
# Change the CSV file name as needed.
import pandas as pd
import matplotlib.pyplot as plt

# Load your CSV file
df = pd.read_csv("ReportVectorStats.csv")  # Change to your CSV path

# Try to use the first column as x-axis if it looks like an index
x_col = df.columns[0]
x = df[x_col]

# Loop through numeric columns (skip non-numeric or index column)
for col in df.select_dtypes(include='number').columns:
    if col == x_col:
        continue  # Skip index column

    plt.figure(figsize=(8, 4))
    plt.plot(x, df[col], marker='o', label=col)
    plt.title(f"{col} over {x_col}")
    plt.xlabel(x_col)
    plt.ylabel(col)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
