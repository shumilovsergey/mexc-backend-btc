import os, time
from flask import Flask, jsonify, request
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from db import (init_db, insert_prices,
                get_range, get_prices_in_range)
from fetch import fetch_btc_prices

# load .env
load_dotenv()

app = Flask(__name__)
init_db()

def load_job():
    now = int(time.time() * 1000)
    # e.g. last 24h; tweak as you like
    one_day = 24 * 3600 * 1000
    prices = fetch_btc_prices(now - one_day, now)
    if prices:
        insert_prices(prices)
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Loaded {len(prices)} entries")

# schedule every 15 minutes
scheduler = BackgroundScheduler()
scheduler.add_job(load_job, 'cron', minute='*/15')
scheduler.start()

@app.route("/")
def status():
    start, end = get_range()
    return jsonify(start_timestamp=start, end_timestamp=end)

@app.route("/load")
def load():
    now = int(time.time() * 1000)
    one_day = 24 * 3600 * 1000
    prices = fetch_btc_prices(now - one_day, now)
    if not prices:
        return " No data fetched (timeout or error)", 500
    insert_prices(prices)
    return f" Loaded {len(prices)} entries"

@app.route("/prices")
def prices():
    try:
        start = int(request.args["start"])
        end   = int(request.args["end"])
    except:
        return "Missing or invalid `start`/`end` query params", 400
    data = get_prices_in_range(start, end)
    return jsonify(data)

if __name__ == "__main__":
    app.run()
