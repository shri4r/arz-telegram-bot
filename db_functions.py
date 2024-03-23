import sqlite3


def create_table():
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


def add_row(usd, gbp, eu):
    con = sqlite3.connect("currencies.db")
    cur = con.cursor()
    cur.execute("INSERT INTO tgju VALUES (?, ?, ?)", (usd, gbp, eu))
    con.commit()
    con.close()


def retrieve_dollar():
    con = sqlite3.connect("currencies.db")
    cur = con.cursor()
    cur.execute("SELECT dollar FROM tgju")
    dollar = cur.fetchone()[0]
    con.close()
    return dollar


def retrieve_pound():
    con = sqlite3.connect("currencies.db")
    cur = con.cursor()
    cur.execute("SELECT pound FROM tgju")
    pound = cur.fetchone()[0]
    con.close()
    return pound


def retrieve_euro():
    con = sqlite3.connect("currencies.db")
    cur = con.cursor()
    cur.execute("SELECT euro FROM tgju")
    euro = cur.fetchone()[0]
    con.close()
    return euro
