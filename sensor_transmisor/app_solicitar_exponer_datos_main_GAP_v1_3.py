import sqlite3
from flask import Flask, render_template, request, jsonify, Response, stream_with_context
from solicitar_sensores import solicitar_sensores
from datetime import datetime
from time import time
import json

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

    modo = request.args.get('modo', 'NORMAL').upper()  # NORMAL, LC, STOP
    comando_str = request.args.get('comando', '')      # e.g., "ABC"
    frecuencia = request.args.get('frecuencia')        # e.g., "10"

    #comandos = list(comando_str) if comando_str else []  # ['A', 'B', 'C']
    comandos = comando_str.split(',') if comando_str else []
    print(">> GET params:", request.args)
    print(f"[RX] modo={modo}, comandos={comandos}, tipo={type(comandos)}, frecuencia={frecuencia}")

    

    # Validación básica
    if modo not in ['NORMAL', 'LC', 'STOP']:
        return jsonify({'error': 'Modo inválido. Usa normal, LC o STOP.'}), 400

    # Protección contra spam
    if ip in ultimas_llamadas and (ahora - ultimas_llamadas[ip]) < 5:
        return jsonify({'error': 'Solicitudes demasiado frecuentes. Espere un momento.'}), 429
    ultimas_llamadas[ip] = ahora
    # Validación de tiempo entre lecturas automáticas
    ts_ultimo, ts_penultimo = obtener_ultimos_timestamps()
    if ts_ultimo and ts_penultimo:
        gap = (ts_ultimo - ts_penultimo).total_seconds()
        tiempo_desde_ultimo = (datetime.now() - ts_ultimo).total_seconds()
        if tiempo_desde_ultimo < (gap * 0.3):
            tiempo_restante = round(gap - tiempo_desde_ultimo, 1)
            return jsonify({'error': f'Sistema ocupado. Intente en {tiempo_restante} segundos.'}), 429
    
########################################################################################################
    if modo == 'NORMAL':
        comando_final = ','.join(comandos) #+ '#'  # "ABC#"
        print(f"[DEBUG antes de solicitar S] Tipo de retorno en modo NORMAL: {type(comando_final)}")
        datos = solicitar_sensores(comando_final, modo=modo, frecuencia=frecuencia)
       # print(f"[DEBUG final Flask] datos: {datos}, tipo: {type(datos)}")

        if hasattr(datos, '__iter__') and not isinstance(datos, dict):
            return jsonify({'error': 'Modo NORMAL retornó un generador inesperadamente'}), 500
        return jsonify(datos)

    elif modo == 'LC':
        def generar_datos():
            for dato in solicitar_sensores(comandos, modo=modo, frecuencia=frecuencia):
                yield f"data: {json.dumps(dato)}\n\n"
        return Response(stream_with_context(generar_datos()), mimetype='text/event-stream')

    elif modo == 'STOP':
        comando_final = "STOP#"
        datos = solicitar_sensores(comando_final, modo=modo, frecuencia=frecuencia)
        if hasattr(datos, '__iter__') and not isinstance(datos, dict):
            return jsonify({'error': 'Modo STOP retornó un generador inesperadamente 2'}), 500
        return jsonify(datos)

    else:
        return jsonify({'error': 'Modo no reconocido'}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
