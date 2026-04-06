import RPi.GPIO as GPIO
import serial
import time

# Configuración de pines para M0 y M1
M0_PIN = 29
M1_PIN = 31

# Configurar GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(M0_PIN, GPIO.OUT)
GPIO.setup(M1_PIN, GPIO.OUT)

# Establecer el modo del E32 (Modo 0)
GPIO.output(M0_PIN, GPIO.LOW)
GPIO.output(M1_PIN, GPIO.LOW)

# Configuración del puerto serial
ser = serial.Serial('/dev/ttyS0', 57600, timeout=1)  # Puerto UART en Raspberry Pi
time.sleep(2)  # Espera para asegurar que el puerto serial esté listo

# Función para enviar un mensaje
def enviar_mensaje(mensaje):
    ser.write(mensaje.encode('utf-8'))
    print(f"Mensaje enviado: {mensaje}")

# Función para recibir un mensaje
def recibir_mensaje():
    if ser.in_waiting > 0:
        mensaje = ser.readline().decode('utf-8').strip()
        print(f"Mensaje recibido: {mensaje}")
        return mensaje
    return None

# Enviar un saludo al Arduino
print("Enviando saludo a Arduino...")
enviar_mensaje("¡Hola desde Raspberry Pi!")

# Esperar y recibir respuesta
while True:
    mensaje_recibido = recibir_mensaje()
    if mensaje_recibido:
        print(f"Mensaje recibido: {mensaje_recibido}")
    time.sleep(1)
