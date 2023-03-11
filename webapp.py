#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Run this app with `python app.py` and
# visit http://127.0.0.1:5000/ in your web browser.
import dash_bootstrap_components as dbc
import flask
from dash import Dash, html, dcc, Output, Input
from common_vars import FLIGHTS, BUS, TRAIN
from get_csv_data import get_csv_data


def get_transport_list(transportation_type):
    ttype = str(transportation_type)
    ttype = ttype.replace('[', '').replace(']', '').replace("'", '')
    transport_list = get_csv_data(
        ttype, 'webapp', True, 'web-app-python')[1]['From_Country']
    return [{'label': item, 'value': item} for item in transport_list]


def update_transport_list(transportation_type):
    return get_transport_list(transportation_type)


def update_button_clicks(dropdown_value):
    return 1


def update_transport_options(transportation_type):
    return update_transport_list(transportation_type)


server = flask.Flask(__name__)
app = Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP],
           suppress_callback_exceptions=True, prevent_initial_callbacks=True)

app.layout = html.Div([
    dbc.Row([
        dbc.Col(
            dcc.Checklist(
                id='checkbox',
                options=[
                    {'label': 'Flights', 'value': FLIGHTS},
                    {'label': 'Bus', 'value': BUS},
                    {'label': 'Train', 'value': TRAIN},
                ],
                value=['flights']
            )
        ),
        dbc.Col(
            dcc.Dropdown(
                id='dropdown',
                options=[],
                multi=True
            )
        ),
        dbc.Col(
            html.Button('Submit', id='submit-button', n_clicks=0)
        )
    ])
])

app.callback(Output('submit-button', 'n_clicks'),
             Input('dropdown', 'value'))(update_button_clicks)

app.callback(Output('dropdown', 'options'),
             Input('checkbox', 'value'))(update_transport_options)

# Debug is False, hot-reloading is disabled
app.run_server(port=5001,host='0.0.0.0', debug=False)
