import pandas as pd
import numpy as np

# Load the CSV file
df = pd.read_csv("data/raw/data.csv")

# Count null values in each column
null_counts = df.isnull().sum()
print(null_counts)

# Select and display information about only the columns
df.loc[:, df.isnull().any()].info()

# Count each unique value in the platform column
print(df['platform'].value_counts())

# Step 1: Get the top 5 most frequent platform values
top_5_platforms = df['platform'].value_counts().head(5).index.tolist()

print("Top 5 platforms:", top_5_platforms)

# Step 2: Find rows where platform is null
null_mask = df['platform'].isnull()
null_count = null_mask.sum()

# Step 3: Randomly select platforms to fill null values
df.loc[null_mask, 'platform'] = np.random.choice(
    top_5_platforms,
    size=null_count
)

# Count each unique value in the category column
print(df['category'].value_counts())

# Step 1: Get the top 5 most frequent category values
top_5_category = df['category'].value_counts().head(5).index.tolist()

print("Top 5 category:", top_5_category)

# Step 2: Find rows where platform is null
null_mask = df['category'].isnull()
null_count = null_mask.sum()

# Step 3: Randomly select platforms to fill null values
df.loc[null_mask, 'category'] = np.random.choice(
    top_5_category,
    size=null_count
)

# Count each unique value in the warehouse_city column
print(df['warehouse_city'].value_counts())

# Step 1: Get the top 5 most frequent warehouse_city values
top_5_warehouse_city = df['warehouse_city'].value_counts().head(5).index.tolist()

print("Top 5 warehouse_city:", top_5_warehouse_city)

# Step 2: Find rows where platform is null
null_mask = df['warehouse_city'].isnull()
null_count = null_mask.sum()

# Step 3: Randomly select platforms to fill null values
df.loc[null_mask, 'warehouse_city'] = np.random.choice(
    top_5_warehouse_city,
    size=null_count
)

# Count each unique value in the order_status column
print(df['order_status'].value_counts())

# Step 1: Get the top 5 most frequent order_status  values
top_5_order_status  = df['order_status'].value_counts().head(5).index.tolist()

print("Top 5 order_status:", top_5_order_status)

# Step 2: Find rows where platform is null
null_mask = df['order_status'].isnull()
null_count = null_mask.sum()

# Step 3: Randomly select platforms to fill null values
df.loc[null_mask, 'order_status'] = np.random.choice(
    top_5_order_status,
    size=null_count
)

df.loc[:, df.isnull().any()].info()

# Count each unique value in the lead_time_days column
print(df['lead_time_days'].value_counts())

# Step 1: Get the top 5 most frequent lead_time_days  values
top_5_lead_time_days  = df['lead_time_days'].value_counts().head(5).index.tolist()

print("Top 5 lead_time_days:", top_5_lead_time_days)

# Step 2: Find rows where platform is null
null_mask = df['lead_time_days'].isnull()
null_count = null_mask.sum()

# Step 3: Randomly select platforms to fill null values
df.loc[null_mask, 'lead_time_days'] = np.random.choice(
    top_5_lead_time_days,
    size=null_count
)

df.loc[:, df.isnull().any()].info()

# Step 1: Get the top 5 most frequent shipping_distance_km  values
top_5_shipping_distance_km  = df['shipping_distance_km'].value_counts().head(5).index.tolist()

print("Top 5 shipping_distance_km:", top_5_shipping_distance_km)

# Step 2: Find rows where platform is null
null_mask = df['shipping_distance_km'].isnull()
null_count = null_mask.sum()

# Step 3: Randomly select platforms to fill null values
df.loc[null_mask, 'shipping_distance_km'] = np.random.choice(
    top_5_shipping_distance_km,
    size=null_count
)

df.loc[:, df.isnull().any()].info()


# Check each column for duplicate values
for column in df.columns:
    duplicate_values = df[column].value_counts()
    duplicate_values = duplicate_values[duplicate_values > 1]

    print(f"\nColumn: {column}")
    print(duplicate_values)


# Identify all string columns
string_columns = df.select_dtypes(
    include=['object', 'string']
).columns

# Remove extra spaces and standardize capitalization
for column in string_columns:
    df[column] = df[column].str.strip().str.lower().str.capitalize()

# 8. Save the cleaned dataset
df.to_csv("data/processed/cleaned_data.csv", index=False)


# After all Do Actul Check
print("All Things Well")
df.loc[:, df.isnull().any()].info()