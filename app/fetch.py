import logging
import requests

def fetch_btc_prices(start_time, end_time):
    url = "https://contract.mexc.com/api/v1/contract/kline"
    params = {
        "symbol":   "BTC_USDT",
        "interval": "Min15",
        "start":    start_time,
        "end":      end_time
    }
    try:
        res = requests.get(url, params=params, timeout=10)
        res.raise_for_status()
        return res.json().get("data", [])
    except requests.Timeout:
        logging.error(f"[TIMEOUT] Fetch {start_time}–{end_time}")
    except requests.RequestException as e:
        logging.error(f"[REQUEST ERROR] {e}")
    return []
