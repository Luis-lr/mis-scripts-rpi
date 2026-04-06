import serial
import sqlite3
import time

# Configurar el puerto serial (ajusta el puerto y la velocidad)
ser = serial.Serial('/dev/ttyS0',57600)  # Cambia el puerto y la velocidad según tu configuración

# Conectar a la base de datos
conn = sqlite3.connect('serial_data.db')
cursor = conn.cursor()

# Leer continuamente del puerto serial
while True:
    if ser.in_waiting > 0:
        # Leer el dato del puerto serial
        data = ser.readline().decode('utf-8').strip()

        # Almacenar el dato en la base de datos
        cursor.execute('''
            INSERT INTO serial_data (value) VALUES (?)
        ''', (data,))  # Inserta el valor en la tabla

        # Confirmar el cambio
        conn.commit()

        print(f'Dato almacenado: {data}')

    time.sleep(1)  # Esperar 1 segundo antes de leer el siguiente dato

# Cerrar la conexión cuando termine (aunque en este caso, el script seguirá corriendo)
conn.close()
