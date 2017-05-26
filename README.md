# spread-logger

Logs the spread for BTC and ETH between Gemini and Coinbase

[Coinbase API docs](https://developers.coinbase.com/api/v2?python#introduction)
[Gemini API docs](https://docs.gemini.com/rest-api/#introduction)

# How to use
1. Clone this repo
2. I use Python3.4 for this, so `mkvirtualenv` using Python3.4.
3. `pip install -r requirements.txt`
4. Run `spread_logger.py` (ie: `python spread_logger.py`) and leave it running for as long as you want. The default to check for the latest prices is 60 seconds,
but you can change that by editing the last line in `spread_logger` (ie: to run every 20 seconds, `run_spread_logger(20)`) but be careful about hitting rate limits
