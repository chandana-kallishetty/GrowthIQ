"""
GrowthIQ — Page 1: Executive Overview
====================================
High-level strategic cockpit for executive leadership: revenue velocity,
unit economics, blended marketing efficiency, and merchandise mix.
"""

import streamlit as st
import pandas as pd
from src.visualisation.ui import (
    inject_custom_css,
    render_sidebar,
    render_metric_card,
    render_insights_box,
    render_table_with_export,
    COLOR_BURGUNDY,
    COLOR_GOLD,
)
from src.analytics.kpis import kpi_summary, order_facts, monthly_kpi_trends
from src.analytics.products import category_performance, product_performance
from src.analytics.attribution import compute_attribution_models
from src.visualisation.charts import (
    plot_revenue_trend,
    plot_category_pie,
    plot_channel_comparison,
)

st.set_page_config(
    page_title="Executive Overview | GrowthIQ",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_custom_css()
ctx = render_sidebar()

orders = ctx["orders"]
sessions = ctx["sessions"]
items = ctx["order_items"]
products = ctx["products"]
spend = ctx["campaign_spend"]

# Top Page Banner
st.markdown(
    """
    <div style="margin-bottom: 1.2rem;">
        <h1 style="margin-bottom: 0.1rem;">Executive Performance Overview</h1>
        <div style="font-size: 0.88rem; color: #6B5C60;">
            Comprehensive commercial pulse: top-line revenue, blended unit economics, gross margins, and acquisition returns.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Compute Top-Level KPIs
facts = order_facts(orders, items)
kpis = kpi_summary(orders, sessions, items, spend_df=spend)

# Executive KPI Cards - Row 1: Commercial Volume & Margin
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(
        render_metric_card("Net Realized Revenue", f"₹{kpis['revenue']:,.0f}", f"Gross: ₹{kpis['gross_revenue']:,.0f} (Excl. Refunds)"),
        unsafe_allow_html=True,
    )
with c2:
    st.markdown(
        render_metric_card("Completed Orders", f"{kpis['orders']:,}", f"{kpis['units_sold']:,} total units sold"),
        unsafe_allow_html=True,
    )
with c3:
    st.markdown(
        render_metric_card("Average Order Value", f"₹{kpis['aov']:,.0f}", f"Units / order: {(kpis['units_sold']/kpis['orders']):.1f}" if kpis['orders'] > 0 else ""),
        unsafe_allow_html=True,
    )
with c4:
    st.markdown(
        render_metric_card("Gross Profit Margin", f"{kpis['gross_margin_pct']:.1f}%", f"Profit: ₹{kpis['gross_profit']:,.0f}"),
        unsafe_allow_html=True,
    )

# Executive KPI Cards - Row 2: Marketing & Growth Efficiency
c5, c6, c7, c8 = st.columns(4)
with c5:
    st.markdown(
        render_metric_card("Total Marketing Spend", f"₹{kpis['spend']:,.0f}", f"Across {spend['channel'].nunique() if not spend.empty else 0} channels"),
        unsafe_allow_html=True,
    )
with c6:
    st.markdown(
        render_metric_card("Blended ROAS", f"{kpis['roas']:.2f}x", "Attributed Revenue / Spend"),
        unsafe_allow_html=True,
    )
with c7:
    st.markdown(
        render_metric_card("Blended Paid CAC", f"₹{kpis['cac']:,.0f}", f"Across {kpis['customers']:,} purchasers"),
        unsafe_allow_html=True,
    )
with c8:
    st.markdown(
        render_metric_card("Session Conversion Rate", f"{kpis['conversion']:.2%}", f"{kpis['sessions']:,} total sessions"),
        unsafe_allow_html=True,
    )

# Dynamic Automated Executive Insights
monthly_df = monthly_kpi_trends(facts)
cat_df = category_performance(product_performance(orders, items, products))

insights = []
if not monthly_df.empty:
    best_month = monthly_df.loc[monthly_df["revenue_inr"].idxmax()]
    insights.append(
        f"**Peak Revenue Velocity:** **{best_month['month']}** was the highest revenue month generating **₹{best_month['revenue_inr']:,.0f}** across **{best_month['orders']:,}** orders."
    )
if not cat_df.empty:
    top_cat = cat_df.iloc[0]
    insights.append(
        f"**Merchandise Powerhouse:** **{top_cat['category']}** leads the portfolio contributing **{top_cat['revenue_share_pct']:.1f}%** of total sales (₹{top_cat['revenue_inr']:,.0f}) with an average gross margin of **{top_cat['gross_margin_pct']:.1f}%**."
    )
if kpis["repeat_rate"] > 0:
    insights.append(
        f"**Customer Retention Health:** **{kpis['repeat_customers']:,}** customers ({kpis['repeat_rate']:.1%}) have placed repeat orders, demonstrating steady baseline customer retention."
    )
if kpis["roas"] > 0:
    insights.append(
        f"**Capital Efficiency:** The portfolio achieved a blended return on advertising spend (ROAS) of **{kpis['roas']:.2f}x** at a blended acquisition cost of **₹{kpis['cac']:,.0f}** per buyer."
    )

render_insights_box("Executive Performance Summary & Strategic Highlights", insights)

st.markdown("---")

# Main Visualizations: Revenue Trend & Merchandise Mix
col_left, col_right = st.columns([0.62, 0.38])
with col_left:
    if not monthly_df.empty:
        st.plotly_chart(plot_revenue_trend(monthly_df), use_container_width=True)
    else:
        st.info("No transaction data available for the selected range.")

with col_right:
    if not cat_df.empty:
        st.plotly_chart(plot_category_pie(cat_df), use_container_width=True)
    else:
        st.info("No merchandise data available.")

# Monthly Trajectory Table with Download
st.subheader("Monthly Commercial & Unit Economics Trajectory")
if not monthly_df.empty:
    display_monthly = monthly_df[
        ["month", "orders", "units", "revenue_inr", "aov", "gross_profit_inr", "gross_margin_pct", "mom_revenue_growth_pct"]
    ].copy()
    display_monthly.columns = [
        "Month",
        "Orders",
        "Units Sold",
        "Revenue (INR)",
        "AOV (INR)",
        "Gross Profit (INR)",
        "Gross Margin (%)",
        "MoM Growth (%)",
    ]
    render_table_with_export(
        display_monthly,
        filename="growthiq_monthly_executive_kpis",
        label="Export Monthly KPIs (CSV)",
        format_dict={
            "Revenue (INR)": "₹{:,.0f}",
            "AOV (INR)": "₹{:,.0f}",
            "Gross Profit (INR)": "₹{:,.0f}",
            "Gross Margin (%)": "{:.1f}%",
            "MoM Growth (%)": "{:+.1f}%",
            "Orders": "{:,}",
            "Units Sold": "{:,}",
        },
    )

