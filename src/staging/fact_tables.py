import pandas as pd
import os
import time
from datetime import datetime
from src.pipeline.extract.binance_extractor import BinanceKlineExtractor

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


def get_bridge_trade_context(
    start_time: int | None = None,
    end_time: int | None = None,
) -> pd.DataFrame:
    return (
        pd.concat(
            [
                BinanceKlineExtractor(symbol=symbol)
                .get_df(start_time=start_time, end_time=end_time)
                .assign(
                    date_key=lambda d: pd.to_datetime(d["date"])
                    .astype("int64")
                    .floordiv(10**9),
                    symbol=symbol,
                    exchange="Binance",
                    timeframe="1d",
                )
                .assign(
                    symbol_key=lambda d: d["symbol"].map(SYMBOL_MAP),
                    exchange_key=lambda d: d["exchange"].map(EXCHANGE_MAP),
                    timeframe_key=lambda d: d["timeframe"].map(TIMEFRAME_MAP),
                )
                for symbol in SYMBOL_MAP
            ],
            ignore_index=True,
        )
        .reset_index(drop=True)
        .assign(bridge_id=lambda d: d.index + 1)
        .reindex(
            columns=[
                "bridge_id",
                "date_key",
                "symbol_key",
                "exchange_key",
                "timeframe_key",
            ]
        )
    )


def get_fact_price(
    bridge: pd.DataFrame, start_time=None, end_time=None
) -> pd.DataFrame:
    return (
        pd.concat(
            [
                BinanceKlineExtractor(symbol=symbol)
                .get_df(start_time=start_time, end_time=end_time)
                .melt(
                    id_vars=["date"],
                    value_vars=["open", "high", "low", "close"],
                    var_name="price_type",
                    value_name="price",
                )
                .assign(
                    date_key=lambda d: pd.to_datetime(d["date"]).astype("int64")
                    // 10**9,
                    price_type_key=lambda d: d["price_type"].map(PRICE_TYPE_MAP),
                    symbol=symbol,
                    exchange="Binance",
                    timeframe="1d",
                )
                .assign(
                    symbol_key=lambda d: d["symbol"].map(SYMBOL_MAP),
                    exchange_key=lambda d: d["exchange"].map(EXCHANGE_MAP),
                    timeframe_key=lambda d: d["timeframe"].map(TIMEFRAME_MAP),
                )
                .merge(
                    bridge[
                        [
                            "bridge_id",
                            "date_key",
                            "symbol_key",
                            "exchange_key",
                            "timeframe_key",
                        ]
                    ],
                    on=["date_key", "symbol_key", "exchange_key", "timeframe_key"],
                    how="inner",
                )
                for symbol in SYMBOL_MAP
            ],
            ignore_index=True,
        )
        .filter(items=["bridge_id", "price_type_key", "price"])
        .reindex(columns=["bridge_id", "price_type_key", "price"])
        .rename(columns={"bridge_id": "bridge_key"})
    )


def get_fact_volume(
    bridge: pd.DataFrame,
    start_time: int | None = None,
    end_time: int | None = None,
) -> pd.DataFrame:
    rename_map = {
        "volume": "base_volume",
        "quote_asset_volume": "quote_volume",
        "taker_buy_base_asset_volume": "taker_buy_base_volume",
        "taker_buy_quote_asset_volume": "taker_buy_quote_volume",
    }
    return (
        pd.concat(
            [
                BinanceKlineExtractor(symbol=symbol)
                .get_df(start_time=start_time, end_time=end_time)
                .rename(columns=rename_map)
                .melt(
                    id_vars=["date"],
                    value_vars=list(rename_map.values()),
                    var_name="volume_type",
                    value_name="volume",
                )
                .assign(
                    date_key=lambda d: pd.to_datetime(d["date"]).astype("int64")
                    // 10**9,
                    volume_type_key=lambda d: d["volume_type"].map(VOLUME_TYPE_MAP),
                    symbol=symbol,
                    exchange="Binance",
                    timeframe="1d",
                )
                .assign(
                    symbol_key=lambda d: d["symbol"].map(SYMBOL_MAP),
                    exchange_key=lambda d: d["exchange"].map(EXCHANGE_MAP),
                    timeframe_key=lambda d: d["timeframe"].map(TIMEFRAME_MAP),
                )
                .merge(
                    bridge[
                        [
                            "bridge_id",
                            "date_key",
                            "symbol_key",
                            "exchange_key",
                            "timeframe_key",
                        ]
                    ],
                    on=["date_key", "symbol_key", "exchange_key", "timeframe_key"],
                    how="inner",
                )
                for symbol in SYMBOL_MAP
            ],
            ignore_index=True,
        )
        .filter(items=["bridge_id", "volume_type_key", "volume"])
        .reindex(columns=["bridge_id", "volume_type_key", "volume"])
        .rename(columns={"bridge_id": "bridge_key"})
    )


def get_fact_num_trades(
    bridge: pd.DataFrame,
    start_time: int | None = None,
    end_time: int | None = None,
) -> pd.DataFrame:
    return (
        pd.concat(
            [
                BinanceKlineExtractor(symbol=symbol)
                .get_df(start_time=start_time, end_time=end_time)
                .assign(
                    date_key=lambda d: pd.to_datetime(d["date"]).astype("int64")
                    // 10**9,
                    symbol=symbol,
                    exchange="Binance",
                    timeframe="1d",
                )
                .assign(
                    symbol_key=lambda d: d["symbol"].map(SYMBOL_MAP),
                    exchange_key=lambda d: d["exchange"].map(EXCHANGE_MAP),
                    timeframe_key=lambda d: d["timeframe"].map(TIMEFRAME_MAP),
                )
                .merge(
                    bridge[
                        [
                            "bridge_id",
                            "date_key",
                            "symbol_key",
                            "exchange_key",
                            "timeframe_key",
                        ]
                    ],
                    on=["date_key", "symbol_key", "exchange_key", "timeframe_key"],
                    how="inner",
                )
                for symbol in SYMBOL_MAP
            ],
            ignore_index=True,
        )
        .filter(items=["bridge_id", "number_of_trades"])
        .reindex(columns=["bridge_id", "number_of_trades"])
        .rename(columns={"bridge_id": "bridge_key"})
    )


if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    OUTPUT_DIR = os.path.join(BASE_DIR, "..", "..", "init-db", "data")
    start_time = int(datetime(2017, 1, 1).timestamp() * 1000)
    end_time = int(time.time() * 1000)
    bridge = get_bridge_trade_context()

    get_bridge_trade_context(start_time=start_time, end_time=end_time).to_csv(
        os.path.join(OUTPUT_DIR, "bridge_trade_context.csv"), index=False
    )

    get_fact_price(
        bridge=bridge,
        start_time=start_time,
        end_time=end_time,
    ).to_csv(os.path.join(OUTPUT_DIR, "fact_price.csv"), index=False)

    get_fact_volume(
        bridge=bridge,
        start_time=start_time,
        end_time=end_time,
    ).to_csv(os.path.join(OUTPUT_DIR, "fact_volume.csv"), index=False)

    get_fact_num_trades(
        bridge=bridge,
        start_time=start_time,
        end_time=end_time,
    ).to_csv(os.path.join(OUTPUT_DIR, "fact_num_trades.csv"), index=False)
