from flask import Flask, render_template, request, jsonify
from solicitar_sensores import solicitar_sensores

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/leer_sensores')
def leer_sensores():
    comandos_str = request.args.get('comandos', '')
    comandos = comandos_str.split(',') if comandos_str else []
    
    print(f"Comandos recibidos desde HTML: {comandos}")  # <-- Aquí imprimes los comandos


    if not comandos:
        return jsonify({'error': 'No se enviaron comandos válidos'}), 400

    datos = solicitar_sensores(comandos)
    return jsonify(datos)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
