import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# STEP 2: Make the output folder
folder = "outputs/most_sell"
os.makedirs(folder, exist_ok=True)   # creates the folder if it is missing

# STEP 3: Style settings (bold text + bright colors)
sns.set_theme(style="whitegrid")
plt.rcParams["font.weight"] = "bold"         # all text bold
plt.rcParams["axes.labelweight"] = "bold"    # x and y labels bold
plt.rcParams["axes.titleweight"] = "bold"    # title bold

# STEP 4: Load and prepare data
df = pd.read_csv("data/processed/cleaned_data.csv")

df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["quantity_sold"] = pd.to_numeric(df["quantity_sold"], errors="coerce")
df["sales_revenue_inr"] = pd.to_numeric(df["sales_revenue_inr"], errors="coerce")

df = df.dropna(subset=["date", "category"])          # remove bad rows
df["month"] = df["date"].dt.to_period("M").astype(str)   # example: 2026-01

# STEP 5: One function that draws and saves a graph
def make_chart(data, value_column, title, y_label, file_name):
    plt.figure(figsize=(15, 7))

    sns.barplot(
        data=data,
        x="month",
        y=value_column,
        hue="category",
        palette="bright",        # strong, saturated colors
        edgecolor="black",       # black border on each bar
        linewidth=1.2,
        errorbar=None
    )

    plt.title(title, fontsize=20, color="black")
    plt.xlabel("Month", fontsize=14)
    plt.ylabel(y_label, fontsize=14)
    plt.xticks(rotation=45, ha="right", fontsize=12)
    plt.yticks(fontsize=12)
    plt.ticklabel_format(style="plain", axis="y")   # no 1e6 style numbers
    plt.legend(title="Product Category", bbox_to_anchor=(1.02, 1), loc="upper left")
    plt.tight_layout()

    # Save first, then show
    plt.savefig(f"{folder}/{file_name}", dpi=300, bbox_inches="tight", facecolor="white")
    plt.show()
    plt.close()

# STEP 6: Quantity graph
monthly_quantity = df.groupby(["month", "category"], as_index=False)["quantity_sold"].sum()

best_quantity = monthly_quantity.loc[
    monthly_quantity.groupby("month")["quantity_sold"].idxmax()
]
print("\nTOP-SELLING CATEGORY BY MONTH (QUANTITY)")
print(best_quantity.to_string(index=False))

make_chart(
    data=monthly_quantity,
    value_column="quantity_sold",
    title="Monthly Units Sold by Product Category",
    y_label="Total Quantity Sold",
    file_name="monthly_quantity_by_category.png"
)

# STEP 7: Revenue graph
monthly_revenue = df.groupby(["month", "category"], as_index=False)["sales_revenue_inr"].sum()

best_revenue = monthly_revenue.loc[
    monthly_revenue.groupby("month")["sales_revenue_inr"].idxmax()
]
print("\nTOP CATEGORY BY MONTH (REVENUE)")
print(best_revenue.to_string(index=False))

make_chart(
    data=monthly_revenue,
    value_column="sales_revenue_inr",
    title="Monthly Revenue by Product Category",
    y_label="Sales Revenue (INR)",
    file_name="monthly_revenue_by_category.png"
)

# STEP 2: Output folder
folder = "outputs/most_sell"
os.makedirs(folder, exist_ok=True)

# STEP 3: Style (bold text + bright colors)
sns.set_theme(style="whitegrid")
plt.rcParams["font.weight"] = "bold"
plt.rcParams["axes.labelweight"] = "bold"
plt.rcParams["axes.titleweight"] = "bold"

# STEP 4: Load and prepare data
df = pd.read_csv("data/processed/cleaned_data.csv")

df["quantity_sold"] = pd.to_numeric(df["quantity_sold"], errors="coerce")
df["sales_revenue_inr"] = pd.to_numeric(df["sales_revenue_inr"], errors="coerce")
df = df.dropna(subset=["category", "product_name"])

# STEP 5: Total sales of every product in every category
product_sales = df.groupby(["category", "product_name"], as_index=False).agg(
    quantity_sold=("quantity_sold", "sum"),
    sales_revenue_inr=("sales_revenue_inr", "sum")
)

# STEP 6: Best product in each category
# By quantity
top_by_quantity = product_sales.loc[
    product_sales.groupby("category")["quantity_sold"].idxmax()
].sort_values("quantity_sold", ascending=False)

# By revenue
top_by_revenue = product_sales.loc[
    product_sales.groupby("category")["sales_revenue_inr"].idxmax()
].sort_values("sales_revenue_inr", ascending=False)

print("\nTOP PRODUCT IN EACH CATEGORY (QUANTITY)")
print(top_by_quantity.to_string(index=False))

print("\nTOP PRODUCT IN EACH CATEGORY (REVENUE)")
print(top_by_revenue.to_string(index=False))

# Save the tables as CSV files
top_by_quantity.to_csv(f"{folder}/top_product_by_quantity.csv", index=False)
top_by_revenue.to_csv(f"{folder}/top_product_by_revenue.csv", index=False)

# STEP 7: Function to draw and save a graph
def make_chart(data, value_column, title, y_label, file_name):
    plt.figure(figsize=(15, 7))

    ax = sns.barplot(
        data=data,
        x="category",
        y=value_column,
        hue="category",
        palette="bright",
        edgecolor="black",
        linewidth=1.2,
        legend=False
    )

    # Write product name + value on top of each bar
    for bar, (_, row) in zip(ax.patches, data.iterrows()):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"{row['product_name']}\n{row[value_column]:,.0f}",
            ha="center",
            va="bottom",
            fontsize=11,
            fontweight="bold"
        )

    plt.ylim(0, data[value_column].max() * 1.2)   # extra space for the text
    plt.title(title, fontsize=20, color="black")
    plt.xlabel("Product Category", fontsize=14)
    plt.ylabel(y_label, fontsize=14)
    plt.xticks(rotation=45, ha="right", fontsize=12)
    plt.yticks(fontsize=12)
    plt.ticklabel_format(style="plain", axis="y")
    plt.tight_layout()

    plt.savefig(f"{folder}/{file_name}", dpi=300, bbox_inches="tight", facecolor="white")
    plt.show()
    plt.close()

# STEP 8: Draw both graphs
make_chart(
    data=top_by_quantity,
    value_column="quantity_sold",
    title="Best-Selling Product in Each Category (Quantity)",
    y_label="Total Quantity Sold",
    file_name="top_product_by_quantity.png"
)

make_chart(
    data=top_by_revenue,
    value_column="sales_revenue_inr",
    title="Best-Selling Product in Each Category (Revenue)",
    y_label="Sales Revenue (INR)",
    file_name="top_product_by_revenue.png"
)

# STEP 3: Style (bold text + bright colors)
sns.set_theme(style="whitegrid")
plt.rcParams["font.weight"] = "bold"
plt.rcParams["axes.labelweight"] = "bold"
plt.rcParams["axes.titleweight"] = "bold"

# STEP 4: Load data
df = pd.read_csv("data/processed/cleaned_data.csv")

df["quantity_sold"] = pd.to_numeric(df["quantity_sold"], errors="coerce")
df["sales_revenue_inr"] = pd.to_numeric(df["sales_revenue_inr"], errors="coerce")

# STEP 5: Keep only School backpack rows
# str.contains finds the name even if capital letters or spaces differ
backpack = df[df["product_name"].str.contains("school backpack", case=False, na=False)]

print("Rows found:", len(backpack))

# STEP 6: Where is School backpack sold the most?
result = backpack.groupby(
    ["facility_type", "warehouse_city", "warehouse_state"], as_index=False
).agg(
    quantity_sold=("quantity_sold", "sum"),
    sales_revenue_inr=("sales_revenue_inr", "sum")
).sort_values("quantity_sold", ascending=False)

print("\nSCHOOL BACKPACK - SALES BY FACILITY, CITY, STATE")
print(result.to_string(index=False))

# Best location
best = result.iloc[0]
print("\nBEST LOCATION")
print("Facility type :", best["facility_type"])
print("City          :", best["warehouse_city"])
print("State         :", best["warehouse_state"])
print("Quantity sold :", best["quantity_sold"])

result.to_csv(f"{folder}/school_backpack_by_location.csv", index=False)

# STEP 7: Graph of the top 10 locations
top10 = result.head(10).copy()
top10["location"] = top10["warehouse_city"] + ", " + top10["warehouse_state"]

plt.figure(figsize=(14, 7))
sns.barplot(
    data=top10,
    x="location",
    y="quantity_sold",
    hue="facility_type",
    palette="bright",
    edgecolor="black",
    linewidth=1.2
)

plt.title("School Backpack - Top 10 Locations (Quantity)", fontsize=20)
plt.xlabel("Warehouse City, State", fontsize=14)
plt.ylabel("Total Quantity Sold", fontsize=14)
plt.xticks(rotation=45, ha="right", fontsize=12)
plt.yticks(fontsize=12)
plt.legend(title="Facility Type")
plt.tight_layout()

plt.savefig(f"{folder}/school_backpack_by_location.png", dpi=300, bbox_inches="tight", facecolor="white")
plt.show()
plt.close()