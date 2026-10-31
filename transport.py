import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# STEP 2: Output folder
folder = "outputs/transport"
os.makedirs(folder, exist_ok=True)

# STEP 3: Style (bold text)
plt.rcParams["font.weight"] = "bold"

# STEP 4: Load data and keep only School backpack
df = pd.read_csv("data/processed/cleaned_data.csv")

backpack = df[df["product_name"].str.contains("school backpack", case=False, na=False)]
backpack = backpack.dropna(subset=["logistics_partner"])

print("Rows found:", len(backpack))

# STEP 5: Count how many times each partner is used
partner_count = backpack["logistics_partner"].value_counts()

print("\nSCHOOL BACKPACK - LOGISTICS PARTNER USAGE")
print(partner_count)

print("\nMOST USED PARTNER:", partner_count.idxmax())

# Save the table
partner_count.to_csv(f"{folder}/school_backpack_logistics_partner.csv")

# STEP 6: Draw the pie graph
colors = sns.color_palette("bright", len(partner_count))

plt.figure(figsize=(10, 8))

plt.pie(
    partner_count,
    labels=partner_count.index,
    autopct="%1.1f%%",                 # show percentage on each slice
    startangle=90,
    colors=colors,
    wedgeprops={"edgecolor": "black", "linewidth": 1.5},
    textprops={"fontsize": 14, "fontweight": "bold"},
    explode=[0.08] + [0] * (len(partner_count) - 1)   # pull out the biggest slice
)

plt.title("School Backpack - Logistics Partner Usage", fontsize=20, fontweight="bold")
plt.tight_layout()

# Save first, then show
plt.savefig(f"{folder}/school_backpack_logistics_pie.png", dpi=300, bbox_inches="tight", facecolor="white")
plt.show()
plt.close()

# STEP 3: Style (bold text + bright colors)
sns.set_theme(style="whitegrid")
plt.rcParams["font.weight"] = "bold"
plt.rcParams["axes.labelweight"] = "bold"
plt.rcParams["axes.titleweight"] = "bold"

# STEP 4: Load data and keep only School backpack
df = pd.read_csv("data/processed/cleaned_data.csv")
df["delivery_days"] = pd.to_numeric(df["delivery_days"], errors="coerce")

backpack = df[df["product_name"].str.contains("school backpack", case=False, na=False)]
backpack = backpack.dropna(subset=["logistics_partner", "delivery_days"])

print("Rows found:", len(backpack))

# STEP 5: Average delivery days for each partner
delivery = backpack.groupby("logistics_partner", as_index=False).agg(
    average_days=("delivery_days", "mean"),
    fastest_days=("delivery_days", "min"),
    slowest_days=("delivery_days", "max"),
    orders=("delivery_days", "count")
).sort_values("average_days")          # fastest partner first

delivery["average_days"] = delivery["average_days"].round(2)

print("\nSCHOOL BACKPACK - DELIVERY DAYS BY LOGISTICS PARTNER")
print(delivery.to_string(index=False))

print("\nFASTEST PARTNER:", delivery.iloc[0]["logistics_partner"])
print("SLOWEST PARTNER:", delivery.iloc[-1]["logistics_partner"])

delivery.to_csv(f"{folder}/school_backpack_delivery_days.csv", index=False)

# STEP 6: Bar chart - average delivery days
plt.figure(figsize=(12, 7))

ax = sns.barplot(
    data=delivery,
    x="logistics_partner",
    y="average_days",
    hue="logistics_partner",
    palette="bright",
    edgecolor="black",
    linewidth=1.2,
    legend=False
)

# Write the number of days on top of each bar
for bar in ax.patches:
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f"{bar.get_height():.1f} days",
        ha="center",
        va="bottom",
        fontsize=13,
        fontweight="bold"
    )

plt.ylim(0, delivery["average_days"].max() * 1.2)   # space for the text
plt.title("School Backpack - Average Delivery Days by Logistics Partner", fontsize=20)
plt.xlabel("Logistics Partner", fontsize=14)
plt.ylabel("Average Delivery Days", fontsize=14)
plt.xticks(rotation=30, ha="right", fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()

plt.savefig(f"{folder}/school_backpack_delivery_days_bar.png", dpi=300, bbox_inches="tight", facecolor="white")
plt.show()
plt.close()

# STEP 7: Box plot - spread of delivery days
plt.figure(figsize=(12, 7))

sns.boxplot(
    data=backpack,
    x="logistics_partner",
    y="delivery_days",
    hue="logistics_partner",
    order=delivery["logistics_partner"],     # same order as the bar chart
    palette="bright",
    linewidth=1.5,
    legend=False
)

plt.title("School Backpack - Delivery Days Spread by Logistics Partner", fontsize=20)
plt.xlabel("Logistics Partner", fontsize=14)
plt.ylabel("Delivery Days", fontsize=14)
plt.xticks(rotation=30, ha="right", fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()

plt.savefig(f"{folder}/school_backpack_delivery_days_box.png", dpi=300, bbox_inches="tight", facecolor="white")
plt.show()
plt.close()


#Warehouse Location Heatmap

# STEP 1: Make the output folder
folder = "outputs/most_sell"
os.makedirs(folder, exist_ok=True)

# STEP 2: Style settings (bold text + bright colors)
sns.set_theme(style="whitegrid")
plt.rcParams["font.weight"] = "bold"
plt.rcParams["axes.labelweight"] = "bold"
plt.rcParams["axes.titleweight"] = "bold"

# STEP 3: Load and prepare data
df = pd.read_csv("data/processed/cleaned_data.csv")

df["quantity_sold"] = pd.to_numeric(
    df["quantity_sold"], errors="coerce"
)

df = df.dropna(
    subset=[
        "product_name",
        "facility_type",
        "warehouse_city",
        "warehouse_state",
        "quantity_sold"
    ]
)

# STEP 4: Keep only School Backpack rows
backpack = df[
    df["product_name"].str.contains(
        "school backpack",
        case=False,
        na=False
    )
]

print("Rows found:", len(backpack))

# STEP 5: Calculate sales quantity by warehouse location
location_sales = backpack.groupby(
    ["facility_type", "warehouse_city", "warehouse_state"],
    as_index=False
).agg(
    total_quantity=("quantity_sold", "sum")
)

print("\nSCHOOL BACKPACK - SALES BY WAREHOUSE LOCATION")
print(location_sales.to_string(index=False))

# STEP 6: Select Top 10 warehouse locations
top10 = location_sales.sort_values(
    "total_quantity",
    ascending=False
).head(10).copy()

# Create location name
top10["location"] = (
    top10["warehouse_city"] + ", " +
    top10["warehouse_state"]
)

print("\nTOP 10 WAREHOUSE LOCATIONS")
print(top10.to_string(index=False))

# Save the table
top10.to_csv(
    f"{folder}/school_backpack_top10_warehouse_heatmap.csv",
    index=False
)

# STEP 7: Create Pivot Table
heatmap_data = top10.pivot_table(
    index="facility_type",
    columns="location",
    values="total_quantity",
    aggfunc="sum",
    fill_value=0
)

# STEP 8: Draw Heatmap
plt.figure(figsize=(16, 8))

sns.heatmap(
    data=heatmap_data,
    annot=True,
    fmt=",.0f",
    cmap="YlOrRd",
    linewidths=1,
    linecolor="black",
    cbar_kws={"label": "Total Quantity Sold"},
    annot_kws={"size": 11, "weight": "bold"}
)

plt.title(
    "School Backpack - Top 10 Warehouse Location Heatmap",
    fontsize=20,
    fontweight="bold",
    pad=20
)

plt.xlabel("Warehouse City, State", fontsize=14)
plt.ylabel("Facility Type", fontsize=14)

plt.xticks(rotation=45, ha="right", fontsize=11)
plt.yticks(rotation=0, fontsize=12)

plt.tight_layout()

# STEP 9: Save first, then show
plt.savefig(
    f"{folder}/school_backpack_warehouse_heatmap.png",
    dpi=300,
    bbox_inches="tight",
    facecolor="white"
)

plt.show()
plt.close()


# Logistics Partner Delivery Heatmap

# STEP 1: Make the output folder
folder = "outputs/transport"
os.makedirs(folder, exist_ok=True)

# STEP 2: Style settings (bold text + bright colors)
sns.set_theme(style="whitegrid")
plt.rcParams["font.weight"] = "bold"
plt.rcParams["axes.labelweight"] = "bold"
plt.rcParams["axes.titleweight"] = "bold"

# STEP 3: Load and prepare data
df = pd.read_csv("data/processed/cleaned_data.csv")

df["delivery_days"] = pd.to_numeric(
    df["delivery_days"], errors="coerce"
)

df["shipping_distance_km"] = pd.to_numeric(
    df["shipping_distance_km"], errors="coerce"
)

df["quantity_sold"] = pd.to_numeric(
    df["quantity_sold"], errors="coerce"
)

# STEP 4: Keep only School Backpack rows
backpack = df[
    df["product_name"].str.contains(
        "school backpack",
        case=False,
        na=False
    )
]

backpack = backpack.dropna(
    subset=[
        "logistics_partner",
        "delivery_days",
        "shipping_distance_km"
    ]
)

print("Rows found:", len(backpack))

# STEP 5: Calculate delivery performance by logistics partner
delivery = backpack.groupby(
    "logistics_partner", as_index=False
).agg(
    average_delivery_days=("delivery_days", "mean"),
    fastest_delivery_days=("delivery_days", "min"),
    slowest_delivery_days=("delivery_days", "max"),
    average_shipping_distance=("shipping_distance_km", "mean"),
    total_orders=("delivery_days", "count")
)

delivery["average_delivery_days"] = (
    delivery["average_delivery_days"].round(2)
)

delivery["average_shipping_distance"] = (
    delivery["average_shipping_distance"].round(2)
)

print("\nSCHOOL BACKPACK - LOGISTICS DELIVERY PERFORMANCE")
print(delivery.to_string(index=False))

# STEP 6: Sort logistics partners by average delivery days
delivery = delivery.sort_values(
    "average_delivery_days",
    ascending=True
)

# Save the performance table
delivery.to_csv(
    f"{folder}/school_backpack_delivery_heatmap.csv",
    index=False
)

# STEP 7: Create Pivot Table
heatmap_data = delivery.set_index(
    "logistics_partner"
)[
    [
        "average_delivery_days",
        "fastest_delivery_days",
        "slowest_delivery_days",
        "average_shipping_distance",
        "total_orders"
    ]
]

# STEP 8: Draw Heatmap
plt.figure(figsize=(15, 8))

sns.heatmap(
    data=heatmap_data,
    annot=True,
    fmt=".2f",
    cmap="YlOrRd",
    linewidths=1,
    linecolor="black",
    cbar_kws={"label": "Metric Value"},
    annot_kws={"size": 11, "weight": "bold"}
)

plt.title(
    "School Backpack - Logistics Partner Delivery Performance Heatmap",
    fontsize=19,
    fontweight="bold",
    pad=20
)

plt.xlabel("Delivery Performance Metrics", fontsize=14)
plt.ylabel("Logistics Partner", fontsize=14)

plt.xticks(rotation=25, ha="right", fontsize=10)
plt.yticks(rotation=0, fontsize=12)

plt.tight_layout()

# STEP 9: Save first, then show
plt.savefig(
    f"{folder}/school_backpack_delivery_heatmap.png",
    dpi=300,
    bbox_inches="tight",
    facecolor="white"
)

plt.show()
plt.close()
