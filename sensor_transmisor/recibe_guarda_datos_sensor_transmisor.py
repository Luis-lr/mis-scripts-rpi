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
struct_size = 33
formato_struct = '<cffffffff'  # 1 char + 8 floats

# Asegúrate de que esta tabla ya esté creada:
cursor.execute('''
CREATE TABLE IF NOT EXISTS alertas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    volt_bat REAL,
    carga_bat REAL
)
''')
conn.commit()

struct_size = 33
formato_struct = '<cffffffff'  # 1 char + 8 floats

def esperar_encabezado(serial_port, encabezado=b'\xAA'):
    while True:
        byte = serial_port.read(1)
        if byte == encabezado:
            return
try:
    print("Esperando datos desde Arduino...\n")
    while True:
        esperar_encabezado(ser)  # Esperar hasta que llegue el encabezado correcto
        data = ser.read(struct_size)  # Leer los 33 bytes restantes

        if len(data) == struct_size:
            valores = struct.unpack(formato_struct, data)
            tipo = valores[0]  # Esto es un bytes, ejemplo b'A'
            print(f"Datos crudos: {data} ({len(data)} bytes)")

            volt_analog = valores[1]
            volt_bat = valores[2]
            carga_bat = valores[3]
            temp_dht = valores[4]
            hum_dht = valores[5]
            temp_ds18 = valores[6]
            temp_sht = valores[7]
            hum_sht = valores[8]    

            print("Datos desempaquetados:")
            print(f"Tipo: {tipo}")
            print(f"Voltaje analógico: {volt_analog}")
            print(f"Voltaje batería: {volt_bat}")
            print(f"Carga batería: {carga_bat}")
            print(f"DHT: Temp={temp_dht}, Hum={hum_dht}")
            print(f"DS18B20: Temp={temp_ds18}")
            print(f"SHT: Temp={temp_sht}, Hum={hum_sht}")

            timestamp = datetime.now().replace(microsecond=0).isoformat()
            if tipo == b'A':
                cursor.execute('''
                    INSERT INTO alertas (timestamp, volt_bat, carga_bat)
                    VALUES (?, ?, ?)
                ''', (
                    timestamp,
                    round(volt_bat, 2),
                    round(carga_bat, 2)
                ))
                conn.commit()
                print("⚠️ Alerta guardada en base de datos.")
            else:
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
                print("Lecturas guardadas en base de datos.")

        else:
            print(f"Error: se esperaban {struct_size} bytes, pero llegaron {len(data)} bytes")
    else:
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nFinalizado por el usuario.")
finally:
    ser.close()
    conn.close()
    GPIO.cleanup()
