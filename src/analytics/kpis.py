"""
GrowthIQ Executive KPIs Module
------------------------------
Calculates core business, revenue, order, and marketing unit economics.
"""

from typing import Dict, Any
import pandas as pd
import numpy as np


def order_facts(orders: pd.DataFrame, items: pd.DataFrame) -> pd.DataFrame:
    """
    Enriches orders with line-item revenue, line gross profit, and item quantity.
    """
    if orders.empty or items.empty:
        return pd.DataFrame()

    items_calc = items.copy()
    items_calc["line_revenue_inr"] = items_calc["selling_unit_price_inr"] * items_calc["quantity"]

    if "line_gross_profit_inr" not in items_calc.columns:
        items_calc["line_gross_profit_inr"] = items_calc["line_revenue_inr"] * 0.65

    item_agg = items_calc.groupby("order_id", as_index=False).agg(
        revenue_inr=("line_revenue_inr", "sum"),
        gross_profit_inr=("line_gross_profit_inr", "sum"),
        units=("quantity", "sum"),
    )

    orders_df = orders.copy()
    if not pd.api.types.is_datetime64_any_dtype(orders_df["order_date"]):
        orders_df["order_date"] = pd.to_datetime(orders_df["order_date"], errors="coerce")

    merged = orders_df.merge(item_agg, on="order_id", how="left")
    merged["revenue_inr"] = merged["revenue_inr"].fillna(0.0)
    merged["gross_profit_inr"] = merged["gross_profit_inr"].fillna(0.0)
    merged["units"] = merged["units"].fillna(0).astype(int)
    return merged


def kpi_summary(
    orders: pd.DataFrame,
    sessions: pd.DataFrame,
    items: pd.DataFrame,
    spend_df: pd.DataFrame = None,
) -> Dict[str, Any]:
    """
    Computes top-level executive KPIs across orders, sessions, and marketing expenditure.
    """
    facts = order_facts(orders, items)

    # Net revenue accounts for completed orders (excluding refunded / cancelled)
    completed_facts = facts[facts["order_status"] == "Completed"] if "order_status" in facts.columns else facts
    refunded_facts = facts[facts["order_status"] == "Refunded"] if "order_status" in facts.columns else pd.DataFrame()

    gross_revenue = float(facts["revenue_inr"].sum()) if not facts.empty else 0.0
    net_revenue = float(completed_facts["revenue_inr"].sum()) if not completed_facts.empty else 0.0
    refunded_revenue = float(refunded_facts["revenue_inr"].sum()) if not refunded_facts.empty else 0.0

    order_count = int(facts["order_id"].nunique()) if not facts.empty else 0
    completed_orders = int(completed_facts["order_id"].nunique()) if not completed_facts.empty else 0
    units_sold = int(completed_facts["units"].sum()) if not completed_facts.empty else 0

    session_count = int(sessions["session_id"].nunique()) if not sessions.empty else 0
    unique_customers = int(completed_facts["customer_id"].nunique()) if not completed_facts.empty else 0

    gross_profit = float(completed_facts["gross_profit_inr"].sum()) if not completed_facts.empty else 0.0
    gross_margin_pct = (gross_profit / net_revenue * 100) if net_revenue > 0 else 0.0

    # Total spend: prefer campaign_spend if supplied, fallback to session_cost_inr
    if spend_df is not None and not spend_df.empty:
        total_spend = float(spend_df["spend_inr"].sum())
    elif not sessions.empty and "session_cost_inr" in sessions.columns:
        total_spend = float(sessions["session_cost_inr"].sum())
    else:
        total_spend = 0.0

    aov = (net_revenue / completed_orders) if completed_orders > 0 else 0.0
    conversion_rate = (completed_orders / session_count) if session_count > 0 else 0.0
    roas = (net_revenue / total_spend) if total_spend > 0 else 0.0
    cac = (total_spend / unique_customers) if unique_customers > 0 else 0.0

    # Repeat customer share
    if not completed_facts.empty:
        cust_order_counts = completed_facts.groupby("customer_id")["order_id"].nunique()
        repeat_customers = int((cust_order_counts > 1).sum())
        repeat_rate = (repeat_customers / unique_customers) if unique_customers > 0 else 0.0
    else:
        repeat_customers = 0
        repeat_rate = 0.0

    return {
        "gross_revenue": gross_revenue,
        "revenue": net_revenue,
        "refunded_revenue": refunded_revenue,
        "refund_rate": (refunded_revenue / gross_revenue) if gross_revenue > 0 else 0.0,
        "orders": completed_orders,
        "total_orders_placed": order_count,
        "units_sold": units_sold,
        "aov": aov,
        "sessions": session_count,
        "conversion": conversion_rate,
        "customers": unique_customers,
        "repeat_customers": repeat_customers,
        "repeat_rate": repeat_rate,
        "spend": total_spend,
        "gross_profit": gross_profit,
        "gross_margin_pct": gross_margin_pct,
        "roas": roas,
        "cac": cac,
    }


def monthly_kpi_trends(facts: pd.DataFrame) -> pd.DataFrame:
    """
    Computes monthly aggregation of revenue, orders, AOV, gross margin, and MoM growth rate.
    """
    if facts.empty:
        return pd.DataFrame()

    df = facts[facts["order_status"] == "Completed"].copy() if "order_status" in facts.columns else facts.copy()
    if not pd.api.types.is_datetime64_any_dtype(df["order_date"]):
        df["order_date"] = pd.to_datetime(df["order_date"])

    df["month"] = df["order_date"].dt.strftime("%Y-%m")

    monthly = (
        df.groupby("month", as_index=False)
        .agg(
            revenue_inr=("revenue_inr", "sum"),
            orders=("order_id", "nunique"),
            customers=("customer_id", "nunique"),
            units=("units", "sum"),
            gross_profit_inr=("gross_profit_inr", "sum"),
        )
        .sort_values("month")
    )

    monthly["aov"] = monthly["revenue_inr"] / monthly["orders"]
    monthly["gross_margin_pct"] = (monthly["gross_profit_inr"] / monthly["revenue_inr"]) * 100
    monthly["mom_revenue_growth_pct"] = monthly["revenue_inr"].pct_change() * 100
    return monthly

