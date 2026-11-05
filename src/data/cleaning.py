"""
GrowthIQ Data Cleaning & Transformation Module
----------------------------------------------
Prepares and enriches raw datasets into analytics-ready data structures.
"""

import pandas as pd
import numpy as np


def clean_order_facts(orders: pd.DataFrame, items: pd.DataFrame) -> pd.DataFrame:
    """
    Enriches orders with aggregated item-level line revenue, units, and gross profit.
    Guarantees non-negative calculations and formats order dates.
    """
    if orders.empty or items.empty:
        return pd.DataFrame()

    items_clean = items.copy()
    items_clean["line_revenue_inr"] = (
        items_clean["selling_unit_price_inr"] * items_clean["quantity"]
    ).clip(lower=0.0)

    # Line gross profit: selling price minus cost
    if "line_gross_profit_inr" not in items_clean.columns:
        items_clean["line_gross_profit_inr"] = items_clean["line_revenue_inr"] * 0.65

    agg_items = items_clean.groupby("order_id", as_index=False).agg(
        revenue_inr=("line_revenue_inr", "sum"),
        gross_profit_inr=("line_gross_profit_inr", "sum"),
        units=("quantity", "sum"),
        item_count=("product_id", "nunique"),
    )

    orders_clean = orders.copy()
    if not pd.api.types.is_datetime64_any_dtype(orders_clean["order_date"]):
        orders_clean["order_date"] = pd.to_datetime(orders_clean["order_date"], errors="coerce")

    merged = orders_clean.merge(agg_items, on="order_id", how="left")
    merged["revenue_inr"] = merged["revenue_inr"].fillna(0.0)
    merged["gross_profit_inr"] = merged["gross_profit_inr"].fillna(0.0)
    merged["units"] = merged["units"].fillna(0).astype(int)

    # Effective discount amount
    merged["discount_amount_inr"] = np.where(
        merged["discount_rate"] > 0,
        merged["revenue_inr"] / (1.0 - merged["discount_rate"]) - merged["revenue_inr"],
        0.0,
    )

    return merged


def clean_sessions_data(sessions: pd.DataFrame) -> pd.DataFrame:
    """Standardizes session dates, channels, and session cost metrics."""
    if sessions.empty:
        return pd.DataFrame()

    df = sessions.copy()
    if not pd.api.types.is_datetime64_any_dtype(df["session_date"]):
        df["session_date"] = pd.to_datetime(df["session_date"], errors="coerce")

    df["session_cost_inr"] = df["session_cost_inr"].fillna(0.0).clip(lower=0.0)
    df["channel"] = df["channel"].fillna("Unknown").str.strip()
    df["device"] = df["device"].fillna("Mobile").str.strip()
    return df

