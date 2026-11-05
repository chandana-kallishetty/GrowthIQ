"""
GrowthIQ — Page 5: Conversion Funnel & User Friction
====================================================
Detailed analysis of the standard e-commerce milestone funnel: drop-off rates,
checkout leakage, and device-level conversion friction.
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
from src.analytics.funnel import funnel_metrics, device_funnel_comparison
from src.visualisation.charts import plot_funnel_chart, apply_theme, DISCRETE_PALETTE

st.set_page_config(
    page_title="Conversion Funnel | GrowthIQ",
    page_icon="🌪️",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_custom_css()
ctx = render_sidebar()

events = ctx["events"]
sessions = ctx["sessions"]

st.markdown(
    """
    <div style="margin-bottom: 1.2rem;">
        <h1 style="margin-bottom: 0.1rem;">E-Commerce Conversion Funnel</h1>
        <div style="font-size: 0.88rem; color: #6B5C60;">
            Visitor progression through browse, product discovery, carting, and checkout completion. Identifying leakage points.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Compute Funnel & Device Breakdown
funnel = funnel_metrics(events)
dev_funnel = device_funnel_comparison(events, sessions)

if funnel.empty:
    st.warning("No website event telemetry found for current filter selection.")
    st.stop()

# Headline Funnel KPIs
top_sessions = funnel.iloc[0]["sessions"] if len(funnel) > 0 else 0
purchases = funnel.iloc[-1]["sessions"] if len(funnel) >= 5 else 0
overall_cvr = (purchases / top_sessions) if top_sessions > 0 else 0.0

cart_add_stage = funnel[funnel["stage_key"] == "add_to_cart"]
cart_sessions = cart_add_stage.iloc[0]["sessions"] if not cart_add_stage.empty else 0
cart_to_purchase_cvr = (purchases / cart_sessions) if cart_sessions > 0 else 0.0

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(render_metric_card("Total Sessions", f"{top_sessions:,}", "Top-of-funnel entry visits"), unsafe_allow_html=True)
with c2:
    st.markdown(render_metric_card("Cart Adds", f"{cart_sessions:,}", f"{(cart_sessions/top_sessions):.1%} of all visitors" if top_sessions > 0 else ""), unsafe_allow_html=True)
with c3:
    st.markdown(render_metric_card("Completed Orders", f"{purchases:,}", "Final checkout completions"), unsafe_allow_html=True)
with c4:
    st.markdown(render_metric_card("Overall Conversion", f"{overall_cvr:.2%}", f"Cart-to-purchase: {cart_to_purchase_cvr:.1%}"), unsafe_allow_html=True)

# Funnel Leakage Insights
insights = []
if len(funnel) >= 5:
    # Identify milestone with largest absolute dropoff
    funnel_calc = funnel.iloc[1:].copy()
    largest_drop = funnel_calc.loc[funnel_calc["dropoff_pct"].idxmax()]
    insights.append(
        f"**Primary Leakage Point:** The largest friction occurs at **{largest_drop['stage']}**, where **{largest_drop['dropoff_pct']:.1%}** of previous stage visitors drop off. Enhancing product imagery, reviews, and size charts can boost add-to-cart velocity."
    )

if not dev_funnel.empty and "overall_conversion_pct" in dev_funnel.columns:
    dev_sorted = dev_funnel.sort_values("overall_conversion_pct", ascending=False)
    best_dev = dev_sorted.iloc[0]
    worst_dev = dev_sorted.iloc[-1]
    insights.append(
        f"**Device Disparity:** **{best_dev['device']}** converts at **{best_dev['overall_conversion_pct']:.2f}%**, compared to **{worst_dev['device']}** at **{worst_dev['overall_conversion_pct']:.2f}%**. Optimizing mobile 1-click checkout (UPI / Apple Pay) represents an immediate revenue multiplier."
    )

render_insights_box("Funnel Health & User Experience Bottlenecks", insights)

st.markdown("---")

# Visualizations: Funnel Chart & Device Comparison
col_left, col_right = st.columns([0.55, 0.45])
with col_left:
    st.plotly_chart(plot_funnel_chart(funnel), use_container_width=True)

with col_right:
    if not dev_funnel.empty and "overall_conversion_pct" in dev_funnel.columns:
        fig_dev = px.bar(
            dev_funnel,
            x="device",
            y="overall_conversion_pct",
            color="device",
            color_discrete_sequence=DISCRETE_PALETTE,
            title="Overall Conversion Rate by Device (%)",
        )
        st.plotly_chart(apply_theme(fig_dev, "Conversion Rate by Device Type (%)", height=420), use_container_width=True)
    else:
        st.info("No device funnel data available.")

# Funnel Milestone Table
st.subheader("Funnel Milestones & Drop-Off Metrics")
display_funnel = funnel[
    ["stage", "description", "sessions", "pct_of_top", "step_conversion_pct", "dropoff_pct"]
].copy()
display_funnel.columns = [
    "Milestone Stage",
    "Description",
    "Unique Sessions",
    "% of Top Funnel",
    "Step Conversion Rate (%)",
    "Stage Drop-Off (%)",
]

render_table_with_export(
    display_funnel,
    filename="growthiq_conversion_funnel_metrics",
    label="Export Funnel Metrics (CSV)",
    format_dict={
        "Unique Sessions": "{:,}",
        "% of Top Funnel": "{:.1%}",
        "Step Conversion Rate (%)": "{:.1%}",
        "Stage Drop-Off (%)": "{:.1%}",
    },
)

st.markdown("---")

# Device Breakdown Table
st.subheader("Device Funnel Progression Breakdown")
if not dev_funnel.empty:
    render_table_with_export(
        dev_funnel,
        filename="growthiq_device_funnel_comparison",
        label="Export Device Funnel (CSV)",
        format_dict={
            "session_start": "{:,}",
            "view_item": "{:,}",
            "add_to_cart": "{:,}",
            "begin_checkout": "{:,}",
            "purchase": "{:,}",
            "overall_conversion_pct": "{:.2f}%",
            "cart_add_rate_pct": "{:.2f}%",
            "cart_to_purchase_rate_pct": "{:.2f}%",
        },
    )

