import pandas as pd

# Show all columns when displaying data
pd.set_option("display.max_columns", None)

# Show all rows when displaying data
pd.set_option("display.max_rows", None)

# Load the CSV file
df = pd.read_csv("data/raw/data.csv")

# Show the first 5 rows
print(df.head())

# Display the data type of every column
print(df.dtypes)

# Show the number of rows and columns
print(df.shape)

# Show only the number of rows
print(df.shape[0])

# Show only the number of columns
print(df.shape[1])

# Show all column names
print(df.columns.tolist())

# Show column data types and missing-value counts
df.info()

# First 5 rows
print(df.head())

# First 10 rows
print(df.head(10))

# Last 5 rows
print(df.tail())

# Random 5 rows
print(df.sample(5))

# Show one particular row
print(df.iloc[0])

# Summary of numeric columns
print(df.describe())

# Summary of all columns, including text
print(df.describe(include="all").T)

# Show missing values as True or False
print(df.isnull())

# Count missing values in every column
print(df.isnull().sum())

# Show only columns that have missing values
missing = df.isnull().sum()
print(missing[missing > 0])

# Calculate missing percentages
missing_percent = df.isnull().mean() * 100
print(missing_percent[missing_percent > 0].round(2))

# Count duplicate rows
print(df.duplicated().sum())

# Display duplicate rows
print(df[df.duplicated()])

# Display all rows where product_id appears more than once, including the first occurrence.
print(df[df["supplier_id"].duplicated(keep=False)])

# Display all rows involved in duplicates
print(df[df.duplicated(keep=False)])

# Count different values in each column
print(df.nunique())

# Show values in one column
print(df["category"].unique())

# Count how often each value appears
print(df["category"].value_counts(dropna=False))

# Show one column
print(df["category"])

# Show two columns
print(df[["category", "quantity_sold"]])

# Find rows where quantity sold is greater than 10
print(df[df["quantity_sold"] > 10])

# Find rows where quantity sold is zero
print(df[df["quantity_sold"] == 0])

# Show the highest revenue first
print(df.sort_values("sales_revenue_inr", ascending=False))

# Find the product details for product_id P01188
print(df[df["product_id"] == "P01188"])

# Display product details and revenue
print(df.loc[
    df["product_id"] == "P01188",
    ["product_id", "product_name", "sales_revenue_inr"]
])

# Show the lowest sales revenue first
print(df.sort_values("sales_revenue_inr", ascending=True))

# Calculate total sales revenue for each category
result = df.groupby("category")["sales_revenue_inr"].sum()
print(result)

# Show all columns containing numeric data
print(df.select_dtypes(include="number").columns.tolist())

# Display all rows where supplier_id appears more than once
print(df[df["supplier_id"].duplicated(keep=False)])

# Show the smallest values in ascending order
print(df.select_dtypes(include="number").min().sort_values(ascending=True))

# Show the largest values in ascending order
print(df.select_dtypes(include="number").max().sort_values(ascending=True))