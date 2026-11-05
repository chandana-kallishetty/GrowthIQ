"""
GrowthIQ Shared UI & SaaS Design Components
-------------------------------------------
Provides consistent luxury styling, sidebar filtering controls, metric cards,
and downloadable table components across all Streamlit dashboard pages.
"""

from typing import Dict, Any, Tuple, List
import streamlit as st
import pandas as pd
from src.data.loader import load_all_tables
from src.data.cleaning import clean_order_facts

# Palette Constants
COLOR_BURGUNDY = "#4B2634"
COLOR_BURGUNDY_DARK = "#351A24"
COLOR_ROSE_WINE = "#8E4A5C"
COLOR_GOLD = "#C5A059"
COLOR_GOLD_LIGHT = "#E2C889"
COLOR_TAUPE = "#8C7A6B"
COLOR_IVORY_BG = "#FFFDF9"
COLOR_CARD_BG = "#FAF6F0"
COLOR_BORDER = "#E8DFD5"
COLOR_TEXT_DARK = "#2E2327"
COLOR_TEXT_MUTED = "#6B5C60"


def inject_custom_css():
    """Injects high-end, responsive SaaS stylesheet for the GrowthIQ platform."""
    st.markdown(
        f"""
        <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Playfair+Display:ital,wght@0,600;0,700;1,400&display=swap');

        /* Global Typography & Reset */
        html, body, [class*="css"] {{
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            color: {COLOR_TEXT_DARK};
        }}

        .stApp {{
            background-color: {COLOR_IVORY_BG};
        }}

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {{
            background-color: #F8F3ED !important;
            border-right: 1px solid {COLOR_BORDER};
        }}
        
        section[data-testid="stSidebar"] .block-container {{
            padding-top: 2rem;
        }}

        /* Headers */
        h1, h2, h3, h4 {{
            font-family: 'Playfair Display', Georgia, serif !important;
            color: {COLOR_BURGUNDY} !important;
            font-weight: 700 !important;
            letter-spacing: -0.01em;
        }}

        h1 {{
            font-size: 2.1rem !important;
            margin-bottom: 0.3rem !important;
        }}

        h2 {{
            font-size: 1.5rem !important;
            margin-top: 1.2rem !important;
            margin-bottom: 0.6rem !important;
        }}

        h3 {{
            font-size: 1.2rem !important;
            margin-top: 1rem !important;
        }}

        /* Metric KPI Card Container */
        .metric-card {{
            background: {COLOR_CARD_BG};
            border: 1px solid {COLOR_BORDER};
            border-radius: 12px;
            padding: 1.1rem 1.2rem;
            margin-bottom: 0.8rem;
            box-shadow: 0 2px 6px rgba(75, 38, 52, 0.04);
            transition: all 0.2s ease-in-out;
        }}

        .metric-card:hover {{
            box-shadow: 0 4px 12px rgba(75, 38, 52, 0.08);
            border-color: {COLOR_GOLD};
        }}

        .metric-label {{
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-weight: 600;
            color: {COLOR_TEXT_MUTED};
            margin-bottom: 0.35rem;
        }}

        .metric-value {{
            font-size: 1.65rem;
            font-weight: 700;
            color: {COLOR_BURGUNDY};
            letter-spacing: -0.02em;
            line-height: 1.1;
        }}

        .metric-subtext {{
            font-size: 0.75rem;
            color: {COLOR_TAUPE};
            margin-top: 0.3rem;
        }}

        /* Synthetic Badge Watermark */
        .synthetic-badge {{
            display: inline-flex;
            align-items: center;
            background: #EFE8E1;
            border: 1px solid {COLOR_BORDER};
            color: {COLOR_TEXT_MUTED};
            font-size: 0.72rem;
            font-weight: 600;
            padding: 3px 10px;
            border-radius: 20px;
            margin-top: 0.5rem;
            letter-spacing: 0.03em;
        }}

        /* Insights Recommendation Box */
        .insight-box {{
            background: #FAF5F0;
            border-left: 4px solid {COLOR_GOLD};
            border-top: 1px solid {COLOR_BORDER};
            border-right: 1px solid {COLOR_BORDER};
            border-bottom: 1px solid {COLOR_BORDER};
            border-radius: 0 10px 10px 0;
            padding: 1.1rem 1.4rem;
            margin: 1.2rem 0;
        }}

        .insight-title {{
            font-size: 0.88rem;
            font-weight: 700;
            color: {COLOR_BURGUNDY};
            text-transform: uppercase;
            letter-spacing: 0.06em;
            margin-bottom: 0.5rem;
        }}

        .insight-item {{
            font-size: 0.86rem;
            color: {COLOR_TEXT_DARK};
            line-height: 1.5;
            margin-bottom: 0.4rem;
        }}

        /* Streamlit Native Element Overrides */
        [data-testid="stMetric"] {{
            background: {COLOR_CARD_BG};
            border: 1px solid {COLOR_BORDER};
            padding: 14px 18px;
            border-radius: 12px;
            box-shadow: 0 2px 5px rgba(75, 38, 52, 0.03);
        }}

        [data-testid="stMetricLabel"] {{
            font-size: 0.8rem !important;
            font-weight: 600 !important;
            color: {COLOR_TEXT_MUTED} !important;
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }}

        [data-testid="stMetricValue"] {{
            color: {COLOR_BURGUNDY} !important;
            font-weight: 700 !important;
        }}

        div[data-testid="stExpander"] {{
            background: {COLOR_CARD_BG};
            border: 1px solid {COLOR_BORDER} !important;
            border-radius: 10px !important;
        }}

        .stButton>button {{
            background-color: {COLOR_BURGUNDY} !important;
            color: #FFFFFF !important;
            border-radius: 8px !important;
            border: none !important;
            font-weight: 600 !important;
            padding: 0.45rem 1.1rem !important;
            transition: all 0.2s ease;
        }}

        .stButton>button:hover {{
            background-color: {COLOR_ROSE_WINE} !important;
            box-shadow: 0 2px 8px rgba(75, 38, 52, 0.25) !important;
        }}

        /* Download Button Styling */
        .stDownloadButton>button {{
            background-color: transparent !important;
            color: {COLOR_BURGUNDY} !important;
            border: 1px solid {COLOR_BURGUNDY} !important;
            border-radius: 8px !important;
            font-size: 0.82rem !important;
            padding: 0.35rem 0.85rem !important;
        }}

        .stDownloadButton>button:hover {{
            background-color: {COLOR_BURGUNDY} !important;
            color: #FFFFFF !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_data(show_spinner=False)
def get_cached_tables() -> Dict[str, pd.DataFrame]:
    """Loads and caches all raw/synthetic tables in memory."""
    return load_all_tables()


def render_sidebar():
    """
    Renders global interactive navigation and filters in the Streamlit sidebar.
    Returns filtered orders, sessions, order_items, products, spend, and raw tables.
    """
    tables = get_cached_tables()

    with st.sidebar:
        # Brand Wordmark Header
        st.markdown(
            f"""
            <div style="padding-bottom: 0.6rem; border-bottom: 1px solid {COLOR_BORDER}; margin-bottom: 1.2rem;">
                <div style="font-family: 'Playfair Display', Georgia, serif; font-size: 1.7rem; font-weight: 700; color: {COLOR_BURGUNDY}; letter-spacing: -0.02em;">
                    Growth<span style="color: {COLOR_GOLD};">IQ</span>
                </div>
                <div style="font-size: 0.7rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.15em; color: {COLOR_TAUPE};">
                    Marketing Intelligence
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("### 🎛️ Analysis Controls")

        orders_raw = tables["orders"].copy()
        if not pd.api.types.is_datetime64_any_dtype(orders_raw["order_date"]):
            orders_raw["order_date"] = pd.to_datetime(orders_raw["order_date"])

        min_d = orders_raw["order_date"].min().date()
        max_d = orders_raw["order_date"].max().date()

        # Date Range Filter
        date_selection = st.date_input(
            "Order Date Range",
            value=(min_d, max_d),
            min_value=min_d,
            max_value=max_d,
            help="Filter analytical calculations across selected transaction dates.",
        )

        # Channel Filter
        available_channels = sorted(tables["sessions"]["channel"].dropna().unique().tolist())
        selected_channels = st.multiselect(
            "Acquisition Channels",
            options=available_channels,
            default=available_channels,
            help="Select one or more marketing channels.",
        )

        # Category Filter
        available_categories = sorted(tables["products"]["category"].dropna().unique().tolist())
        selected_categories = st.multiselect(
            "Product Categories",
            options=available_categories,
            default=available_categories,
            help="Filter catalogue performance by merchandise department.",
        )

        # Reset button
        if st.button("Reset All Filters", use_container_width=True):
            st.session_state["reset_trigger"] = True
            st.rerun()

        st.markdown("---")

        # Synthetic Case Study Watermark
        st.markdown(
            f"""
            <div style="background: {COLOR_CARD_BG}; border: 1px solid {COLOR_BORDER}; border-radius: 8px; padding: 12px; font-size: 0.75rem; color: {COLOR_TEXT_MUTED}; line-height: 1.4;">
                <strong style="color: {COLOR_BURGUNDY};">🔒 Data Governance Notice:</strong><br>
                All customer records, transaction histories, and ad spends are <strong>100% synthetically generated</strong>.
                Inspired by modern athleisure e-commerce. No access to proprietary retailer databases is claimed.
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Apply Filters to DataFrames
    orders_filtered = orders_raw.copy()
    sessions_filtered = tables["sessions"].copy()
    spend_filtered = tables["campaign_spend"].copy()

    if not pd.api.types.is_datetime64_any_dtype(sessions_filtered["session_date"]):
        sessions_filtered["session_date"] = pd.to_datetime(sessions_filtered["session_date"])
    if not pd.api.types.is_datetime64_any_dtype(spend_filtered["spend_date"]):
        spend_filtered["spend_date"] = pd.to_datetime(spend_filtered["spend_date"])

    if isinstance(date_selection, (tuple, list)) and len(date_selection) == 2:
        start_d, end_d = date_selection
        orders_filtered = orders_filtered[
            (orders_filtered["order_date"].dt.date >= start_d)
            & (orders_filtered["order_date"].dt.date <= end_d)
        ]
        sessions_filtered = sessions_filtered[
            (sessions_filtered["session_date"].dt.date >= start_d)
            & (sessions_filtered["session_date"].dt.date <= end_d)
        ]
        spend_filtered = spend_filtered[
            (spend_filtered["spend_date"].dt.date >= start_d)
            & (spend_filtered["spend_date"].dt.date <= end_d)
        ]

    # Filter Channels
    if selected_channels:
        orders_filtered = orders_filtered[orders_filtered["channel"].isin(selected_channels)]
        sessions_filtered = sessions_filtered[sessions_filtered["channel"].isin(selected_channels)]
        spend_filtered = spend_filtered[spend_filtered["channel"].isin(selected_channels)]

    # Filter Products by Category
    products_filtered = tables["products"].copy()
    if selected_categories:
        products_filtered = products_filtered[products_filtered["category"].isin(selected_categories)]

    valid_prod_ids = set(products_filtered["product_id"].unique())
    items_filtered = tables["order_items"].copy()
    items_filtered = items_filtered[
        items_filtered["order_id"].isin(orders_filtered["order_id"])
        & items_filtered["product_id"].isin(valid_prod_ids)
    ]

    # Recalculate orders linked to filtered items
    valid_order_ids = set(items_filtered["order_id"].unique())
    orders_filtered = orders_filtered[orders_filtered["order_id"].isin(valid_order_ids)]

    # Filter events
    valid_session_ids = set(sessions_filtered["session_id"].unique())
    events_filtered = tables["events"][tables["events"]["session_id"].isin(valid_session_ids)].copy()

    return {
        "orders": orders_filtered,
        "sessions": sessions_filtered,
        "order_items": items_filtered,
        "products": products_filtered,
        "campaign_spend": spend_filtered,
        "events": events_filtered,
        "inventory": tables["inventory"],
        "customers": tables["customers"],
        "campaigns": tables["campaigns"],
        "categories": tables["product_categories"],
        "all_tables": tables,
    }


def render_metric_card(title: str, value: str, subtext: str = "") -> str:
    """Returns HTML for an elegant executive metric card."""
    return f"""
    <div class="metric-card">
        <div class="metric-label">{title}</div>
        <div class="metric-value">{value}</div>
        {f'<div class="metric-subtext">{subtext}</div>' if subtext else ''}
    </div>
    """


def render_insights_box(title: str, points: List[str]):
    """Renders a styled callout box containing automated analytical observations."""
    points_html = "".join([f'<div class="insight-item">• {pt}</div>' for pt in points])
    st.markdown(
        f"""
        <div class="insight-box">
            <div class="insight-title">💡 {title}</div>
            {points_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_table_with_export(
    df: pd.DataFrame, filename: str, label: str = "Download CSV", format_dict: dict = None
):
    """Renders a styled dataframe along with a direct CSV download button."""
    if df.empty:
        st.info("No data available for current filter selection.")
        return

    col1, col2 = st.columns([0.82, 0.18])
    with col2:
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label=f"📥 {label}",
            data=csv,
            file_name=f"{filename}.csv",
            mime="text/csv",
            use_container_width=True,
        )

    styled_df = df.copy()
    if format_dict:
        try:
            st.dataframe(styled_df.style.format(format_dict), use_container_width=True, hide_index=True)
        except Exception:
            st.dataframe(styled_df, use_container_width=True, hide_index=True)
    else:
        st.dataframe(styled_df, use_container_width=True, hide_index=True)

