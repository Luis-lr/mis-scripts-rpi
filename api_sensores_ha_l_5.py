
from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

DB_PATH = "/home/dietpi/sensores_actuadores_ha.db"

@app.route("/humedad/ultimos", methods=["GET"])
def obtener_ultimos_valores():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT timestamp, humedad FROM m_s ORDER BY timestamp DESC LIMIT 5")
        resultados = cursor.fetchall()
        conn.close()
        if resultados:
            data = [{"timestamp": row[0], "humedad": row[1]} for row in resultados]
            return jsonify(data)
        else:
            return jsonify({"error": "Sin datos"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
