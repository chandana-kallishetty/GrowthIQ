"""
GrowthIQ SQLite Database Builder Script
---------------------------------------
Builds and populates growthiq.db from sql/schema.sql and CSV tables.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.data.loader import build_database
from src.database.connection import get_connection

if __name__ == "__main__":
    print("Building GrowthIQ SQLite database...")
    db_path = build_database(force=True)
    print(f"Database successfully built at: {db_path}")

    # Verify table row counts in SQLite
    tables = [
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

    print("\nVerifying SQLite table row counts:")
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        for tbl in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {tbl};")
            count = cursor.fetchone()[0]
            print(f"  ✓ {tbl:<22} {count:>8,} rows")

    print("\nDatabase build and verification complete!")
