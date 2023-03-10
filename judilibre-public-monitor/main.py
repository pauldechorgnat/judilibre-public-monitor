from dash import Dash
from dash import dcc
from dash import Input
from dash import Output
from dash import State
from data.load_data import get_ca_data
from data.load_data import load_data
from graphs import get_chamber_graph
from graphs import get_jurisidction_graph
from graphs import get_location_graph
from graphs import get_nac_graph
from graphs import get_nac_location_graph
from graphs import get_source_graph
from graphs import get_time_graph
from graphs import get_time_location_graph
from graphs import get_type_graph
from layout import get_layout

EXTERNAL_STYLESHEETS = ["assets/custom.css"]

app = Dash(
    title="Judilibre - Tableau de suivi",
    external_stylesheets=EXTERNAL_STYLESHEETS,
)

app._favicon = "images/cour-de-cassation.png"

app.layout = get_layout()


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
    Input("dummy-input", "value"),
)
def update_graphs(n_clicks):
    df = load_data(path="./data")

    nb_decisions = f"{df.shape[0]:,}".replace(",", " ")
    max_date = df["decision_date"].max()

    max_date = f"{max_date.day:02}/{max_date.month:02}/{max_date.year:04}"

    nb_decisions_cc = (df["jurisdiction"] == "cc").sum()
    nb_decisions_cc = f"{nb_decisions_cc:,}".replace(",", " ")
    nb_decisions_ca = (df["jurisdiction"] == "ca").sum()
    nb_decisions_ca = f"{nb_decisions_ca:,}".replace(",", " ")

    source_graph = get_source_graph(df=df)
    # jurisdiction_graph = get_jurisidction_graph(df=df)
    time_graph = get_time_graph(df=df, date_type="decision_date")
    location_graph = get_location_graph(df=df, include_cc=False)
    nac_graph = get_nac_graph(df=df)
    chamber_graph = get_chamber_graph(df=df)
    type_graph = get_type_graph(df=df)
    return (
        source_graph,
        # jurisdiction_graph,
        time_graph,
        location_graph,
        nac_graph,
        nb_decisions,
        max_date,
        chamber_graph,
        type_graph,
        nb_decisions_cc,
        nb_decisions_ca,
    )


@app.callback(
    Output("time-location-graph", "figure"),
    Output("nac-location-graph", "figure"),
    Input("time-location-input", "value"),
)
def update_time_location_graph(locations):
    df = load_data(path="./data")
    time_location_graph = get_time_location_graph(df=df, locations=locations)
    nac_location_graph = get_nac_location_graph(df=df, locations=locations)
    return time_location_graph, nac_location_graph


@app.callback(
    Output("download-ca-data", "data"),
    State("download-ca-choice", "value"),
    Input("download-ca-submit", "n_clicks"),
    # prevent_initial_callbacks=True,
)
def download_ca_data(ca_choice, n_clicks):
    if not n_clicks:
        return None
    df = load_data(path="./data")
    df = get_ca_data(df=df, choice=ca_choice)
    return dcc.send_data_frame(df.to_csv, filename=f"{ca_choice}.csv")


if __name__ == "__main__":
    from argparse import ArgumentParser

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
