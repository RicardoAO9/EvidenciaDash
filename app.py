import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash
from dash import dcc
from dash import html, Output, Input
import dash_bootstrap_components as dbc
import os
import plotly.offline as pyo
from siniestros import *
from dataframe3 import *

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

############################################## SINIESTROS ##############################################

#CartaIntro
siniestros_intro = dbc.Col(
    html.Div([
        html.H2("Siniestros", className="display-3", style={'textAlign':'center'}),
        html.Hr(className="my-2"),
        html.P("Certificados a nivel cobertura que hayan realizado una reclamación o presentado un movimiento."),
    ],className="h-100 p-5 text-white rounded-3", style={'background':'#000080'}),
    md=4,
)

montos_genero = dbc.Col(
    html.Div([
        dcc.Graph(id="bar1", figure=bar1())
        ],className="h-100 p-0",),
    md=8,
)

jumbotron_sin = dbc.Row(
    [siniestros_intro, montos_genero],
    className="align-items-md-center",
)

#Siniestros coberturas
unsin = mo_gen.index.unique()

@app.callback(
    Output('bar2', 'figure'),
    Input('check1', 'value'))
def update_graph1(value):
    unsinl=list(unsin)
    valuel=list(value)
    list1 = list(set(unsinl) - set(valuel))
    df = mo_gen1.drop(list1, axis=0)
    df.reset_index(inplace=True)
    fig = go.Figure(data=[
    go.Bar(name="Monto Reclamado", x=df["COBERTURA"], y=df['MONTO_RECLAMADO'], marker_color="#4682B4"),
    go.Bar(name="Monto Pagado", x=df["COBERTURA"], y=df['MONTO_PAGADO'], marker_color="#3D59AB")
    ])
    fig.update_layout(
      title='Montos reclamados y pagados por cobertura',
      yaxis=dict(
        title='Pesos mexicanos',
        ),
      font=dict(
        family="Arial"
        ),
      )
    return fig

@app.callback(
    Output('bar3', 'figure'),
    Input('check2', 'value'))
def update_graph2(value):
    unsinl=list(unsin)
    valuel=list(value)
    list1 = list(set(unsinl) - set(valuel))
    df = mo_gen2.drop(list1, axis=0)
    df.reset_index(inplace=True)
    fig = go.Figure(data=[
    go.Bar(name="Diferencia en montos", x=df["COBERTURA"], y=df['DIFERENCIA_EN_MONTOS'], marker_color="#000080"),
    ])
    fig.update_layout(
      title='Diferencia en montos por cobertura',
      yaxis=dict(
        title='Pesos mexicanos',
        ),
      font=dict(
        family="Arial"
        ),
      )
    return fig

#Siniestros entidades
unsin2 = dfsin['ENTIDAD'].unique()
unsin2.sort()

@app.callback(
    Output('sca1', 'figure'),
    Input('drop1', 'value'))
def update_graph3(value):
    df = dfsin[dfsin["ENTIDAD"]==value]
    fig = px.scatter(df, x="MONTO PAGADO", y="MONTO RECLAMADO", color="SEXO", color_discrete_sequence=["#AB4F6B","#3D59AB"],
                     title="Montos pagados y reclamados de {}".format(value))
    fig.update_layout(
        font=dict(
        family="Arial"
        ),
    )
    return fig

############################################## EMISION ##############################################

#CartaIntro
emision_intro = dbc.Col(
    html.Div([
        html.H2("Emision", className="display-3", style={'textAlign':'center'}),
        html.Hr(className="my-2"),
        html.P("Emisión de certificados a nivel cobertura"),
    ],className="h-100 p-5 text-white rounded-3", style={'background':'#80120D'}),
    md=4,
)

graficaemi = dbc.Col(
    html.Div([
        dcc.Graph(id="fig9", figure=fig9()),
        ],className="h-100 p-0",),
    md=8,
)

jumbotron_emi = dbc.Row(
    [graficaemi, emision_intro,],
    className="align-items-md-center",
)

#
unemi=emi_fv.index.unique(level=0)

@app.callback(
    Output('bar4', 'figure'),
    Input('check3', 'value'))
def update_graph4(value):
    unemil=list(unemi)
    valuel=list(value)
    list1 = list(set(unemil) - set(valuel))
    df = emi_fv.drop(list1, axis=0)
    df.reset_index(inplace=True)
    fig = px.bar(df, x='FORMA DE VENTA', y='NUMERO DE ASEGURADOS', color='SEXO', 
                 color_discrete_sequence=["#3D59AB","#AB4F6B"], barmode='group', 
                 title='Numero de asegurados por forma de venta')
    return fig

############################################## COMISIONES ##############################################

#CartaIntro
comisiones_intro = dbc.Col(
    html.Div([
        html.H2("Comision", className="display-3", style={'textAlign':'center'}),
        html.Hr(className="my-2"),
        html.P("Datos de venta y de comision de certificados"),
    ],className="h-100 p-5 text-white rounded-3", style={'background':'#000080'}),
    md=4,
)

graficacom = dbc.Col(
    html.Div([
        dcc.Graph(id="fig12", figure=fig12()),
        ],className="h-100 p-0",),
    md=8,
)

jumbotron_com = dbc.Row(
    [comisiones_intro, graficacom],
    className="align-items-md-center",
)

#
uncom=com_mp.index.unique(level=0)

@app.callback(
    Output('bar5', 'figure'),
    Input('check4', 'value'))
def update_graph5(value):
    uncoml=list(uncom)
    valuel=list(value)
    list1 = list(set(uncoml) - set(valuel))
    df = com_mp.drop(list1, axis=0)
    df.reset_index(inplace=True)
    fig = px.bar(df, x='MODALIDAD DE LA POLIZA', y='NUMERO DE ASEGURADOS', color='SEXO', 
                 color_discrete_sequence=["#3D59AB","#AB4F6B"], barmode='group', 
                 title='Numero de asegurados por modalidad de poliza')
    return fig

############################################### ENTIDADES ###############################################

unent=dfent.columns.drop(['ï»¿CLAVE_INS', 'TIPO DE INSTITUCION', 'FECHA DE CORTE', 'RAMO',
       'ENTIDAD', 'AÃ‘O'])

@app.callback(
    Output('lin1', 'figure'),
    Input('drop2', 'value'))
def update_graph3(value):   
    df=dfent.drop(['ï»¿CLAVE_INS','TIPO DE INSTITUCION', 'RAMO','ENTIDAD', 'AÃ‘O'], axis=1)
    df['FECHA DE CORTE'] = pd.to_datetime(df['FECHA DE CORTE'],dayfirst=True)
    df=df.groupby(['FECHA DE CORTE']).sum()
    df=df.reset_index()
    df.sort_values(by="FECHA DE CORTE", inplace=True)
    fig = px.line(df, x="FECHA DE CORTE", y=value, title='Histórico de {}'.format(value), markers=True)
    fig.update_traces(line_color='#80120D')
    fig.update_layout(
        font=dict(
        family="Arial"
        ),
    )   
    return fig

#CartaIntro
entidades_intro = dbc.Col(
    html.Div([
        html.H2("Entidades", className="display-3", style={'textAlign':'center'}),
        html.Hr(className="my-2"),
        html.P("Ors_entidades: base de operación, ramo o seguro con datos de series de tiempo."),
    ],className="h-100 p-5 text-white rounded-3", style={'background':'#80120D'}),
    md=4,
)

graficaent = dbc.Col(
    html.Div([
        dcc.Graph(id="fig24", figure=fig24()),
        ],className="h-100 p-0",),
    md=8,
)

jumbotron_ent = dbc.Row(
    [graficaent, entidades_intro,],
    className="align-items-md-center",
)

############################################# PROYECCIONES ##############################################



################################################# APP ###################################################

app.layout = html.Div([
    html.H1("Dashboard Equipo 3 CCM", id="start", style={'textAlign':'center','color':'#000080'}),
    html.Hr(),
    dbc.Nav([
        dbc.NavItem(dbc.NavLink("Siniestros", href="#siniestros", active=True, external_link=True, style={'background':'#000080'})),
        dbc.NavItem(dbc.NavLink("Emision", href="#emision", active=True, external_link=True, style={'background':'#80120D'})),
        dbc.NavItem(dbc.NavLink("Comisiones", href="#comisiones", active=True, external_link=True, style={'background':'#000080'})),
        dbc.NavItem(dbc.NavLink("Entidades", href="#entidades", active=True, external_link=True, style={'background':'#80120D'})),
        dbc.NavItem(dbc.NavLink("Proyecciones", href="#", active=True, external_link=True, style={'background':'#000080'})),                
    ],pills=True, justified=True, class_name="mx-2"),

    html.Hr(id="siniestros",className="ty-3"),
    jumbotron_sin,
    dcc.Checklist(unsin, unsin, id='check1', inline=True),
    dcc.Graph(id="bar2"),
    dcc.Checklist(unsin, unsin, id='check2', inline=True),
    dcc.Graph(id="bar3"),    
    dcc.Dropdown(unsin2, 'Ciudad de México', id='drop1'),
    dcc.Graph(id='sca1'),
    dcc.Graph(id="his1", figure=his1()),
    dcc.Graph(id="pie1", figure=pie1()),

    html.Hr(id="emision",className="my-4"),
    jumbotron_emi,
    dcc.Checklist(unemi, unemi, id='check3', inline=True),
    dcc.Graph(id="bar4"),

    html.Hr(id="comisiones",className="my-4"),
    jumbotron_com,
    dcc.Checklist(uncom, uncom, id='check4', inline=True),
    dcc.Graph(id="bar5"),

    html.Hr(id="entidades",className="my-4"),
    jumbotron_ent,
    dcc.Dropdown(unent, 'PRIMA EMITIDA', id='drop2'),
    dcc.Graph(id="lin1"),

],style={'color':'#34495E','font-family':'Helvetica','marginBottom': 50, 'marginTop': 25, 'marginLeft': 25, 'marginRight': 25})

if __name__ == '__main__':
    app.run_server()