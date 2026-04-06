import sqlite3
from flask import Flask, render_template, request, jsonify
from solicitar_sensores_v1_1 import solicitar_sensores_v1_1
from datetime import datetime
from time import time

app = Flask(__name__)
DB_PATH = '/home/dietpi/scripts/sensor_transmisor/sensores_actuadores_ha.db'  # <-- Ajusta esto

# Configura tu umbral de seguridad (segundos)
#GAP_TOTAL = 8.0         # Ciclo completo del Arduino
#GAP_UMBRAL = 5.5        # Tiempo mínimo de espera para aceptar nueva consulta

def obtener_ultimos_timestamps():
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT timestamp FROM lecturas ORDER BY id DESC LIMIT 2;")
        rows = cur.fetchall()
        conn.close()

        if len(rows) == 2:
            ts_ultimo = datetime.fromisoformat(rows[0][0])
            ts_penultimo = datetime.fromisoformat(rows[1][0])
            return ts_ultimo, ts_penultimo
    except Exception as e:
        print(f"Error al consultar base de datos: {e}")
    return None, None

@app.route('/')
def index():
    return render_template('index.html')

# Simple en memoria (no para producción)
ultimas_llamadas = {}

@app.route('/leer_sensores')
def leer_sensores():
    ip = request.remote_addr
    ahora = time()
    
    # Bloqueo si hizo una solicitud hace menos de 5 segundos
    if ip in ultimas_llamadas and (ahora - ultimas_llamadas[ip]) < 5:
        return jsonify({'error': 'Solicitudes demasiado frecuentes. Espere un momento.'}), 429
    
    ultimas_llamadas[ip] = ahora

    comandos_str = request.args.get('comandos', '')
    comandos = comandos_str.split(',') if comandos_str else []
    print(f"Comandos: {comandos}")
    if not comandos:
        return jsonify({'error': 'No se enviaron comandos válidos'}), 400

    ts_ultimo, ts_penultimo = obtener_ultimos_timestamps()
    if ts_ultimo and ts_penultimo:
        ahora = datetime.now()
        gap = (ts_ultimo - ts_penultimo).total_seconds()
        tiempo_desde_ultimo = (ahora - ts_ultimo).total_seconds()

        print(f"[INFO] Última lectura hace {tiempo_desde_ultimo:.2f} s. GAP promedio: {gap:.2f} s")

        # Rechazar si estamos muy cerca del momento de la próxima lectura automática
        if tiempo_desde_ultimo < (gap * 0.3):
            tiempo_restante = round(gap - tiempo_desde_ultimo, 1)
            return jsonify({'error': f'Sistema ocupado. Intente en {tiempo_restante} segundos.'}), 429

    # Paso 2: Enviar solicitud a Arduino
    datos = solicitar_sensores(comandos)
    return jsonify(datos)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
