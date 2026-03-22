import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "..", "..", "init-db", "data")

PRICE_TYPE_MAP = {
    "open": 1,
    "high": 2,
    "low": 3,
    "close": 4,
}

VOLUME_TYPE_MAP = {
    "base_volume": 1,
    "quote_volume": 2,
    "taker_buy_base_volume": 3,
    "taker_buy_quote_volume": 4,
}

EXCHANGE_MAP = {
    "Binance": 1,
    "Coinbase": 2,
    "Kucoin": 3,
    "Bitstamp": 4,
    "Kraken": 5,
    "Bitfinex": 6,
    "Huobi": 7,
    "OKX": 8,
    "Bybit": 9,
    "Gemini": 10,
}

SYMBOL_MAP = {
    "BTCUSDT": 1,
    "ETHUSDT": 2,
    "XRPUSDT": 3,
    "BNBUSDT": 4,
    "SOLUSDT": 5,
}

TIMEFRAME_MAP = {
    "1m": 1,
    "3m": 2,
    "5m": 3,
    "15m": 4,
    "30m": 5,
    "1h": 6,
    "2h": 7,
    "4h": 8,
    "6h": 9,
    "8h": 10,
    "12h": 11,
    "1d": 12,
    "3d": 13,
    "1w": 14,
    "1mo": 15,
}
