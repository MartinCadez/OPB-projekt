import csv
import os
from datetime import datetime, timedelta
from typing import Union
import pandas as pd
from src.utils.logger import logger
from src.extractors.country_code_extractor import CountryCodeExtractor
from src.extractors.holidays_extractor import HolidayExtractor


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

    logger.info(f"CSV file created at: {output_path}")


def get_dim_country(output_path: str = "dim_country.csv"):
    return CountryCodeExtractor().get_df().to_csv(output_path, index=False)


def get_dim_holiday(output_path: str = "dim_holiday.csv"):
    return (
        HolidayExtractor()
        .get_df()
        .assign(
            date_id=lambda df: pd.to_datetime(df["date"]).apply(
                lambda d: int(d.timestamp())
            )
        )
        .merge(
            CountryCodeExtractor().get_df(),
            left_on="country_code",
            right_on="alpha2_code",
            how="left",
        )
        .dropna(subset=["country_id"])
        .assign(
            holiday_id=lambda df: df.index + 1,
            country_id=lambda df: df["country_id"].astype(int),
        )
        .reindex(columns=["holiday_id", "date_id", "country_id", "name"])
        .reset_index(drop=True)
        .to_csv(output_path, index=False)
    )


if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    OUTPUT_DIR = os.path.join(BASE_DIR, "..", "..", "init-db", "data")

    get_dim_date(
        start_date="2015-01-01",
        end_date="2025-12-31",
        output_path=os.path.join(OUTPUT_DIR, "dim_date.csv"),
    )

    get_dim_country(output_path=os.path.join(OUTPUT_DIR, "dim_country.csv"))

    get_dim_holiday(output_path=os.path.join(OUTPUT_DIR, "dim_holiday.csv"))
