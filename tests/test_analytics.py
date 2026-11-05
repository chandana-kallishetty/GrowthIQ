"""
GrowthIQ Analytics Engine Tests
-------------------------------
Validates order calculations, executive KPI formulas, conversion rates, and monthly trends.
"""

import pandas as pd
import numpy as np
from src.analytics.kpis import order_facts, kpi_summary, monthly_kpi_trends
from src.analytics.funnel import funnel_metrics


def test_order_facts_calculation():
    """Validates line item aggregation to order level."""
    orders = pd.DataFrame(
        [
            {"order_id": "O1", "customer_id": "C1", "order_date": "2025-01-01", "channel": "Email", "order_status": "Completed"},
            {"order_id": "O2", "customer_id": "C2", "order_date": "2025-01-02", "channel": "Direct", "order_status": "Completed"},
        ]
    )
    items = pd.DataFrame(
        [
            {"order_id": "O1", "product_id": "P1", "quantity": 2, "selling_unit_price_inr": 1500.0, "line_gross_profit_inr": 1800.0},
            {"order_id": "O1", "product_id": "P2", "quantity": 1, "selling_unit_price_inr": 2000.0, "line_gross_profit_inr": 1200.0},
            {"order_id": "O2", "product_id": "P3", "quantity": 1, "selling_unit_price_inr": 2500.0, "line_gross_profit_inr": 1600.0},
        ]
    )
    facts = order_facts(orders, items)
    assert len(facts) == 2
    # Order 1: (2 * 1500) + (1 * 2000) = 5000
    assert facts.loc[facts["order_id"] == "O1", "revenue_inr"].iloc[0] == 5000.0
    assert facts.loc[facts["order_id"] == "O1", "units"].iloc[0] == 3
    assert facts.loc[facts["order_id"] == "O1", "gross_profit_inr"].iloc[0] == 3000.0
    # Order 2: 2500
    assert facts.loc[facts["order_id"] == "O2", "revenue_inr"].iloc[0] == 2500.0


def test_kpi_summary_metrics():
    """Validates executive KPI summary math (AOV, Conversion, ROAS, CAC)."""
    orders = pd.DataFrame(
        [
            {"order_id": "O1", "customer_id": "C1", "order_date": "2025-01-01", "channel": "Email", "order_status": "Completed"},
            {"order_id": "O2", "customer_id": "C1", "order_date": "2025-02-01", "channel": "Email", "order_status": "Completed"},
        ]
    )
    items = pd.DataFrame(
        [
            {"order_id": "O1", "product_id": "P1", "quantity": 1, "selling_unit_price_inr": 2000.0, "line_gross_profit_inr": 1200.0},
            {"order_id": "O2", "product_id": "P1", "quantity": 1, "selling_unit_price_inr": 3000.0, "line_gross_profit_inr": 1800.0},
        ]
    )
    sessions = pd.DataFrame(
        [
            {"session_id": "S1", "session_cost_inr": 500.0},
            {"session_id": "S2", "session_cost_inr": 500.0},
            {"session_id": "S3", "session_cost_inr": 500.0},
            {"session_id": "S4", "session_cost_inr": 500.0},
        ]
    )

    kpis = kpi_summary(orders, sessions, items)
    assert kpis["revenue"] == 5000.0
    assert kpis["orders"] == 2
    assert kpis["aov"] == 2500.0
    assert kpis["customers"] == 1
    assert kpis["sessions"] == 4
    assert kpis["conversion"] == 0.5  # 2 orders / 4 sessions
    assert kpis["spend"] == 2000.0
    assert kpis["roas"] == 2.5  # 5000 / 2000
    assert kpis["cac"] == 2000.0  # 2000 / 1 customer
    assert kpis["repeat_customers"] == 1
    assert kpis["repeat_rate"] == 1.0


def test_kpi_summary_empty_safe():
    """Ensures empty inputs do not crash with division by zero."""
    orders = pd.DataFrame(columns=["order_id", "customer_id", "order_date", "channel", "order_status"])
    sessions = pd.DataFrame(columns=["session_id", "session_cost_inr"])
    items = pd.DataFrame(columns=["order_id", "product_id", "quantity", "selling_unit_price_inr", "line_gross_profit_inr"])

    res = kpi_summary(orders, sessions, items)
    assert res["revenue"] == 0.0
    assert res["orders"] == 0
    assert res["aov"] == 0.0
    assert res["conversion"] == 0.0
    assert res["roas"] == 0.0
    assert res["cac"] == 0.0


def test_funnel_counts_unique_sessions():
    """Validates unique session deduplication in funnel stage metrics."""
    events = pd.DataFrame(
        [
            {"session_id": "S1", "event_name": "session_start"},
            {"session_id": "S1", "event_name": "view_item"},
            {"session_id": "S1", "event_name": "view_item"},  # duplicate event in same session
            {"session_id": "S2", "event_name": "session_start"},
            {"session_id": "S3", "event_name": "session_start"},
            {"session_id": "S3", "event_name": "view_item"},
            {"session_id": "S3", "event_name": "add_to_cart"},
        ]
    )
    result = funnel_metrics(events)
    # Sessions: 3, Views: 2, Cart: 1
    assert result.loc[result["stage_key"] == "session_start", "sessions"].iloc[0] == 3
    assert result.loc[result["stage_key"] == "view_item", "sessions"].iloc[0] == 2
    assert result.loc[result["stage_key"] == "add_to_cart", "sessions"].iloc[0] == 1
