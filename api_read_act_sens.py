from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect("sensores_actuadores.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/sensores", methods=["GET"])
def get_sensores():
    conn = get_db_connection()
    sensores = conn.execute("SELECT * FROM sensores").fetchall()
    conn.close()
    return jsonify([dict(sensor) for sensor in sensores])

@app.route("/sensores/<int:sensor_id>/mediciones", methods=["GET"])
def get_mediciones(sensor_id):
    conn = get_db_connection()
    mediciones = conn.execute("SELECT * FROM mediciones WHERE sensor_id = ?", (sensor_id,)).fetchall()
    conn.close()
    return jsonify([dict(medicion) for medicion in mediciones])

@app.route("/actuadores", methods=["GET"])
def get_actuadores():
    conn = get_db_connection()
    actuadores = conn.execute("SELECT * FROM actuadores").fetchall()
    conn.close()
    return jsonify([dict(actuador) for actuador in actuadores])

@app.route("/actuadores/<int:actuador_id>/estados", methods=["GET"])
def get_estados_actuador(actuador_id):
    conn = get_db_connection()
    estados = conn.execute("SELECT * FROM estados_actuadores WHERE actuador_id = ?", (actuador_id,)).fetchall()
    conn.close()
    return jsonify([dict(estado) for estado in estados])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
