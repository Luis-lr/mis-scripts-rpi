

import serial
import time

# Configura el puerto serial (ajusta según el puerto que estés usando)
ser = serial.Serial('/dev/ttyS0', 57600, timeout=3)  # Usamos un timeout de 3 segundos

# Tiempo máximo de espera para recibir un mensaje
timeout = 3
start_time = time.time()

print("Esperando mensaje...")

while True:
    if ser.in_waiting > 0:
        # Lee los datos recibidos
        data = ser.readline()  # Lee la línea completa
        try:
            # Intentamos decodificar los datos recibidos
            mensaje = data.decode('utf-8').strip()
            print(f"Mensaje recibido: {mensaje}")
            start_time = time.time()  # Reinicia el temporizador cada vez que recibimos un mensaje
        except UnicodeDecodeError:
            # Si no se puede decodificar, imprime los datos crudos (bytes)
            print(f"Error de decodificación. Datos crudos: {data}")
            start_time = time.time()  # Reinicia el temporizador
    elif time.time() - start_time > timeout:
        print("No se ha recibido ningún mensaje en los últimos 3 segundos. Saliendo...")
        break  # Sale del script si han pasado 3 segundos sin mensaje

ser.close()  # Cierra el puerto serial
