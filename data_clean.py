import pandas as pd
import numpy as np

# Load the CSV file
df = pd.read_csv("data/raw/data.csv")

# # Display available column names
# print(df.columns.tolist())

# # Count missing numeric values using NumPy
# numeric_data = df.select_dtypes(include="number").to_numpy(dtype=float)

# print("Missing numeric values:", np.isnan(numeric_data).sum())

# # Check repeated values in every column
# for col in df.columns:
#     values = df[col].dropna().to_numpy()

#     if len(values) > 0:
#         unique_values, counts = np.unique(values, return_counts=True)

#         # Count occurrences beyond the first occurrence
#         repeated_count = np.sum(counts[counts > 1] - 1)

#         print(f"{col}: {repeated_count} repeated values")

# # Store repeated-value counts for all columns
# duplicate_counts = {}

# for col in df.columns:
#     values = df[col].dropna().to_numpy()

#     if len(values) > 0:
#         _, counts = np.unique(values, return_counts=True)
#         duplicate_counts[col] = np.sum(counts - 1)

# # Calculate mean and median for quantity sold
# quantity = pd.to_numeric(df["quantity_sold"], errors="coerce").to_numpy()

# print("Mean quantity:", np.nanmean(quantity))
# print("Median quantity:", np.nanmedian(quantity))

# # Sort columns from highest to lowest repeated count
# result = pd.Series(duplicate_counts).sort_values(ascending=False)

# print(result)
# print("\nColumn with the most repeated values:")
# print(result.index[0], "=", result.iloc[0])

# # Standardize category names and remove extra spaces
# df["category"] = df["category"].str.strip().str.title()

# # Display the corrected category names
# print(df["category"].unique())

# # Count each category after standardization
# print(df["category"].value_counts(dropna=False))

# # Count missing values in each column
# print(df.isnull().sum())

# # Show only columns that contain missing values
# missing = df.isnull().sum()
# print(missing[missing > 0])

# # Fill missing text values with "Unknown"
# text_columns = [
#     "platform",
#     "category",
#     "warehouse_city",
#     "order_status",
#     "lead_time_days"
#     "shipping_distance_km"
# ]

# for col in text_columns:
#     if col in df.columns:
#         df[col] = df[col].fillna("Unknown")


# # Check missing values again
# print("Missing values after filling text columns:")
# print(df.isnull().sum())

# # Fill missing values with each column's median
# numeric_columns = [
#     "lead_time_days",
#     "shipping_distance_km"
# ]

# for col in numeric_columns:
#     df[col] = df[col].fillna(df[col].median())

# # Check missing values again
# print(df[["lead_time_days", "shipping_distance_km"]].isnull().sum())

# # Save the corrected dataset to a new file
# df.to_csv("data/processed/data_cleaned.csv", index=False)