import os

import pandas as pd

from .data_utils import CHAMBERS_CC
from .data_utils import CLEAN_COLUMN_NAMES
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
    df = df.drop_duplicates(subset=["id"])
    df_nac = pd.read_csv(os.path.join(path, nac_reference_filename))

    # cleaning data
    df.loc[df["jurisdiction"] == "cc", "location"] = "Cour de cassation"

    df["court"] = "Cour de casation"
    df.loc[df["jurisdiction"] != "cc", "court"] = df.loc[
        df["jurisdiction"] != "cc", "location"
    ].apply(lambda location: LOCATIONS.get(location, "Non renseigné"))
    df["location"] = df["court"].apply(remove_cour_dappel)

    df["chamber"] = df["chamber"].fillna("Non renseigné")

    df.loc[df["jurisdiction"] == "cc", "chamber"] = df.loc[
        df["jurisdiction"] == "cc", "chamber"
    ].apply(CHAMBERS_CC.get)

    df.loc[df["jurisdiction"] == "cc", "formation"] = df.loc[
        df["jurisdiction"] == "cc", "formation"
    ].apply(FORMATIONS_CC.get)

    df["jurisdiction"] = df["jurisdiction"].apply(
        lambda jurisidction: JURISDICTIONS.get(jurisidction, "Non renseigné")
    )

    df["decision_date"] = pd.to_datetime(df["decision_date"])

    df["type"] = df["type"].apply(lambda t: TYPES.get(t, "Autre"))
    df["source"] = df["source"].apply(lambda source: SOURCES.get(source, "Autre"))

    df["formation"] = df["formation"].fillna("Non renseigné")

    df.loc[df["nac"].isna(), "nac"] = "Non renseigné"

    df["publication"] = df["publication"].astype(str)
    df["n_decisions"] = 1

    df = (
        df.groupby(
            [
                "source",
                "jurisdiction",
                "court",
                "location",
                "nac",
                "chamber",
                "type",
                "decision_date",
                "formation",
                "publication",
            ]
        )
        .agg({"n_decisions": "sum"})
        .reset_index()
    )

    df = pd.merge(
        left=df, right=df_nac, how="left", left_on=["nac"], right_on=["Code NAC"]
    )

    df["publication"] = df["publication"].apply(lambda x: [i for i in x])

    df.info()

    return df


def get_download_data(
    df: pd.DataFrame,
    choice: str = "ca_location",
    # start_date: datetime.date = datetime.date(year=2000, month=1, day=1),
    # end_date: datetime.date = datetime.date.today(),
):
    if choice == "ca_location":
        df = (
            df.loc[df["jurisdiction"] == "Cours d'appel"]
            .rename(columns=CLEAN_COLUMN_NAMES)
            .groupby(["Cour"])
            .agg({"Nombre de décisions": "sum"})
        )
    elif choice == "ca_nac":
        df = (
            df.loc[df["jurisdiction"] == "Cours d'appel"]
            .rename(columns=CLEAN_COLUMN_NAMES)
            .groupby(["Code NAC", "Intitulé NAC"])
            .agg({"Nombre de décisions": "sum"})
        )
    elif choice == "ca_location_nac":
        df = (
            df.loc[df["jurisdiction"] == "Cours d'appel"]
            .rename(columns={"n_decisions": "Nombre de décisions", "court": "Cour"})
            .groupby(["Cour", "Code NAC", "Intitulé NAC"])
            .agg({"Nombre de décisions": "sum"})
        )
    elif choice == "all_ids":
        df = pd.read_parquet("./full_date.parquet")
        df = df[["id"]].set_index("id")
    else:
        df = (
            df.rename(CLEAN_COLUMN_NAMES)
            .drop(["N1", "N2", "nac"], axis=1)
            .set_index("Code NAC")
        )
    return df


def aggregate_data(path_to_raw_data: str):
    dfs = []
    for f in os.listdir(path_to_raw_data):
        if ".parquet" in f:
            dfs.append(pd.read_parquet(os.path.join(path_to_raw_data, f)))

    return pd.concat(dfs)
