import requests
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc


def obtener_datos_anemia():
    # URL de la API
    url = "https://systems.inei.gob.pe/SIRTOD/app/consulta/getTableDataYear?indicador_listado=394568%2C394565%2C394567%2C394563&tipo_ubigeo=1&desde_anio=2000&hasta_anio=2023&ubigeo_listado=&idioma=ES"

    # Realizar la solicitud GET
    response = requests.get(url)

    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        data = response.json()  # Obtener los datos en formato JSON

        # Convertir los datos a un DataFrame de pandas
        df = pd.DataFrame(data)
        
        # Mostrar el DataFrame completo
        df['año'] = df['año'].astype(int)

        df_pivot = df.pivot_table(index=['ubigeo', 'departamento', 'indicador'], columns='año', values='dato', aggfunc='first')

        df_pivot = df_pivot.replace({',': '.'}, regex=True)  # Elimina las comas

        df_pivot = df_pivot.apply(pd.to_numeric, errors='coerce')
        df_pivot = df_pivot.apply(lambda row: row.fillna(row.mean()), axis=1)
        df_final = df_pivot.round(2).reser_index()

        return df_final
    else:
        raise Exception(f"Error en la solicitud: {response.status_code}")
