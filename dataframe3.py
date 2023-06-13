import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import plotly.offline as pyo
import numpy as np

#LIMPIEZA
dfemi = pd.read_csv('downloads/Emision.csv',encoding='cp1252', sep=',', on_bad_lines='warn')
dfcom = pd.read_csv('downloads/Comisiones.csv',encoding='cp1252', sep=',', on_bad_lines='warn')
dfent = pd.read_csv('downloads/Ors_entidad.csv',encoding='cp1252', sep=',', on_bad_lines='warn')

def obj_flt(df,col):
  df[col] = pd.to_numeric(df[col].replace('[^0-9\.-]','',regex=True), downcast='float')
def obj_int(df,col):
  df[col] = pd.to_numeric(df[col].replace('[^0-9\.-]','',regex=True), downcast='integer')
def limp(df):
  df.replace('No disponible ', np.NaN, inplace=True)
  df.replace('No disponible', np.NaN, inplace=True)
  df.dropna(inplace=True)

dfemi.rename(columns={"ENTIDAD ":"ENTIDAD"}, inplace=True)
limp(dfemi)
emi_num = ['PRIMA EMITIDA', 'SUMA ASEGURADA']
emi_int = ['EDAD', 'NUMERO DE ASEGURADOS']
for x in emi_num:
  obj_flt(dfemi,x)
for x in emi_int:
  obj_int(dfemi,x)
dfemi.dropna(inplace=True)

limp(dfcom)
com_num = ['PRIMA CEDIDA', 'COMISIONES DIRECTAS', 'FONDO DE INVERSIÓN', 'FONDO DE ADMINISTRACION', 
         'MONTO DE DIVIDENDOS', 'MONTO DE RESCATE']
com_int = ['EDAD','NUMERO DE ASEGURADOS']
for x in com_num:
  obj_flt(dfcom,x)
for x in com_int:
  obj_int(dfcom,x)
dfcom.dropna(inplace=True)

limp(dfent)
ent_num=['NUMERO DE SINIESTROS / RECLAMACIONES','PRIMA EMITIDA',	'COMISION DIRECTA','SUMA ASEGURADA',
         'MONTO DE SINIESTRALIDAD','MONTO DE VENCIMIENTOS','MONTO DE RESCATE','AJUSTE DE GASTOS',
         'MONTO DE DIVIDENDOS','MONTO DE SALVAMENTO','MONTO RECUPERADO']
ent_int=['NUMERO DE POLIZAS VIGENTES',	'RIESGOS ASEGURAADOS', 'RIESGOS ASEGURADOS VIGENTES',
         'NUMERO DE SINIESTROS / RECLAMACIONES','AÃ‘O']
for x in ent_num:
  obj_flt(dfent,x)
for x in ent_int:
  obj_int(dfent,x)
dfent.dropna(inplace=True)

############################################## EMISION ##############################################

emi_fv=dfemi.drop(['CLAVE_INS', 'EDAD', 'PLAN DE LA POLIZA','COBERTURA', 'MONEDA', 'ENTIDAD',  
       'PRIMA EMITIDA','SUMA ASEGURADA', 'MODALIDAD DE LA POLIZA',], axis=1)
emi_fv=emi_fv.groupby(['FORMA DE VENTA','SEXO']).sum()
emi_fv=emi_fv.sort_values(by='NUMERO DE ASEGURADOS', ascending=False)

def fig9():
    fig = px.pie(dfemi, names='SEXO', color_discrete_sequence=["#3D59AB","#AB4F6B"], title='Distribución de Género de Asegurados')
    return fig

############################################## COMISIONES ##############################################

com_mp=dfcom.drop(['CLAVE_INS', 'EDAD', 'PLAN DE LA POLIZA', 'MONEDA', 'ENTIDAD ', 'FORMA DE VENTA',
   'TIPO DIVIDENDO', 'PRIMA CEDIDA', 'COMISIONES DIRECTAS', 'FONDO DE INVERSIÓN',
   'FONDO DE ADMINISTRACION', 'MONTO DE DIVIDENDOS', 'MONTO DE RESCATE'], axis=1)
com_mp=com_mp.groupby(['MODALIDAD DE LA POLIZA','SEXO']).sum()
com_mp=com_mp.sort_values(by='NUMERO DE ASEGURADOS', ascending=False)

def fig12():
    fig = px.pie(dfcom, names='SEXO', color_discrete_sequence=["#3D59AB","#AB4F6B"], title='Distribución de Género de Asegurados')
    return fig

############################################### ENTIDADES ###############################################

def fig24():
    dfent2=dfent.drop(['ï»¿CLAVE_INS','TIPO DE INSTITUCION','FECHA DE CORTE','RAMO',
                        'ENTIDAD','RIESGOS ASEGURAADOS',
                        'RIESGOS ASEGURADOS VIGENTES', 'NUMERO DE SINIESTROS / RECLAMACIONES', "PRIMA EMITIDA",
                        'COMISION DIRECTA', 'SUMA ASEGURADA','MONTO DE SINIESTRALIDAD',
                        'MONTO DE VENCIMIENTOS', 'MONTO DE RESCATE','AJUSTE DE GASTOS','MONTO DE DIVIDENDOS',
                        'MONTO DE SALVAMENTO','MONTO RECUPERADO'], axis=1)
    dfent2=dfent2.groupby('AÃ‘O')['NUMERO DE POLIZAS VIGENTES'].sum()
    dfent2=dfent2.reset_index()
    dfent2.sort_values(by='AÃ‘O',inplace=True)
    fig = px.bar(dfent2, x='AÃ‘O', y='NUMERO DE POLIZAS VIGENTES', title='Numero de polizas vigentes por año')
    fig.update_traces(marker_color='#80120D')
    fig.update_layout(
        font=dict(
        family="Arial"
        ),
    )    
    return fig