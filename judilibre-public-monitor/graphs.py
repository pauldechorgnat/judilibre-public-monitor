import pandas as pd
import plotly.express as px
from data.data_utils import LOCATIONS_CA
from data.data_utils import LOCATIONS_TJ
from data.data_utils import remove_cour_dappel
from palettes import COLORS
from palettes import PALETTES

LABELS = {
    "n_decisions": "Nombre de décisions",
    "jurisdiction": "Juridiction",
    "location": "Cour d'appel",
    "decision_year": "Année de la décision",
    "decision_month": "Mois de la décision",
    "source": "Source",
    "chamber": "Chambre",
    "formation": "Formation",
    "type": "Type de la décision",
    "publication": "Type de publication de la décision",
    "Niveau 1": "Niveau 1 (NAC)",
    "Niveau 2": "Niveau 2 (NAC)",
    "Code NAC": "Code NAC",
    "Intitulé NAC": "Intitulé NAC",
    "court": "Cour d'appel",
    "nac": "Code NAC",
}


CA_TO_COLORS = {
    remove_cour_dappel(LOCATIONS_CA[k]): c
    for k, c in zip(LOCATIONS_CA.keys(), PALETTES["pal_gouv_qual1"] * 10)
}
TJ_TO_COLORS = {
    remove_cour_dappel(LOCATIONS_TJ[k]): c
    for k, c in zip(LOCATIONS_TJ.keys(), PALETTES["pal_gouv_qual1"] * 10)
}

LEVELS_TO_COLORS = {
    n: c
    for n, c in zip(
        [
            "Droit des personnes",
            "Droit de la famille",
            "Droit des affaires ",
            "Entreprises en difficulté-surendettement",
            "Entreprises en difficulté",
            "Contrats",
            "Responsabilité et quasi-contrats",
            "Biens - Propriété littéraire et artistique ",
            "Relations du travail et protection sociale",
            "Relations avec les personnes publiques",
        ],
        PALETTES["pal_gouv_qual1"],
    )
}

JURISDICTIONS_TO_COLORS = {
    "Cour de cassation": COLORS["cc"],
    "Cours d'appel": COLORS["ca"],
    "Tribunaux judiciaires": COLORS["tj"],
}


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
        color_discrete_map=JURISDICTIONS_TO_COLORS,
        labels=LABELS,
    )

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
    )

    return fig


def get_time_by_year_graph(df: pd.DataFrame):
    """Returns a graph of decisions per year and jurisdiction"""

    df = (
        df.groupby(["decision_year", "jurisdiction"])
        .agg({"n_decisions": "sum"})
        .reset_index()
    )

    fig = px.bar(
        data_frame=df,
        x="decision_year",
        y="n_decisions",
        color="jurisdiction",
        color_discrete_map=JURISDICTIONS_TO_COLORS,
        range_x=[1980, 2024],
        labels=LABELS,
    )

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
    )

    return fig


def get_time_by_month_cc_graph(df: pd.DataFrame):
    df_time = df.groupby(["decision_month"]).agg({"n_decisions": "sum"}).reset_index()

    df_time["n_decisions_lisse"] = (
        df_time["n_decisions"].rolling(window=12, center=True).mean()
    )

    fig = px.bar(
        data_frame=df_time,
        x="decision_month",
        y="n_decisions",
        color_discrete_sequence=[COLORS["cc"]],
        labels=LABELS,
    )

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
    )

    return fig


def get_chamber_cc_graph(df: pd.DataFrame):
    """Returns a graph of decisions per formation (Cour de cassation)"""

    df = df.groupby(["chamber"]).agg({"n_decisions": "sum"}).reset_index()

    fig = px.bar(
        data_frame=df,
        x="chamber",
        y="n_decisions",
        labels=LABELS,
        color_discrete_sequence=[COLORS["cc"]],
    )

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
    )

    return fig


def get_type_cc_graph(df: pd.DataFrame):
    """Returns a graph of decisions per formation (Cour de cassation)"""

    df = df.groupby("type").agg({"n_decisions": "sum"}).reset_index()

    fig = px.bar(
        data_frame=df,
        x="type",
        y="n_decisions",
        labels=LABELS,
        color_discrete_sequence=[COLORS["cc"]],
    )

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def get_formation_cc_graph(df):
    df_formation_cc = (
        df.loc[:, ["formation", "n_decisions"]]
        .fillna("Non renseigné")
        .loc[df["formation"] != "Non renseigné"]
        .groupby(["formation"])
        .agg({"n_decisions": "sum"})
        .reset_index()
    )

    fig = px.bar(
        data_frame=df_formation_cc,
        x="formation",
        y="n_decisions",
        labels=LABELS,
        color_discrete_sequence=[COLORS["cc"]],
    )

    fig.update_layout(plot_bgcolor="rgb(255, 255, 255)")

    return fig


def get_publication_cc_graph(df):
    df_publications = (
        df.loc[:, ["publication", "n_decisions"]]
        .groupby("publication")
        .sum()
        .reset_index()
    )

    fig = px.bar(
        data_frame=df_publications,
        x="publication",
        y="n_decisions",
        color_discrete_sequence=[COLORS["cc"]],
        # log_y=True,
        labels=LABELS,
    )

    fig.update_layout(plot_bgcolor="rgb(255, 255, 255)")

    return fig


def get_location_ca_graph(df: pd.DataFrame):
    """Returns a graph of decisions per location (cours d'appel)"""
    df_location = df.groupby(["location"]).agg({"n_decisions": "sum"}).reset_index()

    fig = px.bar(
        data_frame=df_location,
        x="location",
        y="n_decisions",
        color_discrete_sequence=[COLORS["ca"]],
        labels=LABELS,
    )

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
    )

    return fig


def get_nac_level_ca_graph(df: pd.DataFrame):
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
        # color_discrete_sequence=PALETTES["pal_gouv_qual1"],
        color_discrete_map=LEVELS_TO_COLORS,
        labels=LABELS,
    )

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
    )

    return fig


def get_nac_ca_graph(df: pd.DataFrame):
    """Returns a graph of decisions per code NAC (cours d'appel)"""
    df_nac = (
        df.groupby(["nac", "Niveau 1", "N1", "Intitulé NAC"])
        .agg({"n_decisions": "sum"})
        .reset_index()
    )

    fig = px.bar(
        data_frame=df_nac[df_nac["n_decisions"] != 0].sort_values(["N1", "nac"]),
        x="nac",
        y="n_decisions",
        color="Niveau 1",
        # color_discrete_sequence=PALETTES["pal_gouv_qual1"],
        color_discrete_map=LEVELS_TO_COLORS,
        hover_data=["n_decisions", "nac", "Intitulé NAC", "Niveau 1"],
        labels=LABELS,
    )

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
    )

    return fig


def get_location_tj_graph(df: pd.DataFrame):
    """Returns a graph of decisions per location (TJ)"""
    df_location = df.groupby(["location"]).agg({"n_decisions": "sum"}).reset_index()

    fig = px.bar(
        data_frame=df_location,
        x="location",
        y="n_decisions",
        color_discrete_sequence=[COLORS["tj"]],
        labels={**LABELS, "location": "Tribunal judiciaire"},
    )

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
    )

    return fig


def get_nac_level_tj_graph(df: pd.DataFrame):
    """Returns a graph of decisions per NAC level (1 and 2) (TJ)"""

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
        # color_discrete_sequence=PALETTES["pal_gouv_qual1"],
        color_discrete_map=LEVELS_TO_COLORS,
        labels=LABELS,
    )

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
    )

    return fig


def get_nac_tj_graph(df: pd.DataFrame):
    """Returns a graph of decisions per code NAC (TJ)"""
    df_nac = (
        df.groupby(["nac", "Niveau 1", "N1", "Intitulé NAC"])
        .agg({"n_decisions": "sum"})
        .reset_index()
    )

    fig = px.bar(
        data_frame=df_nac[df_nac["n_decisions"] != 0].sort_values(["N1", "nac"]),
        x="nac",
        y="n_decisions",
        color="Niveau 1",
        # color_discrete_sequence=PALETTES["pal_gouv_qual1"],
        color_discrete_map=LEVELS_TO_COLORS,
        hover_data=["n_decisions", "nac", "Intitulé NAC", "Niveau 1"],
        labels=LABELS,
    )

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
    )

    return fig


def get_time_selected_location_ca_graph(
    df: pd.DataFrame, locations: list[str] = ["Paris", "Versailles", "Aix-en-Provence"]
):
    """Returns a graph of decisions per month and cour d'appel"""

    df_time = df.copy()
    df_time = df_time[df_time["location"].isin(locations)]

    df_time = (
        df_time.groupby(["decision_month", "location", "court"])
        .agg({"n_decisions": "sum"})
        .reset_index()
        .sort_values(by=["decision_month", "location"])
    )

    fig = px.bar(
        data_frame=df_time,
        x="decision_month",
        y="n_decisions",
        color="location",
        color_discrete_map=CA_TO_COLORS,
        labels=LABELS,
    )

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
    )

    return fig


def get_nac_level_selected_location_ca_graph(
    df: pd.DataFrame, locations: list[str] = ["Paris"]
):
    df_nac = (
        df[df["location"].isin(locations)]
        .groupby(["N1", "Niveau 1", "location"])
        .agg({"n_decisions": "sum"})
        .reset_index()
        .dropna(subset=["N1", "Niveau 1"])
        .sort_values(by=["N1", "location"])
    )

    fig = px.bar(
        data_frame=df_nac,
        x="Niveau 1",
        y="n_decisions",
        color="location",
        barmode="stack",
        color_discrete_map=CA_TO_COLORS,
        labels=LABELS,
    )

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
    )

    return fig


def get_nac_selected_location_ca_graph(
    df: pd.DataFrame, locations: list[str] = ["Paris", "Versailles", "Aix-en-Provence"]
):
    """Returns a graph of decisions per Code NAC and cour d'appel"""
    df_nac = (
        df.loc[df["location"].isin(locations)]
        .groupby(["nac", "Intitulé NAC", "location"])
        .agg({"n_decisions": "sum"})
        .reset_index()
        .dropna(subset=["nac"])
        .sort_values(by=["nac", "location"])
    )

    fig = px.bar(
        data_frame=df_nac,
        x="nac",
        y="n_decisions",
        color="location",
        barmode="stack",
        color_discrete_map=CA_TO_COLORS,
        hover_data=["nac", "Intitulé NAC", "n_decisions", "location"],
        labels=LABELS,
    )
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
    )

    return fig


def get_time_selected_location_tj_graph(
    df: pd.DataFrame,
    locations: list[str] = [
        "Paris",
    ],
):
    """Returns a graph of decisions per month and cour d'appel"""

    df_time = df.copy()
    df_time = df_time[df_time["location"].isin(locations)]

    df_time = (
        df_time.groupby(["decision_month", "location", "court"])
        .agg({"n_decisions": "sum"})
        .reset_index()
        .sort_values(by=["decision_month", "location"])
    )

    fig = px.bar(
        data_frame=df_time,
        x="decision_month",
        y="n_decisions",
        color="location",
        color_discrete_map=TJ_TO_COLORS,
        labels={
            **LABELS,
            "location": "Tribunal judiciaire",
            "court": "Tribunal judiciaire",
        },
    )

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
    )

    return fig


def get_nac_level_selected_location_tj_graph(
    df: pd.DataFrame, locations: list[str] = ["Paris"]
):
    df_nac = (
        df[df["location"].isin(locations)]
        .groupby(["N1", "Niveau 1", "location"])
        .agg({"n_decisions": "sum"})
        .reset_index()
        .dropna(subset=["N1", "Niveau 1"])
        .sort_values(by=["N1", "location"])
    )

    fig = px.bar(
        data_frame=df_nac,
        x="Niveau 1",
        y="n_decisions",
        color="location",
        barmode="stack",
        color_discrete_map=TJ_TO_COLORS,
        labels={
            **LABELS,
            "location": "Tribunal judiciaire",
            "court": "Tribunal judiciaire",
        },
    )

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
    )

    return fig


def get_nac_selected_location_tj_graph(
    df: pd.DataFrame,
    locations: list[str] = [
        "Paris",
    ],
):
    """Returns a graph of decisions per Code NAC and cour d'appel"""
    df_nac = (
        df.loc[df["location"].isin(locations)]
        .groupby(["nac", "Intitulé NAC", "location"])
        .agg({"n_decisions": "sum"})
        .reset_index()
        .dropna(subset=["nac"])
        .sort_values(by=["nac", "location"])
    )

    fig = px.bar(
        data_frame=df_nac,
        x="nac",
        y="n_decisions",
        color="location",
        barmode="stack",
        color_discrete_map=TJ_TO_COLORS,
        hover_data=["nac", "Intitulé NAC", "n_decisions", "location"],
        labels={
            **LABELS,
            "location": "Tribunal judiciaire",
            "court": "Tribunal judiciaire",
        },
    )
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
    )

    return fig
