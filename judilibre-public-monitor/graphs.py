import datetime

import pandas as pd
import plotly.express as px
from data.data_utils import LOCATIONS
from data.data_utils import remove_cour_dappel
from palettes import COLORS
from palettes import PALETTES
from plotly import graph_objects as go


def get_source_graph(df: pd.DataFrame):
    df_source = (
        df.groupby(["source", "jurisdiction"]).agg({"n_decisions": "sum"}).reset_index()
    )
    df_source["jurisdiction"] = df_source["jurisdiction"].replace(
        {"cc": "Cour de cassation", "ca": "Cours d'appel"}
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


def get_jurisidction_graph(df: pd.DataFrame):
    df_source = df.groupby("jurisdiction").agg({"n_decisions": "sum"}).reset_index()

    fig = go.Figure(
        go.Bar(
            x=df_source["jurisdiction"],
            y=df_source["n_decisions"],
            marker={"color": COLORS["bleu_france"]},
        )
    )
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
    )

    return fig


def get_location_graph(df: pd.DataFrame, include_cc: bool = False):
    df_location = df.groupby("location").agg({"n_decisions": "sum"}).reset_index()

    if not include_cc:
        df_location = df_location[df_location["location"] != "cc"]

    df_location["location"] = (
        df_location["location"]
        .apply(lambda location: LOCATIONS.get(location, "Non renseigné"))
        .apply(remove_cour_dappel)
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
    df_nac = df.groupby("nac").agg({"n_decisions": "sum"}).reset_index()

    df_nac = df_nac.dropna(subset=["nac"])

    fig = go.Figure(
        go.Bar(
            x=df_nac["nac"],
            y=df_nac["n_decisions"],
            marker={"color": COLORS["bleu_france"]},
        )
    )
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
    )

    return fig


def get_time_graph(df: pd.DataFrame, date_type: str = "decision_date"):
    df_time = df.copy()

    df_time[date_type] = pd.to_datetime(df_time[date_type])
    df_time[date_type] = df_time[date_type].dt.year
    # df_time[date_type] = pd.to_datetime({"year": df_time[date_type].dt.year, "month": 1, "day": 1})

    df_time = (
        df_time.groupby([date_type, "jurisdiction"])
        .agg({"n_decisions": "sum"})
        .reset_index()
    )

    df_time["jurisdiction"] = df_time["jurisdiction"].replace(
        {"cc": "Cour de cassation", "ca": "Cours d'appel"}
    )

    fig = px.line(
        data_frame=df_time,
        x=date_type,
        y="n_decisions",
        color="jurisdiction",
        color_discrete_map={
            "Cour de cassation": COLORS["rouge_marianne"],
            "Cours d'appel": COLORS["bleu_france"],
        },
        # range_x=[1980, 2025],
        labels={
            "n_decisions": "Nombre de décisions",
            date_type: "Année",
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
    date_type = "decision_date"

    df_time = df.copy()
    df_time = df_time[df_time["jurisdiction"] == "ca"]

    df_time[date_type] = pd.to_datetime(df_time[date_type])
    df_time[date_type] = df_time[date_type] - (
        df_time[date_type].dt.day - 1
    ) * datetime.timedelta(days=1)

    df_time = (
        df_time.groupby([date_type, "location"])
        .agg({"n_decisions": "sum"})
        .reset_index()
    )

    df_time["location"] = (
        df_time["location"].apply(LOCATIONS.get).apply(remove_cour_dappel)
    )

    df_time = df_time[df_time["location"].isin(locations)].sort_values(
        by=["location", date_type]
    )

    fig = px.line(
        data_frame=df_time,
        x=date_type,
        y="n_decisions",
        color="location",
        color_discrete_sequence=PALETTES["pal_gouv_qual1"],
        labels={
            "n_decisions": "Nombre de décisions par mois",
            "location": "Cour d'appel",
            date_type: "Mois",
        },
    )

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
    )

    return fig


def get_nac_location_graph(
    df: pd.DataFrame, locations: list[str] = ["Paris", "Versailles", "Aix-en-Provence"]
):
    df_nac = df.groupby(["nac", "location"]).agg({"n_decisions": "sum"}).reset_index()

    df_nac = df_nac.dropna(subset=["nac"])

    df_nac["location"] = (
        df_nac["location"]
        .apply(lambda location: LOCATIONS.get(location, "Non renseigné"))
        .apply(remove_cour_dappel)
    )

    df_nac = df_nac[df_nac["location"].isin(locations)].sort_values(
        by=["location", "nac"]
    )

    fig = px.bar(
        data_frame=df_nac,
        x="nac",
        y="n_decisions",
        color="location",
        barmode="stack",
        color_discrete_sequence=PALETTES["pal_gouv_qual1"],
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
    df = df[df["jurisdiction"] == "cc"].copy()

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
    df = df[df["jurisdiction"] == "cc"].copy()

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
