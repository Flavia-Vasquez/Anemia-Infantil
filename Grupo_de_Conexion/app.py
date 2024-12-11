from flask import Flask, render_template, jsonify
from webscraping_v2 import obtener_datos_anemia

app = Flask(__name__)

@app.route('/')
def index():
    # Renderiza la página HTML del dashboard
    return render_template('be_pages_dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
