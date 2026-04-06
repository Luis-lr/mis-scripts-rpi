import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('serial_data.db')
cursor = conn.cursor()

# Consultar los últimos 5 registros
cursor.execute('SELECT timestamp, value FROM serial_data ORDER BY timestamp DESC LIMIT 5')
rows = cursor.fetchall()

# Mostrar los resultados
for row in rows:
    print(f"Timestamp: {row[0]}, Value: {row[1]}")

# Cerrar la conexión
conn.close()
