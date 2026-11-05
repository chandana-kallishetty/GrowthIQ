"""
GrowthIQ — Page 2: Marketing Performance & Attribution
======================================================
Deep dive into acquisition channel efficiency, campaign-level unit economics,
and First-Touch vs. Last-Touch multi-touch attribution comparisons.
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
from src.analytics.attribution import compute_attribution_models
from src.visualisation.charts import (
    plot_channel_comparison,
    plot_spend_vs_revenue_bubble,
    apply_theme,
    DISCRETE_PALETTE,
)

st.set_page_config(
    page_title="Marketing Performance | GrowthIQ",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_custom_css()
ctx = render_sidebar()

orders = ctx["orders"]
sessions = ctx["sessions"]
items = ctx["order_items"]
spend = ctx["campaign_spend"]
campaigns = ctx["campaigns"]

st.markdown(
    """
    <div style="margin-bottom: 1.2rem;">
        <h1 style="margin-bottom: 0.1rem;">Marketing & Attribution Intelligence</h1>
        <div style="font-size: 0.88rem; color: #6B5C60;">
            Multi-touch channel efficiency, campaign-level unit economics (ROAS, CAC, CTR, CPC), and attribution role comparisons.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Compute Attribution Comparison
comp, ft_agg, lt_agg = compute_attribution_models(orders, sessions, items, spend_df=spend)

# Top Channel Summary Cards
total_spend = comp["spend_inr"].sum() if not comp.empty else 0.0
total_lt_rev = comp["lt_revenue_inr"].sum() if not comp.empty else 0.0
blended_roas = (total_lt_rev / total_spend) if total_spend > 0 else 0.0
total_buyers = comp["lt_customers"].sum() if not comp.empty else 0
blended_cac = (total_spend / total_buyers) if total_buyers > 0 else 0.0

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(render_metric_card("Marketing Outlay", f"₹{total_spend:,.0f}", "Paid media & lifecycle channels"), unsafe_allow_html=True)
with c2:
    st.markdown(render_metric_card("Attributed Sales", f"₹{total_lt_rev:,.0f}", "Last-touch attributed revenue"), unsafe_allow_html=True)
with c3:
    st.markdown(render_metric_card("Blended ROAS", f"{blended_roas:.2f}x", "Revenue / Total Spend"), unsafe_allow_html=True)
with c4:
    st.markdown(render_metric_card("Acquisition CAC", f"₹{blended_cac:,.0f}", "Spend / Attributed Customers"), unsafe_allow_html=True)

# Attribution Insights Box
insights = []
if not comp.empty:
    paid_comp = comp[comp["spend_inr"] > 0]
    if not paid_comp.empty:
        best_roas_ch = paid_comp.loc[paid_comp["lt_roas"].idxmax()]
        lowest_cac_ch = paid_comp.loc[paid_comp["lt_cac"].idxmin()]
        insights.append(
            f"**Highest Return Channel:** **{best_roas_ch['channel']}** delivers the strongest ROAS at **{best_roas_ch['lt_roas']:.2f}x**, generating **₹{best_roas_ch['lt_revenue_inr']:,.0f}** from an outlay of **₹{best_roas_ch['spend_inr']:,.0f}**."
        )
        insights.append(
            f"**Lowest Acquisition Cost:** **{lowest_cac_ch['channel']}** provides the most cost-effective customer acquisition with a CAC of **₹{lowest_cac_ch['lt_cac']:,.0f}** per buyer."
        )

    # Attribution shift insights
    closers = comp[comp["revenue_variance_lt_minus_ft"] > 50000]
    introducers = comp[comp["revenue_variance_lt_minus_ft"] < -50000]
    if not closers.empty:
        ch_list = ", ".join(closers["channel"].tolist())
        insights.append(
            f"**Conversion Closers:** **{ch_list}** captures significantly higher credit in Last-Touch than First-Touch (+₹{closers['revenue_variance_lt_minus_ft'].sum():,.0f}), reflecting high down-funnel closing power."
        )
    if not introducers.empty:
        ch_list = ", ".join(introducers["channel"].tolist())
        insights.append(
            f"**Discovery / Introducers:** **{ch_list}** acts as the primary top-of-funnel discovery engine, introducing customers who later convert via direct or retention channels."
        )

render_insights_box("Attribution Dynamics & Acquisition Highlights", insights)

st.markdown("---")

# Visualizations: First vs Last Touch & Spend vs Revenue Bubble
col1, col2 = st.columns([0.55, 0.45])
with col1:
    if not comp.empty:
        st.plotly_chart(plot_channel_comparison(comp), use_container_width=True)
    else:
        st.info("No channel attribution data.")

with col2:
    if not comp.empty:
        st.plotly_chart(plot_spend_vs_revenue_bubble(comp), use_container_width=True)
    else:
        st.info("No spend vs revenue data.")

# Comprehensive Channel Performance Table
st.subheader("Channel Efficiency & Attribution Breakdown")
st.caption(
    "Comparison of marketing expenditure, First-Touch (origin) revenue, and Last-Touch (converting) revenue. "
    "Variance = Last-Touch minus First-Touch."
)

if not comp.empty:
    display_comp = comp[
        [
            "channel",
            "spend_inr",
            "ft_orders",
            "ft_revenue_inr",
            "ft_roas",
            "ft_cac",
            "lt_orders",
            "lt_revenue_inr",
            "lt_roas",
            "lt_cac",
            "revenue_variance_lt_minus_ft",
            "channel_role",
        ]
    ].copy()
    display_comp.columns = [
        "Channel",
        "Spend (INR)",
        "FT Orders",
        "FT Revenue (INR)",
        "FT ROAS",
        "FT CAC (INR)",
        "LT Orders",
        "LT Revenue (INR)",
        "LT ROAS",
        "LT CAC (INR)",
        "LT vs FT Variance (INR)",
        "Strategic Role",
    ]

    render_table_with_export(
        display_comp,
        filename="growthiq_channel_attribution_performance",
        label="Export Channel Performance (CSV)",
        format_dict={
            "Spend (INR)": "₹{:,.0f}",
            "FT Revenue (INR)": "₹{:,.0f}",
            "LT Revenue (INR)": "₹{:,.0f}",
            "LT vs FT Variance (INR)": "₹{:,.0f}",
            "FT CAC (INR)": "₹{:,.0f}",
            "LT CAC (INR)": "₹{:,.0f}",
            "FT ROAS": "{:.2f}x",
            "LT ROAS": "{:.2f}x",
            "FT Orders": "{:,}",
            "LT Orders": "{:,}",
        },
    )

st.markdown("---")

# Campaign-Level Breakdown Section
st.subheader("Campaign-Level Unit Economics & Engagement")
if not spend.empty:
    # Aggregate spend, impressions, clicks by campaign
    camp_summary = (
        spend.groupby(["channel", "campaign"], as_index=False)
        .agg(
            spend_inr=("spend_inr", "sum"),
            impressions=("impressions", "sum"),
            clicks=("clicks", "sum"),
        )
        .sort_values("spend_inr", ascending=False)
    )

    camp_summary["ctr_pct"] = np.where(
        camp_summary["impressions"] > 0,
        (camp_summary["clicks"] / camp_summary["impressions"]) * 100,
        0.0,
    )
    camp_summary["cpc_inr"] = np.where(
        camp_summary["clicks"] > 0, camp_summary["spend_inr"] / camp_summary["clicks"], 0.0
    )
    camp_summary["cpm_inr"] = np.where(
        camp_summary["impressions"] > 0,
        (camp_summary["spend_inr"] / camp_summary["impressions"]) * 1000,
        0.0,
    )

    # Merge campaign orders & revenue if available
    completed_orders = orders[orders["order_status"] == "Completed"] if "order_status" in orders.columns else orders
    items_calc = items.copy()
    items_calc["line_rev"] = items_calc["selling_unit_price_inr"] * items_calc["quantity"]
    order_rev_map = items_calc.groupby("order_id")["line_rev"].sum().to_dict()

    comp_orders_calc = completed_orders.copy()
    comp_orders_calc["rev"] = comp_orders_calc["order_id"].map(order_rev_map).fillna(0.0)

    camp_sales = (
        comp_orders_calc.groupby("campaign", as_index=False)
        .agg(attributed_orders=("order_id", "nunique"), attributed_revenue=("rev", "sum"))
    )

    camp_table = camp_summary.merge(camp_sales, on="campaign", how="left").fillna(
        {"attributed_orders": 0, "attributed_revenue": 0.0}
    )
    camp_table["roas"] = np.where(
        camp_table["spend_inr"] > 0, camp_table["attributed_revenue"] / camp_table["spend_inr"], 0.0
    )

    display_camp = camp_table[
        ["channel", "campaign", "spend_inr", "impressions", "clicks", "ctr_pct", "cpc_inr", "attributed_orders", "attributed_revenue", "roas"]
    ].copy()
    display_camp.columns = [
        "Channel",
        "Campaign",
        "Spend (INR)",
        "Impressions",
        "Clicks",
        "CTR (%)",
        "CPC (INR)",
        "Orders",
        "Revenue (INR)",
        "ROAS",
    ]

    render_table_with_export(
        display_camp,
        filename="growthiq_campaign_performance",
        label="Export Campaign Performance (CSV)",
        format_dict={
            "Spend (INR)": "₹{:,.0f}",
            "Revenue (INR)": "₹{:,.0f}",
            "CPC (INR)": "₹{:.2f}",
            "CTR (%)": "{:.2f}%",
            "ROAS": "{:.2f}x",
            "Impressions": "{:,}",
            "Clicks": "{:,}",
            "Orders": "{:,}",
        },
    )

