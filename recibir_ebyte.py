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
ser = serial.Serial('/dev/serial0',57600, timeout=1)

def esperar_aux_high(tiempo_limite=3):
    """Espera a que AUX pase a HIGH dentro del tiempo límite."""
    start_time = time.time()
    while GPIO.input(AUX) == 0:
        if time.time() - start_time > tiempo_limite:
            print("Error: AUX no pasó a HIGH en tiempo límite. Saliendo...")
            GPIO.cleanup()
            exit()
    print("AUX pasó a HIGH.")



# Contador para enviar múltiples mensajes
#contador = 0
struct_size = 14

try:
    print("Esperando datos desde Arduino...\n")
    while True:
        if ser.in_waiting >= struct_size:
            data = ser.read(struct_size)

            # Desempaquetar en el mismo orden y tipos: <Lhff
            Count, Bits, Volts, Amps = struct.unpack('<Lhff', data)

            print(f"Recibido -> Count: {Count}, Bits: {Bits}, Volts: {Volts:.2f}, Amps: {Amps:.2f}")
        else:
            time.sleep(0.1)

except KeyboardInterrupt:
    print("\nFinalizado por el usuario.")
finally:
    ser.close()
