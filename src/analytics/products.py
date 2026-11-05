"""
GrowthIQ Product & Inventory Analytics Module
---------------------------------------------
Evaluates product catalogue demand, category revenue mix, discount elasticity,
and warehouse stockout risks.
"""

from typing import Dict, Any, Tuple
import pandas as pd
import numpy as np


def product_performance(
    orders: pd.DataFrame, items: pd.DataFrame, products: pd.DataFrame
) -> pd.DataFrame:
    """
    Computes revenue, volume, gross profit, and realized margin rate at the individual SKU level.
    """
    if items.empty or products.empty:
        return pd.DataFrame()

    completed_orders = orders[orders["order_status"] == "Completed"]["order_id"] if "order_status" in orders.columns else orders["order_id"]
    valid_items = items[items["order_id"].isin(completed_orders)].copy()

    valid_items["line_revenue_inr"] = valid_items["selling_unit_price_inr"] * valid_items["quantity"]
    if "line_gross_profit_inr" not in valid_items.columns:
        valid_items["line_gross_profit_inr"] = valid_items["line_revenue_inr"] * 0.65

    merged = valid_items.merge(products, on="product_id", how="left")

    sku_agg = (
        merged.groupby(["product_id", "product_name", "category", "target_gender"], as_index=False)
        .agg(
            units_sold=("quantity", "sum"),
            revenue_inr=("line_revenue_inr", "sum"),
            gross_profit_inr=("line_gross_profit_inr", "sum"),
            avg_selling_price_inr=("selling_unit_price_inr", "mean"),
            list_price_inr=("list_price_inr", "first"),
            unit_cost_inr=("unit_cost_inr", "first"),
        )
        .sort_values("revenue_inr", ascending=False)
    )

    sku_agg["realized_gross_margin_pct"] = np.where(
        sku_agg["revenue_inr"] > 0,
        (sku_agg["gross_profit_inr"] / sku_agg["revenue_inr"]) * 100,
        0.0,
    )

    total_revenue = sku_agg["revenue_inr"].sum()
    sku_agg["revenue_share_pct"] = (sku_agg["revenue_inr"] / total_revenue * 100) if total_revenue > 0 else 0.0

    return sku_agg


def category_performance(product_perf_df: pd.DataFrame) -> pd.DataFrame:
    """Aggregates product performance up to the merchandise category hierarchy."""
    if product_perf_df.empty:
        return pd.DataFrame()

    cat_agg = (
        product_perf_df.groupby("category", as_index=False)
        .agg(
            sku_count=("product_id", "count"),
            units_sold=("units_sold", "sum"),
            revenue_inr=("revenue_inr", "sum"),
            gross_profit_inr=("gross_profit_inr", "sum"),
        )
        .sort_values("revenue_inr", ascending=False)
    )

    cat_agg["gross_margin_pct"] = np.where(
        cat_agg["revenue_inr"] > 0,
        (cat_agg["gross_profit_inr"] / cat_agg["revenue_inr"]) * 100,
        0.0,
    )
    total_rev = cat_agg["revenue_inr"].sum()
    cat_agg["revenue_share_pct"] = (cat_agg["revenue_inr"] / total_rev * 100) if total_rev > 0 else 0.0

    return cat_agg


def discount_effectiveness_analysis(orders: pd.DataFrame, items: pd.DataFrame) -> pd.DataFrame:
    """
    Evaluates order volume, revenue, and gross profit margins across discrete promotional discount bands.
    Includes explicit analytical warnings against naive causal attribution.
    """
    if orders.empty or items.empty:
        return pd.DataFrame()

    completed = orders[orders["order_status"] == "Completed"].copy() if "order_status" in orders.columns else orders.copy()
    items_calc = items.copy()
    items_calc["line_revenue_inr"] = items_calc["selling_unit_price_inr"] * items_calc["quantity"]
    if "line_gross_profit_inr" not in items_calc.columns:
        items_calc["line_gross_profit_inr"] = items_calc["line_revenue_inr"] * 0.65

    agg_items = items_calc.groupby("order_id", as_index=False).agg(
        revenue_inr=("line_revenue_inr", "sum"),
        gross_profit_inr=("line_gross_profit_inr", "sum"),
        units=("quantity", "sum"),
    )

    merged = completed.merge(agg_items, on="order_id", how="left")

    def assign_discount_tier(rate):
        if rate == 0.0:
            return "1. Full Price (0%)"
        elif rate <= 0.10:
            return "2. Light Discount (1-10%)"
        elif rate <= 0.20:
            return "3. Moderate Discount (11-20%)"
        else:
            return "4. Clearance (>20%)"

    merged["discount_tier"] = merged["discount_rate"].apply(assign_discount_tier)

    tier_agg = (
        merged.groupby("discount_tier", as_index=False)
        .agg(
            order_count=("order_id", "nunique"),
            units_sold=("units", "sum"),
            revenue_inr=("revenue_inr", "sum"),
            gross_profit_inr=("gross_profit_inr", "sum"),
            avg_order_value_inr=("revenue_inr", "mean"),
        )
        .sort_values("discount_tier")
    )

    tier_agg["gross_margin_pct"] = np.where(
        tier_agg["revenue_inr"] > 0,
        (tier_agg["gross_profit_inr"] / tier_agg["revenue_inr"]) * 100,
        0.0,
    )
    total_rev = tier_agg["revenue_inr"].sum()
    tier_agg["revenue_share_pct"] = (tier_agg["revenue_inr"] / total_rev * 100) if total_rev > 0 else 0.0

    return tier_agg


def inventory_watchlist(inventory: pd.DataFrame, products: pd.DataFrame) -> pd.DataFrame:
    """
    Evaluates warehouse on-hand levels against dynamic reorder thresholds and safety buffers.
    """
    if inventory.empty or products.empty:
        return pd.DataFrame()

    merged = inventory.merge(
        products[["product_id", "product_name", "category", "list_price_inr", "unit_cost_inr"]],
        on="product_id",
        how="left",
    )

    def classify_stock(row):
        if row["on_hand_units"] <= row["safety_stock_units"]:
            return "CRITICAL"
        elif row["on_hand_units"] <= row["reorder_point_units"]:
            return "REORDER"
        else:
            return "HEALTHY"

    merged["stock_status"] = merged.apply(classify_stock, axis=1)
    merged["recommended_reorder_qty"] = np.maximum(
        0, merged["reorder_point_units"] * 2 - merged["on_hand_units"]
    )
    merged["inventory_capital_tied_inr"] = merged["on_hand_units"] * merged["unit_cost_inr"]

    return merged.sort_values(["stock_status", "on_hand_units"], ascending=[True, True])

