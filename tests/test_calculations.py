"""
GrowthIQ Advanced Calculations Test Suite
-----------------------------------------
Validates RFM segmentation, K-Means clustering, marketing attribution models,
cohort retention matrices, and discount band elasticity.
"""

import pytest
import pandas as pd
import numpy as np
from src.data.loader import load_all_tables
from src.analytics.segmentation import calculate_rfm, cluster_customers_kmeans
from src.analytics.attribution import compute_attribution_models
from src.analytics.cohorts import build_cohort_matrices
from src.analytics.products import (
    product_performance,
    category_performance,
    discount_effectiveness_analysis,
    inventory_watchlist,
)


@pytest.fixture(scope="module")
def data():
    return load_all_tables()


def test_rfm_segmentation_logic(data):
    """Ensures RFM correctly calculates recency, frequency, monetary, and assigns valid segments."""
    rfm = calculate_rfm(data["orders"], data["order_items"])
    assert not rfm.empty
    assert "recency_days" in rfm.columns
    assert "frequency" in rfm.columns
    assert "monetary_inr" in rfm.columns
    assert "segment" in rfm.columns

    # Valid segments
    expected_segments = {
        "VIP Champions",
        "Loyal Customers",
        "Promising Newcomers",
        "Potential Loyalists",
        "At-Risk High Value",
        "Hibernating / Lapsed",
        "Active Regulars",
    }
    actual_segments = set(rfm["segment"].unique())
    assert actual_segments.issubset(expected_segments)

    # Sanity checks
    assert (rfm["recency_days"] >= 0).all()
    assert (rfm["frequency"] >= 1).all()
    assert (rfm["monetary_inr"] > 0).all()


def test_kmeans_clustering_execution(data):
    """Ensures K-Means clustering runs cleanly and returns cluster labels and profiles."""
    rfm = calculate_rfm(data["orders"], data["order_items"])
    clustered, summary = cluster_customers_kmeans(rfm, n_clusters=4, random_state=42)

    assert "cluster" in clustered.columns
    assert "cluster_label" in clustered.columns
    assert clustered["cluster"].nunique() == 4
    assert summary["inertia"] > 0
    assert len(summary["cluster_profiles"]) == 4


def test_marketing_attribution_models(data):
    """Validates First-Touch vs Last-Touch channel attribution comparison."""
    comp, ft, lt = compute_attribution_models(
        data["orders"], data["sessions"], data["order_items"], data["campaign_spend"]
    )

    assert not comp.empty
    assert "channel" in comp.columns
    assert "ft_revenue_inr" in comp.columns
    assert "lt_revenue_inr" in comp.columns
    assert "revenue_variance_lt_minus_ft" in comp.columns

    # Sum of revenue under FT and LT should both be close to total completed order revenue
    total_ft_rev = comp["ft_revenue_inr"].sum()
    total_lt_rev = comp["lt_revenue_inr"].sum()
    assert abs(total_ft_rev - total_lt_rev) < 1.0  # Conservation of attributed revenue


def test_cohort_retention_matrices(data):
    """Validates cohort retention matrix calculation and M0 baseline."""
    ret_mat, counts_mat, rev_mat = build_cohort_matrices(data["orders"], data["order_items"])

    assert not ret_mat.empty
    assert not counts_mat.empty
    assert not rev_mat.empty

    # M0 retention rate must be 1.0 (100%) for all cohorts
    assert "M0" in ret_mat.columns
    assert np.allclose(ret_mat["M0"].values, 1.0)

    # Subsequent periods retention must be between 0.0 and 1.0
    for col in ret_mat.columns:
        valid_vals = ret_mat[col].dropna()
        assert (valid_vals >= 0.0).all()
        assert (valid_vals <= 1.0).all()


def test_discount_band_analysis(data):
    """Validates discount tier aggregation and gross margin rates."""
    tier_df = discount_effectiveness_analysis(data["orders"], data["order_items"])
    assert not tier_df.empty
    assert "discount_tier" in tier_df.columns
    assert "gross_margin_pct" in tier_df.columns

    # Margin on full price should be higher than clearance
    full_price_row = tier_df[tier_df["discount_tier"].str.contains("Full Price")]
    clearance_row = tier_df[tier_df["discount_tier"].str.contains("Clearance")]

    if not full_price_row.empty and not clearance_row.empty:
        assert full_price_row["gross_margin_pct"].iloc[0] > clearance_row["gross_margin_pct"].iloc[0]


def test_inventory_watchlist_classification(data):
    """Validates inventory status flags (CRITICAL, REORDER, HEALTHY)."""
    inv_df = inventory_watchlist(data["inventory"], data["products"])
    assert not inv_df.empty
    assert "stock_status" in inv_df.columns
    valid_statuses = {"CRITICAL", "REORDER", "HEALTHY"}
    assert set(inv_df["stock_status"].unique()).issubset(valid_statuses)

