"""SQLite storage, compatible with existing TEXT-based databases."""
import sqlite3
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path(__file__).resolve().with_name("currencies.db")


def get_db_connection():
    return sqlite3.connect(str(DB_PATH), timeout=5)


def create_table():
    with closing(get_db_connection()) as con, con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS tgju(
                dollar TEXT,
                pound TEXT,
                euro TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)


def add_row(usd, gbp, eur):
    values = tuple(int(value) for value in (usd, gbp, eur))
    if any(value <= 0 for value in values):
        raise ValueError("All prices must be positive tomans")
    with closing(get_db_connection()) as con, con:
        con.execute(
            "INSERT INTO tgju (dollar, pound, euro, created_at) "
            "VALUES (?, ?, ?, CURRENT_TIMESTAMP)", values
        )


def retrieve_latest():
    """Return the latest valid snapshot, or None for missing/invalid data.

    Database errors propagate for callers to handle. Skip invalid legacy rows.
    """
    create_table()
    with closing(get_db_connection()) as con:
        rows = con.execute(
            "SELECT dollar, pound, euro, created_at FROM tgju ORDER BY rowid DESC"
        )
        for row in rows:
            try:
                prices = tuple(int(value) for value in row[:3])
                updated_at = datetime.fromisoformat(row[3]).replace(tzinfo=timezone.utc)
                if all(value > 0 for value in prices):
                    return dict(zip(("dollar", "pound", "euro"), prices),
                                updated_at=updated_at)
            except (ValueError, TypeError):
                continue
    return None


def retrieve_dollar():
    latest = retrieve_latest()
    return latest["dollar"] if latest else None


def retrieve_pound():
    latest = retrieve_latest()
    return latest["pound"] if latest else None


def retrieve_euro():
    latest = retrieve_latest()
    return latest["euro"] if latest else None
