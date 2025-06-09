import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")  # reserved for future authenticated endpoints

# Fetch historical BTC price data from MEXC
def fetch_btc_prices(start_time, end_time):
    url = "https://contract.mexc.com/api/v1/contract/kline"
    params = {
        "symbol": "BTC_USDT",
        "interval": "Min15",
        "start": start_time,
        "end": end_time
    }
    headers = {}
    if API_KEY:
        headers["ApiKey"] = API_KEY
    res = requests.get(url, params=params, headers=headers)
    res.raise_for_status()
    return res.json().get("data", [])