from uuid import uuid4

import numpy as np
import pandas as pd
from data_utils import CHAMBERS_CA
from data_utils import CHAMBERS_CC
from data_utils import DECISION_TYPES
from data_utils import LETTERS
from data_utils import LOCATIONS_CA
from data_utils import LOCATIONS_CC
from data_utils import NUMBERS


def generate_nac_codes(sample_size: int = 1_000):
    number1 = np.random.choice(NUMBERS, size=sample_size, replace=True)
    number2 = np.random.choice(NUMBERS, size=sample_size, replace=True)
    letter = np.random.choice(LETTERS[26:], size=sample_size, replace=True)

    return pd.Series(number1) + pd.Series(number2) + pd.Series(letter)


def generate_dates(sample_size: int = 1_000):
    days = np.random.randint(low=1, high=29, size=sample_size)
    months = np.random.randint(low=1, high=13, size=sample_size)
    years = 1970 + np.random.randint(low=0, high=50, size=sample_size)
    return pd.to_datetime({"year": years, "month": months, "day": days})


def generate_decision_types(sample_size: int = 1000):
    decision_types = np.random.choice(
        list(DECISION_TYPES.keys()), size=sample_size, replace=True
    )
    return pd.Series(decision_types)


def generate_ca_data(sample_size: int = 10_000):
    ids = [str(uuid4()) for _ in range(sample_size)]
    numbers = [str(uuid4()) for _ in range(sample_size)]
    sources = np.random.choice(
        ["dila", "jurica"], p=[0.2, 0.8], replace=True, size=sample_size
    )
    nacs = generate_nac_codes(sample_size=sample_size)
    decision_dates = generate_dates(sample_size=sample_size)
    update_dates = generate_dates(sample_size=sample_size)
    locations = np.random.choice(
        list(LOCATIONS_CA.keys()), replace=True, size=sample_size
    )
    chambers = np.random.choice(
        list(CHAMBERS_CA.keys()), replace=True, size=sample_size
    )
    types = generate_decision_types(sample_size=sample_size)

    df = pd.DataFrame(
        {
            "id": ids,
            "source": sources,
            "nac": nacs,
            "decision_date": decision_dates,
            "update_date": update_dates,
            "locations": locations,
            "chambers": chambers,
            "types": types,
            "jurisdiction": "ca",
            "number": numbers,
        }
    )

    dates_min, dates_max = df[["decision_date", "update_date"]].min(axis=1), df[
        ["decision_date", "update_date"]
    ].max(axis=1)
    df["update_date"] = dates_max
    df["decision_date"] = dates_min

    return df


def generate_cc_data(sample_size: int = 10_000):
    ids = [str(uuid4()) for _ in range(sample_size)]
    numbers = [str(uuid4()) for _ in range(sample_size)]
    sources = np.random.choice(
        ["dila", "jurinet"], p=[0.2, 0.8], replace=True, size=sample_size
    )
    nacs = None
    decision_dates = generate_dates(sample_size=sample_size)
    update_dates = generate_dates(sample_size=sample_size)
    locations = np.random.choice(
        list(LOCATIONS_CC.keys()), replace=True, size=sample_size
    )
    chambers = np.random.choice(
        list(CHAMBERS_CC.keys()), replace=True, size=sample_size
    )
    types = generate_decision_types(sample_size=sample_size)

    df = pd.DataFrame(
        {
            "id": ids,
            "source": sources,
            "nac": nacs,
            "decision_date": decision_dates,
            "update_date": update_dates,
            "locations": locations,
            "chambers": chambers,
            "types": types,
            "jurisdiction": "cc",
            "number": numbers,
        }
    )

    dates_min, dates_max = df[["decision_date", "update_date"]].min(axis=1), df[
        ["decision_date", "update_date"]
    ].max(axis=1)
    df["update_date"] = dates_max
    df["decision_date"] = dates_min

    return df


def generate_data(
    ca_sample_size: int = 10_000,
    cc_sample_size: int = 10_0000,
    filename: str = "data/full_data_fake.parquet",
):
    df = pd.concat(
        [
            generate_ca_data(sample_size=ca_sample_size),
            generate_cc_data(sample_size=cc_sample_size),
        ]
    )

    df.to_parquet(filename, index=False)


if __name__ == "__main__":
    import logging
    from argparse import ArgumentParser

    argument_parser = ArgumentParser()

    argument_parser.add_argument(
        "-f",
        "--file-name",
        default="data/full_data_fake.parquet",
        help="Name of the file where to save fake data",
    )

    argument_parser.add_argument(
        "-s",
        "--sample-size",
        help="Number of rows in the fake data",
        default=10_000,
        type=int,
    )

    argument_parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
    )

    arguments = argument_parser.parse_args()

    verbose = arguments.verbose
    sample_size = arguments.sample_size
    file_name = arguments.file_name

    if verbose:
        logging.basicConfig(level=logging.DEBUG)

    logging.debug(
        f"Creating a file with {sample_size} rows and saving it at `{file_name}`"
    )

    generate_data(
        ca_sample_size=sample_size, cc_sample_size=sample_size, filename=file_name
    )

    logging.debug("Done!")

    logging.debug(f"Reading data from `{file_name}`")

    df = pd.read_parquet(file_name)

    logging.debug(df.head())
