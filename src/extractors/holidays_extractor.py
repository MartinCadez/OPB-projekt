import csv
import holidays
from datetime import date
import os
from typing import Dict, List
from src.logging import logger


class HolidayExtractor:
    def __init__(
        self,
        years: range = range(2017, 2025),
        output_dir: str = os.path.dirname(os.path.abspath(__file__)),
        output_file: str = "holidays.csv",
    ) -> None:
        self.years: range = years
        self.output_dir: str = os.path.abspath(output_dir)
        self.output_file: str = os.path.join(self.output_dir, output_file)

    def generate_csv(self) -> None:
        supported_countries: List[str] = holidays.utils.list_supported_countries()
        try:
            with open(self.output_file, "w", newline="", encoding="utf-8") as csvfile:
                writer: csv._writer = csv.writer(csvfile)
                writer.writerow(["country_code", "date", "name"])
                logger.info("Writing CSV header")

                for country_code in sorted(supported_countries):
                    country_holidays: Dict[date, str] = holidays.country_holidays(
                        country_code, years=self.years
                    )

                    for hol_date, name in sorted(country_holidays.items()):
                        if isinstance(hol_date, date):
                            writer.writerow([country_code, hol_date.isoformat(), name])
                        else:
                            logger.warning(
                                f"Skipping invalid date format for {country_code}: {hol_date} (type: {type(hol_date)})"
                            )
        except Exception as e:
            logger.error(f"Failed to write CSV file {self.output_file}: {str(e)}")
            raise

        logger.info(f"CSV file generated: {self.output_file}")


if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    OUTPUT_DIR = os.path.join(BASE_DIR, "..", "..", "init-db", "data")

    extractor: HolidayExtractor = HolidayExtractor(
        years=range(2017, 2025), output_dir=OUTPUT_DIR, output_file="holidays.csv"
    )
    extractor.generate_csv()
