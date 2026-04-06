import sys
import serial
import time
import RPi.GPIO as GPIO
import struct
import sqlite3
from datetime import datetime

# Configuración de pines GPIO
M0 = 17
M1 = 27
AUX = 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(M0, GPIO.OUT)
GPIO.setup(M1, GPIO.OUT)
GPIO.setup(AUX, GPIO.IN)

# Configurar módulo en modo 1 (recepción normal)
GPIO.output(M0, GPIO.HIGH)
GPIO.output(M1, GPIO.LOW)
time.sleep(0.1)

print("E32 listo después del retardo")

# Puerto serie del E32
ser = serial.Serial('/dev/serial0', 57600, timeout=1)
# Puerto serie del RN42
ser_bt = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)

# Redirección de salida
class DuplicadorSalida:
    def __init__(self, terminal, serial_port):
        self.terminal = terminal
        self.serial_port = serial_port

    def write(self, mensaje):
        self.terminal.write(mensaje)
        self.terminal.flush()
        self.serial_port.write(mensaje.encode())

    def flush(self):
        self.terminal.flush()
        self.serial_port.flush()

sys.stdout = DuplicadorSalida(sys.__stdout__, ser_bt)

# Función para esperar AUX en HIGH
def esperar_aux_high(tiempo_limite=3):
    start_time = time.time()
    while GPIO.input(AUX) == 0:
        if time.time() - start_time > tiempo_limite:
            print("Error: AUX no pasó a HIGH en tiempo límite. Saliendo...")
            GPIO.cleanup()
            exit()
    print("AUX pasó a HIGH.")

# Base de datos SQLite3
conn = sqlite3.connect('sensores_actuadores_ha.db')
cursor = conn.cursor()

# Crear tabla si no existe
cursor.execute('''
CREATE TABLE IF NOT EXISTS lecturas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    volt_analog REAL,
    volt_bat REAL,
    temp_dht REAL,
    hum_dht REAL,
    temp_ds18 REAL,
    temp_sht REAL,
    hum_sht REAL
)
''')
conn.commit()

# Estructura del paquete: 7 floats (28 bytes)
struct_size = 28
formato_struct = '<fffffff'

try:
    print("Esperando datos desde Arduino...\n")
    while True:
        if ser.in_waiting >= struct_size:
            data = ser.read(struct_size)
            valores = struct.unpack(formato_struct, data)
            (
                volt_analog,
                volt_bat,
                temp_dht,
                hum_dht,
                temp_ds18,
                temp_sht,
                hum_sht
            ) = valores

            timestamp = datetime.now().replace(microsecond=0).isoformat()

            # Guardar en base de datos
            cursor.execute('''
                INSERT INTO lecturas (timestamp, volt_analog, volt_bat, temp_dht, hum_dht, temp_ds18, temp_sht, hum_sht)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                timestamp,
                round(volt_analog, 2),
                round(volt_bat, 2),
                round(temp_dht, 2),
                round(hum_dht, 2),
                round(temp_ds18, 2),
                round(temp_sht, 2),
                round(hum_sht, 2)
            ))    
            conn.commit()

            # Imprimir en pantalla + RN42
            print("Lectura recibida:")
            print(f"  Voltaje analógico: {volt_analog:.2f} V")
            print(f"  Voltaje batería:   {volt_bat:.2f} V")
            print(f"  DHT11 -> Temp:     {temp_dht:.2f} °C, Humedad: {hum_dht:.2f} %")
            print(f"  DS18B20 -> Temp:   {temp_ds18:.2f} °C")
            print(f"  SHT10 -> Temp:     {temp_sht:.2f} °C, Humedad: {hum_sht:.2f} %")
            print("-" * 40)

        else:
            time.sleep(0.1)

except KeyboardInterrupt:
    print("\nFinalizado por el usuario.")
finally:
    ser.close()
    conn.close()
    GPIO.cleanup()
