"""
GrowthIQ Data Quality Automated Tests
-------------------------------------
Validates primary key uniqueness, foreign key referential integrity,
domain sign constraints, and funnel event taxonomies.
"""

import pytest
import pandas as pd
from src.data.loader import load_all_tables
from src.data.validation import (
    run_full_validation_suite,
    check_primary_keys,
    check_foreign_keys,
    check_business_constraints,
)


@pytest.fixture(scope="module")
def tables():
    return load_all_tables()


def test_full_validation_suite_passes(tables):
    """Ensures the comprehensive validation suite passes 100% of checks."""
    report = run_full_validation_suite(tables)
    assert report["status"] == "PASSED", f"Validation failed with {report['failed_checks']} failures."
    assert report["failed_checks"] == 0
    assert report["pass_rate_pct"] == 100.0


def test_primary_key_uniqueness(tables):
    """Ensures designated primary keys have zero duplicates and zero nulls."""
    pk_results = check_primary_keys(tables)
    for res in pk_results:
        assert res["passed"] is True, f"PK failure in {res['table']}.{res['column']}: {res['message']}"


def test_foreign_key_referential_integrity(tables):
    """Ensures child tables have no orphaned foreign keys pointing to nonexistent parents."""
    fk_results = check_foreign_keys(tables)
    for res in fk_results:
        assert res["passed"] is True, f"FK broken in {res['relationship']}: {res['message']}"


def test_business_domain_constraints(tables):
    """Ensures prices, quantities, and discount rates satisfy non-negative domain rules."""
    constraints = check_business_constraints(tables)
    for res in constraints:
        assert res["passed"] is True, f"Constraint failed for {res['target']}: {res['message']}"


def test_no_orphaned_order_items(tables):
    """Guarantees every order_item belongs to a verified order."""
    orders = tables["orders"]
    order_items = tables["order_items"]
    orphan_items = order_items[~order_items["order_id"].isin(orders["order_id"])]
    assert len(orphan_items) == 0, f"Found {len(orphan_items)} orphaned order items!"


def test_funnel_event_names(tables):
    """Guarantees only standard, sanctioned event names exist in events table."""
    events = tables["events"]
    valid_names = {"session_start", "view_item", "add_to_cart", "begin_checkout", "purchase"}
    unrecognised = set(events["event_name"].unique()) - valid_names
    assert len(unrecognised) == 0, f"Unrecognised funnel events: {unrecognised}"

