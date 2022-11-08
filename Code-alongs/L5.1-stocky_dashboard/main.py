import os
import dash
from load_data import StockData
from time_filtering import filter_time
import plotly_express as px
import pandas as pd
from dash import html, dcc  # dcc - dash core components
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input

directory_path = os.path.dirname(__file__)
path = os.path.join(directory_path, "stocksdata")

print(path)

stockdata_object = StockData(path)

# pick one stock (to test)
# print(stockdata_object.stock_dataframe("AAPL"))

symbol_dict = {"AAPL": "Apple", "NVDA": "Nvidia", "TSLA": "Tesla", "IBM": "IBM"}

df_dict = {symbol: stockdata_object.stock_dataframe(symbol) for symbol in symbol_dict}

stock_options_dropdown = [
    {"label": name, "value": symbol} for symbol, name in symbol_dict.items()
]

slider_marks = {
    i: mark
    for i, mark in enumerate(
        ["1 day", "1 week", "1 month", "3 months", "1 year", "5 years", "Max"]
    )
}

ohlc_options = [
    {"label": option, "value": option} for option in ("open", "high", "low", "close")
]
# print(df_dict.keys()) # See the keys in df_dict
# print(df_dict["TSLA"][0]) #Get the Tesla Dataframe

# create a Dash App.
app = dash.Dash(__name__)

app.layout = html.Main(
    [
        html.H1("Knock off Avanza"),  # html H1 = Header 1 (rubrik)
        html.P("Choose a stock"),
        dcc.Dropdown(
            id="stockpicker-dropdown",
            options=stock_options_dropdown,
            value="AAPL",
        ),
        html.P(id="highest-value"),
        html.P(id="lowest-value"),
        dcc.RadioItems(
            id="ohlc-radio", options=ohlc_options, value="close"
        ),  # creates the "button" object.
        dcc.Graph(id="stock-graph"),
        dcc.Slider(
            id="time-slider", min=0, max=6, marks=slider_marks, value=2, step=None
        ),  # value = 2 = 1 month, step allows us to snap between values.
        # storing intermediate value on clients browser in order to share between several callbacks.
        dcc.Store(id="filtered-df"),
    ]
)


@app.callback(
    Output("filtered-df", "data"),
    Input("stockpicker-drowpdown", "value"),
    Input("time-slider", "value"),
)
def filter_df(stock, time_index):
    dff_daily, dff_intraday = df_dict[stock]

    dff = dff_intraday if time_index <= 2 else dff_daily

    days = {i: day for i, day in enumerate([1, 7, 30, 90, 365, 365 * 5])}

    dff = dff if time_index == 6 else filter_time(dff, days=days[time_index])

    return dff.to_json()


@app.callback(
    Output("highest_value", "children"),
    Output("lowest_value", "children"),
    Input("filtered-df", "data"),
    Input("olhc-radio", "value"),
)
def highest_lowest_value_update(json_df, ohlc):
    dff = pd.read_json(json_df)
    highest_value = dff[ohlc].max()
    lowest_value = dff[ohlc].min()
    return highest_value, lowest_value


@app.callback(
    Output("stock-graph", "figure"),
    Input("filtered-df", "data"),
    Input("stockpicker-dropdown", "value"),
    Input("ohlc-radio", "value"),
)
def update_graph(json_df, stock, ohlc):
    dff = pd.read_json(json_df)
    return px.line(dff, x=dff.index, y=ohlc, title=symbol_dict[stock])


if __name__ == "__main__":
    app.run_server(debug=True)
