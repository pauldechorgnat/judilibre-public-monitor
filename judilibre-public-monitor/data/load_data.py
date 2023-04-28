import datetime
import os

import pandas as pd

from .data_utils import FORMATIONS_CC
from .data_utils import JURISDICTIONS
from .data_utils import LOCATIONS
from .data_utils import remove_cour_dappel
from .data_utils import SOURCES
from .data_utils import TYPES


def load_data(
    path: str = ".",
    main_filename: str = "full_data.parquet",
    nac_reference_filename: str = "nac_reference.csv",
):
    df = pd.read_parquet(os.path.join(path, main_filename))

    df_nac = pd.read_csv(os.path.join(path, nac_reference_filename))

    # cleaning data
    df.loc[df["jurisdiction"] == "cc", "location"] = "Cour de cassation"

    df["court"] = "Cour de casation"
    df.loc[df["jurisdiction"] == "ca", "court"] = df.loc[
        df["jurisdiction"] == "ca", "location"
    ].apply(lambda location: LOCATIONS.get(location, "Non renseigné"))

    df["location"] = df["court"].apply(remove_cour_dappel)

    df["formation_clean"] = "Non renseigné"

    df.loc[df["jurisdiction"] == "cc", "formation_clean"] = df.loc[
        df["jurisdiction"] == "cc", "chamber"
    ].apply(FORMATIONS_CC.get)

    df["jurisdiction"] = df["jurisdiction"].apply(
        lambda jurisidction: JURISDICTIONS.get(jurisidction, "Non renseigné")
    )

    df["decision_date"] = pd.to_datetime(df["decision_date"])

    df["type"] = df["type"].apply(lambda t: TYPES.get(t, "Autre"))
    df["source"] = df["source"].apply(lambda source: SOURCES.get(source, "Autre"))

    df.loc[df["nac"].isna(), "nac"] = "Non renseigné"

    df["n_decisions"] = 1

    df = (
        df.groupby(
            [
                "source",
                "jurisdiction",
                "court",
                "location",
                "nac",
                "formation_clean",
                "type",
                "decision_date",
            ]
        )
        .agg({"n_decisions": "sum"})
        .reset_index()
    )

    df = pd.merge(
        left=df, right=df_nac, how="left", left_on=["nac"], right_on=["Code NAC"]
    )
    return df


def get_download_data(
    df: pd.DataFrame,
    choice: str = "ca_location",
    start_date: datetime.date = datetime.date(year=2000, month=1, day=1),
    end_date: datetime.date = datetime.date.today(),
):
    if choice == "ca_location":
        df = df.groupby(["location"]).agg({"n_decisions": "sum"})
    elif choice == "ca_nac":
        df = df.groupby(["nac", "Intitulé NAC"]).agg({"n_decisions": "sum"})
    else:
        df = df.groupby(["location", "nac", "Intitulé NAC"]).agg({"n_decisions": "sum"})

    return df


def aggregate_data(path_to_raw_data: str):
    dfs = []
    for f in os.listdir(path_to_raw_data):
        if ".parquet" in f:
            dfs.append(pd.read_parquet(os.path.join(path_to_raw_data, f)))

    return pd.concat(dfs)
