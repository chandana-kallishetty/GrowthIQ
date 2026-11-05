"""
GrowthIQ Data Visualisation & Themed Plotly Engine
--------------------------------------------------
Implements premium e-commerce charts adhering to the GrowthIQ brand identity:
Warm ivory, deep burgundy, muted taupe, and champagne-gold accents.
"""

from typing import Dict, Any, List
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# GrowthIQ Visual Identity Palette
COLOR_BURGUNDY = "#4B2634"
COLOR_BURGUNDY_DARK = "#351A24"
COLOR_ROSE_WINE = "#8E4A5C"
COLOR_BLUSH = "#B56B7D"
COLOR_GOLD = "#C5A059"
COLOR_GOLD_LIGHT = "#E2C889"
COLOR_TAUPE = "#8C7A6B"
COLOR_IVORY_BG = "#FFFDF9"
COLOR_CARD_BG = "#FAF6F0"
COLOR_BORDER = "#E8DFD5"
COLOR_TEXT_DARK = "#2E2327"
COLOR_TEXT_MUTED = "#6B5C60"

DISCRETE_PALETTE = [
    COLOR_BURGUNDY,
    COLOR_GOLD,
    COLOR_ROSE_WINE,
    COLOR_TAUPE,
    "#5A6B7C",  # Slate blue accent
    "#A35D6A",  # Dusty mauve
    "#C49E65",  # Warm ochre
    "#6D8B74",  # Sage green
]


def apply_theme(fig: go.Figure, title: str = "", height: int = 400) -> go.Figure:
    """Applies cohesive GrowthIQ typography, colors, borders, and margins to any Plotly figure."""
    fig.update_layout(
        title={
            "text": f"<b>{title}</b>",
            "font": {"family": "sans-serif", "size": 16, "color": COLOR_BURGUNDY},
            "x": 0.01,
            "xanchor": "left",
        },
        paper_bgcolor=COLOR_IVORY_BG,
        plot_bgcolor=COLOR_IVORY_BG,
        font={"family": "sans-serif", "color": COLOR_TEXT_DARK, "size": 12},
        height=height,
        margin={"l": 40, "r": 30, "t": 50, "b": 40},
        legend={
            "bgcolor": "rgba(255, 253, 249, 0.8)",
            "bordercolor": COLOR_BORDER,
            "borderwidth": 1,
            "font": {"size": 11, "color": COLOR_TEXT_DARK},
        },
        xaxis={
            "gridcolor": COLOR_BORDER,
            "showline": True,
            "linecolor": COLOR_BORDER,
            "tickfont": {"color": COLOR_TEXT_MUTED},
        },
        yaxis={
            "gridcolor": COLOR_BORDER,
            "showline": True,
            "linecolor": COLOR_BORDER,
            "tickfont": {"color": COLOR_TEXT_MUTED},
        },
        hoverlabel={
            "bgcolor": COLOR_BURGUNDY,
            "font_size": 12,
            "font_family": "sans-serif",
            "font_color": "#FFFFFF",
        },
    )
    return fig


def plot_revenue_trend(monthly_df: pd.DataFrame) -> go.Figure:
    """Renders monthly revenue and gross profit dual-line trend."""
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=monthly_df["month"],
            y=monthly_df["revenue_inr"],
            name="Net Revenue",
            mode="lines+markers",
            line={"color": COLOR_BURGUNDY, "width": 3},
            marker={"size": 7, "color": COLOR_BURGUNDY},
            hovertemplate="Month: %{x}<br>Net Revenue: ₹%{y:,.0f}<extra></extra>",
        )
    )

    if "gross_profit_inr" in monthly_df.columns:
        fig.add_trace(
            go.Scatter(
                x=monthly_df["month"],
                y=monthly_df["gross_profit_inr"],
                name="Gross Profit",
                mode="lines+markers",
                line={"color": COLOR_GOLD, "width": 2, "dash": "dash"},
                marker={"size": 6, "color": COLOR_GOLD},
                hovertemplate="Month: %{x}<br>Gross Profit: ₹%{y:,.0f}<extra></extra>",
            )
        )

    return apply_theme(fig, "Monthly Net Revenue & Gross Profit Trajectory (INR)")


def plot_channel_comparison(comp_df: pd.DataFrame) -> go.Figure:
    """Renders grouped bar comparison of First-Touch vs Last-Touch revenue by marketing channel."""
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=comp_df["channel"],
            y=comp_df["ft_revenue_inr"],
            name="First-Touch Revenue",
            marker_color=COLOR_TAUPE,
            hovertemplate="Channel: %{x}<br>First-Touch: ₹%{y:,.0f}<extra></extra>",
        )
    )

    fig.add_trace(
        go.Bar(
            x=comp_df["channel"],
            y=comp_df["lt_revenue_inr"],
            name="Last-Touch Revenue",
            marker_color=COLOR_BURGUNDY,
            hovertemplate="Channel: %{x}<br>Last-Touch: ₹%{y:,.0f}<extra></extra>",
        )
    )

    fig.update_layout(barmode="group")
    return apply_theme(fig, "Channel Attribution: First-Touch vs. Last-Touch Revenue (INR)")


def plot_spend_vs_revenue_bubble(comp_df: pd.DataFrame) -> go.Figure:
    """Renders spend vs revenue scatter plot where bubble radius scales with order volume."""
    fig = px.scatter(
        comp_df,
        x="spend_inr",
        y="lt_revenue_inr",
        size="lt_orders",
        color="channel",
        color_discrete_sequence=DISCRETE_PALETTE,
        hover_name="channel",
        hover_data={"lt_roas": ":.2f", "spend_inr": ":,.0f", "lt_revenue_inr": ":,.0f"},
    )
    return apply_theme(fig, "Marketing Spend vs Attributed Revenue (Bubble size = Orders)")


def plot_category_pie(cat_df: pd.DataFrame) -> go.Figure:
    """Renders donut chart for product category revenue share."""
    fig = px.pie(
        cat_df,
        names="category",
        values="revenue_inr",
        hole=0.48,
        color_discrete_sequence=DISCRETE_PALETTE,
    )
    fig.update_traces(
        textinfo="percent+label",
        hovertemplate="Category: %{label}<br>Revenue: ₹%{value:,.0f} (%{percent})<extra></extra>",
    )
    return apply_theme(fig, "Revenue Contribution Mix by Merchandise Category", height=380)


def plot_top_products_bar(prod_df: pd.DataFrame, top_n: int = 10) -> go.Figure:
    """Renders horizontal bar chart for top bestselling SKUs."""
    top = prod_df.head(top_n).iloc[::-1]
    fig = px.bar(
        top,
        x="revenue_inr",
        y="product_name",
        orientation="h",
        color="category",
        color_discrete_sequence=DISCRETE_PALETTE,
    )
    fig.update_traces(
        hovertemplate="Product: %{y}<br>Revenue: ₹%{x:,.0f}<extra></extra>"
    )
    return apply_theme(fig, f"Top {top_n} Bestselling Products by Realized Revenue (INR)", height=420)


def plot_funnel_chart(funnel_df: pd.DataFrame) -> go.Figure:
    """Renders conversion funnel with milestone volumes and stage conversions."""
    fig = go.Figure(
        go.Funnel(
            y=funnel_df["stage"],
            x=funnel_df["sessions"],
            textinfo="value+percent initial",
            marker={"color": [COLOR_BURGUNDY, COLOR_ROSE_WINE, COLOR_BLUSH, COLOR_GOLD, COLOR_TAUPE]},
            connector={"line": {"color": COLOR_BORDER, "width": 1}},
        )
    )
    return apply_theme(fig, "E-Commerce Session Progression & Milestone Funnel", height=420)


def plot_cohort_heatmap(retention_matrix: pd.DataFrame) -> go.Figure:
    """Renders styled heatmap for monthly cohort retention rates."""
    z_values = retention_matrix.values * 100
    y_labels = retention_matrix.index.tolist()
    x_labels = retention_matrix.columns.tolist()

    text_values = [
        [f"{val:.1f}%" if not np.isnan(val) and val > 0 else "" for val in row]
        for row in z_values
    ]

    fig = go.Figure(
        data=go.Heatmap(
            z=z_values,
            x=x_labels,
            y=y_labels,
            text=text_values,
            texttemplate="%{text}",
            colorscale=[
                [0.0, "#FAF6F0"],
                [0.15, "#E2D3CD"],
                [0.35, "#C49EAA"],
                [0.65, "#8E4A5C"],
                [1.0, COLOR_BURGUNDY],
            ],
            colorbar={"title": "Retention %", "tickfont": {"color": COLOR_TEXT_DARK}},
            hoverongaps=False,
            hovertemplate="Cohort: %{y}<br>Period: %{x}<br>Retention: %{z:.1f}%<extra></extra>",
        )
    )

    fig.update_yaxes(autorange="reversed")
    return apply_theme(fig, "Monthly Customer Cohort Retention Rate (%)", height=440)


def plot_rfm_scatter(rfm_df: pd.DataFrame) -> go.Figure:
    """Renders 2D scatter plot of Recency vs Monetary with Frequency bubble size and segment colors."""
    fig = px.scatter(
        rfm_df,
        x="recency_days",
        y="monetary_inr",
        size="frequency",
        color="segment",
        color_discrete_sequence=DISCRETE_PALETTE,
        hover_data={"customer_id": True, "frequency": True, "aov_inr": ":,.0f"},
    )
    fig.update_xaxes(autorange="reversed", title="Recency (Days Ago - Lower is Better)")
    fig.update_yaxes(title="Monetary Value (INR)")
    return apply_theme(fig, "Customer RFM Landscape: Recency vs. Monetary Value")


def plot_kmeans_clusters(df: pd.DataFrame) -> go.Figure:
    """Renders 3D scatter visualization of K-Means clusters across RFM dimensions."""
    label_col = "cluster_label" if "cluster_label" in df.columns else "cluster"
    fig = px.scatter(
        df,
        x="frequency",
        y="monetary_inr",
        color=label_col,
        size="monetary_inr",
        color_discrete_sequence=DISCRETE_PALETTE,
        hover_data=["customer_id", "recency_days"],
    )
    return apply_theme(fig, "K-Means Discovered Customer Personas")


def plot_discount_tiers_bar(tier_df: pd.DataFrame) -> go.Figure:
    """Renders dual-axis or bar chart of discount tier volume and realized gross margin %."""
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=tier_df["discount_tier"],
            y=tier_df["order_count"],
            name="Orders Placed",
            marker_color=COLOR_BURGUNDY,
            yaxis="y",
            hovertemplate="Tier: %{x}<br>Orders: %{y:,}<extra></extra>",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=tier_df["discount_tier"],
            y=tier_df["gross_margin_pct"],
            name="Gross Margin %",
            mode="lines+markers",
            line={"color": COLOR_GOLD, "width": 3},
            marker={"size": 8, "color": COLOR_GOLD},
            yaxis="y2",
            hovertemplate="Tier: %{x}<br>Gross Margin: %{y:.1f}%<extra></extra>",
        )
    )

    fig.update_layout(
        yaxis={"title": "Order Volume", "gridcolor": COLOR_BORDER},
        yaxis2={
            "title": "Gross Margin (%)",
            "overlaying": "y",
            "side": "right",
            "showgrid": False,
            "tickformat": ".0f",
        },
        legend={"x": 0.02, "y": 0.98},
    )
    return apply_theme(fig, "Discount Band Volume vs. Realized Gross Margin (%)")

