from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)
DB_PATH = '/home/dietpi/scripts/sensor_transmisor/sensores_actuadores_ha.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/lecturas', methods=['GET'])
def get_lecturas():
    conn = get_db_connection()
    lecturas = conn.execute('SELECT * FROM lecturas').fetchall()
    conn.close()
    return jsonify([dict(row) for row in lecturas])

@app.route('/lecturas/<int:lectura_id>', methods=['GET'])
def get_lectura(lectura_id):
    conn = get_db_connection()
    lectura = conn.execute('SELECT * FROM lecturas WHERE id = ?', (lectura_id,)).fetchone()
    conn.close()
    if lectura is None:
        return jsonify({'error': 'Lectura no encontrada'}), 404
    return jsonify(dict(lectura))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
