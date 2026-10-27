import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# STEP 2: Output folder
folder = "outputs/purchase"
os.makedirs(folder, exist_ok=True)

# STEP 3: Style (bold text + bright colors)
sns.set_theme(style="whitegrid")
plt.rcParams["font.weight"] = "bold"
plt.rcParams["axes.labelweight"] = "bold"
plt.rcParams["axes.titleweight"] = "bold"

# STEP 4: Load data
df = pd.read_csv("data/processed/cleaned_data.csv")

df["purchase_order_quantity"] = pd.to_numeric(df["purchase_order_quantity"], errors="coerce")
df = df.dropna(subset=["product_name", "category", "purchase_order_quantity"])

# STEP 5: Total purchase order quantity for each product
orders = df.groupby(["category", "product_name"], as_index=False).agg(
    total_ordered=("purchase_order_quantity", "sum")
).sort_values("total_ordered", ascending=False)

# Top 10 products overall
top10 = orders.head(10)
print("\nTOP 10 PRODUCTS BY PURCHASE ORDER QUANTITY")
print(top10.to_string(index=False))

# Top product inside each category
top_in_category = orders.loc[
    orders.groupby("category")["total_ordered"].idxmax()
].sort_values("total_ordered", ascending=False)

print("\nTOP PRODUCT IN EACH CATEGORY")
print(top_in_category.to_string(index=False))

# Total for each category
category_total = df.groupby("category", as_index=False)["purchase_order_quantity"].sum()
category_total = category_total.sort_values("purchase_order_quantity", ascending=False)

print("\nTOP CATEGORY:", category_total.iloc[0]["category"])

orders.to_csv(f"{folder}/purchase_order_by_product.csv", index=False)
top_in_category.to_csv(f"{folder}/purchase_order_top_in_category.csv", index=False)

# STEP 6: Graph - Top 10 products (colored by category)
plt.figure(figsize=(14, 8))

ax = sns.barplot(
    data=top10,
    y="product_name",
    x="total_ordered",
    hue="category",
    dodge=False,                 # one bar per product
    palette="bright",
    edgecolor="black",
    linewidth=1.2
)

# Write the number at the end of each bar
for bar in ax.patches:
    width = bar.get_width()
    if width > 0:
        ax.text(
            width,
            bar.get_y() + bar.get_height() / 2,
            f" {width:,.0f}",
            va="center",
            fontsize=12,
            fontweight="bold"
        )

plt.xlim(0, top10["total_ordered"].max() * 1.15)   # space for the text
plt.title("Top 10 Products by Purchase Order Quantity", fontsize=20)
plt.xlabel("Total Purchase Order Quantity", fontsize=14)
plt.ylabel("Product Name", fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.legend(title="Category")
plt.tight_layout()

plt.savefig(f"{folder}/purchase_order_top10_products.png", dpi=300, bbox_inches="tight", facecolor="white")
plt.show()
plt.close()

# STEP 7: Graph - Total purchase order by category
plt.figure(figsize=(12, 7))

ax = sns.barplot(
    data=category_total,
    x="category",
    y="purchase_order_quantity",
    hue="category",
    palette="bright",
    edgecolor="black",
    linewidth=1.2,
    legend=False
)

for bar in ax.patches:
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f"{bar.get_height():,.0f}",
        ha="center",
        va="bottom",
        fontsize=12,
        fontweight="bold"
    )

plt.ylim(0, category_total["purchase_order_quantity"].max() * 1.15)
plt.title("Purchase Order Quantity by Category", fontsize=20)
plt.xlabel("Category", fontsize=14)
plt.ylabel("Total Purchase Order Quantity", fontsize=14)
plt.xticks(rotation=45, ha="right", fontsize=12)
plt.yticks(fontsize=12)
plt.ticklabel_format(style="plain", axis="y")
plt.tight_layout()

plt.savefig(f"{folder}/purchase_order_by_category.png", dpi=300, bbox_inches="tight", facecolor="white")
plt.show()
plt.close()