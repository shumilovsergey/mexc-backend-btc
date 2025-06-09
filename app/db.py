import sqlite3
import os

DB_PATH = os.getenv("DB_PATH", "/data/btc.db")

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
    for ts, open_, high, low, close_, vol in prices:
        c.execute("""
          INSERT OR IGNORE INTO btc_price
          (timestamp, open, high, low, close, volume)
          VALUES (?, ?, ?, ?, ?, ?)
        """, (ts, open_, high, low, close_, vol))
    conn.commit()
    conn.close()

def get_range():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT MIN(timestamp), MAX(timestamp) FROM btc_price")
    start, end = c.fetchone()
    conn.close()
    return start, end

def get_prices_in_range(start, end):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
      SELECT * FROM btc_price
      WHERE timestamp BETWEEN ? AND ?
      ORDER BY timestamp ASC
    """, (start, end))
    rows = c.fetchall()
    conn.close()
    return rows
