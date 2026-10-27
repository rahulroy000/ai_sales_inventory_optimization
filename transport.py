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