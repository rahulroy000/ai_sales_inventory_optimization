
import os
import numpy as np
import pandas as pd

# Load the original CSV file
df = pd.read_csv("data/raw/data.csv")

# Convert required columns to numeric
numeric_columns = [
    "unit_price_inr",
    "unit_cost_inr",
    "quantity_sold",
    "sales_revenue_inr",
    "discount_pct",
    "current_stock",
    "reorder_level",
    "delivery_days",
    "lead_time_days",
    "shipping_distance_km"
]

for col in numeric_columns:
    if col in df.columns:
        # Remove commas before numeric conversion, if present
        df[col] = pd.to_numeric(
            df[col].astype("string").str.replace(",", "", regex=False),
            errors="coerce"
        )

# Create profit and profit margin
if all(col in df.columns for col in [
    "sales_revenue_inr",
    "unit_cost_inr",
    "quantity_sold"
]):
    df["profit"] = (
        df["sales_revenue_inr"]
        - df["unit_cost_inr"] * df["quantity_sold"]
    )

    df["profit_margin"] = (
        df["profit"]
        .div(df["sales_revenue_inr"].where(df["sales_revenue_inr"] > 0))
        * 100
    )

# Create date features
if "date" in df.columns:
    df["date"] = pd.to_datetime(
        df["date"],
        format="mixed",
        errors="coerce"
    )

    df["month"] = df["date"].dt.month
    df["year"] = df["date"].dt.year
    df["weekday"] = df["date"].dt.dayofweek

    df["week_of_year"] = (
        df["date"].dt.isocalendar().week.astype("Int64")
    )

    # Saturday = 5, Sunday = 6
    df["is_weekend"] = (
        df["date"].dt.dayofweek.isin([5, 6])
        .astype("boolean")
    )

    # Approximate festive season: October and November
    festive_months = [10, 11]

    df["is_festive_season"] = (
        df["date"].dt.month.isin(festive_months)
        .astype("boolean")
    )

    # Keep missing dates as missing values
    df.loc[
        df["date"].isna(),
        ["is_weekend", "is_festive_season"]
    ] = pd.NA

# Create stock gap and reorder flag
if all(col in df.columns for col in [
    "current_stock",
    "reorder_level"
]):
    df["stock_gap"] = (
        df["current_stock"] - df["reorder_level"]
    )

    # True means stock is below the reorder level
    df["below_reorder"] = (
        df["current_stock"] < df["reorder_level"]
    ).astype("boolean")

# Create delivery delay
if all(col in df.columns for col in [
    "delivery_days",
    "lead_time_days"
]):
    df["delivery_delay"] = (
        df["delivery_days"] - df["lead_time_days"]
    )

# Create shipping distance bands
if "shipping_distance_km" in df.columns:
    df["distance_band"] = pd.cut(
        df["shipping_distance_km"],
        bins=[-np.inf, 100, 500, np.inf],
        labels=["0-100 km", "100-500 km", "500+ km"],
        right=True
    )

# Create discount bands
# Assumes discount_pct uses 0-100, e.g. 15 means 15%
if "discount_pct" in df.columns:
    df["discount_band"] = pd.cut(
        df["discount_pct"],
        bins=[-np.inf, 0, 10, 20, np.inf],
        labels=["0%", "1-10%", "10-20%", "20%+"],
        right=True
    )

# Create cancellation flag
if "order_status" in df.columns:
    status = (
        df["order_status"]
        .astype("string")
        .str.strip()
        .str.lower()
    )

    # Nullable integer: 1 = cancelled, 0 = other known status
    df["is_cancelled"] = pd.Series(
        pd.NA,
        index=df.index,
        dtype="Int64"
    )

    known_status = status.notna() & status.ne("unknown")

    df.loc[known_status, "is_cancelled"] = (
        status[known_status]
        .isin(["cancelled", "canceled"])
        .astype("int64")
    )

# Display the new features
new_columns = [
    "profit",
    "profit_margin",
    "month",
    "year",
    "weekday",
    "week_of_year",
    "is_weekend",
    "is_festive_season",
    "stock_gap",
    "below_reorder",
    "delivery_delay",
    "distance_band",
    "discount_band",
    "is_cancelled"
]

available_columns = [
    col for col in new_columns
    if col in df.columns
]

print("\nNew feature columns:")
print(df[available_columns].head())

print("\nMissing values in new features:")
print(df[available_columns].isnull().sum())

# Create output directory if it does not exist
os.makedirs("data/processed", exist_ok=True)

# Save the feature-engineered dataset
output_path = "data/processed/data_with_features.csv"

df.to_csv(output_path, index=False)

print(f"\nFeature-engineered data saved successfully: {output_path}")
print(f"Dataset shape: {df.shape}")
