import logging
import os

import pandas as pd


def load_data(path: str = "."):
    try:
        df = pd.read_parquet(os.path.join(path, "full_data.parquet"))
    except FileNotFoundError:
        logging.info(f"Real data not found at `{path}`")
        logging.info("Loading fake data")
        df = pd.read_parquet(os.path.join(path, "full_data_fake.parquet"))

    df["decision_date"] = pd.to_datetime(df["decision_date"])
    df["update_date"] = pd.to_datetime(df["update_date"])
    return df


def get_ca_data(df: pd.DataFrame, choice: str = "ca_location"):
    df["n_decisions"] = 1

    if choice == "ca_location":
        df = df.groupby(["location"]).agg({"n_decisions": "sum"}).reset_index()
    elif choice == "ca_nac":
        df = df.groupby(["nac"]).agg({"n_decisions": "sum"}).reset_index()
    else:
        df = df.groupby(["location", "nac"]).agg({"n_decisions": "sum"}).reset_index()

    return df


def aggregate_data(path_to_raw_data: str):
    dfs = []
    for f in os.listdir(path_to_raw_data):
        if ".parquet" in f:
            dfs.append(pd.read_parquet(os.path.join(path_to_raw_data, f)))

    return pd.concat(dfs)
