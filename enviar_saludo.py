import serial
import time
import RPi.GPIO as GPIO

# Configurar los pines GPIO 29 y 31 para M0 y M1
GPIO.setmode(GPIO.BOARD)  # Usamos numeración de pines físicos
GPIO.setup(29, GPIO.OUT)  # M0 en GPIO 29
GPIO.setup(31, GPIO.OUT)  # M1 en GPIO 31

# Configurar el puerto serial para la comunicación con el módulo E32 (ttyS0)
ser = serial.Serial('/dev/ttyS0', 57600, timeout=1)

# Función para configurar M0 y M1 en modo 0 (comunicación transparente)
def set_mode_to_transparent():
    GPIO.output(29, GPIO.LOW)  # M0 en LOW
    GPIO.output(31, GPIO.LOW)  # M1 en LOW

# Esperar para asegurar que la comunicación serial está lista
time.sleep(2)

# Configurar el modo de los pines
set_mode_to_transparent()

# Enviar un saludo al Arduino
saludo = "¡Hola desde Raspberry Pi a través de E32!"
ser.write(saludo.encode('utf-8'))

# Imprimir mensaje en consola
print(f"Mensaje enviado: {saludo}")

# Cerrar el puerto serial
ser.close()

# Limpiar GPIO después de usar
GPIO.cleanup()
