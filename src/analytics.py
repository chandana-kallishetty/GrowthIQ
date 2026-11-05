"""
GrowthIQ Analytics Top-Level Facade (Backward Compatible)
"""

import pandas as pd
import numpy as np

from src.analytics.kpis import order_facts, kpi_summary, monthly_kpi_trends
from src.analytics.attribution import compute_attribution_models
from src.analytics.segmentation import calculate_rfm, cluster_customers_kmeans
from src.analytics.cohorts import build_cohort_matrices, cohort_summary_metrics
from src.analytics.funnel import funnel_metrics, device_funnel_comparison
from src.analytics.products import (
    product_performance,
    category_performance,
    discount_effectiveness_analysis,
    inventory_watchlist,
)


def channel_performance(orders, sessions, items, spend_df=None):
    """Legacy alias that computes channel performance table."""
    comp, _, _ = compute_attribution_models(orders, sessions, items, spend_df)
    return comp.rename(
        columns={
            "lt_orders": "orders",
            "lt_revenue_inr": "revenue_inr",
            "lt_roas": "roas",
            "lt_cac": "cac",
        }
    )


def cohort_retention(orders):
    """Legacy alias returning retention matrix."""
    ret_mat, _, _ = build_cohort_matrices(orders)
    return ret_mat


def customer_rfm(orders, items):
    """Legacy alias returning RFM table."""
    df = calculate_rfm(orders, items)
    if df.empty:
        return df
    df["value_segment"] = df["segment"]
    return df


__all__ = [
    "order_facts",
    "kpi_summary",
    "monthly_kpi_trends",
    "compute_attribution_models",
    "calculate_rfm",
    "cluster_customers_kmeans",
    "build_cohort_matrices",
    "cohort_summary_metrics",
    "funnel_metrics",
    "device_funnel_comparison",
    "product_performance",
    "category_performance",
    "discount_effectiveness_analysis",
    "inventory_watchlist",
    "channel_performance",
    "cohort_retention",
    "customer_rfm",
]
