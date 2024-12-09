import requests
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc



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
else:
    print(f"Error en la solicitud: {response.status_code}")


df_pivot = df.pivot_table(index=['ubigeo', 'departamento', 'indicador'], columns='año', values='dato', aggfunc='first')

df_pivot = df_pivot.replace({',': '.'}, regex=True)  # Elimina las comas

df_pivot = df_pivot.apply(pd.to_numeric, errors='coerce')
df_pivot = df_pivot.apply(lambda row: row.fillna(row.mean()), axis=1)
df = df_pivot.round(2)

print(df.head(20))



df_reset = df.reset_index()

# Crear las opciones para el menú desplegable
departamentos = df_reset['departamento'].unique()
options_departamentos = [{'label': dept, 'value': dept} for dept in departamentos]

# Crear las opciones para los años
anios = df_reset.columns[3:]  # Los años están en las columnas después del índice
options_anios = [{'label': anio, 'value': anio} for anio in anios]

# Crear la aplicación Dash
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Proporción de Anemia Infantil"),
    dcc.Dropdown(
        id='dropdown-departamento',
        options=options_departamentos,
        placeholder="Seleccione un departamento",
    ),
    dcc.Dropdown(
        id='dropdown-anio',
        options=options_anios,
        placeholder="Seleccione un año",
    ),
    dcc.Graph(id='anemia-graph')
])

@app.callback(
    Output('anemia-graph', 'figure'),
    [Input('dropdown-departamento', 'value'),
     Input('dropdown-anio', 'value')]
)
def update_graph(selected_departamento, selected_anio):
    if not selected_departamento or not selected_anio:
        return px.bar(title="Seleccione un departamento y un año para ver el gráfico")
    
    # Filtrar datos por departamento
    df_filtered = df_reset[df_reset['departamento'] == selected_departamento]
    
    # Seleccionar los datos del año elegido
    df_plot = df_filtered[['indicador', selected_anio]].rename(columns={selected_anio: 'dato'})
    
    # Crear el gráfico
    fig = px.bar(
        df_plot,
        x='indicador',
        y='dato',
        title=f"Proporción de Anemia en {selected_departamento} durante {selected_anio}",
        labels={'dato': 'Porcentaje', 'indicador': 'Indicador'},
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)


