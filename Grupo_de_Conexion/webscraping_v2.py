import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# Funcion encargada del WebScraping y el Preprocesamiento de la data
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
        df_final = df_pivot.round(2).reset_index()

        # Convertir los datos al formato requerido
        # Definir los encabezados manualmente (para las 18 columnas restantes)
        headers = [2000, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]

        # Verificar que el número de columnas coincida con los encabezados
        if df_final.shape[1] == len(headers):
            df_final.columns = headers
        else:
            print("El número de columnas en el DataFrame no coincide con la cantidad de encabezados proporcionados.")

        # Agregar las dos nuevas columnas al lado izquierdo
        df_final.insert(0, 'Departamento', '')
        df_final.insert(1, 'Indicador Anemia %', '')

        # Lista de departamentos
        departamentos = [
            "AMAZONAS", "ÁNCASH", "APURÍMAC", "AREQUIPA", "AYACUCHO", "CAJAMARCA", 
            "CALLAO", "CUSCO", "HUANCAVELICA", "HUÁNUCO", "ICA", "JUNÍN", 
            "LA LIBERTAD", "LAMBAYEQUE", "LIMA", "LORETO", "MADRE DE DIOS", "MOQUEGUA", 
            "PASCO", "PIURA", "PUNO", "SAN MARTÍN", "TACNA", "TUMBES", 
            "UCAYALI", "LIMA METROPOLITANA 1/", "LIMA 2/"
        ]

        # Asignar nombres de departamentos
        row_idx = 0
        for departamento in departamentos:
            if departamento == "LIMA METROPOLITANA 1/":
                # Excepción para "LIMA METROPOLITANA 1/"
                df_final.loc[row_idx:row_idx+2, 'Departamento'] = departamento
                row_idx += 3
            else:
                df_final.loc[row_idx:row_idx+3, 'Departamento'] = departamento
                row_idx += 4

        # Llenar la columna 'Indicador Anemia %' con el patrón, omitiendo "Severa" para Lima Metropolitana
        indicadores = ["Leve", "Moderada", "Severa", "Total"]
        indicator_idx = 0

        for idx in range(df_final.shape[0]):
            if df_final.at[idx, 'Departamento'] == "LIMA METROPOLITANA 1/" and indicator_idx == 2:
                # Saltar "Severa" para Lima Metropolitana
                indicator_idx += 1
            df_final.at[idx, 'Indicador Anemia %'] = indicadores[indicator_idx]
            indicator_idx = (indicator_idx + 1) % 4  # Reiniciar el patrón cada 4 indicadores

        # Reemplazar los NaN con el promedio de los valores numéricos en la misma fila
        for col in df_final.columns[2:]:  
            df_final[col] = df_final[col].astype(str).replace('-', np.nan).str.replace(',', '.')
            df_final[col] = pd.to_numeric(df_final[col], errors='coerce') 

        df_final.iloc[:, 2:] = df_final.iloc[:, 2:].apply(
            lambda row: row.fillna(row.mean()), axis=1
        )

        # (Opcional) Volver a formatear los números con comas como separador decimal
        for col in df_final.columns[2:]:
            df_final[col] = df_final[col].apply(lambda x: f"{x:.1f}".replace('.', ','))

        # Lista de las columnas de los años (como está en tu código)
        year_columns = [2000, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]

        # Convertir los valores a float correctamente, reemplazando comas por puntos
        for year in year_columns:
            df_final[year] = df_final[year].str.replace(',', '.').astype(float)

        # Iterar sobre los departamentos
        for depto in df_final['Departamento'].unique():
            # Filtrar las filas correspondientes a 'Leve', 'Moderada', 'Severa' para este departamento
            rows_to_sum = df_final[(df_final['Departamento'] == depto) & (df_final['Indicador Anemia %'].isin(['Leve', 'Moderada', 'Severa']))]

            # Filtrar la fila correspondiente a 'Total' para este departamento
            total_row_idx = df_final[(df_final['Departamento'] == depto) & (df_final['Indicador Anemia %'] == 'Total')].index

            if not rows_to_sum.empty and not total_row_idx.empty:
                # Iterar sobre las columnas de los años
                for year in year_columns:
                    # Sumar los valores de los indicadores 'Leve', 'Moderada', 'Severa' para el año en cuestión
                    total_value = rows_to_sum[year].sum(skipna=True)
                    
                    # Asignar la suma total al año correspondiente en la fila 'Total'
                    df_final.at[total_row_idx[0], year] = total_value
        
        return df_final
    else:
        raise Exception(f"Error en la solicitud: {response.status_code}")