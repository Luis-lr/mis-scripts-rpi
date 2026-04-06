from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# Nueva ruta a la base de datos
DB_PATH = "/home/dietpi/sensores_actuadores_ha.db"

@app.route("/humedad", methods=["GET"])
def obtener_humedad():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT humedad FROM m_s ORDER BY timestamp DESC LIMIT 1")
        resultado = cursor.fetchone()
        conn.close()
        if resultado:
            return jsonify({"humedad": resultado[0]})
        else:
            return jsonify({"error": "Sin datos"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
