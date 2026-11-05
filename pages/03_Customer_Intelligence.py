"""
GrowthIQ — Page 3: Customer Intelligence & RFM Segmentation
===========================================================
Actionable customer segmentation combining rule-based RFM matrices and
unsupervised machine learning (K-Means) clustering.
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
from src.analytics.segmentation import calculate_rfm, cluster_customers_kmeans
from src.visualisation.charts import (
    plot_rfm_scatter,
    plot_kmeans_clusters,
    apply_theme,
    DISCRETE_PALETTE,
)

st.set_page_config(
    page_title="Customer Intelligence | GrowthIQ",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_custom_css()
ctx = render_sidebar()

orders = ctx["orders"]
items = ctx["order_items"]
customers = ctx["customers"]

st.markdown(
    """
    <div style="margin-bottom: 1.2rem;">
        <h1 style="margin-bottom: 0.1rem;">Customer Intelligence & RFM Segmentation</h1>
        <div style="font-size: 0.88rem; color: #6B5C60;">
            Behavioral customer segmentation: RFM (Recency, Frequency, Monetary) scoring, K-Means clustering, and retention risk profiling.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Compute RFM & Clustering
rfm = calculate_rfm(orders, items)

if rfm.empty:
    st.warning("No customer transaction data found for the selected filter parameters.")
    st.stop()

# Headline Customer Metrics
total_purchasers = len(rfm)
repeat_buyers = int((rfm["frequency"] > 1).sum())
repeat_buyer_rate = (repeat_buyers / total_purchasers) if total_purchasers > 0 else 0.0
avg_clv = float(rfm["monetary_inr"].mean()) if total_purchasers > 0 else 0.0
avg_freq = float(rfm["frequency"].mean()) if total_purchasers > 0 else 0.0
median_recency = float(rfm["recency_days"].median()) if total_purchasers > 0 else 0.0

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(render_metric_card("Active Buyers", f"{total_purchasers:,}", "Unique purchasing customers"), unsafe_allow_html=True)
with c2:
    st.markdown(render_metric_card("Repeat Customers", f"{repeat_buyers:,}", f"{repeat_buyer_rate:.1%} repeat purchase share"), unsafe_allow_html=True)
with c3:
    st.markdown(render_metric_card("Average CLV Proxy", f"₹{avg_clv:,.0f}", f"Avg {avg_freq:.1f} orders / customer"), unsafe_allow_html=True)
with c4:
    st.markdown(render_metric_card("Median Recency", f"{median_recency:.0f} days", "Days since last completed purchase"), unsafe_allow_html=True)

# Segment Aggregations & Automated Insights
seg_agg = (
    rfm.groupby("segment", observed=True)
    .agg(
        customer_count=("customer_id", "count"),
        total_revenue=("monetary_inr", "sum"),
        avg_spend=("monetary_inr", "mean"),
        avg_orders=("frequency", "mean"),
        median_recency=("recency_days", "median"),
    )
    .reset_index()
)
total_rev = rfm["monetary_inr"].sum()
seg_agg["revenue_share_pct"] = (seg_agg["total_revenue"] / total_rev * 100) if total_rev > 0 else 0.0
seg_agg["customer_share_pct"] = (seg_agg["customer_count"] / total_purchasers * 100) if total_purchasers > 0 else 0.0

insights = []
vip_row = seg_agg[seg_agg["segment"] == "VIP Champions"]
if not vip_row.empty:
    v_cust = vip_row.iloc[0]["customer_share_pct"]
    v_rev = vip_row.iloc[0]["revenue_share_pct"]
    v_spend = vip_row.iloc[0]["avg_spend"]
    insights.append(
        f"**The VIP Pareto Principle:** **VIP Champions** represent only **{v_cust:.1f}%** of buyers but generate **{v_rev:.1f}%** of total sales (avg spend **₹{v_spend:,.0f}**). Retaining this cohort is critical for high-margin profitability."
    )

at_risk = seg_agg[seg_agg["segment"] == "At-Risk High Value"]
if not at_risk.empty:
    ar_rev = at_risk.iloc[0]["total_revenue"]
    ar_count = at_risk.iloc[0]["customer_count"]
    insights.append(
        f"**Churn Risk Exposure:** **{ar_count:,}** customers are categorized as **At-Risk High Value**, representing **₹{ar_rev:,.0f}** in historical spend who have not purchased recently. Recommended action: automated email re-engagement flow."
    )

newcomers = seg_agg[seg_agg["segment"] == "Promising Newcomers"]
if not newcomers.empty:
    nc_count = newcomers.iloc[0]["customer_count"]
    insights.append(
        f"**Second-Purchase Opportunity:** **{nc_count:,}** recent buyers (**Promising Newcomers**) have placed their first order. Nurturing this segment with targeted cross-sell recommendations can unlock significant lifetime value."
    )

render_insights_box("Customer Behavioral Observations & Retention Opportunities", insights)

st.markdown("---")

# Visualizations: RFM Scatter & Segment Mix Bar
col_left, col_right = st.columns([0.58, 0.42])
with col_left:
    st.plotly_chart(plot_rfm_scatter(rfm), use_container_width=True)

with col_right:
    fig_mix = px.bar(
        seg_agg.sort_values("total_revenue", ascending=True),
        x="total_revenue",
        y="segment",
        orientation="h",
        color="segment",
        color_discrete_sequence=DISCRETE_PALETTE,
        title="Revenue Generated by Customer Segment (INR)",
    )
    st.plotly_chart(apply_theme(fig_mix, "Revenue by Customer Value Segment (INR)"), use_container_width=True)

# Segment Performance Table
st.subheader("RFM Customer Segment Roster")
display_seg = seg_agg[
    ["segment", "customer_count", "customer_share_pct", "total_revenue", "revenue_share_pct", "avg_spend", "avg_orders", "median_recency"]
].copy()
display_seg.columns = [
    "Segment",
    "Customers",
    "Customer Share (%)",
    "Total Revenue (INR)",
    "Revenue Share (%)",
    "Avg Spend (INR)",
    "Avg Orders",
    "Median Recency (Days)",
]

render_table_with_export(
    display_seg,
    filename="growthiq_customer_segments_summary",
    label="Export RFM Segments (CSV)",
    format_dict={
        "Total Revenue (INR)": "₹{:,.0f}",
        "Avg Spend (INR)": "₹{:,.0f}",
        "Customer Share (%)": "{:.1f}%",
        "Revenue Share (%)": "{:.1f}%",
        "Avg Orders": "{:.2f}",
        "Median Recency (Days)": "{:.0f}",
        "Customers": "{:,}",
    },
)

st.markdown("---")

# Machine Learning: K-Means Clustering Section
st.subheader("Unsupervised Machine Learning: K-Means Customer Clustering")
st.caption(
    "Standardized log-transformed features (Recency, Frequency, Monetary) are partitioned into 4 distinct behavioural clusters."
)

clustered_df, cluster_summary = cluster_customers_kmeans(rfm, n_clusters=4, random_state=42)

col_km1, col_km2 = st.columns([0.55, 0.45])
with col_km1:
    st.plotly_chart(plot_kmeans_clusters(clustered_df), use_container_width=True)

with col_km2:
    if "cluster_profiles" in cluster_summary:
        cp = cluster_summary["cluster_profiles"].copy()
        cp = cp[["persona_label", "customer_count", "avg_spend", "avg_frequency", "avg_recency", "total_revenue"]].copy()
        cp.columns = ["Persona Label", "Customers", "Avg Spend (INR)", "Avg Orders", "Avg Recency (Days)", "Total Revenue (INR)"]
        st.markdown("#### Discovered Cluster Personas")
        st.dataframe(
            cp.style.format(
                {
                    "Avg Spend (INR)": "₹{:,.0f}",
                    "Total Revenue (INR)": "₹{:,.0f}",
                    "Avg Orders": "{:.2f}",
                    "Avg Recency (Days)": "{:.0f}",
                    "Customers": "{:,}",
                }
            ),
            use_container_width=True,
            hide_index=True,
        )

