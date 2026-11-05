"""
GrowthIQ Database Connection Module
-----------------------------------
Provides thread-safe SQLite connection management with foreign key enforcement
and WAL (Write-Ahead Logging) mode for concurrent dashboard reads.
"""

import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DB_PATH = ROOT / "growthiq.db"


def get_connection(db_path: Path = None) -> sqlite3.Connection:
    """Returns an active SQLite connection with row factory and foreign keys enabled."""
    target_path = db_path or DB_PATH
    conn = sqlite3.connect(str(target_path))
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.row_factory = sqlite3.Row
    return conn

