import sqlite3

# Conectar (o crear) la base de datos SQLite
conn = sqlite3.connect('serial_data.db')

# Crear un cursor para ejecutar comandos SQL
cursor = conn.cursor()

# Crear la tabla (si no existe ya)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS serial_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        value REAL
    )
''')

# Confirmar los cambios y cerrar la conexión
conn.commit()
conn.close()

print("Base de datos y tabla creadas correctamente.")
