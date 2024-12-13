import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
from webscraping_v2 import obtener_datos_anemia

# Leer el archivo CSV
df = obtener_datos_anemia()

# Convertir los años a cadenas si es necesario e incluir el año 2000, pero excluir del 2001 al 2007
year_columns = ['2000'] + [str(year) for year in range(2008, 2023 + 1)]
valid_years = [year for year in year_columns if year != '2000']  # Años sin el 2000

# Filtrar el DataFrame para valores "Total"
df_total = df[df['Indicador Anemia %'] == 'Total']

# Normalizar los nombres de los departamentos (primera letra mayúscula)
lista_dptos = df_total['Departamento'].str.title()




# -----------------------------------------------------------------------------------------------------

## **Porcentaje de Anemia por Nivel y Departamento en el Año Seleccionado**
# Función para generar el gráfico y la interpretación
## Función para generar el gráfico de proporciones de anemia
def comparar_niveles_anemia(anio, departamento):
    # Filtrar datos por año y departamento
    df_anio = df[['Departamento', 'Indicador Anemia %', anio]]
    df_filtrado = df_anio[df_anio['Departamento'].str.title() == departamento.title()]  # Normalizar a título
    
    # Excluir la categoría 'Total'
    df_filtrado = df_filtrado[df_filtrado['Indicador Anemia %'] != 'Total']
    
    # Renombrar las columnas para claridad
    df_filtrado.columns = ['Departamento', 'Indicador', 'Proporción']
    
    # Calcular el porcentaje de "No tiene anemia"
    total_proporcion = df_filtrado['Proporción'].sum()
    no_anemia = 100 - total_proporcion  # Suponiendo que los porcentajes son sobre 100%
    
    # Crear un nuevo DataFrame para "No tiene anemia"
    df_no_anemia = pd.DataFrame({'Indicador': ['No tiene\nanemia'], 'Proporción': [no_anemia]})
    
    # Concatenar el DataFrame original con el nuevo DataFrame
    df_filtrado = pd.concat([df_filtrado, df_no_anemia], ignore_index=True)
    
    # Filtro para evitar considerar 'No tiene anemia' en el nivel más prevalente
    df_filtrado_sin_no_anemia = df_filtrado[df_filtrado['Indicador'] != 'No tiene\nanemia']
    
    # Verificar si hay al menos un nivel de anemia para no generar error
    if df_filtrado_sin_no_anemia.empty:
        return None, "No hay datos suficientes para generar la interpretación."
    
    # Obtener el nivel más prevalente y menos prevalente
    nivel_mayor = df_filtrado_sin_no_anemia.loc[df_filtrado_sin_no_anemia['Proporción'].idxmax()]
    nivel_menor = df_filtrado.loc[df_filtrado['Proporción'].idxmin()]
    
    interpretacion = f"""
    En el año {anio}, en el departamento de {departamento}:
    El nivel de anemia más prevalente fue '{nivel_mayor['Indicador']}' con una proporción de {nivel_mayor['Proporción']}%.
    El nivel de anemia menos prevalente fue '{nivel_menor['Indicador']}' con una proporción de {nivel_menor['Proporción']}%.
    """
    
    # Crear el gráfico circular
    plt.figure(figsize=(4, 4))  # Ajustar el tamaño de la figura
    plt.pie(df_filtrado['Proporción'], labels=df_filtrado['Indicador'], autopct='%1.1f%%', startangle=90, 
            colors=['#44a4f4', '#FFA07A', '#d475ee', '#a0df61'])  # Colores personalizados
    plt.axis('equal')  # Para que el gráfico sea un círculo
        
    # Guardar el gráfico en memoria y codificar en base64
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight', dpi=800)  # Ajustar el tamaño y la resolución
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode()
    plt.close()  # Limpiar el gráfico después de generarlo

    return img_base64, interpretacion 

# Nueva función para graficar anemia interactivo
def graficar_anemia_interactivo(anio):
    """
    Genera un gráfico de barras con la suma de porcentajes de anemia total por departamento para el año seleccionado.
    Devuelve la imagen en formato base64.
    """
    # Normalizar los nombres de los departamentos (primera letra mayúscula)
    df['Departamento'] = df['Departamento'].str.title()
    
    # Filtrar los datos para el año seleccionado
    df_filtrado = df[df[anio].notnull()]  # Asegurarse de que haya datos para el año seleccionado
    
    if df_filtrado.empty:
        print(f"No hay datos disponibles para el año {anio}.")
        return None
    
    # Asegurarse de que los datos sean numéricos
    df_filtrado[anio] = pd.to_numeric(df_filtrado[anio], errors='coerce')
    
    # Agrupar por departamento y sumar los porcentajes de anemia
    df_agrupado = df_filtrado.groupby('Departamento')[anio].sum().reset_index()
    
    # Crear el gráfico de barras
    plt.figure(figsize=(10, 6))
    plt.bar(df_agrupado['Departamento'], df_agrupado[anio].astype(float), color='skyblue', edgecolor='black')
    
    # Personalizar el gráfico
    plt.title(f"Porcentaje Total de Anemia por Departamento en {anio}", fontsize=14)
    plt.xlabel("Departamentos", fontsize=12)
    plt.ylabel("Porcentaje Total (%)", fontsize=12)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    # Guardar el gráfico en memoria y codificar en base64
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight', dpi=800)  # Ajustar el tamaño y la resolución
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode()
    plt.close()  # Limpiar el gráfico después de generarlo

    return img_base64

# Filtrar datos relevantes (sin columnas categóricas para el análisis numérico)
""" numeric_data = df.iloc[:, 2:] """

# Calcular estimadores estadísticos
""" descriptive_stats = numeric_data.describe().T
descriptive_stats["Range"] = descriptive_stats["max"] - descriptive_stats["min"]
descriptive_stats """

# Gráficos: Evolución temporal de los indicadores de anemia
""" plt.figure(figsize=(12, 6))
for indicator in df["Indicador Anemia %"].unique():
    subset = df[df["Indicador Anemia %"] == indicator]
    mean_values = subset.iloc[:, 2:].mean()
    plt.plot(mean_values.index, mean_values.values, label=indicator) """

# Personalización del gráfico
""" plt.title("Evolución temporal de los indicadores de anemia", fontsize=14)
plt.xlabel("Año", fontsize=12)
plt.ylabel("Porcentaje (%)", fontsize=12)
plt.legend(title="Indicador", fontsize=10)
plt.grid(True, linestyle="--", alpha=0.6)
plt.xticks(rotation=45)
plt.show()
 """
# Interpretación
interpretacion = """
Interpretación:
1. La anemia leve muestra una tendencia ligeramente ascendente, pasando del 20% al 23% en los últimos años.
2. La anemia moderada tiene una disminución significativa, reduciéndose de un 18% a un 9% aproximadamente.
3. La anemia severa permanece estable en niveles muy bajos, oscilando entre el 2% y el 1.2%.
4. El porcentaje total de anemia muestra una tendencia descendente moderada, pasando del 40% a 33%, con algunos altibajos recientes.

Conclusión:
La disminución de la anemia moderada es un punto positivo, mientras que la anemia leve parece mantenerse como un desafío constante. Es crucial seguir trabajando en estrategias de prevención y tratamiento para reducir el impacto total de la anemia.
"""

""" print(interpretacion) """

def grafico_estadistico(departamento, indicador):
    """
    Genera un gráfico estadístico (líneas) para un indicador en un departamento específico a lo largo de los años.

    Args:
        departamento (str): Nombre del departamento.
        indicador (str): Indicador de anemia (e.g., 'Leve', 'Moderada', 'Severa', 'Total').

    Returns:
        fig (matplotlib.figure.Figure): Objeto de la figura generada.
    """
    
    # Filtrar los datos por el departamento y el indicador
    departamento_data = df[(df['Departamento'] == departamento) & (df['Indicador Anemia %'] == indicador)]

    # Reemplazar NaN con 0 para los valores faltantes
    if departamento_data.empty:
        valores = [0] * len(anios)
    else:
        valores = departamento_data[anios].fillna(0).values.flatten().tolist()  # Convertir a lista
    
    # Extraer los años y los valores
    anios = [col for col in df.columns if isinstance(col, int)]
    valores = departamento_data[anios].values.flatten()

    # Crear el gráfico
    fig, ax = plt.subplots()
    ax.plot(anios, valores, marker='o', linestyle='-', color='green')
    ax.set_title(f'Tendencia de {indicador} en {departamento}')
    ax.set_xlabel('Año')
    ax.set_ylabel('Porcentaje (%)')
    ax.grid(True)
    plt.tight_layout()

    return fig

    # Calcular estadísticas clave
    valor_min = valores.min()
    anio_min = anios[valores.argmin()]
    valor_max = valores.max()
    anio_max = anios[valores.argmax()]
    tendencia = "aumento" if valores[-1] > valores[0] else "disminución"

    # Crear un resumen
    resumen = (
        f"Análisis del indicador '{indicador}' en {departamento}:\n"
        f"- Año con el valor más bajo: {anio_min} ({valor_min}%)\n"
        f"- Año con el valor más alto: {anio_max} ({valor_max}%)\n"
        f"- Tendencia general: {tendencia} a lo largo de los años.\n"
    )

    return resumen

#-------------------------------------------------------------------------------------------------------------------------------------

# Función para graficar el análisis temporal excluyendo el año 2000
def plot_analisis_temporal(departamento):
    dept_data = df_total[lista_dptos == departamento]
    plt.plot(valid_years, dept_data[valid_years].values[0], label=departamento)
    plt.title(f'Tendencia de Anemia en {departamento} (2008-2023)')
    plt.xlabel('Año')
    plt.ylabel('Porcentaje de Anemia')
    plt.grid(True)
    plt.legend()

    # Ajustar la rotación y el tamaño de las etiquetas del eje x
    plt.xticks(rotation=45, fontsize=10)
    plt.tight_layout()  # Asegurar que los elementos no se corten
        
    # Guardar el gráfico como archivo PNG
    output_filename = f"Tendencia_Anemia_{departamento}_2008_2023.png"
    plt.savefig(output_filename, dpi=300, bbox_inches='tight')
    print(f"Gráfico guardado como: {output_filename}")

    # Mostrar el gráfico
    plt.show()

    # Interpretación de los datos
    print(f"\nInterpretación de los datos para el departamento {departamento_seleccionado}:")
    print(f"Desde el año 2008 hasta el año 2023, se ha observado una tendencia en los porcentajes de anemia en el departamento de {departamento_seleccionado}.")
        
    max_anemia = dept_data[year_columns].values[0].max()
    min_anemia = dept_data[year_columns].values[0].min()
        
    # Encontrar los años correspondientes a los valores máximo y mínimo
    year_max = year_columns[dept_data[year_columns].values[0].argmax()]
    year_min = year_columns[dept_data[year_columns].values[0].argmin()]
        
    print(f"El valor máximo de anemia fue {max_anemia:.2f}% en el año {year_max} y el valor mínimo fue {min_anemia:.2f}% en el año {year_min}.")
    



# Correlacion y regresion
# Cortegana - Encinas
# se decidio hacerlo juntos, ya q hay se relaccionan mucho ambos analisis

import pandas as pd
import numpy as np
from scipy.stats import pearsonr
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# Función para preparar los datos en un formato adecuado
def prepare_data(raw_df):
    # Pivotar la tabla para que los indicadores sean columnas
    df = raw_df.pivot(index=['DEPARTAMENTO', 'AÑO'], columns='INDICADOR', values='VALOR').reset_index()
    return df

# Función para analizar tendencias temporales
def trend_analysis(df):
    print("\nAnálisis de tendencias temporales:")
    departamento = input("Seleccione el departamento: ")
    indicador = input("Seleccione el indicador: ")

    data = df[(df['DEPARTAMENTO'] == departamento) & (df[indicador].notnull())]

    if data.empty:
        print("\nNo hay suficientes datos para realizar el análisis.")
        return

    X = data[['AÑO']].values.reshape(-1, 1)
    Y = data[indicador].values.reshape(-1, 1)
    model = LinearRegression()
    model.fit(X, Y)

    slope = model.coef_[0][0]
    intercept = model.intercept_[0]
    r2 = r2_score(Y, model.predict(X))

    print(f"\nTendencia: {indicador} = {slope:.4f} * AÑO + {intercept:.4f}")
    print(f"Coeficiente de determinación R²: {r2:.4f}")

# Función para predicción de valores futuros
def future_prediction(df):
    print("\nPredicción de valores futuros:")
    departamento = input("Seleccione el departamento: ")
    indicador = input("Seleccione el indicador: ")

    data = df[(df['DEPARTAMENTO'] == departamento) & (df[indicador].notnull())]

    if data.empty:
        print("\nNo hay suficientes datos para realizar la predicción.")
        return

    X = data[['AÑO']].values.reshape(-1, 1)
    Y = data[indicador].values.reshape(-1, 1)
    model = LinearRegression()
    model.fit(X, Y)

    try:
        future_year = int(input("Ingrese el año para el cual desea predecir el valor: "))
        prediction = model.predict([[future_year]])[0][0]
        print(f"\nPredicción: En el año {future_year}, {indicador} será aproximadamente {prediction:.4f}")
    except ValueError:
        print("\nAño inválido.")

# Función para evaluar relaciones entre indicadores
def relationship_analysis(df):
    print("\nEvaluación de relaciones entre indicadores:")
    indicador_x = input("Seleccione el primer indicador (X): ")
    indicador_y = input("Seleccione el segundo indicador (Y): ")

    data = df[[indicador_x, indicador_y]].dropna()

    if data.empty:
        print("\nNo hay suficientes datos para evaluar la relación.")
        return

    correlation, p_value = pearsonr(data[indicador_x], data[indicador_y])
    print(f"\nCorrelación de Pearson entre {indicador_x} y {indicador_y}: {correlation:.4f}")
    print(f"Valor p: {p_value:.4e}")
    if p_value < 0.05:
        print("La correlación es estadísticamente significativa.")
    else:
        print("La correlación no es estadísticamente significativa.")

# Función para comparar tendencias entre departamentos
def compare_departments(df):
    print("\nComparación de tendencias entre departamentos:")
    indicador = input("Seleccione el indicador: ")

    unique_departments = df['DEPARTAMENTO'].unique()

    for departamento in unique_departments:
        data = df[(df['DEPARTAMENTO'] == departamento) & (df[indicador].notnull())]

        if not data.empty:
            X = data[['AÑO']].values.reshape(-1, 1)
            Y = data[indicador].values.reshape(-1, 1)
            model = LinearRegression()
            model.fit(X, Y)

            slope = model.coef_[0][0]
            print(f"{departamento}: Pendiente de la tendencia = {slope:.4f}")

# Crear una función para realizar la correlación y regresión lineal
def analyze_data(df):
    print("\nSeleccione el análisis que desea realizar:")
    print("1. Análisis de tendencias temporales")
    print("2. Predicción de valores futuros")
    print("3. Evaluación de relaciones entre indicadores")
    print("4. Comparación de tendencias entre departamentos")

    choice = input("Ingrese el número de su elección: ")

    if choice == '1':
        trend_analysis(df)
    elif choice == '2':
        future_prediction(df)
    elif choice == '3':
        relationship_analysis(df)
    elif choice == '4':
        compare_departments(df)
    else:
        print("\nOpción inválida. Por favor, intente de nuevo.")

# Nueva función para graficar anemia interactivo
def graficar_anemia_interactivo(anio):
    """
    Genera un gráfico de barras con la suma de porcentajes de anemia total por departamento para el año seleccionado.
    Devuelve la imagen en formato base64.
    """
    # Normalizar los nombres de los departamentos (primera letra mayúscula)
    df['Departamento'] = df['Departamento'].str.title()
    
    # Filtrar los datos para el año seleccionado
    df_filtrado = df[df[anio].notnull()]  # Asegurarse de que haya datos para el año seleccionado
    
    if df_filtrado.empty:
        print(f"No hay datos disponibles para el año {anio}.")
        return None
    
    # Asegurarse de que los datos sean numéricos
    df_filtrado[anio] = pd.to_numeric(df_filtrado[anio], errors='coerce')
    
    # Agrupar por departamento y sumar los porcentajes de anemia
    df_agrupado = df_filtrado.groupby('Departamento')[anio].sum().reset_index()
    
    # Crear el gráfico de barras
    plt.figure(figsize=(10, 6))
    plt.bar(df_agrupado['Departamento'], df_agrupado[anio].astype(float), color='skyblue', edgecolor='black')
    
    # Personalizar el gráfico
    plt.title(f"Porcentaje Total de Anemia por Departamento en {anio}", fontsize=14)
    plt.xlabel("Departamentos", fontsize=12)
    plt.ylabel("Porcentaje Total (%)", fontsize=12)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    # Guardar el gráfico en memoria y codificar en base64
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight', dpi=800)  # Ajustar el tamaño y la resolución
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode()
    plt.close()  # Limpiar el gráfico después de generarlo

    return img_base64
