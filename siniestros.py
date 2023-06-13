import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import dash
from dash import dcc
from dash import html
import os
import plotly.offline as pyo
import requests

dfsin = pd.read_csv('downloads/Siniestros.csv',encoding='cp1252', sep=',', on_bad_lines='warn')

def obj_flt(df,col):
  df[col] = pd.to_numeric(df[col].replace('[^0-9\.-]','',regex=True), downcast='float')
def obj_int(df,col):
  df[col] = pd.to_numeric(df[col].replace('[^0-9\.-]','',regex=True), downcast='integer')

dfsin.replace('No disponible ', np.NaN, inplace=True)
dfsin.replace('No disponible', np.NaN, inplace=True)
dfsin['ENTIDAD'].replace('Sin domicilio fijo', np.NaN, inplace=True)
dfsin['ENTIDAD'].replace('No aplica', np.NaN, inplace=True)
dfsin['ENTIDAD'].replace('En el Extranjero', np.NaN, inplace=True)
dfsin.dropna(inplace=True)

sin_num=['MONTO RECLAMADO','VENCIMIENTOS','MONTO PAGADO','MONTO DE REASEGURO']
sin_int=['EDAD','NUMERO DE SINIESTROS']
for x in sin_num:
  obj_flt(dfsin,x)
for x in sin_int:
  obj_int(dfsin,x)
dfsin.dropna(inplace=True)

#COMPARACION DE MONTOS RECLAMADOS Y PAGADOS POR SEXO
si_montos_s=dfsin.drop(['CLAVE_INS', 'EDAD', 'CAUSA DEL SINIESTRO', 'PLAN DE LA POLIZA', 
                      'MODALIDAD DE LA POLIZA', 'NUMERO DE SINIESTROS', 'VENCIMIENTOS', 
                      'MONTO DE REASEGURO', 'ENTIDAD', 'COBERTURA'],axis=1)
si_montos_s.columns = si_montos_s.columns.map(lambda x: x.replace(' ', '_'))
si_montos_s["DIFERENCIA_EN_MONTOS"]=si_montos_s.eval("MONTO_RECLAMADO-MONTO_PAGADO")
si_montos_s = si_montos_s[si_montos_s["MONTO_RECLAMADO"]>0]

mo_gen_s=si_montos_s.groupby(["SEXO"]).sum()
mo_gen_s.reset_index(inplace=True)

def bar1():
  color1=["#B559AA","#4682B4"]
  color2=["#AB4F6B","#3D59AB"]
  color3=["#80120D","#000080"]
  fig = go.Figure(data=[
   go.Bar(name="Monto Reclamado", x=mo_gen_s['SEXO'], y=mo_gen_s['MONTO_RECLAMADO'], marker_color=color1),
   go.Bar(name="Monto Pagado", x=mo_gen_s['SEXO'], y=mo_gen_s['MONTO_PAGADO'], marker_color=color2),
   go.Bar(name="Diferencia de Montos", x=mo_gen_s['SEXO'], y=mo_gen_s['DIFERENCIA_EN_MONTOS'], marker_color=color3)
   ])
  fig.update_layout(
    title='Montos reclamados, pagados y su diferencia, clasificado por sexo',
    yaxis=dict(title='Pesos mexicanos',),
    font=dict(family="Arial"),
    )
  return fig


#COMPARACION DE MONTOS RECLAMADOS Y PAGADOS POR COBERTURA
si_montos=dfsin.drop(['CLAVE_INS', 'EDAD', 'SEXO', 'CAUSA DEL SINIESTRO', 'PLAN DE LA POLIZA', 
                      'MODALIDAD DE LA POLIZA', 'NUMERO DE SINIESTROS', 'VENCIMIENTOS', 
                      'MONTO DE REASEGURO'],axis=1)
si_montos.columns = si_montos.columns.map(lambda x: x.replace(' ', '_'))
si_montos["DIFERENCIA_EN_MONTOS"]=si_montos.eval("MONTO_RECLAMADO-MONTO_PAGADO")
si_montos["SUMA_MONTOS"]=si_montos.eval("MONTO_RECLAMADO+MONTO_PAGADO")
si_montos = si_montos[si_montos["MONTO_RECLAMADO"]>0]

mo_gen=si_montos.groupby(["COBERTURA"]).sum()
mo_gen=mo_gen.sort_values(by="SUMA_MONTOS", ascending=False)
mo_gen=mo_gen.drop(["SUMA_MONTOS"],axis=1)

mo_gen1=mo_gen.drop(["DIFERENCIA_EN_MONTOS"],axis=1)
mo_gen2=mo_gen.drop(["MONTO_RECLAMADO","MONTO_PAGADO"],axis=1)

#Piramide poblacional de siniestros
def his1():
    hsin=dfsin.drop(['CLAVE_INS', 'COBERTURA', 'ENTIDAD', 'CAUSA DEL SINIESTRO', 'PLAN DE LA POLIZA', 
       'MODALIDAD DE LA POLIZA', 'NUMERO DE SINIESTROS', 'MONTO RECLAMADO', 'VENCIMIENTOS', 'MONTO PAGADO',
       'MONTO DE REASEGURO'], axis=1)
    hsinm=hsin[hsin["SEXO"]=='Masculino']
    hsinf=hsin[hsin["SEXO"]=='Femenino']
    hsinm=hsinm.groupby(["EDAD"]).count()
    hsinf=hsinf.groupby(["EDAD"]).count()
    hsinm.sort_values(by="EDAD",inplace=True)
    hsinf.sort_values(by="EDAD",inplace=True)
    hsinm.reset_index(inplace=True)
    hsinf.reset_index(inplace=True)
    binslst=[0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,105,110,115]
    binslab=['1-5','6-10','11-15','16-20','21-25','26-30','31-35','36-40','41-45','46-50','51-55','56-60',
             '61-65','66-70','71-75','76-80','81-85','86-90','91-95','96-100','101-105','106-110','111-115']
    hsinm["EDADB"]=pd.cut(x=hsinm["EDAD"],bins=binslst,labels=binslab)
    hsinf["EDADB"]=pd.cut(x=hsinf["EDAD"],bins=binslst,labels=binslab)
    hsinm=hsinm.groupby(["EDADB"]).sum()
    hsinf=hsinf.groupby(["EDADB"]).sum()
    hsinm['FEMENINO']=hsinf['SEXO']
    hsin_a=hsinm.drop(["EDAD"],axis=1)
    hsin_a.reset_index(inplace=True)
    hsin_a.rename(columns={"SEXO":"MASCULINO",'EDADB':'EDAD'}, inplace=True)
    mas=hsin_a["MASCULINO"]*-1
    fem=hsin_a["FEMENINO"]
    edad=hsin_a['EDAD']
    fig = go.Figure()
    fig.add_trace(go.Bar(y= edad, x = mas, name = 'Masculino', orientation = 'h', marker_color="#3D59AB"))
    fig.add_trace(go.Bar(y = edad, x = fem, name = 'Femenino', orientation = 'h', marker_color="#AB4F6B"))
    fig.update_layout(title = 'Piramide poblacional de siniestros', barmode = 'relative', bargap = 0.0, 
                      bargroupgap = 0, font=dict(family="Arial")
                      )
    return fig

G10r=list(reversed(px.colors.qualitative.G10))
def pie1():
    piesin=dfsin.groupby(["CAUSA DEL SINIESTRO"]).count()
    piesin.reset_index(inplace=True)
    piesin.sort_values(by="CLAVE_INS",inplace=True,ascending=False)
    piesin=piesin.head(15)
    fig = px.pie(piesin, values='NUMERO DE SINIESTROS', names='CAUSA DEL SINIESTRO', 
                 title='Top 15 causas de siniestros', color_discrete_sequence=G10r)
    fig.update_layout(
        font=dict(
        family="Arial"
        ),
    )    
    return fig