"""
GrowthIQ Marketing Attribution Module
-------------------------------------
Implements First-Touch and Last-Touch attribution models and compares channel
performance across the consumer conversion path.
"""

from typing import Dict, Any, Tuple
import pandas as pd
import numpy as np
from src.analytics.kpis import order_facts


def compute_attribution_models(
    orders: pd.DataFrame,
    sessions: pd.DataFrame,
    items: pd.DataFrame,
    spend_df: pd.DataFrame = None,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Computes First-Touch and Last-Touch attribution for all completed orders.

    Methodology:
    - First-Touch: Identifies the channel and campaign of the earliest session
      recorded for each customer, and assigns order revenue to that origin touchpoint.
    - Last-Touch: Assigns order revenue directly to the converting session's channel.
    """
    facts = order_facts(orders, items)
    if facts.empty:
        empty_df = pd.DataFrame(columns=["channel", "orders", "revenue_inr", "roas", "cac"])
        return empty_df, empty_df, empty_df

    completed = facts[facts["order_status"] == "Completed"] if "order_status" in facts.columns else facts

    # 1. Determine Customer First-Touch from earliest recorded session
    sess_df = sessions.copy()
    if not pd.api.types.is_datetime64_any_dtype(sess_df["session_date"]):
        sess_df["session_date"] = pd.to_datetime(sess_df["session_date"])

    valid_sess = sess_df.dropna(subset=["customer_id"]).sort_values(["session_date", "session_id"])
    first_touches = valid_sess.groupby("customer_id").first().reset_index()
    first_touch_map = dict(zip(first_touches["customer_id"], first_touches["channel"]))

    # Map first touch to completed orders (fallback to order's channel if no prior session)
    completed = completed.copy()
    completed["first_touch_channel"] = completed["customer_id"].map(first_touch_map).fillna(completed["channel"])
    completed["last_touch_channel"] = completed["channel"]

    # 2. Spend by Channel
    if spend_df is not None and not spend_df.empty:
        ch_spend = spend_df.groupby("channel", as_index=False)["spend_inr"].sum()
    else:
        ch_spend = sess_df.groupby("channel", as_index=False)["session_cost_inr"].sum().rename(
            columns={"session_cost_inr": "spend_inr"}
        )

    # 3. First-Touch Aggregation
    ft_agg = (
        completed.groupby("first_touch_channel", as_index=False)
        .agg(
            ft_orders=("order_id", "nunique"),
            ft_customers=("customer_id", "nunique"),
            ft_revenue_inr=("revenue_inr", "sum"),
            ft_gross_profit_inr=("gross_profit_inr", "sum"),
        )
        .rename(columns={"first_touch_channel": "channel"})
    )

    # 4. Last-Touch Aggregation
    lt_agg = (
        completed.groupby("last_touch_channel", as_index=False)
        .agg(
            lt_orders=("order_id", "nunique"),
            lt_customers=("customer_id", "nunique"),
            lt_revenue_inr=("revenue_inr", "sum"),
            lt_gross_profit_inr=("gross_profit_inr", "sum"),
        )
        .rename(columns={"last_touch_channel": "channel"})
    )

    # 5. Merge Comparison Table
    all_channels = sorted(
        list(set(sess_df["channel"].unique()).union(set(completed["channel"].unique())))
    )
    comp = pd.DataFrame({"channel": all_channels})
    comp = comp.merge(ch_spend, on="channel", how="left").fillna({"spend_inr": 0.0})
    comp = comp.merge(ft_agg, on="channel", how="left").fillna(
        {"ft_orders": 0, "ft_customers": 0, "ft_revenue_inr": 0.0, "ft_gross_profit_inr": 0.0}
    )
    comp = comp.merge(lt_agg, on="channel", how="left").fillna(
        {"lt_orders": 0, "lt_customers": 0, "lt_revenue_inr": 0.0, "lt_gross_profit_inr": 0.0}
    )

    # Calculate ROAS & CAC under each model
    comp["ft_roas"] = np.where(comp["spend_inr"] > 0, comp["ft_revenue_inr"] / comp["spend_inr"], 0.0)
    comp["lt_roas"] = np.where(comp["spend_inr"] > 0, comp["lt_revenue_inr"] / comp["spend_inr"], 0.0)

    comp["ft_cac"] = np.where(comp["ft_customers"] > 0, comp["spend_inr"] / comp["ft_customers"], 0.0)
    comp["lt_cac"] = np.where(comp["lt_customers"] > 0, comp["spend_inr"] / comp["lt_customers"], 0.0)

    # Revenue variance: positive means channel gains credit in last touch (closer),
    # negative means channel loses credit in last touch (introducer / discovery).
    comp["revenue_variance_lt_minus_ft"] = comp["lt_revenue_inr"] - comp["ft_revenue_inr"]
    comp["channel_role"] = np.where(
        comp["revenue_variance_lt_minus_ft"] > 50000,
        "Closer / Converter (Email/Direct/Search)",
        np.where(
            comp["revenue_variance_lt_minus_ft"] < -50000,
            "Origin / Introducer (Social/Influencer)",
            "Balanced Touchpoint",
        ),
    )

    return comp, ft_agg, lt_agg

