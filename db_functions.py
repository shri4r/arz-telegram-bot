import sqlite3


def create_table():
    # Connect to the SQLite database file "currencies.db"
    # If the file doesn't exist, it will be created.
    con = sqlite3.connect("currencies.db")
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tgju(
            dollar TEXT,
            pound TEXT,
            euro TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    con.commit()
    con.close()


def add_row(usd, gbp, eur):
    con = sqlite3.connect("currencies.db")
    cur = con.cursor()
    cur.execute("INSERT INTO tgju VALUES (?, ?, ?, CURRENT_TIMESTAMP)", (usd, gbp, eur))
    con.commit()
    con.close()


def retrieve_dollar():
    con = sqlite3.connect("currencies.db")
    cur = con.cursor()
    cur.execute("SELECT dollar FROM tgju ORDER BY rowid DESC LIMIT 1")
    dollar = cur.fetchone()[0]
    con.close()
    return dollar


def retrieve_pound():
    con = sqlite3.connect("currencies.db")
    cur = con.cursor()
    cur.execute("SELECT pound FROM tgju ORDER BY rowid DESC LIMIT 1")
    pound = cur.fetchone()[0]
    con.close()
    return pound


def retrieve_euro():
    con = sqlite3.connect("currencies.db")
    cur = con.cursor()
    cur.execute("SELECT euro FROM tgju ORDER BY rowid DESC LIMIT 1")
    euro = cur.fetchone()[0]
    con.close()
    return euro
