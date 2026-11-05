"""
GrowthIQ SQLite Database & Query Suite Tests
--------------------------------------------
Validates SQLite connection, table schemas, referential integrity pragmas,
and analytical SQL queries execution.
"""

import pytest
import sqlite3
import pandas as pd
from src.database.connection import get_connection, DB_PATH
from src.database.queries import execute_query, load_analysis_queries
from src.data.loader import load_table


def test_database_connection():
    """Ensures database file exists and can establish an active connection."""
    conn = get_connection()
    assert conn is not None
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys;")
    fk_status = cursor.fetchone()[0]
    assert fk_status == 1, "Foreign keys pragma must be active (1)!"
    conn.close()


def test_database_schema_tables_exist():
    """Ensures all 10 core tables are defined and populated in SQLite."""
    expected_tables = {
        "product_categories",
        "products",
        "customers",
        "campaigns",
        "campaign_spend",
        "sessions",
        "events",
        "orders",
        "order_items",
        "inventory",
    }
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables_found = {row[0] for row in cursor.fetchall()}
    conn.close()

    assert expected_tables.issubset(tables_found), f"Missing tables: {expected_tables - tables_found}"


def test_analytical_sql_queries():
    """Validates that all analytical SQL queries in sql/analysis_queries.sql execute successfully."""
    queries = load_analysis_queries()
    assert len(queries) >= 8, f"Expected at least 8 queries, found {len(queries)}"

    for title, q_str in queries.items():
        df = execute_query(q_str)
        assert isinstance(df, pd.DataFrame), f"Query '{title}' failed to return DataFrame"
        assert len(df) > 0, f"Query '{title}' returned 0 rows"


def test_sql_and_pandas_kpi_parity():
    """Ensures total revenue calculated via SQL matches total revenue calculated via Pandas."""
    sql = """
    SELECT ROUND(SUM(oi.quantity * oi.selling_unit_price_inr), 2) AS sql_rev
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.order_status = 'Completed';
    """
    df_sql = execute_query(sql)
    sql_rev = float(df_sql.iloc[0]["sql_rev"])

    orders = load_table("orders")
    items = load_table("order_items")
    completed = orders[orders["order_status"] == "Completed"]
    valid_items = items[items["order_id"].isin(completed["order_id"])]
    pandas_rev = round(float((valid_items["quantity"] * valid_items["selling_unit_price_inr"]).sum()), 2)

    assert abs(sql_rev - pandas_rev) < 0.05, f"Discrepancy: SQL {sql_rev} vs Pandas {pandas_rev}"

