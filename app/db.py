import sqlite3

DB_PATH = "btc.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS btc_price (
        timestamp INTEGER PRIMARY KEY,
        open REAL,
        high REAL,
        low REAL,
        close REAL,
        volume REAL
    )
    """)
    conn.commit()
    conn.close()


def insert_prices(prices):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for p in prices:
        c.execute("""
        INSERT OR IGNORE INTO btc_price (timestamp, open, high, low, close, volume)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (p[0], p[1], p[2], p[3], p[4], p[5]))
    conn.commit()
    conn.close()


def get_min_max_timestamps():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT MIN(timestamp), MAX(timestamp) FROM btc_price")
    mn, mx = c.fetchone()
    conn.close()
    return mn, mx


def get_prices(start=None, end=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if start and end:
        c.execute(
            "SELECT * FROM btc_price WHERE timestamp BETWEEN ? AND ? ORDER BY timestamp ASC",
            (start, end)
        )
    else:
        c.execute("SELECT * FROM btc_price ORDER BY timestamp ASC")
    rows = c.fetchall()
    conn.close()
    return rows