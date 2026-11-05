"""
GrowthIQ Database Query Helpers
-------------------------------
Executes analytical SQL queries against the local SQLite database and returns
strongly typed pandas DataFrames.
"""

from pathlib import Path
import pandas as pd
from .connection import get_connection

ROOT = Path(__file__).resolve().parents[2]
SQL_DIR = ROOT / "sql"


def execute_query(query: str, params=None) -> pd.DataFrame:
    """Executes a SQL query string and returns results as a pandas DataFrame."""
    conn = get_connection()
    try:
        return pd.read_sql_query(query, conn, params=params)
    finally:
        conn.close()


def load_analysis_queries() -> dict:
    """Parses and returns named queries from sql/analysis_queries.sql."""
    file_path = SQL_DIR / "analysis_queries.sql"
    if not file_path.exists():
        return {}
    content = file_path.read_text(encoding="utf-8")
    queries = {}
    sections = content.split("-- QUERY ")
    for sec in sections[1:]:
        lines = sec.strip().split("\n")
        title_line = lines[0]
        query_text = "\n".join(lines[1:])
        queries[title_line.strip()] = query_text.strip()
    return queries

