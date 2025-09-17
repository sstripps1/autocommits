from dash import Dash, dcc, html, callback, Input, Output, State
import dash_design_kit as ddk
import plotly.express as px
from theme import my_theme

app = Dash(__name__)


def get_data():
    # Retrieve data in Python.
    df = px.data.stocks()

    # Post-process data in Python.
    df.fillna(0)
    return df


def run_model(df, stock):
    return df.drop(["date"], axis=1).rolling(10).mean()


app.layout = ddk.App(
    [
        ddk.Header(
            [
                ddk.Logo(src=app.get_asset_url("logo.svg")),
                ddk.Title("Monthly Analysis"),
            ]
        ),
        dcc.Dropdown(
            options=["GOOG", "AAPL", "AMZN"],
            id="title-dropdown",
            value="GOOG",
        ),
        ddk.Card(
            children=[
                ddk.Graph(id="graph-1", style={"height": "65vh"}),
            ],
            width=100,
        ),
        ddk.Card(
            width=60,
            children=ddk.Graph(
                id="graph-2",
                figure=px.line(
                    get_data(),
                    x="date",
                    y=["AMZN", "GOOG"],
                    title="Stock Prices",
                )
            ),
        ),
        ddk.Card(
            width=40,
            children=ddk.Graph(
                id="graph-3",
                figure=px.bar(
                    get_data(),
                    x="date",
                    y=["AAPL", "MSFT"],
                    barmode="stack",
                    title="Stock Prices"
                )
            ),
        ),
    ],
    show_editor=True, # Show DDK editor button.
    theme=my_theme,
)


@callback(
    Output("graph-1", "figure"),
    Input("title-dropdown", "value")
)
def update_graph(dropdown_value):
    df = get_data()
    model = run_model(df, dropdown_value)

    return px.line(
        model,
        y=dropdown_value,
    )


server = app.server
if __name__ == "__main__":
    app.run(debug=True)
