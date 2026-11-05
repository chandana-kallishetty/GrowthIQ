"""
GrowthIQ Data Loader
--------------------
Handles loading and caching of raw/synthetic CSV tables and database synchronization.
"""

from pathlib import Path
import sqlite3
import pandas as pd
from src.database.connection import get_connection, DB_PATH

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"
SQL_DIR = ROOT / "sql"

TABLE_FILES = {
    "product_categories": "product_categories.csv",
    "products": "products.csv",
    "customers": "customers.csv",
    "campaigns": "campaigns.csv",
    "campaign_spend": "campaign_spend.csv",
    "sessions": "sessions.csv",
    "events": "events.csv",
    "orders": "orders.csv",
    "order_items": "order_items.csv",
    "inventory": "inventory.csv",
}


def load_table(name: str, use_synthetic_dir: bool = False) -> pd.DataFrame:
    """Loads a specific CSV table with automated date parsing."""
    if name not in TABLE_FILES:
        raise ValueError(f"Unknown table '{name}'. Available: {list(TABLE_FILES.keys())}")

    base_dir = (DATA_DIR / "synthetic") if use_synthetic_dir else DATA_DIR
    file_path = base_dir / TABLE_FILES[name]

    # Fallback to main data/ if not found in synthetic/
    if not file_path.exists():
        file_path = DATA_DIR / TABLE_FILES[name]

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    df = pd.read_csv(file_path)
    for col in df.columns:
        if col.endswith("_date") or col.endswith("_timestamp"):
            df[col] = pd.to_datetime(df[col], errors="coerce")
    return df


def load_all_tables() -> dict:
    """Loads all 10 core tables into a dictionary of DataFrames."""
    return {tbl: load_table(tbl) for tbl in TABLE_FILES}


def build_database(force: bool = True, db_path: Path = None) -> Path:
    """
    Initializes SQLite schema and bulk-inserts all tabular CSV records.
    Enforces referential integrity in dependency order.
    """
    target_db = db_path or DB_PATH
    schema_path = SQL_DIR / "schema.sql"

    if not schema_path.exists():
        raise FileNotFoundError(f"Schema not found at {schema_path}")

    if force and target_db.exists():
        try:
            target_db.unlink()
        except PermissionError:
            pass  # if file is open, will drop and recreate tables

    schema_sql = schema_path.read_text(encoding="utf-8")

    # Ingestion order honoring foreign keys
    insertion_order = [
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
    ]

    with get_connection(target_db) as conn:
        conn.executescript(schema_sql)
        for tbl in insertion_order:
            if tbl in TABLE_FILES:
                df = load_table(tbl)
                # Convert datetime back to ISO strings for SQLite storage
                for col in df.columns:
                    if pd.api.types.is_datetime64_any_dtype(df[col]):
                        df[col] = df[col].dt.strftime("%Y-%m-%d %H:%M:%S").str.replace(" 00:00:00", "")
                df.to_sql(tbl, conn, if_exists="append", index=False)

    return target_db

