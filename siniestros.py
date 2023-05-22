import pandas as pd
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html
import os
import plotly.offline as pyo

dfsin = pd.read_csv('downloads/Siniestros.csv',encoding='cp1252', sep=',', on_bad_lines='warn')

def obj_flt(df,col):
  df[col] = pd.to_numeric(df[col].replace('[^0-9\.-]','',regex=True), downcast='float')

sin_num=['EDAD','NUMERO DE SINIESTROS','MONTO RECLAMADO','VENCIMIENTOS','MONTO PAGADO',
         'MONTO DE REASEGURO']
for x in sin_num:
  obj_flt(dfsin,x)

dfsin.dropna(inplace=True)


si_montos=dfsin.drop(['CLAVE_INS', 'EDAD', 'SEXO', 'CAUSA DEL SINIESTRO', 'PLAN DE LA POLIZA', 
                      'MODALIDAD DE LA POLIZA', 'NUMERO DE SINIESTROS', 'VENCIMIENTOS', 
                      'MONTO DE REASEGURO'],axis=1)
si_montos.columns = si_montos.columns.map(lambda x: x.replace(' ', '_'))
si_montos["DIFERENCIA_EN_MONTOS"]=si_montos.eval("MONTO_RECLAMADO-MONTO_PAGADO")

mo_gen=si_montos.groupby(["COBERTURA"]).sum()
mo_gen.head()

mo_gen1=mo_gen.drop(["DIFERENCIA_EN_MONTOS"],axis=1)
mo_gen2=mo_gen.drop(["MONTO_RECLAMADO","MONTO_PAGADO"],axis=1)


fig2 = go.Figure(data=[
  go.Bar(name="Monto Reclamado", x=mo_gen1.index, y=mo_gen1['MONTO_RECLAMADO']),
  go.Bar(name="Monto Pagado", x=mo_gen1.index, y=mo_gen1['MONTO_PAGADO'])
  ])
pyo.plot(fig2,filename="BAR1.html")