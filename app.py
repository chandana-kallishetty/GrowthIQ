"""
GrowthIQ — E-Commerce Marketing Intelligence Platform
======================================================
Main Entry Point & Strategic Portal

Domain: Fashion, athleisure and D2C e-commerce analytics.
"""

import streamlit as st
import pandas as pd
from src.visualisation.ui import (
    inject_custom_css,
    render_sidebar,
    render_metric_card,
    render_insights_box,
    COLOR_BURGUNDY,
    COLOR_GOLD,
    COLOR_TAUPE,
    COLOR_CARD_BG,
    COLOR_BORDER,
)
from src.analytics.kpis import kpi_summary, order_facts

st.set_page_config(
    page_title="GrowthIQ | Marketing Intelligence Platform",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_custom_css()
ctx = render_sidebar()

orders = ctx["orders"]
sessions = ctx["sessions"]
items = ctx["order_items"]
spend = ctx["campaign_spend"]

# Top Hero Banner
st.markdown(
    f"""
    <div style="background: linear-gradient(135deg, #FAF4ED 0%, #F5ECE1 100%); border: 1px solid {COLOR_BORDER}; border-radius: 14px; padding: 2rem 2.2rem; margin-bottom: 1.8rem; box-shadow: 0 4px 15px rgba(75, 38, 52, 0.05);">
        <div style="font-size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.15em; color: {COLOR_GOLD}; margin-bottom: 0.4rem;">
            PORTFOLIO INTELLIGENCE PLATFORM
        </div>
        <h1 style="font-size: 2.5rem; color: {COLOR_BURGUNDY}; margin-bottom: 0.5rem; line-height: 1.15;">
            Growth<span style="color: {COLOR_GOLD};">IQ</span> — E-Commerce Marketing Intelligence
        </h1>
        <p style="font-size: 1.05rem; color: #4A3E42; max-width: 850px; line-height: 1.6; margin-bottom: 0;">
            A production-quality marketing data analytics platform designed for fashion and athleisure D2C commerce.
            Transforming multi-touch website telemetry, advertising spend, customer cohorts, and transaction records into high-conviction commercial decisions.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Live Key Performance Indicators
kpis = kpi_summary(orders, sessions, items, spend_df=spend)

c1, c2, c3, c4, c5, c6 = st.columns(6)
with c1:
    st.markdown(render_metric_card("Net Revenue", f"₹{kpis['revenue']:,.0f}", "Realized completed sales"), unsafe_allow_html=True)
with c2:
    st.markdown(render_metric_card("Orders", f"{kpis['orders']:,}", f"{kpis['units_sold']:,} items sold"), unsafe_allow_html=True)
with c3:
    st.markdown(render_metric_card("Average Order Value", f"₹{kpis['aov']:,.0f}", "Per completed order"), unsafe_allow_html=True)
with c4:
    st.markdown(render_metric_card("Blended ROAS", f"{kpis['roas']:.2f}x", "Attributed Revenue / Spend"), unsafe_allow_html=True)
with c5:
    st.markdown(render_metric_card("Blended CAC", f"₹{kpis['cac']:,.0f}", f"Across {kpis['customers']:,} buyers"), unsafe_allow_html=True)
with c6:
    st.markdown(render_metric_card("Repeat Share", f"{kpis['repeat_rate']:.1%}", f"{kpis['repeat_customers']:,} repeat buyers"), unsafe_allow_html=True)

st.markdown("---")

# Navigation Matrix to Dedicated Pages
st.markdown("### 🧭 Analytical Intelligence Modules")
st.markdown("Select an analytical domain below or use the sidebar navigation to explore:")

p1, p2, p3 = st.columns(3)
with p1:
    st.markdown(
        f"""
        <div class="metric-card" style="height: 100%;">
            <h3 style="margin-top: 0; color: {COLOR_BURGUNDY}; font-size: 1.25rem;">01. Executive Overview</h3>
            <p style="font-size: 0.85rem; color: #5C5254; line-height: 1.5;">
                Top-line revenue trajectory, month-over-month sales velocity, merchandise department contribution, and board-level commercial KPIs.
            </p>
            <div style="font-size: 0.75rem; font-weight: 600; color: {COLOR_GOLD}; text-transform: uppercase; letter-spacing: 0.05em;">
                → Navigate to Page 1 in sidebar
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with p2:
    st.markdown(
        f"""
        <div class="metric-card" style="height: 100%;">
            <h3 style="margin-top: 0; color: {COLOR_BURGUNDY}; font-size: 1.25rem;">02. Marketing Performance</h3>
            <p style="font-size: 0.85rem; color: #5C5254; line-height: 1.5;">
                Multi-touch acquisition channels, First-Touch vs. Last-Touch attribution comparison, campaign unit economics (ROAS, CAC, CTR, CPC).
            </p>
            <div style="font-size: 0.75rem; font-weight: 600; color: {COLOR_GOLD}; text-transform: uppercase; letter-spacing: 0.05em;">
                → Navigate to Page 2 in sidebar
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with p3:
    st.markdown(
        f"""
        <div class="metric-card" style="height: 100%;">
            <h3 style="margin-top: 0; color: {COLOR_BURGUNDY}; font-size: 1.25rem;">03. Customer Intelligence</h3>
            <p style="font-size: 0.85rem; color: #5C5254; line-height: 1.5;">
                Behavioral customer segmentation, RFM matrix classification (VIPs, At-Risk, Loyalists), and unsupervised K-Means customer persona clustering.
            </p>
            <div style="font-size: 0.75rem; font-weight: 600; color: {COLOR_GOLD}; text-transform: uppercase; letter-spacing: 0.05em;">
                → Navigate to Page 3 in sidebar
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

p4, p5, p6 = st.columns(3)
with p4:
    st.markdown(
        f"""
        <div class="metric-card" style="height: 100%;">
            <h3 style="margin-top: 0; color: {COLOR_BURGUNDY}; font-size: 1.25rem;">04. Product Analytics</h3>
            <p style="font-size: 0.85rem; color: #5C5254; line-height: 1.5;">
                Catalogue demand, bestselling SKU revenues, realized gross margins, promotional discount elasticity, and warehouse reorder alerts.
            </p>
            <div style="font-size: 0.75rem; font-weight: 600; color: {COLOR_GOLD}; text-transform: uppercase; letter-spacing: 0.05em;">
                → Navigate to Page 4 in sidebar
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with p5:
    st.markdown(
        f"""
        <div class="metric-card" style="height: 100%;">
            <h3 style="margin-top: 0; color: {COLOR_BURGUNDY}; font-size: 1.25rem;">05. Conversion Funnel</h3>
            <p style="font-size: 0.85rem; color: #5C5254; line-height: 1.5;">
                Visitor progression across browse, item view, cart add, and checkout completion milestones. Quantifying user friction and device disparities.
            </p>
            <div style="font-size: 0.75rem; font-weight: 600; color: {COLOR_GOLD}; text-transform: uppercase; letter-spacing: 0.05em;">
                → Navigate to Page 5 in sidebar
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with p6:
    st.markdown(
        f"""
        <div class="metric-card" style="height: 100%;">
            <h3 style="margin-top: 0; color: {COLOR_BURGUNDY}; font-size: 1.25rem;">06. Cohort Analysis</h3>
            <p style="font-size: 0.85rem; color: #5C5254; line-height: 1.5;">
                Longitudinal monthly cohort retention triangles, repeat purchase cadences, and cumulative customer lifetime value accumulation over time.
            </p>
            <div style="font-size: 0.75rem; font-weight: 600; color: {COLOR_GOLD}; text-transform: uppercase; letter-spacing: 0.05em;">
                → Navigate to Page 6 in sidebar
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

p7, _ = st.columns([0.33, 0.67])
with p7:
    st.markdown(
        f"""
        <div class="metric-card" style="height: 100%;">
            <h3 style="margin-top: 0; color: {COLOR_BURGUNDY}; font-size: 1.25rem;">07. Data Quality & Governance</h3>
            <p style="font-size: 0.85rem; color: #5C5254; line-height: 1.5;">
                Automated data quality audits: primary key uniqueness, foreign key referential integrity, null rates, and table memory profiles.
            </p>
            <div style="font-size: 0.75rem; font-weight: 600; color: {COLOR_GOLD}; text-transform: uppercase; letter-spacing: 0.05em;">
                → Navigate to Page 7 in sidebar
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# Architectural & Data Pipeline Overview
st.subheader("System Architecture & Analytics Engineering Pipeline")

st.markdown(
    f"""
    <div style="background: {COLOR_CARD_BG}; border: 1px solid {COLOR_BORDER}; border-radius: 12px; padding: 1.5rem; margin-top: 0.5rem;">
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; text-align: center;">
            <div style="padding: 12px; background: #FFFDF9; border: 1px solid {COLOR_BORDER}; border-radius: 8px;">
                <div style="font-weight: 700; color: {COLOR_BURGUNDY}; margin-bottom: 4px;">1. Ingestion Layer</div>
                <div style="font-size: 0.78rem; color: {COLOR_TAUPE};">10 Interconnected Synthetic CSVs (Sessions, Orders, Spend, Inventory)</div>
            </div>
            <div style="padding: 12px; background: #FFFDF9; border: 1px solid {COLOR_BORDER}; border-radius: 8px;">
                <div style="font-weight: 700; color: {COLOR_BURGUNDY}; margin-bottom: 4px;">2. Relational Database</div>
                <div style="font-size: 0.78rem; color: {COLOR_TAUPE};">SQLite 3 with Foreign Key Enforcement, Constraints & B-Tree Indexes</div>
            </div>
            <div style="padding: 12px; background: #FFFDF9; border: 1px solid {COLOR_BORDER}; border-radius: 8px;">
                <div style="font-weight: 700; color: {COLOR_BURGUNDY}; margin-bottom: 4px;">3. Analytics Engine</div>
                <div style="font-size: 0.78rem; color: {COLOR_TAUPE};">RFM, K-Means Clustering, Multi-Touch Attribution, Cohort Triangles</div>
            </div>
            <div style="padding: 12px; background: #FFFDF9; border: 1px solid {COLOR_BORDER}; border-radius: 8px;">
                <div style="font-weight: 700; color: {COLOR_BURGUNDY}; margin-bottom: 4px;">4. Luxury SaaS UI</div>
                <div style="font-size: 0.78rem; color: {COLOR_TAUPE};">Streamlit + Plotly with Ivory & Burgundy Visual Design</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")
st.caption(
    "GrowthIQ Platform | End-to-End E-Commerce Marketing Intelligence | Independent Synthetic Case Study. "
    "All figures, transactions, customer profiles, and advertising metrics are synthetically generated."
)
