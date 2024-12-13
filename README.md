# Anemia-Infantil

## Introducción

Este proyecto parte del código base del dashboard proporcionado en el repositorio [Template_Codebaseadmin](https://github.com/Anders87x/Template_Codebaseadmin). A partir de este dashboard, realizamos modificaciones específicas en la carpeta que contiene los archivos HTML, adaptándolos para mostrar nuestro análisis sobre la anemia infantil.  

El objetivo principal de este proyecto es ofrecer una herramienta visual e interactiva que permita explorar los datos relacionados con la anemia infantil, identificando patrones y factores relevantes. Estas adecuaciones incluyeron la personalización de los elementos visuales y la incorporación de nuevos datos y gráficos que responden a las necesidades específicas de nuestro análisis.

---

## Algunos cambios Realizados

Se realizaron modificaciones significativas al código HTML del dashboard original para adaptarlo a las necesidades del proyecto. Por ejemplo:

### Código original:

```html
<body>
    <!-- Page Container -->
    <!--
        Available classes for #page-container:

        GENERIC

        'enable-cookies'                            Remembers active color theme between pages (when set through color theme helper Codebase() -> uiHandleTheme())

        SIDEBAR & SIDE OVERLAY

        'sidebar-r'                                 Right Sidebar and left Side Overlay (default is left Sidebar and right Side Overlay)
        'sidebar-mini'                              Mini hoverable Sidebar (screen width > 991px)
        'sidebar-o'                                 Visible Sidebar by default (screen width > 991px)
        'sidebar-o-xs'                              Visible Sidebar by default (screen width < 992px)
        'sidebar-inverse'                           Dark themed sidebar

        'side-overlay-hover'                        Hoverable Side Overlay (screen width > 991px)
        'side-overlay-o'                            Visible Side Overlay by default

        'side-scroll'                               Enables custom scrolling on Sidebar and Side Overlay instead of native scrolling (screen width > 991px)
    -->
</body>
### Código modificado:
<body>
    <!-- Page Container -->
    <div id="page-container" class="page-header-modern main-content-boxed side-trans-enabled sidebar-inverse">

        <!-- Header -->
        <header id="page-header">
            <!-- Header Content -->
            <div class="content-header">
                <div class="d-flex">
                    <div class="dropdown d-inline-block mr-2">
                        <button type="button" class="btn btn-outline-primary dropdown-toggle" id="dropdown-department" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                            Seleccione Departamento
                        </button>
                        <div class="dropdown-menu" aria-labelledby="dropdown-department">
                            <a class="dropdown-item" href="javascript:void(0)" onclick="selectDepartment('Amazonas')">Amazonas</a>
                            <a class="dropdown-item" href="javascript:void(0)" onclick="selectDepartment('Áncash')">Áncash</a>
                            <a class="dropdown-item" href="javascript:void(0)" onclick="selectDepartment('Apurímac')">Apurímac</a>
                            <a class="dropdown-item" href="javascript:void(0)" onclick="selectDepartment('Arequipa')">Arequipa</a>
                        </div>
                    </div>
            
                    <div class="dropdown d-inline-block mr-2">
                        <button type="button" class="btn btn-outline-primary dropdown-toggle" id="dropdown-year" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                            Seleccione Año
                        </button>
                        <div class="dropdown-menu" aria-labelledby="dropdown-year">
                            <a class="dropdown-item" href="javascript:void(0)" onclick="selectYear(2008)">2008</a>
                            <a class="dropdown-item" href="javascript:void(0)" onclick="selectYear(2009)">2009</a>
                            <a class="dropdown-item" href="javascript:void(0)" onclick="selectYear(2010)">2010</a>
                            <a class="dropdown-item" href="javascript:void(0)" onclick="selectYear(2011)">2011</a>
                        </div>
                    </div>
            
                    <button type="submit" class="btn btn-primary" data-toggle="click-ripple">Filtrar</button>
            
                    <button id="boton-descargar-pdf" class="btn" style="position: absolute; top: 30px; right: 100px;">
                        Generar Reporte
                    </button>
                </div>
            </div>
        </header>
    </div>
</body>
### Descripción de los cambios

1. Se añadió un **dropdown interactivo** para seleccionar el departamento y el año del análisis:
    ```html
    <div class="dropdown d-inline-block mr-2">
        <button type="button" class="btn btn-outline-primary dropdown-toggle" id="dropdown-department" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
            Seleccione Departamento
        </button>
        <div class="dropdown-menu" aria-labelledby="dropdown-department">
            <a class="dropdown-item" href="javascript:void(0)" onclick="selectDepartment('Amazonas')">Amazonas</a>
            <a class="dropdown-item" href="javascript:void(0)" onclick="selectDepartment('Áncash')">Áncash</a>
            <a class="dropdown-item" href="javascript:void(0)" onclick="selectDepartment('Apurímac')">Apurímac</a>
            <a class="dropdown-item" href="javascript:void(0)" onclick="selectDepartment('Arequipa')">Arequipa</a>
        </div>
    </div>
    ```

2. Se incorporaron botones para realizar el filtrado de datos y generar reportes en formato PDF:
    ```html
    <button type="submit" class="btn btn-primary" data-toggle="click-ripple">Filtrar</button>
    <button id="boton-descargar-pdf" class="btn" style="position: absolute; top: 30px; right: 100px;">
        Generar Reporte
    </button>
    ```

3. Se ajustaron las clases CSS para mejorar el diseño y la experiencia del usuario:
    ```html
    <div id="page-container" class="page-header-modern main-content-boxed side-trans-enabled sidebar-inverse">
    </div>
    ```

Estas modificaciones mejoraron la funcionalidad del dashboard, permitiendo una interacción más intuitiva y personalizada para el análisis de anemia infantil.
```
## Descripción del Código (app.py)
El archivo principal del proyecto, denominado app.py, contiene la lógica necesaria para ejecutar la aplicación web. A continuación, se detallan los componentes clave de este archivo:

Framework Flask: Utilizado para definir y gestionar la aplicación web.
Ruta principal (/): Esta ruta renderiza la página HTML que alberga el dashboard, identificado como be_pages_dashboard.html.
Integración con Web Scraping: El archivo importa el módulo webscraping_v2, el cual se encarga de la recolección de datos sobre anemia a través de técnicas de web scraping.

A continuación se presenta un fragmento representativo del código implementado:
```python
from flask import Flask, render_template
from webscraping_v2 import obtener_datos_anemia
```
Inicialización de la aplicación Flask
``` python
app = Flask(__name__)
```
Ruta principal que renderiza la página del dashboard
``` python
@app.route('/')
def index():
    ### Renderiza la página HTML del dashboard
    return render_template('be_pages_dashboard.html')
```

Ejecuta la aplicación en modo de depuración
``` python
if __name__ == '__main__':
    app.run(debug=True)
```
Explicación de la Estructura del Proyecto
La estructura del proyecto se organiza de la siguiente manera:
``` python

├── app.py                    # Archivo principal que contiene la configuración de Flask y las rutas de la aplicación.
├── templates/
│   └── be_pages_dashboard.html # Página HTML que se muestra al usuario, representando el dashboard.
├── static/                   # Contiene los archivos estáticos como imágenes, hojas de estilo (CSS) y scripts (JS).
├── webscraping_v2.py         # Módulo responsable de realizar el scraping y obtener los datos sobre anemia.
```

