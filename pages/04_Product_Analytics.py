"""
GrowthIQ — Page 4: Product Analytics & Inventory Economics
==========================================================
Merchandise performance, category economics, promotional discount elasticity,
and warehouse stockout risk monitoring.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from src.visualisation.ui import (
    inject_custom_css,
    render_sidebar,
    render_metric_card,
    render_insights_box,
    render_table_with_export,
    COLOR_BURGUNDY,
    COLOR_GOLD,
    COLOR_TAUPE,
)
from src.analytics.products import (
    product_performance,
    category_performance,
    discount_effectiveness_analysis,
    inventory_watchlist,
)
from src.visualisation.charts import (
    plot_top_products_bar,
    plot_category_pie,
    plot_discount_tiers_bar,
    apply_theme,
    DISCRETE_PALETTE,
)

st.set_page_config(
    page_title="Product Analytics | GrowthIQ",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_custom_css()
ctx = render_sidebar()

orders = ctx["orders"]
items = ctx["order_items"]
products = ctx["products"]
inventory = ctx["inventory"]

st.markdown(
    """
    <div style="margin-bottom: 1.2rem;">
        <h1 style="margin-bottom: 0.1rem;">Product Analytics & Inventory Watchlist</h1>
        <div style="font-size: 0.88rem; color: #6B5C60;">
            Catalogue performance, merchandise margin elasticity, promotional discount efficiency, and warehouse reorder alerts.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Compute Product & Category Metrics
prod_perf = product_performance(orders, items, products)
cat_perf = category_performance(prod_perf)
discount_perf = discount_effectiveness_analysis(orders, items)
inv_df = inventory_watchlist(inventory, products)

# Summary Cards
total_units = prod_perf["units_sold"].sum() if not prod_perf.empty else 0
total_prod_rev = prod_perf["revenue_inr"].sum() if not prod_perf.empty else 0.0
overall_margin = (
    (prod_perf["gross_profit_inr"].sum() / total_prod_rev * 100) if total_prod_rev > 0 else 0.0
)
critical_stockouts = (inv_df["stock_status"] == "CRITICAL").sum() if not inv_df.empty else 0
reorders_needed = (inv_df["stock_status"] == "REORDER").sum() if not inv_df.empty else 0

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(render_metric_card("Total Units Sold", f"{total_units:,}", f"Across {len(prod_perf)} active SKUs"), unsafe_allow_html=True)
with c2:
    st.markdown(render_metric_card("Catalogue Sales", f"₹{total_prod_rev:,.0f}", "Realized net product sales"), unsafe_allow_html=True)
with c3:
    st.markdown(render_metric_card("Realized Margin", f"{overall_margin:.1f}%", f"Profit: ₹{prod_perf['gross_profit_inr'].sum():,.0f}"), unsafe_allow_html=True)
with c4:
    st.markdown(render_metric_card("Inventory Alerts", f"{critical_stockouts + reorders_needed} SKUs", f"{critical_stockouts} Critical | {reorders_needed} Reorder"), unsafe_allow_html=True)

# Product Insights Box
insights = []
if not prod_perf.empty:
    top_sku = prod_perf.iloc[0]
    insights.append(
        f"**Flagship Hero SKU:** **{top_sku['product_name']}** ({top_sku['category']}) is the top revenue generator, delivering **₹{top_sku['revenue_inr']:,.0f}** ({top_sku['units_sold']:,} units) with a realized margin of **{top_sku['realized_gross_margin_pct']:.1f}%**."
    )
if not discount_perf.empty:
    full_price = discount_perf[discount_perf["discount_tier"].str.contains("Full Price")]
    if not full_price.empty:
        fp_share = full_price.iloc[0]["revenue_share_pct"]
        fp_margin = full_price.iloc[0]["gross_margin_pct"]
        insights.append(
            f"**Promotional Discipline:** Full-price orders contribute **{fp_share:.1f}%** of revenue with a robust gross margin of **{fp_margin:.1f}%**. Protecting full-price brand equity sustains commercial health."
        )
if critical_stockouts > 0:
    critical_skus = ", ".join(inv_df[inv_df["stock_status"] == "CRITICAL"]["product_name"].head(3).tolist())
    insights.append(
        f"**Supply Chain Warning:** **{critical_stockouts} SKU(s)** ({critical_skus}) have breached safety stock thresholds and face imminent stockout risk. Immediate vendor purchase orders recommended."
    )

render_insights_box("Product Economics & Supply Chain Observations", insights)

st.markdown("---")

# Visualizations: Top SKUs & Category Mix
col1, col2 = st.columns([0.60, 0.40])
with col1:
    if not prod_perf.empty:
        st.plotly_chart(plot_top_products_bar(prod_perf, top_n=8), use_container_width=True)
    else:
        st.info("No product sales data.")

with col2:
    if not cat_perf.empty:
        st.plotly_chart(plot_category_pie(cat_perf), use_container_width=True)
    else:
        st.info("No category data.")

# Comprehensive Product Performance Table
st.subheader("SKU Performance & Margin Roster")
if not prod_perf.empty:
    display_prod = prod_perf[
        [
            "product_id",
            "product_name",
            "category",
            "target_gender",
            "list_price_inr",
            "unit_cost_inr",
            "units_sold",
            "revenue_inr",
            "revenue_share_pct",
            "gross_profit_inr",
            "realized_gross_margin_pct",
        ]
    ].copy()
    display_prod.columns = [
        "SKU ID",
        "Product Name",
        "Category",
        "Gender",
        "List Price (INR)",
        "Unit Cost (INR)",
        "Units Sold",
        "Revenue (INR)",
        "Revenue Share (%)",
        "Gross Profit (INR)",
        "Gross Margin (%)",
    ]

    render_table_with_export(
        display_prod,
        filename="growthiq_sku_performance_roster",
        label="Export Product Roster (CSV)",
        format_dict={
            "List Price (INR)": "₹{:,.0f}",
            "Unit Cost (INR)": "₹{:,.0f}",
            "Revenue (INR)": "₹{:,.0f}",
            "Gross Profit (INR)": "₹{:,.0f}",
            "Revenue Share (%)": "{:.1f}%",
            "Gross Margin (%)": "{:.1f}%",
            "Units Sold": "{:,}",
        },
    )

st.markdown("---")

# Promotional Discount Elasticity Section
st.subheader("Promotional Discount Tier Analysis")
st.caption(
    "Evaluation of order volume and gross margin across discount bands. "
    "Note: While deeper discounts correlate with higher unit volume, establishing true price elasticity requires controlled A/B price testing."
)

col_d1, col_d2 = st.columns([0.55, 0.45])
with col_d1:
    if not discount_perf.empty:
        st.plotly_chart(plot_discount_tiers_bar(discount_perf), use_container_width=True)

with col_d2:
    if not discount_perf.empty:
        d_display = discount_perf[
            ["discount_tier", "order_count", "units_sold", "revenue_inr", "revenue_share_pct", "gross_profit_inr", "gross_margin_pct"]
        ].copy()
        d_display.columns = ["Discount Band", "Orders", "Units", "Revenue (INR)", "Rev Share (%)", "Profit (INR)", "Margin (%)"]
        st.markdown("#### Discount Band Breakdown")
        st.dataframe(
            d_display.style.format(
                {
                    "Revenue (INR)": "₹{:,.0f}",
                    "Profit (INR)": "₹{:,.0f}",
                    "Rev Share (%)": "{:.1f}%",
                    "Margin (%)": "{:.1f}%",
                    "Orders": "{:,}",
                    "Units": "{:,}",
                }
            ),
            use_container_width=True,
            hide_index=True,
        )

st.markdown("---")

# Inventory Watchlist Section
st.subheader("Inventory Stockout Risk & Replenishment Watchlist")
st.caption("Warehouse stock status categorized by safety stock thresholds and replenishment lead times.")

if not inv_df.empty:
    display_inv = inv_df[
        [
            "product_id",
            "product_name",
            "category",
            "on_hand_units",
            "safety_stock_units",
            "reorder_point_units",
            "stock_status",
            "recommended_reorder_qty",
            "lead_time_days",
            "inventory_capital_tied_inr",
        ]
    ].copy()
    display_inv.columns = [
        "SKU ID",
        "Product Name",
        "Category",
        "On Hand",
        "Safety Stock",
        "Reorder Point",
        "Stock Status",
        "Recommended Reorder",
        "Lead Time (Days)",
        "Capital Tied (INR)",
    ]

    render_table_with_export(
        display_inv,
        filename="growthiq_inventory_watchlist",
        label="Export Inventory Watchlist (CSV)",
        format_dict={
            "Capital Tied (INR)": "₹{:,.0f}",
            "On Hand": "{:,}",
            "Safety Stock": "{:,}",
            "Reorder Point": "{:,}",
            "Recommended Reorder": "{:,}",
            "Lead Time (Days)": "{:} days",
        },
    )

