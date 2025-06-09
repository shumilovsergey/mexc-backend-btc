import time
import atexit
from flask import Flask, jsonify, request
from apscheduler.schedulers.background import BackgroundScheduler

from db import init_db, insert_prices, get_min_max_timestamps, get_prices
from fetch import fetch_btc_prices

app = Flask(__name__)
init_db()

# Job to fetch new price data every hour
def data_fetch_job():
    now = int(time.time() * 1000)
    mn, mx = get_min_max_timestamps()
    start = mx + 1 if mx else now - 24 * 60 * 60 * 1000
    prices = fetch_btc_prices(start, now)
    insert_prices(prices)
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Fetched {len(prices)} entries from {start} to {now}")

# Scheduler setup
scheduler = BackgroundScheduler()
scheduler.add_job(func=data_fetch_job, trigger='interval', minutes=60)
scheduler.start()
atexit.register(lambda: scheduler.shutdown())

# 1️⃣ Progress route: shows min/max timestamps in DB
@app.route("/")
def progress():
    mn, mx = get_min_max_timestamps()
    return jsonify({"start_timestamp": mn, "end_timestamp": mx})

# 2️⃣ Manual load route
@app.route("/load")
def load_route():
    data_fetch_job()
    return "Load job executed", 200

# 3️⃣ Prices route with start/end query parameters
@app.route("/prices")
def prices_route():
    start = request.args.get("start", type=int)
    end = request.args.get("end", type=int)
    data = get_prices(start, end)
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)