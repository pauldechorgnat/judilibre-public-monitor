import os

import pandas as pd

from .load_data import load_data


def compute_source_dataset(df: pd.DataFrame):
    df_source = (
        df.groupby(["source", "jurisdiction", "decision_date"])
        .agg({"n_decisions": "sum"})
        .reset_index()
    )

    return df_source


def compute_time_by_year_dataset(df: pd.DataFrame):
    df_time_by_year = df.copy()

    df_time_by_year["decision_year"] = df_time_by_year["decision_date"].dt.year

    df_time_by_year = (
        df_time_by_year.groupby(["decision_year", "jurisdiction", "decision_date"])
        .agg({"n_decisions": "sum"})
        .reset_index()
    )
    return df_time_by_year


def compute_time_by_month_cc_dataset(df: pd.DataFrame):
    df_time_by_month_cc = df[df["jurisdiction"] == "Cour de cassation"].copy()
    df_time_by_month_cc["decision_month"] = pd.to_datetime(
        {
            "day": 1,
            "month": df_time_by_month_cc["decision_date"].dt.month,
            "year": df_time_by_month_cc["decision_date"].dt.year,
        }
    )

    df_time_by_month_cc = (
        df_time_by_month_cc.groupby(["decision_date", "decision_month"])
        .agg({"n_decisions": "sum"})
        .reset_index()
    )

    df_time_by_month_cc["n_decisions_lisse"] = (
        df_time_by_month_cc["n_decisions"].rolling(window=12, center=True).mean()
    )

    # df_time_by_month_cc = df_time_by_month_cc.rename(
    #     columns={
    #         "n_decisions": "Nombre de décisions",
    #         # "decision_date": "Mois",
    #         "n_decisions_lisse": "Nombre de décisions lissé",
    #     }
    # )

    return df_time_by_month_cc


def compute_chamber_cc_dataset(df: pd.DataFrame):
    df_chamber_cc = df[df["jurisdiction"] == "Cour de cassation"].copy()

    df_chamber_cc = (
        df_chamber_cc.groupby(["chamber", "decision_date"])
        .agg({"n_decisions": "sum"})
        .reset_index()
    )

    return df_chamber_cc


def compute_type_cc_dataset(df: pd.DataFrame):
    df_type_cc = df[df["jurisdiction"] == "Cour de cassation"].copy()

    df_type_cc = (
        df_type_cc.groupby(["type", "decision_date"])
        .agg({"n_decisions": "sum"})
        .reset_index()
    )

    return df_type_cc


def compute_formation_cc_dataset(df: pd.DataFrame):
    df_formation_cc = (
        df.loc[
            df["jurisdiction"] == "Cour de cassation",
            ["formation", "n_decisions", "decision_date"],
        ]
        .fillna("Non renseigné")
        .groupby(["formation", "decision_date"])
        .agg({"n_decisions": "sum"})
        .reset_index()
    )

    return df_formation_cc


def compute_publication_cc_dataset(df: pd.DataFrame):
    df_publications = df.copy()
    df_publications["publication"] = df_publications["publication"].apply(
        lambda x: [i for i in x]
    )
    df_publications = (
        df_publications.loc[
            df["jurisdiction"] == "Cour de cassation",
            ["decision_date", "publication", "n_decisions"],
        ]
        .explode("publication")
        .groupby(["publication", "decision_date"])
        .sum()
        .reset_index()
    )
    df_publications = df_publications.loc[
        df_publications["publication"].isin(["b", "n", "c", "l", "r"])
    ]

    df_publications["publication"] = df_publications["publication"].str.upper()

    return df_publications


def compute_location_ca_dataset(df: pd.DataFrame):
    df_location_ca = (
        df.loc[df["jurisdiction"] == "Cours d'appel"]
        .groupby(["location", "decision_date"])
        .agg({"n_decisions": "sum"})
        .reset_index()
    )

    return df_location_ca


def compute_nac_level_ca_dataset(df: pd.DataFrame):
    df_nac_level_ca = (
        df.groupby(["Niveau 2", "N1", "Niveau 1", "decision_date"])
        .agg({"n_decisions": "sum"})
        .reset_index()
    )
    return df_nac_level_ca


def compute_nac_ca_dataset(df: pd.DataFrame):
    df_nac_ca = (
        df.loc[df["jurisdiction"] == "Cours d'appel"]
        .groupby(["nac", "Niveau 1", "N1", "Intitulé NAC", "decision_date"])
        .agg({"n_decisions": "sum"})
        .reset_index()
    )

    return df_nac_ca


def compute_time_selected_location_ca_dataset(df: pd.DataFrame):
    df_time_selected_location_ca = df.copy()

    df_time_selected_location_ca["decision_month"] = pd.to_datetime(
        {
            "day": 1,
            "month": df_time_selected_location_ca["decision_date"].dt.month,
            "year": df_time_selected_location_ca["decision_date"].dt.year,
        }
    )

    df_time_selected_location_ca = (
        df_time_selected_location_ca.groupby(
            ["decision_month", "decision_date", "location", "court"]
        )
        .agg({"n_decisions": "sum"})
        .reset_index()
        .sort_values(by=["location", "decision_date"])
    )

    return df_time_selected_location_ca


def compute_nac_level_selected_location_ca_dataset(df: pd.DataFrame):
    df_nac_level_selected_location_ca = (
        df.groupby(["N1", "Niveau 1", "location", "decision_date"])
        .agg({"n_decisions": "sum"})
        .reset_index()
        .dropna(subset=["N1", "Niveau 1"])
        .sort_values(by=["location", "N1"])
    )

    return df_nac_level_selected_location_ca


def compute_nac_selected_location_ca_dataset(df: pd.DataFrame):
    df_nac_selected_location_ca = (
        df.groupby(["nac", "Intitulé NAC", "location", "decision_date"])
        .agg({"n_decisions": "sum"})
        .reset_index()
        .dropna(subset=["nac"])
        .sort_values(by=["location", "nac"])
    )
    return df_nac_selected_location_ca


def compute_all_datasets(path="."):
    df = load_data(path=path)

    df_source = compute_source_dataset(df)
    df_source.to_parquet(os.path.join(path, "df_source.parquet"), index=False)

    df_time_by_year = compute_time_by_year_dataset(df)
    df_time_by_year.to_parquet(
        os.path.join(path, "df_time_by_year.parquet"), index=False
    )

    df_time_by_month = compute_time_by_month_cc_dataset(df)
    df_time_by_month.to_parquet(
        os.path.join(path, "df_time_by_month_cc.parquet"), index=False
    )

    df_chamber_cc = compute_chamber_cc_dataset(df)
    df_chamber_cc.to_parquet(os.path.join(path, "df_chamber_cc.parquet"), index=False)

    df_type_cc = compute_type_cc_dataset(df)
    df_type_cc.to_parquet(os.path.join(path, "df_type_cc.parquet"), index=False)

    df_formation_cc = compute_formation_cc_dataset(df)
    df_formation_cc.to_parquet(
        os.path.join(path, "df_formation_cc.parquet"), index=False
    )

    df_publication_cc = compute_publication_cc_dataset(df)
    df_publication_cc.to_parquet(
        os.path.join(path, "df_publication_cc.parquet"), index=False
    )

    df_location_ca = compute_location_ca_dataset(df)
    df_location_ca.to_parquet(os.path.join(path, "df_location_ca.parquet"), index=False)

    df_nac_level_ca = compute_nac_level_ca_dataset(df)
    df_nac_level_ca.to_parquet(
        os.path.join(path, "df_nac_level_ca.parquet"), index=False
    )

    df_nac_ca = compute_nac_ca_dataset(df)
    df_nac_ca.to_parquet(os.path.join(path, "df_nac_ca.parquet"), index=False)

    df_time_selected_location_ca_dataset = compute_time_selected_location_ca_dataset(df)
    df_time_selected_location_ca_dataset.to_parquet(
        os.path.join(path, "df_time_selected_location_ca_dataset.parquet"), index=False
    )

    df_nac_level_selected_location_ca = compute_nac_level_selected_location_ca_dataset(
        df
    )
    df_nac_level_selected_location_ca.to_parquet(
        os.path.join(path, "df_nac_level_selected_location_ca.parquet"), index=False
    )

    df_nac_selected_location_ca = compute_nac_selected_location_ca_dataset(df)
    df_nac_selected_location_ca.to_parquet(
        os.path.join(path, "df_nac_selected_location_ca.parquet"), index=False
    )


def load_static_datasets(path="."):
    df_source = pd.read_parquet(os.path.join(path, "df_source.parquet"))
    df_time_by_year = pd.read_parquet(os.path.join(path, "df_time_by_year.parquet"))

    return df_source, df_time_by_year


def load_general_datasets(path="."):
    df_time_by_month = pd.read_parquet(
        os.path.join(path, "df_time_by_month_cc.parquet")
    )
    df_chamber_cc = pd.read_parquet(os.path.join(path, "df_chamber_cc.parquet"))
    df_type_cc = pd.read_parquet(os.path.join(path, "df_type_cc.parquet"))
    df_formation_cc = pd.read_parquet(os.path.join(path, "df_formation_cc.parquet"))
    df_publication_cc = pd.read_parquet(os.path.join(path, "df_publication_cc.parquet"))
    df_location_ca = pd.read_parquet(os.path.join(path, "df_location_ca.parquet"))
    df_nac_level_ca = pd.read_parquet(os.path.join(path, "df_nac_level_ca.parquet"))
    df_nac_ca = pd.read_parquet(os.path.join(path, "df_nac_ca.parquet"))

    return (
        df_time_by_month,
        df_chamber_cc,
        df_type_cc,
        df_formation_cc,
        df_publication_cc,
        df_location_ca,
        df_nac_level_ca,
        df_nac_ca,
    )


def load_selected_datasets(path="."):
    df_time_selected_location_ca_dataset = pd.read_parquet(
        os.path.join(path, "df_time_selected_location_ca_dataset.parquet")
    )
    df_nac_level_selected_location_ca = pd.read_parquet(
        os.path.join(path, "df_nac_level_selected_location_ca.parquet")
    )
    df_nac_selected_location_ca = pd.read_parquet(
        os.path.join(path, "df_nac_selected_location_ca.parquet")
    )

    return (
        df_time_selected_location_ca_dataset,
        df_nac_level_selected_location_ca,
        df_nac_selected_location_ca,
    )


if __name__ == "__main__":
    compute_all_datasets()
    print("computed")
    load_all_datasets()
