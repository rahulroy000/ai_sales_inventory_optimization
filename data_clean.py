import os
import pandas as pd
import numpy as np

# Load the original CSV file
df = pd.read_csv("data/raw/data.csv")

# Display available column names
print(df.columns.tolist())


# 1. CHECK MISSING NUMERIC VALUES USING NUMPY

# Convert numeric columns into a NumPy array
numeric_data = df.select_dtypes(include="number").to_numpy(dtype=float)

# Count missing numeric values
print("Missing numeric values:", np.isnan(numeric_data).sum())


# 2. CHECK REPEATED VALUES IN EACH COLUMN

# Count repeated values in each column
duplicate_counts = {}

for col in df.columns:
    values = df[col].dropna().to_numpy()

    # Skip columns with no values
    if len(values) > 0:
        try:
            _, counts = np.unique(values, return_counts=True)

            # Count extra occurrences after the first occurrence
            duplicate_counts[col] = np.sum(counts - 1)

        except TypeError:
            # Some mixed data types cannot be compared by np.unique
            print(f"Could not count values in column: {col}")

# Sort columns from most repeated values to least
result = pd.Series(duplicate_counts).sort_values(ascending=False)

print("\nRepeated values by column:")
print(result)

# Show the column with the most repeated values
if not result.empty:
    print("\nMost repeated column:")
    print(result.index[0], "=", result.iloc[0])


# 3. CALCULATE MEAN AND MEDIAN

# Convert quantity_sold into numeric values
quantity = pd.to_numeric(
    df["quantity_sold"], errors="coerce"
).to_numpy(dtype=float)

# Calculate average and middle quantity
print("\nMean quantity:", np.nanmean(quantity))
print("Median quantity:", np.nanmedian(quantity))


# 4. CLEAN ALL TEXT COLUMNS

# Find all text columns
text_columns = df.select_dtypes(
    include=["object", "string"]
).columns

# Remove extra spaces from text values
for col in text_columns:
    df[col] = df[col].str.strip()

# Standardize category names
df["category"] = df["category"].str.title()

# Standardize capitalization in selected text columns
for col in [
    "platform",
    "warehouse_city",
    "warehouse_state",
    "logistics_partner",
    "order_status"
]:
    if col in df.columns:
        df[col] = df[col].str.title()

# Display cleaned categories and their counts
print("\nCategory values:")
print(df["category"].value_counts(dropna=False))


# 5. CONVERT DATE COLUMN

# Convert date text into datetime format
# Invalid dates become NaT
df["date"] = pd.to_datetime(
    df["date"], format="mixed", errors="coerce"
)

print("\nDate range:")
print("Earliest:", df["date"].min())
print("Latest:", df["date"].max())
print("Missing or invalid dates:", df["date"].isna().sum())


# 6. CONVERT NUMERIC COLUMNS

# List columns that should contain numbers
numeric_columns = [
    "quantity_sold",
    "unit_cost_inr",
    "unit_price_inr",
    "discount_pct",
    "discount_inr",
    "sales_revenue_inr",
    "current_stock",
    "reorder_level",
    "safety_stock",
    "lead_time_days",
    "minimum_order_quantity",
    "purchase_order_quantity",
    "order_cost_inr",
    "shipping_distance_km",
    "delivery_days"
]

# Convert each available column to numeric
for col in numeric_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(
            df[col].astype("string").str.replace(",", "", regex=False),
            errors="coerce"
        )


# 7. CHECK EXACT DUPLICATE ROWS

# Count rows where all columns are identical
print("\nExact duplicate rows:", df.duplicated().sum())

# Display exact duplicate rows
print(df[df.duplicated()])

# Remove only completely identical rows
df = df.drop_duplicates()

print("Shape after removing exact duplicates:", df.shape)

# Check repeated order IDs, but do not automatically delete them
if "order_id" in df.columns:
    repeated_orders = df[
        df["order_id"].duplicated(keep=False)
    ]

    print("Rows with repeated order IDs:", len(repeated_orders))


# 8. CHECK INVALID VALUES

# Find negative quantities
print("\nNegative quantities:")
print(df[df["quantity_sold"] < 0])

# Find negative delivery days
print("\nNegative delivery days:")
print(df[df["delivery_days"] < 0])

# Find negative lead times
print("\nNegative lead times:")
print(df[df["lead_time_days"] < 0])

# Find negative shipping distances
print("\nNegative shipping distances:")
print(df[df["shipping_distance_km"] < 0])

# Check discounts above 100 only if discount_pct uses 0-100 format
print("\nDiscounts above 100:")
print(df[df["discount_pct"] > 100])


# 9. CHECK POSSIBLE OUTLIERS USING IQR

# Flag unusually low or high values without deleting them
outlier_counts = {}

for col in df.select_dtypes(include="number").columns:
    values = df[col].dropna()

    if len(values) >= 4:
        q1 = np.percentile(values, 25)
        q3 = np.percentile(values, 75)
        iqr = q3 - q1

        lower_limit = q1 - 1.5 * iqr
        upper_limit = q3 + 1.5 * iqr

        outlier_counts[col] = np.sum(
            (values < lower_limit) | (values > upper_limit)
        )

print("\nPossible outliers by column:")
print(pd.Series(outlier_counts))


# 10. CHECK REVENUE CALCULATION

# Compare recorded revenue with an estimated revenue formula
# Confirm how discount_pct is stored before relying on this check
if all(col in df.columns for col in [
    "quantity_sold", "unit_price_inr", "sales_revenue_inr"
]):

    if "discount_pct" in df.columns:
        discount = df["discount_pct"]
        known_discount = discount.dropna()

        # If discount values look like 5 for 5%, convert to 0.05
        if len(known_discount) > 0 and known_discount.max() > 1:
            discount_rate = discount / 100
        else:
            discount_rate = discount

        discount_rate = discount_rate.fillna(0)
    else:
        discount_rate = pd.Series(0, index=df.index)

    # Calculate estimated revenue
    estimated_revenue = (
        df["quantity_sold"]
        * df["unit_price_inr"]
        * (1 - discount_rate)
    )

    # Compare estimated and recorded revenue
    df["estimated_revenue_check"] = estimated_revenue
    df["revenue_difference_check"] = (
        df["sales_revenue_inr"] - estimated_revenue
    )

    print("\nRevenue differences greater than ₹1:")
    print(
        df[df["revenue_difference_check"].abs() > 1][
            [
                "quantity_sold",
                "unit_price_inr",
                "discount_pct",
                "sales_revenue_inr",
                "estimated_revenue_check",
                "revenue_difference_check"
            ]
        ].head(20)
    )

# 11. CHECK MISSING VALUES

# Count missing values in every column
print("\nMissing values before filling:")
print(df.isnull().sum())

# Show only columns with missing values
missing = df.isnull().sum()
print("\nColumns with missing values:")
print(missing[missing > 0])

# Calculate missing percentages
missing_percent = (df.isnull().mean() * 100).round(2)
print("\nMissing percentages:")
print(missing_percent[missing_percent > 0])

# 12. FILL MISSING TEXT VALUES

# Use Unknown for missing text information
for col in [
    "platform",
    "category",
    "warehouse_city",
    "order_status"
]:
    if col in df.columns:
        df[col] = df[col].fillna("Unknown")


# 13. FILL MISSING LEAD TIME

# Fill missing lead time using the same supplier's median
if "lead_time_days" in df.columns and "supplier_id" in df.columns:

    supplier_median = df.groupby(
        "supplier_id"
    )["lead_time_days"].transform("median")

    df["lead_time_days"] = df[
        "lead_time_days"
    ].fillna(supplier_median)

# Fill any remaining missing lead times with the overall median
if (
    "lead_time_days" in df.columns
    and df["lead_time_days"].notna().any()
):
    df["lead_time_days"] = df[
        "lead_time_days"
    ].fillna(df["lead_time_days"].median())


# Keep missing shipping distances unchanged until you investigate them


# 14. CHECK MISSING VALUES AFTER FILLING

print("\nMissing values after filling:")
print(df.isnull().sum())


# 15. SAVE THE CLEANED DATASET

# Create the output folder if it does not exist
os.makedirs("data/processed", exist_ok=True)

# Save cleaned data without overwriting the original CSV
df.to_csv("data/processed/data_cleaned.csv", index=False)

print("\nCleaned dataset saved successfully.")
