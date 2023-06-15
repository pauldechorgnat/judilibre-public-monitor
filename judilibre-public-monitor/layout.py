import datetime

from dash import dcc
from dash import html
from data.data_utils import LOCATIONS_CA
from data.data_utils import remove_cour_dappel

TODAY = datetime.date.today()


def get_layout(include_download: bool = False):
    return html.Div(
        [
            get_header(),
            get_summary(),
            get_main_content(),
            get_focus_cc(),
            get_focus_ca(),
            get_download(include_download=include_download),
            dcc.Input(id="dummy-input", style={"display": "none"}),
            get_footer(),
            dcc.Interval(id="download-interval", interval=1000 * 60 * 60 * 2),
            html.Div(id="dummy-div", style={"display": "none"}),
        ]
    )


def get_header():
    return html.Header(
        children=[
            html.Img(
                src="/assets/images/cour-de-cassation.svg",
                height="100px",
                alt="Logo de la Cour de cassation",
                id="cour-de-cassation-logo",
            ),
            html.Div(
                [
                    html.H1("API Judilibre", className="main-title"),
                    html.P(
                        "Statistiques des décisions de justice diffusées en Open Data",
                        className="secondary-title",
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
            html.H2("Résumé général", style={"font-size": "2rem"}),
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
            # html.H2("Résumé"),
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
                        "time-by-year", "Nombre de décisions par année", width="70%"
                    ),
                ],
                className="row",
            ),
            html.H2("Analyse", style={"font-size": "2rem"}),
            # html.Hr(style={"margin-top": "3rem", "margin-bottom": "3rem"}),
            html.Div(
                html.P(
                    "Sélectionnez des dates pour restreindre les graphiques suivants:",
                    className="text",
                ),
                className="row",
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.Label(
                                "Date de début",
                                htmlFor="start-date-picker",
                                className="label-for-date-picker",
                            ),
                            dcc.Input(
                                id="start-date-picker",
                                value="01/01/2000",
                                debounce=True,
                                pattern=r"(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(\/|-|\.)(?:0?[13-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})",
                                className="date-picker",
                            ),
                        ],
                        className="date-picker-card",
                    ),
                    html.Div(
                        [
                            html.Label(
                                "Date de fin",
                                htmlFor="end-date-picker",
                                className="label-for-date-picker",
                            ),
                            dcc.Input(
                                id="end-date-picker",
                                value=f"{TODAY.day:02}/{TODAY.month:02}/{TODAY.year:04}",
                                debounce=True,
                                pattern=r"(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(\/|-|\.)(?:0?[13-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})",
                                className="date-picker",
                            ),
                        ],
                        className="date-picker-card",
                    ),
                ],
                className="row",
            ),
        ],
        className="content-container",
    )


def get_focus_cc():
    return html.Div(
        [
            html.Div(
                [
                    get_summary_card(
                        card_content_default=0,
                        card_title="Nombre de décisions",
                        card_content_id="nb-decisions-card-date",
                    ),
                    get_summary_card(
                        card_content_default=0,
                        card_title="Nombre de décisions CA",
                        card_content_id="nb-decisions-ca-card-date",
                    ),
                    get_summary_card(
                        card_content_default=0,
                        card_title="Nombre de décisions CC",
                        card_content_id="nb-decisions-cc-card-date",
                    ),
                    get_summary_card(
                        card_content_default="01/01/1790",
                        card_title="Date dernière décision",
                        card_content_id="date-latest-decision-card-date",
                    ),
                ],
                className="card-container",
            ),
            html.Header(html.H2("Décisions de la Cour de cassation")),
            html.Div(
                get_graph(
                    "time-by-month-cc-graph",
                    "Nombre de décisions par mois",
                ),
                className="row",
            ),
            html.Div(
                [
                    get_graph("chamber-cc-graph", "Nombre de décisions par chambre"),
                    get_graph("type-cc-graph", "Nombre de décisions par type"),
                ],
                className="row",
            ),
            html.Div(
                [
                    get_graph(
                        "formation-cc-graph", "Nombre de décisions par formation"
                    ),
                    get_graph(
                        "publication-cc-graph",
                        "Nombre de décisions par type de publication",
                    ),
                ],
                className="row",
            ),
        ],
        className="content-container",
    )


def get_focus_ca():
    return html.Div(
        [
            html.H2("Décisions des cours d'appel"),
            html.Div(
                [
                    get_graph(
                        "location-ca-graph", "Nombre de décisions par cour d'appel"
                    )
                ],
                className="row",
            ),
            html.Div(
                [
                    get_graph(
                        "nac-level-ca-graph", "Nombre de décisions par niveau d'affaire"
                    )
                ],
                className="row",
            ),
            html.Div(
                [get_graph("nac-ca-graph", "Nombre de décisions par code NAC")],
                className="row",
            ),
            html.H2("Sélection de cours d'appel"),
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
                    graph_id="time-selected-location-ca-graph",
                    graph_title="Nombre de décisions par mois",
                ),
                className="row",
            ),
            html.Div(
                [
                    get_graph(
                        "nac-level-selected-location-ca-graph",
                        "Nombre de décisions par niveau d'affaire",
                    )
                ],
                className="row",
            ),
            html.Div(
                get_graph(
                    "nac-selected-location-ca-graph", "Nombre de décisions par code NAC"
                ),
                className="row",
            ),
        ],
        className="content-container",
    )


def get_download(include_download: bool = False):
    # div_style = {}
    # if not include_download:
    #     div_style["display"] = "none"
    if include_download:
        return html.Div(
            [
                html.H2("Téléchargements"),
                html.Div(
                    [
                        html.Label(
                            "Sélectionnez un jeu de données à télécharger",
                            htmlFor="download-ca-choice",
                            className="label-for-download-picker",
                        ),
                        dcc.Dropdown(
                            {
                                "ca_location": "Nombre de décisions par cour d'appel",
                                "ca_nac": "Nombre de décisions par code NAC",
                                "ca_location_nac": "Nombre de décisions "
                                "par cour d'appel et code NAC",
                                "all_data": "Données complètes agrégées",
                            },
                            "ca_location",
                            multi=False,
                            clearable=False,
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
            # style=div_style,
        )


def get_footer():
    return html.Div(
        [
            html.Img(
                src="/assets/images/Republique_Francaise_RVB.png",
                height="150px",
                className="logo-republic",
                alt="Logo de la République Française",
            ),
            html.Div(
                [
                    html.A("Cour de cassation", href="https://www.courdecassation.fr/"),
                    html.A(
                        "Recherche Judilibre",
                        href="https://www.courdecassation.fr/recherche-judilibre",
                    ),
                    html.A(
                        "Code source",
                        href="https://github.com/pauldechorgnat/judilibre-public-monitor",
                    ),
                    html.A("piste.gouv.fr", href="https://piste.gouv.fr/"),
                    html.A(
                        "api.gouv.fr", href="https://api.gouv.fr/les-api/api-judilibre"
                    ),
                    html.A("Contact", href="mailto:prenom.nom@justice.fr"),
                ],
                className="link-container",
            ),
        ],
        className="footer",
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
        [
            html.P(graph_title, className="graph-title"),
            dcc.Graph(id=graph_id, config={"displaylogo": False}),
        ],
        className="graph-container",
    )
    return div
