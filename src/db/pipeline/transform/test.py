import pandas as pd
import os
import time
from datetime import datetime
from src.extractors.binance_extractor import BinanceKlineExtractor
from src.utils.logger import logger

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
    "ETCUSDT": 2,
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


def get_bridge_trade_context_df(
    start_time: int | None = None,
    end_time: int | None = None,
):
    dfs = []
    for symbol in SYMBOL_MAP:
        try:
            df = BinanceKlineExtractor(symbol=symbol).get_df(
                start_time=start_time, end_time=end_time, timeframe="1d"
            )
            if df.empty:
                logger.warning(f"No data returned for {symbol}")
                continue
            df = df.assign(
                date_key=lambda d: pd.to_datetime(d["date"]).astype("int64") // 10**9,
                symbol=symbol,
                exchange="Binance",
                timeframe="1d",
            ).assign(
                symbol_key=lambda d: d["symbol"].map(SYMBOL_MAP),
                exchange_key=lambda d: d["exchange"].map(EXCHANGE_MAP),
                timeframe_key=lambda d: d["timeframe"].map(TIMEFRAME_MAP),
            )
            dfs.append(df)
        except Exception as e:
            logger.error(f"Error fetching data for {symbol}: {e}")
            continue
    if not dfs:
        logger.error("No data fetched for any symbol")
        return pd.DataFrame(
            columns=[
                "bridge_id",
                "date_key",
                "symbol_key",
                "exchange_key",
                "timeframe_key",
            ]
        )
    return (
        pd.concat(dfs, ignore_index=True)
        .drop_duplicates(
            subset=["date_key", "symbol_key", "exchange_key", "timeframe_key"]
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


def get_bridge_trade_context(
    start_time: int | None = None,
    end_time: int | None = None,
    output_path: str = "bridge_trade_context.csv",
):
    df = get_bridge_trade_context_df(start_time=start_time, end_time=end_time)
    df.to_csv(output_path, index=False)
    logger.info(f"CSV file created at: {output_path}")
    return df


def get_fact_price(
    bridge: pd.DataFrame,
    start_time: int | None = None,
    end_time: int | None = None,
    output_path: str = "fact_price.csv",
):
    dfs = []
    for symbol in SYMBOL_MAP:
        try:
            df = BinanceKlineExtractor(symbol=symbol).get_df(
                start_time=start_time, end_time=end_time, timeframe="1d"
            )
            if df.empty:
                logger.warning(f"No data returned for {symbol} in get_fact_price")
                continue
            df = (
                df.melt(
                    id_vars=["date"],
                    value_vars=["open", "high", "low", "close"],
                    var_name="price_type",
                    value_name="price",
                )
                .assign(
                    date_key=lambda d: pd.to_datetime(d["date"]).astype("int64")
                    // 10**9,
                    price_type_key=lambda d: d["price_type"].map(PRICE_TYPE_MAP),
                )
                .merge(bridge[["bridge_id", "date_key"]], on="date_key", how="inner")
            )
            if df.empty:
                logger.warning(
                    f"No matching rows for {symbol} after merge in get_fact_price"
                )
                continue
            dfs.append(df)
        except Exception as e:
            logger.error(f"Error processing {symbol} in get_fact_price: {e}")
            continue
    if not dfs:
        logger.error("No data processed for any symbol in get_fact_price")
        return pd.DataFrame(columns=["bridge_key", "price_type_key", "price"]).to_csv(
            output_path, index=False
        )
    result = (
        pd.concat(dfs, ignore_index=True)
        .reindex(["bridge_id", "price_type_key", "price"])
        .rename(columns={"bridge_id": "bridge_key"})
    )
    result.to_csv(output_path, index=False)
    logger.info(f"CSV file created at: {output_path}")
    return result


def get_fact_volume(
    bridge: pd.DataFrame,
    start_time: int | None = None,
    end_time: int | None = None,
    output_path: str = "fact_volume.csv",
):
    rename_map = {
        "volume": "base_volume",
        "quote_asset_volume": "quote_volume",
        "taker_buy_base_asset_volume": "taker_buy_base_volume",
        "taker_buy_quote_asset_volume": "taker_buy_quote_volume",
    }
    dfs = []
    for symbol in SYMBOL_MAP:
        try:
            df = BinanceKlineExtractor(symbol=symbol).get_df(
                start_time=start_time, end_time=end_time, timeframe="1d"
            )
            if df.empty:
                logger.warning(f"No data returned for {symbol} in get_fact_volume")
                continue
            df = (
                df.rename(columns=rename_map)
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
                )
                .merge(bridge[["bridge_id", "date_key"]], on="date_key", how="inner")
            )
            if df.empty:
                logger.warning(
                    f"No matching rows for {symbol} after merge in get_fact_volume"
                )
                continue
            dfs.append(df)
        except Exception as e:
            logger.error(f"Error processing {symbol} in get_fact_volume: {e}")
            continue
    if not dfs:
        logger.error("No data processed for any symbol in get_fact_volume")
        return pd.DataFrame(columns=["bridge_key", "volume_type_key", "volume"]).to_csv(
            output_path, index=False
        )
    result = (
        pd.concat(dfs, ignore_index=True)
        .reindex(["bridge_id", "volume_type_key", "volume"])
        .rename(columns={"bridge_id": "bridge_key"})
    )
    result.to_csv(output_path, index=False)
    logger.info(f"CSV file created at: {output_path}")
    return result


def get_fact_num_trades(
    bridge: pd.DataFrame,
    start_time: int | None = None,
    end_time: int | None = None,
    output_path: str = "fact_num_trades.csv",
):
    dfs = []
    for symbol in SYMBOL_MAP:
        try:
            df = BinanceKlineExtractor(symbol=symbol).get_df(
                start_time=start_time, end_time=end_time, timeframe="1d"
            )
            if df.empty:
                logger.warning(f"No data returned for {symbol} in get_fact_num_trades")
                continue
            df = df.assign(
                date_key=lambda d: pd.to_datetime(d["date"]).astype("int64") // 10**9,
                number_of_trades=lambda d: d["number_of_trades"].astype(int),
            ).merge(bridge[["bridge_id", "date_key"]], on="date_key", how="inner")
            if df.empty:
                logger.warning(
                    f"No matching rows for {symbol} after merge in get_fact_num_trades"
                )
                continue
            dfs.append(df)
        except Exception as e:
            logger.error(f"Error processing {symbol} in get_fact_num_trades: {e}")
            continue
    if not dfs:
        logger.error("No data processed for any symbol in get_fact_num_trades")
        return pd.DataFrame(columns=["bridge_key", "number_of_trades"]).to_csv(
            output_path, index=False
        )
    result = (
        pd.concat(dfs, ignore_index=True)
        .reindex(["bridge_id", "number_of_trades"])
        .rename(columns={"bridge_id": "bridge_key"})
    )
    result.to_csv(output_path, index=False)
    logger.info(f"CSV file created at: {output_path}")
    return result


if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    OUTPUT_DIR = os.path.join(BASE_DIR, "..", "..", "init-db", "data")
    start_time = int(datetime(2017, 1, 1).timestamp() * 1000)
    end_time = int(time.time() * 1000)
    bridge = get_bridge_trade_context_df(start_time=start_time, end_time=end_time)

    get_bridge_trade_context(
        start_time=start_time,
        end_time=end_time,
        output_path=os.path.join(OUTPUT_DIR, "bridge_trade_context.csv"),
    )
    get_fact_price(
        bridge=bridge,
        start_time=start_time,
        end_time=end_time,
        output_path=os.path.join(OUTPUT_DIR, "fact_price.csv"),
    )
    get_fact_volume(
        bridge=bridge,
        start_time=start_time,
        end_time=end_time,
        output_path=os.path.join(OUTPUT_DIR, "fact_volume.csv"),
    )
    get_fact_num_trades(
        bridge=bridge,
        start_time=start_time,
        end_time=end_time,
        output_path=os.path.join(OUTPUT_DIR, "fact_num_trades.csv"),
    )
