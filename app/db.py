import sqlite3

# Use /data so DB file persists via mounted volume
DB_PATH = "/data/btc.db"

# Initialize the SQLite database and table
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

# Insert multiple price entries, ignoring duplicates
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

# Get the minimum and maximum timestamps stored
def get_min_max_timestamps():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT MIN(timestamp), MAX(timestamp) FROM btc_price")
    mn, mx = c.fetchone()
    conn.close()
    return mn, mx

# Retrieve price data, optionally filtered by start/end timestamps
def get_prices(start=None, end=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if start is not None and end is not None:
        c.execute(
            "SELECT * FROM btc_price WHERE timestamp BETWEEN ? AND ? ORDER BY timestamp ASC", 
            (start, end)
        )
    else:
        c.execute("SELECT * FROM btc_price ORDER BY timestamp ASC")
    rows = c.fetchall()
    conn.close()
    return rows