from flask import Flask, jsonify, request
import sqlite3
from flask_cors import CORS

# Permitir CORS para todas las rutas
CORS(app)

app = Flask(__name__)

# Función para obtener una conexión a la base de datos
def get_db_connection():
    conn = sqlite3.connect("sensores_actuadores.db")
    conn.row_factory = sqlite3.Row
    return conn

# Ruta para obtener todos los sensores
@app.route("/sensores", methods=["GET"])
def get_sensores():
    try:
        conn = get_db_connection()
        sensores = conn.execute("SELECT * FROM sensores").fetchall()
        conn.close()
        return jsonify([dict(sensor) for sensor in sensores])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ruta para obtener las mediciones de un sensor por su ID
@app.route("/sensores/<int:sensor_id>/mediciones", methods=["GET"])
def get_mediciones(sensor_id):
    try:
        conn = get_db_connection()
        mediciones = conn.execute("SELECT * FROM mediciones WHERE sensor_id = ?", (sensor_id,)).fetchall()
        conn.close()
        return jsonify([dict(medicion) for medicion in mediciones])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ruta para obtener todos los actuadores
@app.route("/actuadores", methods=["GET"])
def get_actuadores():
    try:
        conn = get_db_connection()
        actuadores = conn.execute("SELECT * FROM actuadores").fetchall()
        conn.close()
        return jsonify([dict(actuador) for actuador in actuadores])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ruta para obtener los estados de un actuador por su ID
@app.route("/actuadores/<int:actuador_id>/estados", methods=["GET"])
def get_estados_actuador(actuador_id):
    try:
        conn = get_db_connection()
        estados = conn.execute("SELECT * FROM estados_actuadores WHERE actuador_id = ?", (actuador_id,)).fetchall()
        conn.close()
        return jsonify([dict(estado) for estado in estados])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
