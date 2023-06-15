import datetime
import logging
import os

from dash import Dash
from dash import dcc
from dash import Input
from dash import Output
from dash import State
from data.compute_datasets import compute_all_datasets
from data.compute_datasets import load_general_datasets
from data.compute_datasets import load_selected_datasets
from data.compute_datasets import load_static_datasets
from data.download_latest_data import download_latest_data
from data.load_data import get_download_data
from data.load_data import load_data
from dotenv import load_dotenv
from flask_caching import Cache
from graphs import get_chamber_cc_graph
from graphs import get_formation_cc_graph
from graphs import get_location_ca_graph
from graphs import get_nac_ca_graph
from graphs import get_nac_level_ca_graph
from graphs import get_nac_level_selected_location_ca_graph
from graphs import get_nac_selected_location_ca_graph
from graphs import get_publication_cc_graph
from graphs import get_source_graph
from graphs import get_time_by_month_cc_graph
from graphs import get_time_by_year_graph
from graphs import get_time_selected_location_ca_graph
from graphs import get_type_cc_graph
from layout import get_layout

load_dotenv()

EXTERNAL_STYLESHEETS = ["assets/custom.css"]

LATEST_UPDATE_DATE = datetime.date.today() - datetime.timedelta(days=1)

UPDATE_DATA = bool(int(os.environ.get("UPDATE_DATA")))
INCLUDE_DOWNLOAD = bool(int(os.environ.get("INCLUDE_DOWNLOAD")))


app = Dash(
    title="Judilibre - Tableau de suivi",
    external_stylesheets=EXTERNAL_STYLESHEETS,
)

cache = Cache(app.server, config={"CACHE_TYPE": "filesystem", "CACHE_DIR": "cache"})

app._favicon = "images/cour-de-cassation.svg"

# adding language accessibility

app._index_string = app._index_string.replace("<html>", "<html lang='fr'>")

app.layout = get_layout(include_download=INCLUDE_DOWNLOAD)


def format_date(date_str):
    (day, month, year) = date_str.replace(".", "/").replace("-", "/").split("/")

    return datetime.date(year=int(year), month=int(month), day=int(day))


@app.callback(
    Output("source-graph", "figure"),
    Output("time-by-year", "figure"),
    Output("nb-decisions-card", "children"),
    Output("nb-decisions-cc-card", "children"),
    Output("nb-decisions-ca-card", "children"),
    Output("date-latest-decision-card", "children"),
    Input("dummy-input", "value"),
)
def compute_general_figures(n_clicks):
    df_source, df_time_by_year = load_static_datasets(path="./data")
    source_graph = get_source_graph(df=df_source)
    time_by_year_graph = get_time_by_year_graph(df=df_time_by_year)

    nb_decisions = df_source["n_decisions"].sum()
    nb_decisions = f"{nb_decisions:,}".replace(",", " ")
    max_date = df_source["decision_date"].max()

    max_date = f"{max_date.day:02}/{max_date.month:02}/{max_date.year:04}"

    nb_decisions_cc = df_time_by_year.loc[
        df_time_by_year["jurisdiction"] == "Cour de cassation", "n_decisions"
    ].sum()
    nb_decisions_cc = f"{nb_decisions_cc:,}".replace(",", " ")
    nb_decisions_ca = df_time_by_year.loc[
        df_time_by_year["jurisdiction"] == "Cours d'appel", "n_decisions"
    ].sum()
    nb_decisions_ca = f"{nb_decisions_ca:,}".replace(",", " ")

    return (
        source_graph,
        time_by_year_graph,
        nb_decisions,
        nb_decisions_cc,
        nb_decisions_ca,
        max_date,
    )


@app.callback(
    Output("nb-decisions-card-date", "children"),
    Output("nb-decisions-cc-card-date", "children"),
    Output("nb-decisions-ca-card-date", "children"),
    Output("date-latest-decision-card-date", "children"),
    Output("time-by-month-cc-graph", "figure"),
    Output("chamber-cc-graph", "figure"),
    Output("type-cc-graph", "figure"),
    Output("formation-cc-graph", "figure"),
    Output("publication-cc-graph", "figure"),
    Output("location-ca-graph", "figure"),
    Output("nac-level-ca-graph", "figure"),
    Output("nac-ca-graph", "figure"),
    Input("start-date-picker", "value"),
    Input("end-date-picker", "value"),
)
# @cache.memoize(timeout=3600)
def update_graphs(start_date, end_date):
    (
        df_time_by_month,
        df_chamber_cc,
        df_type_cc,
        df_formation_cc,
        df_publication_cc,
        df_location_ca,
        df_nac_level_ca,
        df_nac_ca,
    ) = load_general_datasets(path="data")

    df_source, df_time_by_year = load_static_datasets(path="./data")

    start_date = format_date(start_date)
    end_date = format_date(end_date)

    # limiting data
    df_time_by_month = df_time_by_month[
        df_time_by_month["decision_date"].dt.date >= start_date
    ]
    df_time_by_month = df_time_by_month[
        df_time_by_month["decision_date"].dt.date <= end_date
    ]

    df_chamber_cc = df_chamber_cc[df_chamber_cc["decision_date"].dt.date >= start_date]
    df_chamber_cc = df_chamber_cc[df_chamber_cc["decision_date"].dt.date <= end_date]

    df_type_cc = df_type_cc[df_type_cc["decision_date"].dt.date >= start_date]
    df_type_cc = df_type_cc[df_type_cc["decision_date"].dt.date <= end_date]

    df_formation_cc = df_formation_cc[
        df_formation_cc["decision_date"].dt.date >= start_date
    ]
    df_formation_cc = df_formation_cc[
        df_formation_cc["decision_date"].dt.date <= end_date
    ]

    df_publication_cc = df_publication_cc[
        df_publication_cc["decision_date"].dt.date >= start_date
    ]
    df_publication_cc = df_publication_cc[
        df_publication_cc["decision_date"].dt.date <= end_date
    ]

    df_location_ca = df_location_ca[
        df_location_ca["decision_date"].dt.date >= start_date
    ]
    df_location_ca = df_location_ca[df_location_ca["decision_date"].dt.date <= end_date]

    df_nac_level_ca = df_nac_level_ca[
        df_nac_level_ca["decision_date"].dt.date >= start_date
    ]
    df_nac_level_ca = df_nac_level_ca[
        df_nac_level_ca["decision_date"].dt.date <= end_date
    ]

    df_nac_ca = df_nac_ca[df_nac_ca["decision_date"].dt.date >= start_date]
    df_nac_ca = df_nac_ca[df_nac_ca["decision_date"].dt.date <= end_date]

    df_source = df_source[df_source["decision_date"].dt.date >= start_date]
    df_source = df_source[df_source["decision_date"].dt.date <= end_date]

    df_time_by_year = df_time_by_year[
        df_time_by_year["decision_date"].dt.date >= start_date
    ]
    df_time_by_year = df_time_by_year[
        df_time_by_year["decision_date"].dt.date <= end_date
    ]

    # computing cards
    nb_decisions = df_source["n_decisions"].sum()
    nb_decisions = f"{nb_decisions:,}".replace(",", " ")
    max_date = df_source["decision_date"].max()

    max_date = f"{max_date.day:02}/{max_date.month:02}/{max_date.year:04}"

    nb_decisions_cc = df_time_by_year.loc[
        df_time_by_year["jurisdiction"] == "Cour de cassation", "n_decisions"
    ].sum()
    nb_decisions_cc = f"{nb_decisions_cc:,}".replace(",", " ")
    nb_decisions_ca = df_time_by_year.loc[
        df_time_by_year["jurisdiction"] == "Cours d'appel", "n_decisions"
    ].sum()

    nb_decisions_ca = f"{nb_decisions_ca:,}".replace(",", " ")

    # computing graphs

    time_by_month_cc_graph = get_time_by_month_cc_graph(df_time_by_month)

    chamber_cc_graph = get_chamber_cc_graph(df_chamber_cc)
    type_cc_graph = get_type_cc_graph(df_type_cc)

    formation_cc_graph = get_formation_cc_graph(df_formation_cc)
    publication_cc_graph = get_publication_cc_graph(df_publication_cc)

    location_ca_graph = get_location_ca_graph(df_location_ca)
    nac_level_ca_graph = get_nac_level_ca_graph(df_nac_level_ca)
    nac_ca_graph = get_nac_ca_graph(df_nac_ca)

    return (
        nb_decisions,
        nb_decisions_cc,
        nb_decisions_ca,
        max_date,
        time_by_month_cc_graph,
        chamber_cc_graph,
        type_cc_graph,
        formation_cc_graph,
        publication_cc_graph,
        location_ca_graph,
        nac_level_ca_graph,
        nac_ca_graph,
    )


@app.callback(
    Output("time-selected-location-ca-graph", "figure"),
    Output("nac-level-selected-location-ca-graph", "figure"),
    Output("nac-selected-location-ca-graph", "figure"),
    Input("time-location-input", "value"),
    Input("start-date-picker", "value"),
    Input("end-date-picker", "value"),
)
def update_time_location_graph(locations, start_date, end_date):
    start_date = format_date(start_date)
    end_date = format_date(end_date)

    (
        df_time_selected_location_ca_dataset,
        df_nac_level_selected_location_ca,
        df_nac_selected_location_ca,
    ) = load_selected_datasets(path="./data")

    df_time_selected_location_ca_dataset = df_time_selected_location_ca_dataset[
        df_time_selected_location_ca_dataset["decision_date"].dt.date <= end_date
    ]
    df_time_selected_location_ca_dataset = df_time_selected_location_ca_dataset[
        df_time_selected_location_ca_dataset["decision_date"].dt.date >= start_date
    ]

    df_nac_level_selected_location_ca = df_nac_level_selected_location_ca[
        df_nac_level_selected_location_ca["decision_date"].dt.date <= end_date
    ]
    df_nac_level_selected_location_ca = df_nac_level_selected_location_ca[
        df_nac_level_selected_location_ca["decision_date"].dt.date >= start_date
    ]

    df_nac_selected_location_ca = df_nac_selected_location_ca[
        df_nac_selected_location_ca["decision_date"].dt.date <= end_date
    ]
    df_nac_selected_location_ca = df_nac_selected_location_ca[
        df_nac_selected_location_ca["decision_date"].dt.date >= start_date
    ]

    time_selected_location_ca_graph = get_time_selected_location_ca_graph(
        df=df_time_selected_location_ca_dataset, locations=locations
    )
    nac_level_selected_location_ca_graph = get_nac_level_selected_location_ca_graph(
        df=df_nac_level_selected_location_ca, locations=locations
    )
    nac_selected_location_ca_graph = get_nac_selected_location_ca_graph(
        df=df_nac_selected_location_ca, locations=locations
    )

    return (
        time_selected_location_ca_graph,
        nac_level_selected_location_ca_graph,
        nac_selected_location_ca_graph,
    )


if INCLUDE_DOWNLOAD:

    @app.callback(
        Output("download-ca-data", "data"),
        State("download-ca-choice", "value"),
        Input("download-ca-submit", "n_clicks"),
        # State("start-date-picker", "date"),
        # State("end-date-picker", "date"),
        # prevent_initial_callbacks=True,
    )
    def download_data(data_choice, n_clicks):
        if not n_clicks:
            return None
        df = load_data(path="./data")
        df = get_download_data(
            df=df,
            choice=data_choice,
            # start_date=start_date, end_date=end_date
        )
        return dcc.send_data_frame(df.to_csv, filename=f"{data_choice}.csv")


@app.callback(
    Output("dummy-div", "children"), Input("download-interval", "n_intervals")
)
def update_data(n_interval):
    global LATEST_UPDATE_DATE
    global UPDATE_DATA
    if (LATEST_UPDATE_DATE != datetime.date.today()) and UPDATE_DATA:
        print(f"{datetime.datetime.now()} - Downloading new data")
        download_latest_data(
            api_key_id=os.environ.get("PISTE_API_KEY"),
            api_url=os.environ.get("PISTE_API_URL"),
            reference_file="./data/full_data.parquet",
            target_file="./data/full_data.parquet",
        )

        compute_all_datasets(path="./data")
        print("Datasets are computed")
        LATEST_UPDATE_DATE = datetime.date.today()


if __name__ == "__main__":
    from argparse import ArgumentParser

    load_dotenv()
    logging.basicConfig(level=logging.INFO)

    argument_parser = ArgumentParser()

    argument_parser.add_argument(
        "-p", "--port", default=9999, type=int, help="Port to use"
    )

    argument_parser.add_argument(
        "-d", "--debug-mode", action="store_true", help="Debug mode"
    )

    arguments = argument_parser.parse_args()

    port = arguments.port
    debug_mode = arguments.debug_mode

    app.run(host="0.0.0.0", debug=debug_mode, port=port)
