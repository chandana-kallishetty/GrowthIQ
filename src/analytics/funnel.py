"""
GrowthIQ Conversion Funnel Analytics Module
-------------------------------------------
Analyzes the standard e-commerce consumer progression from initial visit to checkout
completion, quantifying leakage across funnel milestones and device segments.
"""

from typing import Dict, Any, List
import pandas as pd
import numpy as np

FUNNEL_STAGES = [
    ("session_start", "1. Sessions", "Total browsing sessions initiated"),
    ("view_item", "2. Product Views", "Sessions with at least one SKU viewed"),
    ("add_to_cart", "3. Add to Cart", "Sessions with items added to shopping bag"),
    ("begin_checkout", "4. Checkout Initiated", "Sessions proceeding to checkout flow"),
    ("purchase", "5. Purchases", "Sessions resulting in completed order"),
]


def funnel_metrics(events: pd.DataFrame) -> pd.DataFrame:
    """
    Computes overall unique-session funnel volume, conversion percentages from top,
    and step-by-step milestone progression rates.
    """
    if events.empty:
        return pd.DataFrame(
            columns=["stage_key", "stage", "sessions", "pct_of_top", "step_conversion_pct", "dropoff_pct"]
        )

    # Count distinct sessions per event type
    counts = events.groupby("event_name")["session_id"].nunique().to_dict()

    records = []
    top_volume = counts.get("session_start", 0)
    prev_volume = top_volume

    for stage_key, stage_label, description in FUNNEL_STAGES:
        vol = counts.get(stage_key, 0)
        pct_of_top = (vol / top_volume) if top_volume > 0 else 0.0
        step_conv = (vol / prev_volume) if prev_volume > 0 else 0.0
        dropoff = 1.0 - step_conv if prev_volume > 0 else 0.0

        records.append(
            {
                "stage_key": stage_key,
                "stage": stage_label,
                "description": description,
                "sessions": vol,
                "pct_of_top": pct_of_top,
                "step_conversion_pct": step_conv,
                "dropoff_pct": dropoff,
            }
        )
        prev_volume = vol

    return pd.DataFrame(records)


def device_funnel_comparison(events: pd.DataFrame, sessions: pd.DataFrame) -> pd.DataFrame:
    """
    Breaks down conversion funnel stages across user devices (Mobile, Desktop, Tablet).
    """
    if events.empty or sessions.empty:
        return pd.DataFrame()

    merged = events.merge(sessions[["session_id", "device"]], on="session_id", how="left")
    merged["device"] = merged["device"].fillna("Mobile")

    # Group by device and event_name
    grouped = (
        merged.groupby(["device", "event_name"])["session_id"]
        .nunique()
        .unstack(fill_value=0)
        .reset_index()
    )

    # Reorder columns according to funnel sequence
    stage_cols = [s[0] for s in FUNNEL_STAGES]
    existing_cols = [c for c in stage_cols if c in grouped.columns]

    df = grouped[["device"] + existing_cols].copy()

    # Calculate overall conversion rate
    if "session_start" in df.columns and "purchase" in df.columns:
        df["overall_conversion_pct"] = np.where(
            df["session_start"] > 0, (df["purchase"] / df["session_start"]) * 100, 0.0
        )
    if "session_start" in df.columns and "add_to_cart" in df.columns:
        df["cart_add_rate_pct"] = np.where(
            df["session_start"] > 0, (df["add_to_cart"] / df["session_start"]) * 100, 0.0
        )
    if "add_to_cart" in df.columns and "purchase" in df.columns:
        df["cart_to_purchase_rate_pct"] = np.where(
            df["add_to_cart"] > 0, (df["purchase"] / df["add_to_cart"]) * 100, 0.0
        )

    return df

