import csv
import os
from datetime import datetime, timedelta
from typing import Union
from src.utils.logger import logger

def get_dim_date(
    start_date: Union[str, datetime],
    end_date: Union[str, datetime],
    output_path: str = "dim_date.csv",
) -> None:
    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
    if isinstance(end_date, str):
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

    with open(output_path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["date_id", "full_date"])

        current_date = start_date
        while current_date <= end_date:
            unix_ts = int(current_date.timestamp())
            writer.writerow([unix_ts, current_date.date().isoformat()])
            current_date += timedelta(days=1)

    logger.info("CSV file created at: {outut_path}")

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    OUTPUT_DIR = os.path.join(BASE_DIR, "..", "..", "init-db", "data")

    get_dim_date(
            start_date="2015-01-01",
            end_date="2025-12-31",
            output_path=os.path.join(OUTPUT_DIR, "dim_date.csv")
    )

