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
    
#-----------------------KPI 7 - SLA ----------------------
response = urlopen("https://g986b1d252d1c63-db2022.adb.eu-frankfurt-1.oraclecloudapps.com/ords/tip/kpisl/incvolsl/")
df7 = json.loads(response.read())['items']

sla_no=[]
sla_yes=[]
month_yes=[]
month_no=[]
organization_yes=[]
organization_no=[]
df_monthsla={'202101':0,'202102':0,'202103':0,'202104':0 }
df_monthslano={'202101':0,'202102':0,'202103':0,'202104':0 }

for element in df7:
    if element['resolution_time'] < 4:
        sla_yes.append(element['resolution_time'])
        month_yes.append(element['month'])
        organization_yes.append(element['assigned_organization'])
        df_monthsla[element['month']]=df_monthsla[element['month']]+1

    else:
        sla_no.append(element['resolution_time'])
        month_no.append(element['month'])
        organization_no.append(element['assigned_organization'])
        df_monthslano[element['month']]=df_monthsla[element['month']]+1

df_slayes = pd.DataFrame({'Months': month_yes, 'Data': sla_yes, 'Organization': organization_yes})
df_slano = pd.DataFrame({'Months': month_no, 'Data': sla_no, 'Organization': organization_no})

keys=df_monthsla.keys()
values=df_monthsla.values()
values_org=df_monthsla.values()
slas = pd.DataFrame({'Months': keys, 'Data': values})

keys2=df_monthslano.keys()
values2=df_monthslano.values()
slasno = pd.DataFrame({'Months': keys2, 'Data': values2})



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
    return html.Div(children=[
        html.H1(children="SLA"),
         dcc.Graph(
                id="Priority by share",
                figure=px.bar(slas, x="Months", y="Data", title="SLA meeting the requirements by month")),
        dcc.Graph(
                id="Priority by share",
                figure=px.bar(slasno, x="Months", y="Data", title="SLA NOT meeting the requirements by month"))
                
        
    ]
        )



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
        
        if 'btnclosed' in changed_id:
            return closed_content()
        elif 'btnsla' in changed_id:
            return sla_content()
        else:
            return overview_content()
    

    for view_function in dash_app.server.view_functions:
        if view_function.startswith(dash_app.config.url_base_pathname):
            dash_app.server.view_functions[view_function] = login_required(
                dash_app.server.view_functions[view_function]
            )

    return dash_app
