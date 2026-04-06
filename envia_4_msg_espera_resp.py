import serial
import time
import RPi.GPIO as GPIO

# Configura los pines GPIO para M0 y M1
M0_PIN = 17  # M0 conectado al pin GPIO17 (D17)
M1_PIN = 27  # M1 conectado al pin GPIO27 (D27)

# Configura los pines de la Raspberry Pi como salidas
GPIO.setmode(GPIO.BCM)  # Utiliza la numeración BCM de pines GPIO
GPIO.setup(M0_PIN, GPIO.OUT)
GPIO.setup(M1_PIN, GPIO.OUT)

# Configura el puerto serial
ser = serial.Serial('/dev/ttyS0', 57600, timeout=2)  # Ajusta el puerto y la velocidad de baudios según corresponda

# Lista de mensajes que se van a enviar
mensajes = ["ENCENDER", "APAGAR", "ENCENDER", "APAGAR"]  # Lista de 4 mensajes a enviar
response = None

for i, mensaje in enumerate(mensajes):
    print(f"Enviando mensaje {i + 1}: {mensaje}")  # Indica qué mensaje se está enviando
    ser.write((mensaje + '\n').encode())  # Envía el mensaje al Arduino

    # Esperar la respuesta del Arduino
    response = ser.readline().decode('utf-8').strip()  # Lee la respuesta del Arduino
    if response:
        print(f"Respuesta del Arduino: {response}")
    else:
        print("No se recibió respuesta del Arduino.")

    # Esperar antes de enviar el siguiente mensaje
    time.sleep(2)  # Ajusta este valor si es necesario para dar tiempo suficiente a Arduino para responder

# Confirmación de que el script llegó hasta el final
print("Todos los mensajes han sido enviados.")
