import datetime
import logging

import pandas as pd

from .download_utils import download_data_between_update_dates


def download_latest_data(
    reference_file: str = "./full_data.parquet",
    target_file: str = "./updated_data.parquet",
    api_key_id: str = "XXXXXX",
    api_url: str = "https://sandbox-api.piste.gouv.fr/cassation/judilibre/v1.0",
):
    df = pd.read_parquet(reference_file)
    logging.info(f"Initial data has {df.shape[0]} lines")

    max_date = pd.to_datetime(df["update_date"]).max()

    today = datetime.datetime.now()

    n_days = int((today - max_date) / datetime.timedelta(days=1)) + 1
    if n_days == 1:
        logging.info("No new data to download")
        return

    dates = [
        (max_date + datetime.timedelta(days=i)).date() for i in range(-2, n_days + 1)
    ]

    data = []

    start_end = list(zip(dates[:-1], dates[1:]))

    for start_date, end_date in start_end:
        logging.info(f"Downloading data from {start_date} to {end_date}")

        result = download_data_between_update_dates(
            base_url=api_url,
            headers={"KeyId": api_key_id},
            start_date=start_date,
            end_date=end_date,
            jurisdiction="ca",
        )

        data.append(pd.DataFrame(result))

        result = download_data_between_update_dates(
            base_url=api_url,
            headers={"KeyId": api_key_id},
            start_date=start_date,
            end_date=end_date,
            jurisdiction="cc",
        )

        result = download_data_between_update_dates(
            base_url=api_url,
            headers={"KeyId": api_key_id},
            start_date=start_date,
            end_date=end_date,
            jurisdiction="tj",
        )

        data.append(pd.DataFrame(result))

    df_new = pd.concat(data)

    df = pd.concat([df, df_new])

    df = df.drop_duplicates(subset=["id"])

    logging.info(f"Final data has {df.shape[0]} lines")

    df.to_parquet(target_file, index=False)


if __name__ == "__main__":
    from argparse import ArgumentParser

    argument_parser = ArgumentParser()

    argument_parser.add_argument(
        "-i", "--input-file", default="./full_data.parquet", help="Reference file"
    )

    argument_parser.add_argument(
        "-o",
        "--output-file",
        default="./update_data.parquet",
        help="Output file containing old and updated data",
    )

    argument_parser.add_argument(
        "-u",
        "--url",
        default="https://sandbox-api.piste.gouv.fr/cassation/judilibre/v1.0",
        help="URL API",
    )

    argument_parser.add_argument("-k", "--api-key", default="XXXXX", help="API key")
    argument_parser.add_argument(
        "-v", "--verbose", help="Debug level of verbose", action="store_true"
    )

    arguments = argument_parser.parse_args()

    if arguments.verbose:
        logging.basicConfig(level=logging.INFO)
        logging.info("DEBUG mode:")

    input_file = arguments.input_file
    output_file = arguments.output_file
    api_url = arguments.url
    api_key = arguments.api_key

    download_latest_data(
        reference_file=input_file,
        target_file=output_file,
        api_key_id=api_key,
        api_url=api_url,
    )
