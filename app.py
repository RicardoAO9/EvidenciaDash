import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash
from dash import dcc
from dash import html
import os
import plotly.offline as pyo
from siniestros import *

app = dash.Dash()

app.layout = html.Div([
    html.H1("EVIDENCIA 4", style={'background':'#dad7cd','textAlign':'center','color':'#3D59AB'}),
    html.Hr,
    html.H3("Paloma Pardo"),
    html.H3("Omar Spíndola"),
    html.H3("Martín Guzmán"),
    html.H3("Santiago Peña"),
    html.H3("Ricardo Álvarez"),
    html.P("A continuación presentaremos la evidencia 4 del equipo 3 de CCM."),
    dcc.Tabs([
        dcc.Tab(label="Con Principales Coberturas", children=[ 
            dcc.Graph(id="bar1", figure=bar1())]),
        dcc.Tab(label="Sin Principales Coberturas", children=[
            dcc.Graph(id="bar01", figure=bar01())]),
    ]),
    dcc.Tabs([
        dcc.Tab(label="Con Principales Coberturas", children=[
            dcc.Graph(id="bar2", figure=bar2())]),
        dcc.Tab(label="Sin Principales Coberturas", children=[
            dcc.Graph(id="bar02", figure=bar02())]),
    ]),
    html.P("Hola")
],style={'color':'#34495E','font-family':'Helvetica','marginBottom': 50, 'marginTop': 25, 'marginLeft': 25, 'marginRight': 25})

if __name__ == '__main__':
    app.run_server()