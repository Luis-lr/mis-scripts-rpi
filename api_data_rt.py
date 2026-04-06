from flask import Flask, jsonify
from flask_cors import CORS  # Asegúrate de tener esta importación
import sqlite3

app = Flask(__name__)
CORS(app)  # Permitir CORS en toda la aplicación

@app.route('/data', methods=['GET'])
def get_data():
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect('serial_data.db')
        cursor = conn.cursor()

        cursor.execute('SELECT timestamp, value FROM serial_data ORDER BY timestamp DESC LIMIT 50')
        rows = cursor.fetchall()

        conn.close()

        data = {
            'timestamps': [row[0] for row in rows],
            'values': [row[1] for row in rows]
        }

        return jsonify(data)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

