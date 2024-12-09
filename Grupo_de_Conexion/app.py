from flask import Flask, render_template, jsonify
from webscraping_v2 import obtener_datos_anemia

app = Flask(__name__)

@app.route('/')
def index():
    # Renderiza la página HTML del dashboard
    return render_template('be_pages_dashboard.html')

@app.route('/api/datos', methods=['GET'])
def datos_anemia():
    try:
        df = obtener_datos_anemia()
        datos_json = df.to_dict(orient='records')
        return jsonify(datos_json)
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
