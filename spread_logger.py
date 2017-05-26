from repeated_timer import RepeatedTimer
# from coinbase.wallet.client import Client
import requests
import json
import datetime
import time
import csv

# Not being used yet
# client = Client("api_key", "secret_key")

gemini_url = "https://api.gemini.com/v1"
coinbase_url = "https://api.coinbase.com/v2/prices/ETH-USD"

CURR_TO_API = {
    "gemini": {
        "ETH": "https://api.gemini.com/v1/pubticker/ethusd",
        "BTC": "https://api.gemini.com/v1/pubticker/btcusd"
    },
    "coinbase": {
        "ETH": "https://api.coinbase.com/v2/prices/ETH-USD",
        "BTC": "https://api.coinbase.com/v2/prices/BTC-USD"
    },
}


def fetch_gemini_to_coinbase(curr):
    buy_response = requests.get(CURR_TO_API["gemini"][curr])  # Gemini PI Response
    sell_response = requests.get(CURR_TO_API["coinbase"][curr] + "/sell")
    buy_price = float(json.loads(buy_response.text)["ask"])
    sell_price = float(json.loads(sell_response.text)['data']['amount'])

    profit_amount = sell_price - buy_price
    profit_rate = (profit_amount / buy_price) * 100

    return {
        "buy_price": buy_price,
        "sell_price": sell_price,
        "profit_amount": profit_amount,
        "profit_rate": profit_rate,
        "buy_company": "Gemini",
        "sell_company": "Coinbase",
        "curr": curr
    }


def fetch_coinbase_to_gemini(curr):
    sell_response = requests.get(CURR_TO_API["gemini"][curr])  # Gemini PI Response
    buy_response = requests.get(CURR_TO_API["coinbase"][curr] + "/buy")  # Coinbase PI Response
    sell_price = float(json.loads(sell_response.text)["bid"])
    buy_price = float(json.loads(buy_response.text)['data']['amount'])

    profit_amount = sell_price - buy_price
    profit_rate = (profit_amount / buy_price) * 100

    return {
        "buy_price": buy_price,
        "sell_price": sell_price,
        "profit_amount": profit_amount,
        "profit_rate": profit_rate,
        "buy_company": "Coinbase",
        "sell_company": "Gemini",
        "curr": curr
    }


def create_timestamp():
    return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')


def fetch_curr_spread(curr):
    c_to_g = fetch_coinbase_to_gemini(curr)
    g_to_c = fetch_gemini_to_coinbase(curr)

    spread_data = c_to_g if c_to_g["profit_amount"] > g_to_c["profit_amount"] else g_to_c

    return spread_data


def print_curr_spread(spread_data, timestamp):
    curr = spread_data["curr"]
    print("\n" + curr + " " + timestamp + ":")

    print("Buy: " + spread_data["buy_company"] + " " + '${:,.2f}'.format(spread_data["buy_price"]))
    print("Sell: " + spread_data["sell_company"] + " " + '${:,.2f}'.format(spread_data["sell_price"]))
    print("Profit: " + '${:,.2f}'.format(spread_data["profit_amount"]))
    print("Return: " + '{:,.2f}%'.format(spread_data["profit_rate"]))


def create_log_file(spread):
    row = [
        datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
        spread["curr"],
        spread["buy_company"],
        '${:,.2f}'.format(spread["profit_amount"]),
        '{:,.2f}%'.format(spread["profit_rate"])
    ]

    with open('./spread_logger.csv', 'a') as f:
        w = csv.writer(f)
        w.writerow(row)


def fetch_price_spread(seconds_interval):
    print("\nfetching spread...\n")

    eth_spread = fetch_curr_spread("ETH")
    btc_spread = fetch_curr_spread("BTC")

    timestamp = create_timestamp()

    print_curr_spread(eth_spread, timestamp)
    print_curr_spread(btc_spread, timestamp)

    create_log_file(eth_spread)
    create_log_file(btc_spread)

    print("\nfetching complete. fetching again in " + str(seconds_interval) + " seconds\n")


def run_spread_logger(seconds_interval=60):
    header_row = ["Timestamp", "Currency", "Buy Exchange", "Profit", "Return"]

    with open('./spread_logger.csv', 'a') as f:
        w = csv.writer(f)
        w.writerow(header_row)

    print("starting...\n")
    RepeatedTimer(seconds_interval, fetch_price_spread, seconds_interval)


run_spread_logger()

