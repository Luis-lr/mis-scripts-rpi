import sys
import serial
import time
import RPi.GPIO as GPIO
import struct

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
time.sleep(0.1)  # Pequeña espera para estabilizar

print("E32 listo después del retardo")

# Configurar puerto serie
ser = serial.Serial('/dev/serial0', 57600, timeout=1)

# Configura el puerto del RN42
ser_bt = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)

# Clase para duplicar salida
class DuplicadorSalida:
    def __init__(self, terminal, serial_port):
        self.terminal = terminal
        self.serial_port = serial_port

    def write(self, mensaje):
        # Escribe en el terminal (stdout normal)
        self.terminal.write(mensaje)
        self.terminal.flush()
        # Escribe en el puerto serial (como bytes)
        self.serial_port.write(mensaje.encode())

    def flush(self):
        self.terminal.flush()
        self.serial_port.flush()
# Redirigir stdout a terminal + RN42
sys.stdout = DuplicadorSalida(sys.__stdout__, ser_bt)


def esperar_aux_high(tiempo_limite=3):
    start_time = time.time()
    while GPIO.input(AUX) == 0:
        if time.time() - start_time > tiempo_limite:
            print("Error: AUX no pasó a HIGH en tiempo límite. Saliendo...")
            GPIO.cleanup()
            exit()
    print("AUX pasó a HIGH.")

# Nueva estructura: 7 floats = 28 bytes
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
    GPIO.cleanup()
