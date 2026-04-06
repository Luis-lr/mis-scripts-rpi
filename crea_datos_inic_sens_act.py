import sqlite3
import random
import datetime

# Función para obtener una conexión a la base de datos
def get_db_connection():
    conn = sqlite3.connect("sensores_actuadores.db")
    conn.row_factory = sqlite3.Row
    return conn

# Función para insertar datos aleatorios en la base de datos
def insertar_datos_aleatorios():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Insertar datos aleatorios para sensores
    for i in range(1, 6):  # Asumiendo que hay 5 sensores para ejemplo
        cursor.execute('''INSERT INTO sensores (tipo, ubicacion, estado) VALUES (?, ?, ?)''',
                       (f'sensores_{i}', f'Ubicacion_{i}', random.choice(['activo', 'inactivo'])))
        sensor_id = cursor.lastrowid
        # Insertar mediciones aleatorias para cada sensor
        for j in range(1, 6):  # 5 mediciones por sensor
            cursor.execute('''INSERT INTO mediciones (sensor_id, variable, valor) VALUES (?, ?, ?)''',
                           (sensor_id, f'variable_{j}', random.uniform(0, 100)))

    # Insertar datos aleatorios para actuadores
    for i in range(1, 6):  # Asumiendo que hay 5 actuadores para ejemplo
        cursor.execute('''INSERT INTO actuadores (tipo, ubicacion, estado) VALUES (?, ?, ?)''',
                       (f'actuador_{i}', f'Ubicacion_{i}', random.choice(['activo', 'inactivo'])))
        actuador_id = cursor.lastrowid
        # Insertar estados aleatorios para cada actuador
        for j in range(1, 6):  # 5 estados por actuador
            cursor.execute('''INSERT INTO estados_actuadores (actuador_id, variable, valor) VALUES (?, ?, ?)''',
                           (actuador_id, f'variable_{j}', random.uniform(0, 100)))

    conn.commit()
    conn.close()
    print('Datos aleatorios insertados exitosamente.')

if __name__ == '__main__':
    insertar_datos_aleatorios()
