import os

import pandas as pd

from .data_utils import FORMATIONS_CC
from .data_utils import SOURCES
from .data_utils import TYPES


def load_data(path: str = ".", filename="full_data.parquet"):
    df = pd.read_parquet(os.path.join(path, filename))

    df["formation_clean"] = "Non renseigné"

    df.loc[df["jurisdiction"] == "cc", "formation_clean"] = df.loc[
        df["jurisdiction"] == "cc", "chamber"
    ].apply(FORMATIONS_CC.get)

    df["decision_date"] = pd.to_datetime(df["decision_date"])
    # df["update_date"] = pd.to_datetime(df["update_date"])

    df["type"] = df["type"].apply(lambda t: TYPES.get(t, "Autre"))
    df["source"] = df["source"].apply(lambda source: SOURCES.get(source, "Autre"))

    df.loc[df["jurisdiction"] == "cc", "location"] = "Cour de cassation"

    df.loc[df["nac"].isna(), "nac"] = "Non renseigné"

    df["n_decisions"] = 1

    df = (
        df.groupby(
            [
                "formation_clean",
                "location",
                "source",
                "decision_date",
                "nac",
                "type",
                "jurisdiction",
            ]
        )
        .agg({"n_decisions": "sum"})
        .reset_index()
    )
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
