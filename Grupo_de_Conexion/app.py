from flask import Flask, render_template, jsonify, request
from proceso__análisis1 import comparar_niveles_anemia  # Importa tu función que realiza el análisis

app = Flask(__name__)

@app.route('/')
def index():
    # Renderiza la página HTML del dashboard
    return render_template('be_pages_dashboard.html')

@app.route('/generate-chart', methods=['POST'])
def generate_chart():
    # Recibe los datos enviados desde el frontend
    data = request.get_json()
    year = data.get('year')
    department = data.get('department')

    # Verificar si se enviaron los datos necesarios
    if not year or not department:
        return jsonify({'error': 'Year and Department are required'}), 400

    try:
        # Genera el gráfico y la interpretación usando la función comparar_niveles_anemia
        img_base64, interpretacion = comparar_niveles_anemia(year, department)
        
        # Devuelve el gráfico en formato base64 y la interpretación al frontend
        return jsonify({
            'image_url': f"data:image/png;base64,{img_base64}",
            'interpretation': interpretacion  # Enviar la interpretación
        })
    except Exception as e:
        # Manejo de errores en caso de que falle la función de generación
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
