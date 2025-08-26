import requests
import time
import csv
import os
import logging
from datetime import datetime
from typing import Optional, List, Dict, Any

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


class BinanceKlineExtractor:
    BASE_URL = "https://api3.binance.com"
    ENDPOINT = "/api/v3/klines"

    def __init__(
        self,
        symbol: str = "BTCUSDT",
        interval: str = "1d",
        limit: int = 500,
        output_folder: str = "./",
    ):
        self.symbol = symbol
        self.interval = interval
        self.limit = limit
        self.output_folder = output_folder
        self.params = {
            "symbol": self.symbol,
            "interval": self.interval,
            "limit": self.limit,
        }

    def timestamp_to_date_format(
        self, timestamp: int, date_format: str = "%Y-%m-%d"
    ) -> str:
        return datetime.fromtimestamp(timestamp / 1000).strftime(date_format)

    def extract_kline_data(self, kline: List) -> Dict[str, Any]:
        date = self.timestamp_to_date_format(kline[0], "%Y-%m-%d %H:%M:%S")

        return {
            "date": date,
            "open": kline[1],
            "high": kline[2],
            "low": kline[3],
            "close": kline[4],
            "volume": kline[5],
            "close_time": self.timestamp_to_date_format(kline[6], "%Y-%m-%d %H:%M:%S"),
            "quote_asset_volume": kline[7],
            "number_of_trades": kline[8],
            "taker_buy_base_asset_volume": kline[9],
            "taker_buy_quote_asset_volume": kline[10],
        }

    def get_data(
        self, start_time: Optional[int] = None, end_time: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        params = self.params.copy()
        if start_time:
            params["startTime"] = start_time
        if end_time:
            params["endTime"] = end_time
        else:
            params["endTime"] = int(time.time() * 1000)

        logger.info(f"Fetching data for {self.symbol} with interval {self.interval}")

        data = []
        while True:
            try:
                response = requests.get(self.BASE_URL + self.ENDPOINT, params=params)
                response.raise_for_status()

                klines = response.json()
                if not klines:
                    break

                for kline in klines:
                    data.append(self.extract_kline_data(kline))

                params["startTime"] = klines[-1][0] + 1
                logger.info(f"Fetched {len(klines)} records, total: {len(data)}")

                if len(klines) < self.limit:
                    break

            except requests.exceptions.RequestException as e:
                logger.error(f"Request failed: {e}")
                break

        return data

    def export_data(
        self, data: List[Dict[str, Any]], filename: Optional[str] = None
    ) -> str:
        if not data:
            logger.warning("No data to export")
            return ""

        if not filename:
            start_date = data[0]["date"].split(" ")[0]
            end_date = data[-1]["date"].split(" ")[0]
            filename = f"{self.symbol}_{start_date}_to_{end_date}_{self.interval}.csv"

        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
            logger.info(f"Created output directory: {self.output_folder}")

        filepath = os.path.join(self.output_folder, filename)

        if os.path.exists(filepath):
            response = input(f"File {filepath} already exists. Overwrite? (y/n): ")
            if response.lower() != "y":
                logger.info("Export cancelled by user")
                return ""

        with open(filepath, "w", newline="") as f:
            if data:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)

        logger.info(f"Data exported to {filepath}")
        return filepath


if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    OUTPUT_DIR = os.path.join(BASE_DIR, "..", "..", "init-db", "data")

    for symbol in ["BTCUSDT", "ETCUSDT", "BNBUSDT", "SOLUSDT"]:
        extractor = BinanceKlineExtractor(
            symbol=symbol, interval="1d", limit=1000, output_folder=OUTPUT_DIR
        )

        start_time = int(datetime(2000, 1, 1).timestamp() * 1000)

        data = extractor.get_data(start_time=start_time)

        if data:
            extractor.export_data(data)
