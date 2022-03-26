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

options=["All", "January", "February", "April", "March"]



 #-----------------------KPI 1 - Number of incidents raised by month -----------------------------------
response = urlopen("https://g986b1d252d1c63-db2022.adb.eu-frankfurt-1.oraclecloudapps.com/ords/tip/kpi1/incvol/")
df1 = json.loads(response.read())['items']
#Tranforming the month apperance
for element in df1:
    if element['month'] == '202101':
        element['month'] ='January'
    elif element['month'] == '202102':
        element['month'] ='February'
    elif element['month'] == '202103':
        element['month'] ='March'
    elif element['month'] == '202104':
        element['month'] ='April'

 #-----------------------KPI 2 - Number of incidents raised by priority ----------------------------
response = urlopen("https://g986b1d252d1c63-db2022.adb.eu-frankfurt-1.oraclecloudapps.com/ords/tip/kpi20/incvol20/")
data2 = json.loads(response.read())['items']
df2={}
for element in data2:
    if element['priority']== "Crítica":
        df2["Crítica"]=element['incidences_number']
    elif element['priority']== "Alta":
        df2["Alta"]=element['incidences_number']
    elif element['priority']== "Media":
        df2["Media"]=element['incidences_number']
    elif element['priority']== "Baja":
        df2["Baja"]=element['incidences_number']


 #-----------------------KPI 3 - Number of incidents raised by assigned orgnaization ----------------------
response = urlopen("https://g986b1d252d1c63-db2022.adb.eu-frankfurt-1.oraclecloudapps.com/ords/tip/kpi21/incvol21/")
df3 = json.loads(response.read())['items']
    

 #-----------------------KPI 4 - Number of incidents closed by priority --------------------------
response = urlopen("https://g986b1d252d1c63-db2022.adb.eu-frankfurt-1.oraclecloudapps.com/ords/tip/kpi22/incvol22/")
data4 = json.loads(response.read())['items']
df4={}
for element in data4:
    if element['priority']== "Crítica":
        df4["Crítica"]=element['numberofincidents']
    elif element['priority']== "Alta":
        df4["Alta"]=element['numberofincidents']
    elif element['priority']== "Media":
        df4["Media"]=element['numberofincidents']
    elif element['priority']== "Baja":
        df4["Baja"]=element['numberofincidents']


 #-----------------------KPI 5- Number of incidents closed by month ----------------------
response = urlopen("https://g986b1d252d1c63-db2022.adb.eu-frankfurt-1.oraclecloudapps.com/ords/tip/kpi23/incvol23/")
df5 = json.loads(response.read())['items']

#Tranforming the month apperance
for element in df5:
    if element['month'] == '202101':
        element['month'] ='January'
    elif element['month'] == '202102':
        element['month'] ='February'
    elif element['month'] == '202103':
        element['month'] ='March'
    elif element['month'] == '202104':
        element['month'] ='April'

#-----------------------KPI 6 - Number of incidents closed  by assigned orgnaization ----------------------
response = urlopen("https://g986b1d252d1c63-db2022.adb.eu-frankfurt-1.oraclecloudapps.com/ords/tip/kpi24/incvol24/")
df6 = json.loads(response.read())['items']
    
#-----------------------KPI 6 - Number of incidents closed  by assigned orgnaization ----------------------
#response = urlopen("https://g986b1d252d1c63-db2022.adb.eu-frankfurt-1.oraclecloudapps.com/ords/tip/kpisl/incvolsl/")
#df6 = json.loads(response.read())['items']
    

 #--------------------------------------------------------------------------------------------

def overview_content():
    return html.Div(
        children=[
            html.H1("Raised incidents"),
            html.Div(children=[
                html.Div(children="Number of incidents by priority", className='tittleboxes'),
                html.Div(children=[
                    html.P(children='Critics'),
                    html.H4(children=df2["Crítica"])
                    ],  className='tittleboxes'),
                    html.Div(children=[
                    html.P(children='High'),
                    html.H4(children=df2["Alta"])
                    ],  className='tittleboxes'),
                    html.Div(children=[
                    html.P(children='Medium'),
                    html.H4(children=df2["Media"])
                    ],  className='tittleboxes'),
                    html.Div(children=[
                    html.P(children='Low'),
                    html.H4(children=df2["Baja"])
                    ],  className='tittleboxes')
                    
            ], className = "boxes"),
            
            dcc.Graph(
                id="kpi1-graph",
                figure=px.bar(df1, x="month", y="incidences_number", color="priority", barmode="group",title="Total number of incidents raised per month"),
            ),
            dcc.Graph(
                id="Priority by share",
                figure=px.pie(df3, values="numberincidents", names="assigned_organization", title="Total number of incidents per assigned organization"))
        ]
    )

def closed_content():
    return html.Div(
        children=[
            html.H1("Closed incidents"),
            html.Div(children=[
                html.Div(children="Number of incidents by priority", className='tittleboxes'),
                html.Div(children=[
                    html.P(children='Critics'),
                    html.H4(children=df4["Crítica"])
                    ],  className='tittleboxes'),
                    html.Div(children=[
                    html.P(children='High'),
                    html.H4(children=df4["Alta"])
                    ],  className='tittleboxes'),
                    html.Div(children=[
                    html.P(children='Medium'),
                    html.H4(children=df4["Media"])
                    ],  className='tittleboxes'),
                    html.Div(children=[
                    html.P(children='Low'),
                    html.H4(children=df4["Baja"])
                    ],  className='tittleboxes')
                    
            ], className = "boxes"),
            
            dcc.Graph(
                id="kpi1-graph",
                figure=px.bar(df5, x="month", y="incidences_number", color="priority", barmode="group",title="Total number of incidents closed per month"),
            ),
            dcc.Graph(
                id="Priority by share",
                figure=px.pie(df6, values="numberincidents", names="assigned_organization", title="Total number of incidents per closed organization"))
        ]
    )

def sla_content():
    return html.Div(children=html.H1(children="SLA"))



def create_dash_application(flask_app):
    dash_app = dash.Dash(server=flask_app, name="__name__", url_base_pathname="/dash/")
    dash_app.layout = html.Div([
        html.Div([
        html.H2("Iberia KPIs"),
        ], className="banner"),
    html.Div([
    html.Button('Raised incidents overview', id='btnoverview', n_clicks=0),
    html.Button('Closed incidents overview', id='btnclosed', n_clicks=0),
    html.Button('SLA', id='btnsla', n_clicks=0),
    html.Div(id='container-button')
    ])])
    
    @dash_app.callback(
        Output('container-button','children'),
        Input('btnoverview','n_clicks'),
        Input('btnclosed','n_clicks'),
        Input('btnsla', 'n_clicks')
        )
    def showing(btn1,btn2,btn3):
        changed_id = [p['prop_id'] for p in callback_context.triggered][0]
        if 'btnoverview' in changed_id:
            return overview_content()
        elif 'btnclosed' in changed_id:
            return closed_content()
        elif 'btnsla' in changed_id:
            return html.Div(children="vaale")
        else:
            return html.Div(children="holaaa")
    

    for view_function in dash_app.server.view_functions:
        if view_function.startswith(dash_app.config.url_base_pathname):
            dash_app.server.view_functions[view_function] = login_required(
                dash_app.server.view_functions[view_function]
            )

    return dash_app
