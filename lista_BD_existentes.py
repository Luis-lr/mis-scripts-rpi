import sqlite3

# Conectar a la base de datos SQLite (reemplaza con la ruta de tu archivo .db)
conn = sqlite3.connect('mi_base_de_datos.db')
cursor = conn.cursor()

# Ver las tablas en la base de datos
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tablas = cursor.fetchall()

print("Tablas en la base de datos:", tablas)

# Cerrar la conexión
conn.close()
