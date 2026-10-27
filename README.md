# AI Sales & Inventory Optimization

An end-to-end supply chain analytics project built with plain Python scripts (no notebooks). It explores, cleans and analyzes sales, inventory, purchasing and logistics data to answer real business questions, and prepares the ground for forecasting and inventory-optimization models.

## Business Problem

Retail and supply chain teams need to know what sells, where it sells, how much stock to order, and which logistics partners deliver reliably. This project answers those questions with data and turns the answers into charts and tables that support decisions.

## Dataset

A 30-column order-level dataset (`data/raw/data.csv`) covering:

| Area | Columns (examples) |
|---|---|
| Sales | `date`, `order_id`, `platform`, `quantity_sold`, `sales_revenue_inr`, discount, unit cost/price |
| Product & Supplier | `product_id`, `product_name`, `category`, `supplier_id` |
| Warehouse | `store_id`, `warehouse_id`, `facility_type`, `warehouse_city`, `warehouse_state`, country |
| Inventory | `current_stock`, `reorder_level`, `safety_stock`, `lead_time_days`, MOQ |
| Purchasing | `purchase_order_quantity`, `order_cost_inr`, `order_status` |
| Logistics | `logistics_partner`, `shipping_distance_km`, `delivery_days` |

## Project Structure

```
ai_sales_inventory_optimization/
├── data/
│   ├── raw/data.csv                  # original dataset
│   └── processed/cleaned_data.csv    # output of data_clean.py
├── outputs/
│   ├── most_sell/                    # sales charts and tables
│   ├── purchase/                     # purchase-order charts and tables
│   └── transport/                    # logistics charts and tables
├── business_decisions.txt            # business questions the project answers
├── libraries_import.py               # checks the environment
├── know_data.py                      # data exploration
├── data_clean.py                     # data cleaning
├── most_sell.py                      # sales analysis
├── purchase.py                       # purchase-order analysis
├── transport.py                      # logistics analysis
└── requirements.txt
```

## Workflow

1. **Setup** – `libraries_import.py` confirms pandas, NumPy, Matplotlib, Seaborn and scikit-learn are installed.
2. **Explore** – `know_data.py` inspects shape, dtypes, missing values, duplicates, summary statistics, and simple filters/group-bys.
3. **Clean** – `data_clean.py` fills missing values in categorical and numeric columns, standardizes text (trim, consistent capitalization), and saves `cleaned_data.csv`.
4. **Analyze & Visualize** – the three analysis scripts read the cleaned data and produce charts and CSV tables.

## Analyses and Key Questions

**Sales (`most_sell.py`)**
- Monthly units sold by product category
- Monthly revenue by product category
- Best-selling product in each category, by quantity and by revenue
- School Backpack: top 10 warehouse locations by quantity sold

**Purchasing (`purchase.py`)**
- Top 10 products by purchase order quantity
- Top product in each category
- Total purchase order quantity by category

**Logistics (`transport.py`)** – focused on School Backpack
- Logistics partner usage (pie chart)
- Average delivery days per partner (bar chart)
- Delivery-time spread per partner (box plot)

## Outputs

All charts are saved as high-resolution PNGs (300 dpi) and supporting tables as CSVs in the `outputs/` subfolders, for example:

- `monthly_quantity_by_category.png`, `monthly_revenue_by_category.png`
- `top_product_by_quantity.png`, `top_product_by_revenue.png`
- `school_backpack_by_location.png`
- `purchase_order_top10_products.png`, `purchase_order_by_category.png`
- `school_backpack_logistics_pie.png`, `school_backpack_delivery_days_bar.png`, `school_backpack_delivery_days_box.png`

## How to Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Place the dataset at data/raw/data.csv

# 3. Run the scripts in order
python libraries_import.py
python know_data.py
python data_clean.py        # must run before the analysis scripts
python most_sell.py
python purchase.py
python transport.py
```

## Tech Stack

Python · pandas · NumPy · Matplotlib · Seaborn · scikit-learn

## Data Cleaning Notes

- Missing values in `platform`, `category`, `warehouse_city`, `order_status`, `lead_time_days` and `shipping_distance_km` are filled by randomly sampling from each column's five most frequent values.
- This keeps the dataset complete but can slightly distort distributions. Re-running the script can give slightly different results unless a random seed is set (e.g. `np.random.seed(42)`).

## Next Steps

- Demand and sales forecasting (including festive-season effects)
- Reorder-point and safety-stock optimization
- Supplier and logistics-partner performance scoring
- Dashboard and written case study

## Author

*Rahul Roy* · [LinkedIn](https://www.linkedin.com/in/rahul-royy/) · [GitHub](https://github.com/rahulroy000)