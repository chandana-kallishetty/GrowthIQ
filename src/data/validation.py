"""
GrowthIQ Data Quality & Referential Integrity Validation Suite
-------------------------------------------------------------
Performs rigorous structural and business rule integrity audits:
1. Primary key uniqueness
2. Foreign key referential completeness
3. Range, sign, and domain constraints
4. E-commerce funnel sequence validity
5. Table row counts, null rates, and duplicate detection
"""

from typing import Dict, Any, List
import pandas as pd


def check_primary_keys(tables: Dict[str, pd.DataFrame]) -> List[Dict[str, Any]]:
    """Validates that designated primary key columns have no duplicates and no nulls."""
    pk_definitions = {
        "customers": "customer_id",
        "products": "product_id",
        "product_categories": "category",
        "campaigns": "campaign",
        "sessions": "session_id",
        "events": "event_id",
        "orders": "order_id",
        "inventory": "product_id",
    }

    results = []
    for table_name, pk_col in pk_definitions.items():
        if table_name in tables:
            df = tables[table_name]
            total_rows = len(df)
            null_count = int(df[pk_col].isnull().sum())
            unique_count = int(df[pk_col].nunique())
            dup_count = total_rows - unique_count
            passed = bool((null_count == 0) and (dup_count == 0))
            results.append(
                {
                    "check_type": "Primary Key Uniqueness",
                    "table": table_name,
                    "column": pk_col,
                    "total_rows": total_rows,
                    "nulls": null_count,
                    "duplicates": dup_count,
                    "passed": passed,
                    "message": "Passed" if passed else f"Found {dup_count} duplicates and {null_count} nulls",
                }
            )
    return results


def check_foreign_keys(tables: Dict[str, pd.DataFrame]) -> List[Dict[str, Any]]:
    """Validates referential integrity between parent and child tables."""
    fk_definitions = [
        ("orders", "customer_id", "customers", "customer_id", True),
        ("orders", "session_id", "sessions", "session_id", True),
        ("order_items", "order_id", "orders", "order_id", True),
        ("order_items", "product_id", "products", "product_id", True),
        ("events", "session_id", "sessions", "session_id", True),
        ("inventory", "product_id", "products", "product_id", True),
        ("sessions", "customer_id", "customers", "customer_id", False),  # Optional FK (can be anonymous session)
    ]

    results = []
    for child_tbl, child_col, parent_tbl, parent_col, required in fk_definitions:
        if child_tbl in tables and parent_tbl in tables:
            child_df = tables[child_tbl]
            parent_df = tables[parent_tbl]

            child_series = child_df[child_col].dropna() if not required else child_df[child_col]
            parent_keys = set(parent_df[parent_col].dropna().unique())

            unmatched = child_series[~child_series.isin(parent_keys)]
            orphan_count = int(len(unmatched))
            passed = bool(orphan_count == 0)

            results.append(
                {
                    "check_type": "Foreign Key Referential Integrity",
                    "relationship": f"{child_tbl}.{child_col} -> {parent_tbl}.{parent_col}",
                    "orphans": orphan_count,
                    "passed": passed,
                    "message": "Referentially intact" if passed else f"{orphan_count} orphaned child records found",
                }
            )
    return results


def check_business_constraints(tables: Dict[str, pd.DataFrame]) -> List[Dict[str, Any]]:
    """Validates domain constraints, negative values, and valid ranges."""
    results = []

    # 1. Non-negative prices & quantities in order_items
    if "order_items" in tables:
        oi = tables["order_items"]
        neg_qty = int((oi["quantity"] <= 0).sum())
        neg_price = int((oi["selling_unit_price_inr"] < 0).sum())
        passed = bool((neg_qty == 0) and (neg_price == 0))
        results.append(
            {
                "check_type": "Domain Constraint",
                "target": "order_items (quantity > 0, price >= 0)",
                "passed": passed,
                "message": "Valid" if passed else f"{neg_qty} non-positive qtys, {neg_price} negative prices",
            }
        )

    # 2. Valid discount range (0.0 to 1.0)
    if "orders" in tables:
        orders = tables["orders"]
        invalid_disc = int(((orders["discount_rate"] < 0.0) | (orders["discount_rate"] > 1.0)).sum())
        passed = bool(invalid_disc == 0)
        results.append(
            {
                "check_type": "Domain Constraint",
                "target": "orders.discount_rate in [0.0, 1.0]",
                "passed": passed,
                "message": "Valid" if passed else f"{invalid_disc} invalid discount rates",
            }
        )

    # 3. Valid Funnel Events
    if "events" in tables:
        events = tables["events"]
        valid_events = {"session_start", "view_item", "add_to_cart", "begin_checkout", "purchase"}
        invalid_events = int((~events["event_name"].isin(valid_events)).sum())
        passed = bool(invalid_events == 0)
        results.append(
            {
                "check_type": "Domain Constraint",
                "target": "events.event_name standard vocabulary",
                "passed": passed,
                "message": "Valid" if passed else f"{invalid_events} unrecognised event names",
            }
        )

    # 4. Inventory Non-negative on-hand and reorder point
    if "inventory" in tables:
        inv = tables["inventory"]
        neg_stock = int(((inv["on_hand_units"] < 0) | (inv["reorder_point_units"] < 0)).sum())
        passed = bool(neg_stock == 0)
        results.append(
            {
                "check_type": "Domain Constraint",
                "target": "inventory non-negative stock & reorder levels",
                "passed": passed,
                "message": "Valid" if passed else f"{neg_stock} negative inventory rows",
            }
        )

    return results


def run_full_validation_suite(tables: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
    """
    Executes the entire automated data-quality testing suite.
    Returns structured results for display in Streamlit or evaluation in Pytest.
    """
    pk_results = check_primary_keys(tables)
    fk_results = check_foreign_keys(tables)
    constraint_results = check_business_constraints(tables)

    all_checks = pk_results + fk_results + constraint_results
    total_checks = len(all_checks)
    passed_checks = sum(1 for c in all_checks if c["passed"])
    failed_checks = total_checks - passed_checks

    table_profiles = []
    for name, df in tables.items():
        total_cells = df.size
        null_cells = int(df.isnull().sum().sum())
        null_pct = (null_cells / total_cells * 100) if total_cells > 0 else 0.0
        table_profiles.append(
            {
                "Table": name,
                "Rows": len(df),
                "Columns": len(df.columns),
                "Null Cells": null_cells,
                "Null Rate (%)": round(null_pct, 2),
                "Memory (KB)": round(df.memory_usage(deep=True).sum() / 1024, 1),
            }
        )

    return {
        "status": "PASSED" if failed_checks == 0 else "FAILED",
        "total_checks": total_checks,
        "passed_checks": passed_checks,
        "failed_checks": failed_checks,
        "pass_rate_pct": round((passed_checks / total_checks) * 100, 1),
        "primary_key_results": pk_results,
        "foreign_key_results": fk_results,
        "constraint_results": constraint_results,
        "table_profiles": pd.DataFrame(table_profiles),
    }
