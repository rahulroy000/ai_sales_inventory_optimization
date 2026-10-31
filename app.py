import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

# ============================================================
# INVENTRA-INSPIRED | AI SALES & INVENTORY OPTIMIZATION
# Original Streamlit implementation using the project's CSV.
# ============================================================

st.set_page_config(
    page_title="Stockwise | Sales & Inventory",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------- THEME -----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');

:root {
  --ink: #17211f;
  --muted: #75817d;
  --line: #e8eeeb;
  --canvas: #f6f8f6;
  --panel: #ffffff;
  --green: #176b52;
  --green-soft: #e9f4ef;
  --amber: #b7791f;
  --amber-soft: #fff5df;
  --red: #bd4b4b;
  --red-soft: #fff0ef;
}
html, body, [class*="css"] {
  font-family: 'DM Sans', sans-serif;
}
.stApp { background: var(--canvas); color: var(--ink); }
.block-container {
  max-width: 1500px;
  padding: 1.6rem 2.2rem 2.4rem;
}
[data-testid="stSidebar"] {
  background: #fff;
  border-right: 1px solid var(--line);
}
[data-testid="stSidebar"] > div:first-child { padding-top: 1.5rem; }
.brand {
  display:flex; align-items:center; gap:10px;
  padding: 5px 4px 18px 4px;
}
.brand-mark {
  width:38px;height:38px;border-radius:12px;
  background:#176b52;color:white;display:flex;
  align-items:center;justify-content:center;
  font-size:19px;font-weight:800;
}
.brand-name {font-family:'Manrope';font-weight:800;font-size:18px;color:#17211f;line-height:1.1}
.brand-sub {font-size:10px;color:#84918b;letter-spacing:1.4px;text-transform:uppercase;margin-top:4px}
.nav-caption {
  color:#9aa49f;font-size:10px;font-weight:700;
  letter-spacing:1.5px;text-transform:uppercase;
  margin:18px 0 8px 8px;
}
.page-eyebrow {
  color:#176b52;font-size:11px;font-weight:700;
  text-transform:uppercase;letter-spacing:1.6px;margin-bottom:7px;
}
.page-title {
  font-family:'Manrope';font-size:29px;font-weight:800;
  color:#17211f;letter-spacing:-1px;margin:0;
}
.page-subtitle {color:#7a8580;font-size:13px;margin-top:5px}
.topline {
  display:flex;align-items:center;justify-content:space-between;
  margin-bottom:22px;
}
.panel {
  background:#fff;border:1px solid var(--line);
  border-radius:16px;padding:18px 20px;
}
.panel-title {font-family:'Manrope';font-weight:700;font-size:15px;color:#1c2924}
.panel-sub {font-size:12px;color:#87928d;margin-top:3px}
.kpi {
  background:#fff;border:1px solid var(--line);
  border-radius:15px;padding:17px 18px;min-height:112px;
}
.kpi-label {font-size:12px;color:#7d8983;font-weight:500}
.kpi-value {font-family:'Manrope';font-size:25px;font-weight:800;color:#18251f;margin-top:8px;letter-spacing:-.7px}
.kpi-foot {font-size:11px;color:#89958f;margin-top:4px}
.kpi-icon {
  float:right;width:31px;height:31px;border-radius:10px;
  display:flex;align-items:center;justify-content:center;
  background:#edf5f0;font-size:15px;
}
.pill {
  display:inline-block;border-radius:20px;padding:4px 9px;
  font-size:10px;font-weight:700;letter-spacing:.2px;
}
.pill-green {background:#e8f4ed;color:#176b52}
.pill-amber {background:#fff3dc;color:#a56b16}
.pill-red {background:#ffeded;color:#b64b4b}
.insight {
  background:#f0f7f3;border:1px solid #deede4;
  border-radius:14px;padding:15px 17px;color:#315e4c;
  font-size:13px;line-height:1.55;
}
hr {border-color:var(--line)!important;}
div[data-testid="stDataFrame"] {
  border:1px solid var(--line);border-radius:12px;overflow:hidden;
}
.stButton button {
  border-radius:9px;border:1px solid #dfe8e3;
  font-weight:600;min-height:38px;
}
.stButton button[kind="primary"] {
  background:#176b52;border-color:#176b52;color:#fff;
}
div[data-testid="stSelectbox"] label,
div[data-testid="stDateInput"] label,
div[data-testid="stTextInput"] label {font-size:12px;font-weight:600;color:#52615a}
[data-testid="stMetric"] {
  background:#fff;border:1px solid var(--line);
  border-radius:14px;padding:14px 16px;
}
[data-testid="stMetricLabel"] {font-size:12px;color:#7d8983}
[data-testid="stMetricValue"] {font-family:'Manrope';font-weight:800;color:#18251f}
footer {visibility:hidden}
#MainMenu {visibility:hidden}
</style>
""", unsafe_allow_html=True)

# ----------------------------- DATA -----------------------------
DATA_PATH = Path("data/processed/cleaned_data.csv")

@st.cache_data
def load_data(path_string):
    path = Path(path_string)
    if not path.exists():
        return None
    data = pd.read_csv(path)
    data.columns = data.columns.str.strip()
    if "date" in data.columns:
        data["date"] = pd.to_datetime(data["date"], errors="coerce")
    numeric_cols = [
        "quantity_sold", "sales_revenue_inr", "purchase_order_quantity",
        "current_stock", "reorder_level", "safety_stock", "delivery_days",
        "shipping_distance_km", "lead_time_days", "discount",
        "unit_cost_inr", "unit_price_inr", "order_cost_inr"
    ]
    for col in numeric_cols:
        if col in data.columns:
            data[col] = pd.to_numeric(data[col], errors="coerce")
    return data

df = load_data(str(DATA_PATH))
if df is None:
    st.error(f"Dataset not found: `{DATA_PATH}`")
    st.info("Run the app from your project root, where the `data/processed/cleaned_data.csv` file exists.")
    st.stop()
if df.empty:
    st.warning("The cleaned dataset is empty.")
    st.stop()

def has(*cols, frame=None):
    frame = df if frame is None else frame
    return all(c in frame.columns for c in cols)

def money(value):
    return f"₹{value:,.0f}"

def safe_sum(frame, col):
    return frame[col].sum() if col in frame.columns else 0

def heading(eyebrow, title, subtitle):
    st.markdown(
        f'<div class="topline"><div><div class="page-eyebrow">{eyebrow}</div>'
        f'<div class="page-title">{title}</div>'
        f'<div class="page-subtitle">{subtitle}</div></div></div>',
        unsafe_allow_html=True
    )

def panel_heading(title, subtitle=None):
    st.markdown(f'<div class="panel-title">{title}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="panel-sub">{subtitle}</div>', unsafe_allow_html=True)

def kpi_card(label, value, foot, icon):
    st.markdown(
        f'<div class="kpi"><div class="kpi-icon">{icon}</div>'
        f'<div class="kpi-label">{label}</div><div class="kpi-value">{value}</div>'
        f'<div class="kpi-foot">{foot}</div></div>',
        unsafe_allow_html=True
    )

def filtered_data(frame):
    out = frame.copy()
    if "date" in out.columns and out["date"].notna().any():
        dates = out["date"].dropna()
        min_d, max_d = dates.min().date(), dates.max().date()
        chosen = st.sidebar.date_input(
            "Date range", value=(min_d, max_d),
            min_value=min_d, max_value=max_d,
            key="date_filter"
        )
        if isinstance(chosen, tuple) and len(chosen) == 2:
            start, end = chosen
            out = out[out["date"].dt.date.between(start, end)]
    if "category" in out.columns:
        categories = sorted(out["category"].dropna().astype(str).unique())
        selected = st.sidebar.multiselect(
            "Product category", categories, default=[],
            placeholder="All categories", key="category_filter"
        )
        if selected:
            out = out[out["category"].astype(str).isin(selected)]
    return out

# ----------------------------- SIDEBAR -----------------------------
with st.sidebar:
    st.markdown("""
    <div class="brand">
      <div class="brand-mark">S</div>
      <div><div class="brand-name">Stockwise</div>
      <div class="brand-sub">AI Inventory Suite</div></div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="nav-caption">Workspace</div>', unsafe_allow_html=True)
    page = st.radio(
        "Navigation",
        ["Overview", "Sales analytics", "Products", "Inventory",
         "Purchasing", "Logistics", "AI insights", "Data explorer"],
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.markdown('<div class="nav-caption">Filters</div>', unsafe_allow_html=True)
    data = filtered_data(df)
    st.markdown("---")
    st.caption(f"● Dataset connected")
    st.caption(f"{len(data):,} records in current view")
    st.caption("Stockwise · Project workspace")

# ----------------------------- HEADER -----------------------------
if page == "Overview":
    heading("WORKSPACE / OVERVIEW", "Good morning", "Here’s what’s happening across your sales and inventory.")
elif page == "Sales analytics":
    heading("ANALYTICS / SALES", "Sales analytics", "Understand revenue, demand and category performance.")
elif page == "Products":
    heading("CATALOG / PRODUCTS", "Product performance", "Explore your catalog and identify top-performing products.")
elif page == "Inventory":
    heading("OPERATIONS / INVENTORY", "Inventory health", "Monitor stock coverage and identify records that need replenishment.")
elif page == "Purchasing":
    heading("OPERATIONS / PURCHASING", "Purchase overview", "Track purchase quantities across categories and products.")
elif page == "Logistics":
    heading("OPERATIONS / LOGISTICS", "Logistics performance", "Compare delivery timelines and partner performance.")
elif page == "AI insights":
    heading("INTELLIGENCE / AI", "AI insights", "Explore model-ready data and decision-support signals.")
else:
    heading("WORKSPACE / DATA", "Data explorer", "Inspect, filter and export your processed dataset.")

# ----------------------------- OVERVIEW -----------------------------
if page == "Overview":
    revenue = safe_sum(data, "sales_revenue_inr")
    units = safe_sum(data, "quantity_sold")
    product_count = data["product_name"].nunique() if has("product_name", frame=data) else 0
    order_count = data["order_id"].nunique() if has("order_id", frame=data) else len(data)
    reorder_count = 0
    if has("current_stock", "reorder_level", frame=data):
        reorder_count = int((data["current_stock"] <= data["reorder_level"]).sum())

    k1, k2, k3, k4 = st.columns(4)
    with k1: kpi_card("Total revenue", money(revenue), "Across selected period", "₹")
    with k2: kpi_card("Units sold", f"{units:,.0f}", "Total quantity sold", "↗")
    with k3: kpi_card("Total orders", f"{order_count:,}", "Unique order IDs where available", "▤")
    with k4: kpi_card("Reorder signals", f"{reorder_count:,}", "Rows at or below reorder level", "⚑")

    st.write("")
    left, right = st.columns([1.55, 1])
    with left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        panel_heading("Revenue overview", "Monthly revenue trend")
        if has("date", "sales_revenue_inr", frame=data):
            tmp = data.dropna(subset=["date"]).copy()
            if not tmp.empty:
                tmp["Month"] = tmp["date"].dt.to_period("M").astype(str)
                monthly = tmp.groupby("Month")["sales_revenue_inr"].sum().sort_index()
                st.area_chart(monthly, color="#238565", height=260)
            else:
                st.info("No valid dates available for the selected filters.")
        else:
            st.info("Date and revenue columns are required for this chart.")
        st.markdown('</div>', unsafe_allow_html=True)
    with right:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        panel_heading("Sales by category", "Revenue contribution")
        if has("category", "sales_revenue_inr", frame=data):
            cat = data.groupby("category")["sales_revenue_inr"].sum().sort_values(ascending=False)
            st.bar_chart(cat, color="#238565", height=260)
        else:
            st.info("Category and revenue columns are required.")
        st.markdown('</div>', unsafe_allow_html=True)

    st.write("")
    left, right = st.columns([1.2, 1])
    with left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        panel_heading("Top products", "Best sellers by units sold")
        if has("product_name", "quantity_sold", frame=data):
            top = data.groupby("product_name")["quantity_sold"].sum().nlargest(7).reset_index()
            top.columns = ["Product", "Units sold"]
            st.dataframe(top, hide_index=True, use_container_width=True)
        else:
            st.info("Product and quantity columns are unavailable.")
        st.markdown('</div>', unsafe_allow_html=True)
    with right:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        panel_heading("Inventory attention", "Rows at or below reorder level")
        if has("product_name", "current_stock", "reorder_level", frame=data):
            risk = data[data["current_stock"] <= data["reorder_level"]]
            if not risk.empty:
                cols = ["product_name", "current_stock", "reorder_level"]
                if "warehouse_city" in risk.columns: cols.append("warehouse_city")
                st.dataframe(risk[cols].drop_duplicates().head(7), hide_index=True, use_container_width=True)
            else:
                st.markdown('<div class="insight">No records currently fall at or below their reorder level in this filtered view.</div>', unsafe_allow_html=True)
        else:
            st.info("Stock and reorder columns are unavailable.")
        st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------- SALES -----------------------------
elif page == "Sales analytics":
    if has("sales_revenue_inr", frame=data):
        a, b, c = st.columns(3)
        a.metric("Revenue", money(data["sales_revenue_inr"].sum()))
        b.metric("Units sold", f"{safe_sum(data, 'quantity_sold'):,.0f}")
        b2 = data["sales_revenue_inr"].mean()
        c.metric("Average revenue / row", money(b2))
    l, r = st.columns(2)
    with l:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        panel_heading("Monthly units sold")
        if has("date", "quantity_sold", frame=data):
            tmp = data.dropna(subset=["date"]).copy()
            tmp["Month"] = tmp["date"].dt.to_period("M").astype(str)
            st.line_chart(tmp.groupby("Month")["quantity_sold"].sum().sort_index(), color="#238565")
        else: st.info("Required columns unavailable.")
        st.markdown('</div>', unsafe_allow_html=True)
    with r:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        panel_heading("Revenue by category")
        if has("category", "sales_revenue_inr", frame=data):
            st.bar_chart(data.groupby("category")["sales_revenue_inr"].sum().sort_values(ascending=False), color="#238565")
        else: st.info("Required columns unavailable.")
        st.markdown('</div>', unsafe_allow_html=True)
    st.write("")
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    panel_heading("Revenue leaders", "Top products by revenue")
    if has("product_name", "sales_revenue_inr", frame=data):
        leaders = data.groupby("product_name")["sales_revenue_inr"].sum().nlargest(15).reset_index()
        leaders.columns = ["Product", "Revenue (INR)"]
        st.dataframe(leaders, hide_index=True, use_container_width=True)
    else: st.info("Product and revenue columns unavailable.")
    st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------- PRODUCTS -----------------------------
elif page == "Products":
    if has("product_name", frame=data):
        search = st.text_input("Search products", placeholder="Type a product name...")
        products = data.copy()
        if search:
            products = products[products["product_name"].astype(str).str.contains(search, case=False, na=False)]
        metrics = []
        group_cols = ["product_name"]
        aggregations = {}
        if "quantity_sold" in products.columns: aggregations["quantity_sold"] = "sum"
        if "sales_revenue_inr" in products.columns: aggregations["sales_revenue_inr"] = "sum"
        if "category" in products.columns: aggregations["category"] = "first"
        if aggregations:
            summary = products.groupby("product_name").agg(aggregations).reset_index()
            summary = summary.rename(columns={
                "product_name":"Product", "category":"Category",
                "quantity_sold":"Units sold", "sales_revenue_inr":"Revenue (INR)"
            })
            st.dataframe(summary.sort_values(summary.columns[-1], ascending=False) if len(summary.columns)>1 else summary,
                         hide_index=True, use_container_width=True)
        else:
            st.dataframe(products, use_container_width=True, hide_index=True)
    else:
        st.info("The product_name column is not available.")

# ----------------------------- INVENTORY -----------------------------
elif page == "Inventory":
    required = ["product_name", "current_stock", "reorder_level"]
    if has(*required, frame=data):
        inv = data.copy().dropna(subset=["current_stock", "reorder_level"])
        inv["Status"] = np.where(inv["current_stock"] <= inv["reorder_level"], "Reorder", "Healthy")
        reorder = inv[inv["Status"] == "Reorder"]
        healthy = inv[inv["Status"] == "Healthy"]
        c1, c2, c3 = st.columns(3)
        c1.metric("Reorder records", f"{len(reorder):,}")
        c2.metric("Healthy records", f"{len(healthy):,}")
        c3.metric("Average stock", f"{inv['current_stock'].mean():,.1f}")
        st.write("")
        st.markdown('<div class="insight">Inventory signal is calculated from current_stock ≤ reorder_level. It is a rule-based alert, not an ML stockout prediction.</div>', unsafe_allow_html=True)
        st.write("")
        show_cols = ["product_name", "current_stock", "reorder_level", "Status"]
        for optional in ["category", "warehouse_city", "warehouse_state", "safety_stock"]:
            if optional in inv.columns: show_cols.append(optional)
        tab1, tab2 = st.tabs(["Needs attention", "All inventory"])
        with tab1:
            st.dataframe(reorder[show_cols].drop_duplicates(), use_container_width=True, hide_index=True)
        with tab2:
            st.dataframe(inv[show_cols], use_container_width=True, hide_index=True)
    else:
        st.warning("Inventory view requires product_name, current_stock and reorder_level.")

# ----------------------------- PURCHASING -----------------------------
elif page == "Purchasing":
    if has("category", "purchase_order_quantity", frame=data):
        a, b = st.columns(2)
        with a:
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            panel_heading("Purchase quantity by category")
            st.bar_chart(data.groupby("category")["purchase_order_quantity"].sum().sort_values(ascending=False), color="#238565")
            st.markdown('</div>', unsafe_allow_html=True)
        with b:
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            panel_heading("Top purchased products")
            if "product_name" in data.columns:
                top = data.groupby("product_name")["purchase_order_quantity"].sum().nlargest(10)
                st.bar_chart(top, color="#238565")
            else: st.info("Product names unavailable.")
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Category and purchase_order_quantity columns are required.")

# ----------------------------- LOGISTICS -----------------------------
elif page == "Logistics":
    if has("logistics_partner", "delivery_days", frame=data):
        stats = data.groupby("logistics_partner").agg(
            Average_days=("delivery_days", "mean"),
            Min_days=("delivery_days", "min"),
            Max_days=("delivery_days", "max"),
            Records=("delivery_days", "count")
        ).sort_values("Average_days")
        a, b = st.columns([1, 1.2])
        with a:
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            panel_heading("Average delivery days")
            st.bar_chart(stats["Average_days"], color="#238565")
            st.markdown('</div>', unsafe_allow_html=True)
        with b:
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            panel_heading("Partner comparison")
            st.dataframe(stats.round(2), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Logistics partner and delivery_days columns are required.")

# ----------------------------- AI INSIGHTS -----------------------------
elif page == "AI insights":
    st.markdown('<div class="insight"><b>AI workspace</b><br>Connect trained models here to generate predictions. The current page shows descriptive signals from your dataset; it does not claim to run a trained model.</div>', unsafe_allow_html=True)
    st.write("")
    if has("product_name", "quantity_sold", frame=data):
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        panel_heading("Demand signals", "Products with highest historical sales volume")
        demand = data.groupby("product_name")["quantity_sold"].sum().sort_values(ascending=False).head(10)
        st.bar_chart(demand, color="#238565")
        st.markdown('</div>', unsafe_allow_html=True)
    st.write("")
    if has("logistics_partner", "delivery_days", frame=data):
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        panel_heading("Delivery signals", "Average observed delivery time by partner")
        delivery = data.groupby("logistics_partner")["delivery_days"].mean().sort_values()
        st.bar_chart(delivery, color="#238565")
        st.markdown('</div>', unsafe_allow_html=True)
    st.caption("Next integration: load the saved regression/classification pipeline and add prediction forms.")

# ----------------------------- DATA EXPLORER -----------------------------
elif page == "Data explorer":
    c1, c2, c3 = st.columns(3)
    c1.metric("Rows", f"{len(data):,}")
    c2.metric("Columns", f"{len(data.columns):,}")
    c3.metric("Missing cells", f"{int(data.isna().sum().sum()):,}")
    search_col = st.selectbox("Filter by column", ["All columns"] + data.columns.tolist())
    if search_col != "All columns":
        value = st.text_input(f"Search in {search_col}")
        view = data[data[search_col].astype(str).str.contains(value, case=False, na=False)] if value else data
    else:
        view = data
    st.dataframe(view, use_container_width=True, hide_index=True)
    with st.expander("Missing value summary"):
        missing = data.isna().sum().rename("Missing values")
        st.dataframe(missing[missing > 0].to_frame(), use_container_width=True)
    st.download_button(
        "Download current view as CSV",
        data=view.to_csv(index=False).encode("utf-8"),
        file_name="stockwise_filtered_data.csv",
        mime="text/csv"
    )

# ----------------------------- FOOTER -----------------------------
st.markdown("---")
st.caption("Stockwise · AI Sales & Inventory Optimization · Built with Streamlit")
