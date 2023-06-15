import datetime
import logging
from itertools import product

import pandas as pd
from dotenv import load_dotenv
from download_utils import download_data_between_update_dates


def download_historic_ca_data():
    start_date = datetime.date(year=1790, month=1, day=1)

    end_dates = [
        datetime.date(year=2000, month=1, day=1),
        datetime.date(year=2005, month=1, day=1),
        datetime.date(year=2007, month=9, day=1),
    ]

    n_weeks = int((datetime.date.today() - end_dates[-1]).days / 7) + 1

    end_dates += [
        datetime.date(year=2007, month=9, day=1) + datetime.timedelta(days=7 * i)
        for i in range(1, n_weeks + 1)
    ]

    end_dates += [datetime.date(year=2021, month=11, day=d) for d in range(14, 24)]

    for end_date in sorted(set(end_dates)):
        logging.info(f"{start_date} -> {end_date}")
        data = download_data_between_update_dates(
            start_date=start_date, end_date=end_date, jurisdiction="ca"
        )
        df = pd.DataFrame(data)

        logging.info(str(df.shape))

        df.to_parquet(f"data/raw_data/data_ca_{start_date}-{end_date}.parquet")

        start_date = end_date


def download_historic_cc_data():
    start_date = datetime.date(year=1790, month=1, day=1)
    end_dates = [
        datetime.date(year=1960, month=1, day=1),
        datetime.date(year=1970, month=1, day=1),
    ]

    end_dates += [datetime.date(year=y, month=1, day=1) for y in range(1971, 1987)]

    end_dates += [
        datetime.date(year=y, month=m, day=1)
        for y, m in product(range(1987, 2022), [1, 6])
    ]
    end_dates += [
        datetime.date(year=y, month=m, day=1)
        for y, m in product(range(2021, 2024), range(1, 13))
    ]

    for end_date in end_dates:
        logging.info(f"{start_date} -> {end_date}")

        data = download_data_between_update_dates(
            start_date=start_date, end_date=end_date, jurisdiction="cc"
        )

        df = pd.DataFrame(data)

        logging.info(str(df.shape))

        df.to_parquet(f"data/raw_data/data_cc_{start_date}-{end_date}.parquet")

        start_date = end_date


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    load_dotenv()

    download_historic_ca_data()
    download_historic_cc_data()
