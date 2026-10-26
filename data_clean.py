import pandas as pd
import numpy as np

# Load the CSV file
df = pd.read_csv("data/raw/data.csv")

# Display available column names
print(df.columns.tolist())