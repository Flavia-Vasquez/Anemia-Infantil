import pandas as pd
import matplotlib.pyplot as plt
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

# Solicitar al usuario que seleccione un departamento
departamentos_disponibles = lista_dptos.unique()
print("Departamentos disponibles:")
for idx, dept in enumerate(departamentos_disponibles):
    print(f"{idx + 1}. {dept}")

# Pedir al usuario seleccionar el número del departamento
seleccion = int(input("Seleccione el número del departamento que desea visualizar: ")) - 1

# Validar la selección
if 0 <= seleccion < len(departamentos_disponibles):
    departamento_seleccionado = departamentos_disponibles[seleccion]

# Solicitar al usuario que seleccione un año específico
print("Años disponibles:", ", ".join(year_columns))
anio_seleccionado = input("Seleccione el año que desea visualizar: ")

# Solicitar al usuario que seleccione un indicador
indicadores_disponibles = df['Indicador Anemia %'].unique()
print("Indicadores disponibles:")
for idx, ind in enumerate(indicadores_disponibles):
    print(f"{idx + 1}. {ind}")

seleccion_indicador = int(input("Seleccione el número del indicador que desea visualizar: ")) - 1
indicador_seleccionado = indicadores_disponibles[seleccion_indicador]

# -----------------------------------------------------------------------------------------------------

## **Porcentaje de Anemia por Nivel y Departamento en el Año Seleccionado**
# Función para generar el gráfico y la interpretación
def comparar_niveles_anemia(anio, departamento):
    # Filtrar datos por año y departamento
    df_anio = df[['Departamento', 'Indicador Anemia %', anio]]
    df_filtrado = df_anio[df_anio['Departamento'].str.upper() == departamento.upper()]
    
    # Excluir la categoría 'Total'
    df_filtrado = df_filtrado[df_filtrado['Indicador Anemia %'] != 'Total']
    
    # Renombrar las columnas para claridad
    df_filtrado.columns = ['Departamento', 'Indicador', 'Proporción']
    
    # Crear el gráfico
    plt.figure(figsize=(8, 5))
    bars = plt.bar(df_filtrado['Indicador'], df_filtrado['Proporción'], color=['#6495ED', '#FFA07A', '#8A2BE2'])
    
    # Agregar etiquetas encima de las barras
    for bar in bars:
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f"{bar.get_height():.1f}%", 
                 ha='center', va='bottom', fontsize=10)
    
    # Personalizar el gráfico
    plt.title(f'Porcentaje de Anemia por Nivel en {anio}\nDepartamento: {departamento}', fontsize=14)
    plt.xlabel('Nivel de Anemia', fontsize=12)
    plt.ylabel('Porcentaje (%)', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()

    # Interpretación textual
    nivel_mayor = df_filtrado.loc[df_filtrado['Proporción'].idxmax()]
    nivel_menor = df_filtrado.loc[df_filtrado['Proporción'].idxmin()]
    
    print("\n--- INTERPRETACIÓN ---")
    print(f"En el año {anio}, en el departamento de {departamento}:\n")
    print(f"- El nivel de anemia más prevalente fue '{nivel_mayor['Indicador']}' con una proporción de {nivel_mayor['Proporción']}%.")
    print(f"- El nivel de anemia menos prevalente fue '{nivel_menor['Indicador']}' con una proporción de {nivel_menor['Proporción']}%.")
    
# Ejemplo de uso
comparar_niveles_anemia(anio_seleccionado, departamento_seleccionado) """

# -----------------------------------------------------------------------------------------------------

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

# Crear un gráfico
grafico = grafico_estadistico(departamento_seleccionado, indicador_seleccionado)
print(grafico)

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
    
# Generar el primer gráfico
analisis_temporal(departamento_seleccionado)
