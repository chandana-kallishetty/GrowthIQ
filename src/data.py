"""
GrowthIQ Data Module Facade (Backward Compatible)
"""

from src.data.loader import load_table, load_all_tables, build_database, TABLE_FILES, ROOT, DATA_DIR as DATA, DB_PATH as DB
from src.database.connection import get_connection
from src.data.cleaning import clean_order_facts, clean_sessions_data
from src.data.validation import (
    run_full_validation_suite,
    check_primary_keys,
    check_foreign_keys,
    check_business_constraints,
)

__all__ = [
    "load_table",
    "load_all_tables",
    "build_database",
    "get_connection",
    "TABLE_FILES",
    "ROOT",
    "DATA",
    "DB",
    "clean_order_facts",
    "clean_sessions_data",
    "run_full_validation_suite",
    "check_primary_keys",
    "check_foreign_keys",
    "check_business_constraints",
]
