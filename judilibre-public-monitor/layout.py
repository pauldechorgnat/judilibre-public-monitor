import datetime

from dash import dcc
from dash import html
from data.data_utils import LOCATIONS_CA
from data.data_utils import remove_cour_dappel

DISCLAIMER = open("assets/texts/disclaimer.txt").read()


def get_layout():
    return html.Div(
        [
            get_header(),
            get_summary(),
            get_main_content(),
            get_focus_cc(),
            get_focus_ca(),
            dcc.Input(id="dummy-input", style={"display": "none"}),
        ]
    )


def get_header():
    return html.Header(
        children=[
            # html.Img(
            #     src="/assets/images/france.png",
            #     height="100px", id="france-bloc-marque"
            # ),
            html.Img(
                src="/assets/images/cour-de-cassation.svg",
                height="100px",
                alt="Logo de la Cour de cassation",
                id="cour-de-cassation-bloc-marque",
            ),
            html.Div(
                [
                    html.H1("API Judilibre", className="main-title"),
                    html.P(
                        "Statistiques des données ouvertes", className="secondary-title"
                    ),
                ],
                className="title-container",
            ),
        ],
        className="header-container",
    )


def get_summary():
    return html.Div(
        [
            html.H2("Total"),
            html.Div(
                [
                    get_summary_card(
                        card_content_default=0,
                        card_title="Nombre de décisions",
                        card_content_id="nb-decisions-card",
                    ),
                    get_summary_card(
                        card_content_default=0,
                        card_title="Nombre de décisions CA",
                        card_content_id="nb-decisions-ca-card",
                    ),
                    get_summary_card(
                        card_content_default=0,
                        card_title="Nombre de décisions CC",
                        card_content_id="nb-decisions-cc-card",
                    ),
                    get_summary_card(
                        card_content_default="01/01/1790",
                        card_title="Date dernière décision",
                        card_content_id="date-latest-decision-card",
                    ),
                ],
                className="card-container",
            ),
            html.H2("Résumé"),
        ],
        className="content-container",
    )


def get_main_content():
    return html.Div(
        [
            html.Div(
                [
                    get_graph(
                        "source-graph",
                        "Nombre de décisions par source",
                        width="30%",
                    ),
                    get_graph(
                        "time-graph", "Nombre de décisions par année", width="70%"
                    ),
                ],
                className="row",
            ),
            html.Div(
                [
                    html.Label("Date de début", htmlFor="start-date-picker"),
                    dcc.DatePickerSingle(
                        id="start-date-picker",
                        min_date_allowed=datetime.date(year=1790, month=1, day=1),
                        max_date_allowed=datetime.date.today(),
                        date=datetime.date(year=2000, month=1, day=1),
                    ),
                    html.Label("Date de fin", htmlFor="end-date-picker"),
                    dcc.DatePickerSingle(
                        id="end-date-picker",
                        min_date_allowed=datetime.date(year=1790, month=1, day=1),
                        max_date_allowed=datetime.date.today(),
                        date=datetime.date.today(),
                    ),
                ]
            ),
        ],
        className="content-container",
    )


def get_summary_card(
    # card_id: str,
    card_title: str,
    card_content_id: str,
    card_content_default: str = "0",
):
    return html.Div(
        [
            html.P(card_content_default, className="card-content", id=card_content_id),
            html.P(card_title, className="card-title"),
        ],
        className="card",
        # id=card_id
    )


def get_graph(graph_id: str, graph_title: str, width: str = None):
    if width:
        div = html.Div(
            [
                html.P(graph_title, className="graph-title"),
                dcc.Graph(
                    id=graph_id,
                    config={"displaylogo": False},
                ),
            ],
            className="graph-container",
            style={"width": width},
        )
        return div

    div = html.Div(
        [html.P(graph_title, className="graph-title"), dcc.Graph(id=graph_id)],
        className="graph-container",
    )
    return div


def get_focus_ca():
    return html.Div(
        [
            html.H2("Décisions des cours d'appel"),
            html.Div(
                [get_graph("location-graph", "Nombre de décisions par cour d'appel")],
                className="row",
            ),
            html.Div(
                [get_graph("nac-graph", "Nombre de décisions par code NAC")],
                className="row",
            ),
            html.Label(
                "Choix d'une ou plusieurs cour(s) d'appel:",
                htmlFor="time-location-input",
            ),
            dcc.Dropdown(
                {remove_cour_dappel(v): v for v in LOCATIONS_CA.values()},
                ["Paris"],
                id="time-location-input",
                multi=True,
            ),
            html.Div(
                get_graph(
                    graph_id="time-location-graph",
                    graph_title="Nombre de décisions par mois",
                ),
                className="row",
            ),
            html.Div(
                get_graph("nac-location-graph", "Nombre de décisions par code NAC"),
                className="row",
            ),
            html.Div(
                [
                    html.Label(
                        "Selectionnez un jeu de données à télécharger",
                        htmlFor="download-ca-choice",
                    ),
                    dcc.Dropdown(
                        {
                            "ca_location": "Nombre de décisions par cour d'appel",
                            "ca_nac": "Nombre de décisions par code NAC",
                            "ca_location_nac": "Nombre de décisions "
                            "par cour d'appel et code NAC",
                        },
                        "ca_location",
                        multi=False,
                        id="download-ca-choice",
                        style={"width": "100%"},
                    ),
                ],
                className="row",
            ),
            html.Div(
                [
                    html.Button("Télécharger", id="download-ca-submit"),
                    dcc.Download(id="download-ca-data"),
                ],
                className="row",
            ),
        ],
        className="content-container",
    )


def get_focus_cc():
    return html.Div(
        [
            html.Header(html.H2("Décisions de la Cour de cassation")),
            html.Div(
                [
                    get_graph("chamber-graph", "Nombre de décisions par formation"),
                    get_graph("type-graph", "Nombre de décisions par type"),
                ],
                className="row",
            ),
        ],
        className="content-container",
    )
