import sqlite3


def get_db_connection():
    """Return a new connection to the database."""
    return sqlite3.connect("currencies.db")


def create_table():
    """Create the tgju table if it doesn't exist."""
    try:
        with get_db_connection() as con:
            cur = con.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS tgju(
                    dollar TEXT,
                    pound TEXT,
                    euro TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if con:
            con.close()


def add_row(usd, gbp, eur):
    """Add a new row to the tgju table."""
    try:
        with get_db_connection() as con:
            cur = con.cursor()
            cur.execute(
                "INSERT INTO tgju VALUES (?, ?, ?, CURRENT_TIMESTAMP)", (usd, gbp, eur)
            )
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if con:
            con.close()


def retrieve_dollar():
    """Retrieve the latest dollar value from the tgju table."""
    try:
        with get_db_connection() as con:
            cur = con.cursor()
            cur.execute("SELECT dollar FROM tgju ORDER BY rowid DESC LIMIT 1")
            dollar = cur.fetchone()[0]
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if con:
            con.close()
    return dollar


def retrieve_pound():
    """Retrieve the latest pound value from the tgju table."""
    try:
        with get_db_connection() as con:
            cur = con.cursor()
            cur.execute("SELECT pound FROM tgju ORDER BY rowid DESC LIMIT 1")
            pound = cur.fetchone()[0]
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if con:
            con.close()
    return pound


def retrieve_euro():
    """Retrieve the latest euro value from the tgju table."""
    try:
        with get_db_connection() as con:
            cur = con.cursor()
            cur.execute("SELECT euro FROM tgju ORDER BY rowid DESC LIMIT 1")
            euro = cur.fetchone()[0]
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if con:
            con.close()
    return euro
