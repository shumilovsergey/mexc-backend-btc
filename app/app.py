import os
import time
import logging
from flask import Flask, jsonify, request
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler

from db import init_db, insert_prices, get_range, get_prices_in_range
from fetch import fetch_btc_prices

# Load .env
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

app = Flask(__name__)
init_db()

def load_job():
    now = int(time.time() * 1000)
    one_day = 24 * 3600 * 1000
    start_ts = now - one_day
    logging.info(f"Scheduled fetch: {start_ts} → {now}")
    prices = fetch_btc_prices(start_ts, now)
    logging.info(f"Received {len(prices)} entries")
    if prices:
        insert_prices(prices)
        logging.info(f"Stored {len(prices)} new rows")
    else:
        logging.error("⚠️ No data fetched in scheduled job")

# Schedule every 15 minutes
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
    logging.info("Manual /load triggered")
    prices = fetch_btc_prices(now - one_day, now)
    if not prices:
        logging.error(" No data fetched (timeout or error)")
        return " No data fetched (timeout or error)", 500
    insert_prices(prices)
    logging.info(f"Loaded {len(prices)} entries")
    return f"Loaded {len(prices)} entries"

@app.route("/prices")
def prices():
    try:
        start = int(request.args["start"])
        end   = int(request.args["end"])
    except (KeyError, ValueError):
        return "Missing or invalid `start`/`end` query params", 400
    data = get_prices_in_range(start, end)
    return jsonify(data)

if __name__ == "__main__":
    # Flask will use FLASK_RUN_HOST and FLASK_RUN_PORT from env
    app.run()
