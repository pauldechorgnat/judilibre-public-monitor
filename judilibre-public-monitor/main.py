import datetime
import logging
import os

from dash import Dash
from dash import dcc
from dash import Input
from dash import Output
from dash import State
from data.download_latest_data import download_latest_data
from data.load_data import get_download_data
from data.load_data import load_data
from dotenv import load_dotenv
from flask_caching import Cache
from graphs import get_chamber_graph
from graphs import get_formation_time_graph
from graphs import get_location_graph
from graphs import get_nac_graph
from graphs import get_nac_level_graph
from graphs import get_nac_level_location_graph
from graphs import get_nac_location_graph
from graphs import get_source_graph
from graphs import get_time_graph
from graphs import get_time_location_graph
from graphs import get_type_graph
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


@app.callback(
    Output("source-graph", "figure"),
    # Output("jurisdiction-graph", "figure"),
    Output("time-graph", "figure"),
    Output("location-graph", "figure"),
    Output("nac-graph", "figure"),
    Output("nb-decisions-card", "children"),
    Output("date-latest-decision-card", "children"),
    Output("chamber-graph", "figure"),
    Output("type-graph", "figure"),
    Output("nb-decisions-cc-card", "children"),
    Output("nb-decisions-ca-card", "children"),
    Output("nac-level-graph", "figure"),
    Output("formation-time-graph", "figure"),
    Input("dummy-input", "value"),
    Input("start-date-picker", "date"),
    Input("end-date-picker", "date"),
)
# @cache.memoize(timeout=3600)
def update_graphs(n_clicks, start_date, end_date):
    df = load_data(path="./data")

    source_graph = get_source_graph(df=df)
    time_graph = get_time_graph(df=df)

    nb_decisions = df["n_decisions"].sum()
    nb_decisions = f"{nb_decisions:,}".replace(",", " ")
    max_date = df["decision_date"].max()

    max_date = f"{max_date.day:02}/{max_date.month:02}/{max_date.year:04}"

    nb_decisions_cc = df.loc[
        df["jurisdiction"] == "Cour de cassation", "n_decisions"
    ].sum()
    nb_decisions_cc = f"{nb_decisions_cc:,}".replace(",", " ")
    nb_decisions_ca = df.loc[df["jurisdiction"] == "Cours d'appel", "n_decisions"].sum()
    nb_decisions_ca = f"{nb_decisions_ca:,}".replace(",", " ")

    df = df[df["decision_date"] >= start_date]
    df = df[df["decision_date"] <= end_date]

    location_graph = get_location_graph(df=df)
    nac_graph = get_nac_graph(df=df)
    chamber_graph = get_chamber_graph(df=df)
    type_graph = get_type_graph(df=df)

    nac_level_graph = get_nac_level_graph(df=df)

    formation_time_graph = get_formation_time_graph(df=df)

    return (
        source_graph,
        time_graph,
        location_graph,
        nac_graph,
        nb_decisions,
        max_date,
        chamber_graph,
        type_graph,
        nb_decisions_cc,
        nb_decisions_ca,
        nac_level_graph,
        formation_time_graph,
    )


@app.callback(
    Output("time-location-graph", "figure"),
    Output("nac-location-graph", "figure"),
    Output("level-location-graph", "figure"),
    Input("time-location-input", "value"),
    Input("start-date-picker", "date"),
    Input("end-date-picker", "date"),
)
def update_time_location_graph(locations, start_date, end_date):
    df = load_data(path="./data")
    df = df[df["decision_date"] >= start_date]
    df = df[df["decision_date"] <= end_date]
    time_location_graph = get_time_location_graph(df=df, locations=locations)
    nac_location_graph = get_nac_location_graph(df=df, locations=locations)
    nac_level_location_graph = get_nac_level_location_graph(df=df, locations=locations)
    return time_location_graph, nac_location_graph, nac_level_location_graph


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
