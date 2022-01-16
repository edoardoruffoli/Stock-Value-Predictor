import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

import common.costants as const

stylesheet = ['./assets/style.css']

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])

app.layout = html.Div([
    html.Div(
        className="app-header",
        children=[
            html.Div('Stock Value Predictor', className="title")
        ]
    ),
    html.Div(
        className="set-option",
        children=[
            html.Label('Select Stock:'),
            dcc.Dropdown(
                id='select-stock',
                options=[{'label': i['name'], 'value': i['ticker']} for i in const.target_company],
                value="NONE"
            ),
        ]
    ),
    html.Div(
        className="graph-view",
        children=[
            dcc.Graph(id='stocks-view')
        ]
    )
])

@app.callback(
    Output("stocks-view", "figure"),
    Input("select-stock", "value")
)
def show_stock_graph(ticker):
    if ticker == 'NONE':
        return {}
    file_name = "data/historical_data/" + str(ticker) + ".json"
    stocks_df = pd.read_json(file_name, lines=True)
    print(stocks_df.head())
    fig = px.line(stocks_df,
                  x="Date",
                  y="Open",
                  title=ticker,
                  line_shape="spline",
                  render_mode="svg")
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)