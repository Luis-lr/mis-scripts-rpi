import sqlite3

def crear_base_datos():
    conexion = sqlite3.connect("sensores_actuadores.db")
    cursor = conexion.cursor()
    
    cursor.executescript('''
    CREATE TABLE IF NOT EXISTS sensores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT NOT NULL,
        ubicacion TEXT,
        estado TEXT CHECK(estado IN ('activo', 'inactivo')) DEFAULT 'activo'
    );
    
    CREATE TABLE IF NOT EXISTS mediciones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sensor_id INTEGER,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        variable TEXT,
        valor REAL,
        FOREIGN KEY (sensor_id) REFERENCES sensores(id) ON DELETE CASCADE
    );
    
    CREATE TABLE IF NOT EXISTS actuadores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT NOT NULL,
        ubicacion TEXT,
        estado TEXT CHECK(estado IN ('activo', 'inactivo')) DEFAULT 'activo'
    );
    
    CREATE TABLE IF NOT EXISTS estados_actuadores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        actuador_id INTEGER,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        variable TEXT,
        valor REAL,
        FOREIGN KEY (actuador_id) REFERENCES actuadores(id) ON DELETE CASCADE
    );
    ''')
    
    conexion.commit()
    conexion.close()
    print("Base de datos creada exitosamente.")

if __name__ == "__main__":
    crear_base_datos()
