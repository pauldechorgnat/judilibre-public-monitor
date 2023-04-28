import datetime

import pandas as pd
import plotly.express as px
from palettes import COLORS
from palettes import PALETTES


def get_source_graph(df: pd.DataFrame):
    """Returns a graph of decisions per source and jurisidiction"""
    df_source = (
        df.groupby(["source", "jurisdiction"]).agg({"n_decisions": "sum"}).reset_index()
    )

    fig = px.bar(
        data_frame=df_source,
        x="source",
        y="n_decisions",
        color="jurisdiction",
        color_discrete_map={
            "Cour de cassation": COLORS["rouge_marianne"],
            "Cours d'appel": COLORS["bleu_france"],
        },
        labels={
            "source": "Source",
            "n_decisions": "Nombre de décisions",
            "jurisdiction": "Juridiction",
        },
    )

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
    )

    return fig


def get_location_graph(df: pd.DataFrame):
    """Returns a graph of decisions per location (cours d'appel)"""
    df_location = (
        df.loc[df["jurisdiction"] == "Cours d'appel"]
        .groupby(["location"])
        .agg({"n_decisions": "sum"})
        .reset_index()
    )

    fig = px.bar(
        data_frame=df_location,
        x="location",
        y="n_decisions",
        color_discrete_sequence=[
            COLORS["bleu_france"],
        ],
        labels={"location": "Cour d'appel", "n_decisions": "Nombre de décisions"},
    )

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
    )

    return fig


def get_nac_graph(df: pd.DataFrame):
    """Returns a graph of decisions per code NAC (cours d'appel)"""
    df_nac = (
        df.loc[df["jurisdiction"] == "Cours d'appel"]
        .groupby(["nac", "Niveau 1", "N1", "Intitulé NAC"])
        .agg({"n_decisions": "sum"})
        .reset_index()
    )

    fig = px.bar(
        data_frame=df_nac[df_nac["n_decisions"] != 0].sort_values(["N1", "nac"]),
        x="nac",
        y="n_decisions",
        color="Niveau 1",
        color_discrete_sequence=PALETTES["pal_gouv_qual1"],
        hover_data=["n_decisions", "nac", "Intitulé NAC", "Niveau 1"],
        labels={
            "n_decisions": "Nombre de décisions",
            "nac": "Code Nature Affaire Civile",
        },
    )

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
    )

    return fig


def get_time_graph(df: pd.DataFrame):
    """Returns a graph of decisions per year and jurisdiction"""
    df_time = df.copy()

    df_time["decision_year"] = df_time["decision_date"].dt.year

    df_time = (
        df_time.groupby(["decision_year", "jurisdiction"])
        .agg({"n_decisions": "sum"})
        .reset_index()
    )

    fig = px.line(
        data_frame=df_time,
        x="decision_year",
        y="n_decisions",
        color="jurisdiction",
        color_discrete_map={
            "Cour de cassation": COLORS["rouge_marianne"],
            "Cours d'appel": COLORS["bleu_france"],
        },
        range_x=[1980, 2024],
        labels={
            "n_decisions": "Nombre de décisions",
            "decision_year": "Année",
            "jurisdiction": "Juridiction",
        },
    )

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
    )

    return fig


def get_time_location_graph(
    df: pd.DataFrame, locations: list[str] = ["Paris", "Versailles", "Aix-en-Provence"]
):
    """Returns a graph of decisions per month and cour d'appel"""

    df_time = df.copy()
    df_time = df_time[df_time["location"].isin(locations)]

    df_time["decision_date"] = df_time["decision_date"] - (
        df_time["decision_date"].dt.day - 1
    ) * datetime.timedelta(days=1)

    df_time = (
        df_time.groupby(["decision_date", "location", "court"])
        .agg({"n_decisions": "sum"})
        .reset_index()
        .sort_values(by=["location", "decision_date"])
    )

    fig = px.line(
        data_frame=df_time,
        x="decision_date",
        y="n_decisions",
        color="location",
        color_discrete_sequence=PALETTES["pal_gouv_qual1"],
        labels={
            "n_decisions": "Nombre de décisions",
            "court": "Cour d'appel",
            "decision_date": "Mois",
        },
    )

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
    )

    return fig


def get_nac_location_graph(
    df: pd.DataFrame, locations: list[str] = ["Paris", "Versailles", "Aix-en-Provence"]
):
    """Returns a graph of decisions per Code NAC and cour d'appel"""
    df_nac = (
        df.loc[df["location"].isin(locations)]
        .groupby(["nac", "Intitulé NAC", "location"])
        .agg({"n_decisions": "sum"})
        .reset_index()
        .dropna(subset=["nac"])
        .sort_values(by=["location", "nac"])
    )

    fig = px.bar(
        data_frame=df_nac,
        x="nac",
        y="n_decisions",
        color="location",
        barmode="stack",
        color_discrete_sequence=PALETTES["pal_gouv_qual1"],
        hover_data=["nac", "Intitulé NAC", "n_decisions", "location"],
        labels={
            "nac": "Code NAC",
            "location": "Cour d'appel",
            "n_decisions": "Nombre de décisions",
        },
    )
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
    )

    return fig


def get_chamber_graph(df: pd.DataFrame):
    """Returns a graph of decisions per formation (Cour de cassation)"""
    df = df[df["jurisdiction"] == "Cour de cassation"].copy()

    df = (
        df.groupby(
            [
                "formation_clean",
            ]
        )
        .agg({"n_decisions": "sum"})
        .reset_index()
    )

    fig = px.bar(
        data_frame=df,
        x="formation_clean",
        y="n_decisions",
        labels={
            "formation_clean": "Formation ou chambre",
            "n_decisions": "Nombre de décisions",
        },
        color_discrete_sequence=[COLORS["rouge_marianne"]],
    )

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
    )

    return fig


def get_type_graph(df: pd.DataFrame):
    """Returns a graph of decisions per formation (Cour de cassation)"""
    df = df[df["jurisdiction"] == "Cour de cassation"].copy()

    df = df.groupby("type").agg({"n_decisions": "sum"}).reset_index()

    fig = px.bar(
        data_frame=df,
        x="type",
        y="n_decisions",
        labels={"type": "Type de décision", "n_decisions": "Nombre de décisions"},
        color_discrete_sequence=[COLORS["rouge_marianne"]],
    )

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def get_nac_level_graph(df: pd.DataFrame):
    """Returns a graph of decisions per NAC level (1 and 2) (Cours d'appel)"""

    df_level = (
        df.groupby(["Niveau 2", "N1", "Niveau 1"])
        .agg({"n_decisions": "sum"})
        .reset_index()
    )

    fig = px.bar(
        data_frame=df_level.sort_values("N1"),
        x="Niveau 1",
        y="n_decisions",
        color="Niveau 1",
        hover_data=["n_decisions", "Niveau 1", "Niveau 2"],
        color_discrete_sequence=PALETTES["pal_gouv_qual1"],
        labels={"n_decisions": "Nombre de décisions"},
    )

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
    )

    return fig


def get_nac_level_location_graph(df: pd.DataFrame, locations: list[str] = ["Paris"]):
    df_nac = (
        df[df["location"].isin(locations)]
        .groupby(["N1", "Niveau 1", "location"])
        .agg({"n_decisions": "sum"})
        .reset_index()
        .dropna(subset=["N1", "Niveau 1"])
        .sort_values(by=["location", "N1"])
    )

    fig = px.bar(
        data_frame=df_nac,
        x="Niveau 1",
        y="n_decisions",
        color="location",
        barmode="stack",
        color_discrete_sequence=PALETTES["pal_gouv_qual1"],
        labels={
            "Niveau 1": "Niveau 1",
            "location": "Cour d'appel",
            "n_decisions": "Nombre de décisions",
        },
    )

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
    )

    return fig


def get_formation_time_graph(df: pd.DataFrame):
    df_time = df.copy()
    df_time["decision_date"] = df_time["decision_date"] - (
        df_time["decision_date"].dt.day - 1
    ) * datetime.timedelta(days=1)

    df_time = (
        df_time.groupby(["decision_date"]).agg({"n_decisions": "sum"}).reset_index()
    )

    # df_time = df_time[df_time["formation_clean"] != "Non renseigné"]

    fig = px.line(
        data_frame=df_time,
        x="decision_date",
        y="n_decisions",
        # color="formation_clean",
        # color_discrete_sequence=PALETTES["pal_gouv_qual1"],
        color_discrete_sequence=[COLORS["rouge_marianne"]],
        # range_x=[1980, 2024],
        labels={
            "n_decisions": "Nombre de décisions",
            "decision_date": "Mois",
            # "jurisdiction": "Juridiction",
        },
    )

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
    )

    return fig
