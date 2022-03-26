import dash
import dash_core_components as dcc
import dash_html_components as html
from flask_login.utils import login_required
import plotly.express as px
import pandas as pd
from urllib import response
from urllib.request import urlopen
from urllib import response
from email.utils import decode_rfc2231
import json
from datetime import datetime
from dash import Dash, html, Input, Output, callback_context, State
from dash.exceptions import PreventUpdate

options=["January", "February", "April", "March"]


def overview_content():
    return html.Div(
        children=[
            html.H1(children="Overview"),
            html.Div(children=html.H1(children="KPI1")),
            dcc.Graph(
                id="kpi1-graph",
                figure=px.bar(df1, x="month", y="incidences_number", color="priority", barmode="group"),
            ),
            dcc.Graph(
                id="kpi1-graph",
                figure=px.bar(df1, x="month", y="incidences_number", barmode="group"),
            ),
        ]
    )

 
response = urlopen("https://ge81ee28f924217-db202201141801.adb.eu-amsterdam-1.oraclecloudapps.com/ords/tip/kpi1/incvol/")
df1 = json.loads(response.read())['items']

for element in df1:
    if element['month'] == '202101':
        element['month'] ='January'
    elif element['month'] == '202102':
        element['month'] ='February'
    elif element['month'] == '202103':
        element['month'] ='March'
    elif element['month'] == '202104':
        element['month'] ='April'

def sla_content():
    return html.Div(children=html.H1(children="SLA"))



def create_dash_application(flask_app):
    dash_app = dash.Dash(server=flask_app, name="dash", url_base_pathname="/dash/")
    dash_app.layout = html.Div([
        html.Div([
        html.H2("Iberia KPIs"),
        html.Img(src="/iberialogo.png")
        ], className="banner"),
    html.Div([
    html.Button('Overview', id='btnoverview', n_clicks=0),
    html.Button('SLA', id='btnsla', n_clicks=0),
    dcc.Dropdown(options, id='multi-variable',multi=True ),
    html.Div(id='container-button')
    ])])
    
    @dash_app.callback(
        Output('container-button','children'),
        Input('btnoverview','n_clicks'),
        Input('btnsla', 'n_clicks')
        )
    def showing(btn1,btn2):
        changed_id = [p['prop_id'] for p in callback_context.triggered][0]
        if 'btnoverview' in changed_id:
            return overview_content()
        elif 'btnsla' in changed_id:
            return html.Div(children="vaale")
        else:
            return html.Div(children="holaaa")
            
    @dash_app.callback(
        Output("multi-variable", "options"),
        Input("multi-variable", "search_value"),
        State("multi-variable", "value")
    )
    def update_multi_options(search_value, value):
        if not search_value:
            raise PreventUpdate
        # Make sure that the set values are in the option list, else they will disappear
        # from the shown select list, but still part of the `value`.
        variab= [
            o for o in options if search_value in o["label"] or o["value"] in (value or [])
        ]
        return "don"



    
    

    for view_function in dash_app.server.view_functions:
        if view_function.startswith(dash_app.config.url_base_pathname):
            dash_app.server.view_functions[view_function] = login_required(
                dash_app.server.view_functions[view_function]
            )

    return dash_app
