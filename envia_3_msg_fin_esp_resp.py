import serial
import time
import RPi.GPIO as GPIO

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
# Esperar 5 segundos (ajusta según necesidad)
time.sleep(0.1)

print("E32 listo después del retardo")
# Configurar puerto serie
ser = serial.Serial('/dev/serial0', 57600, timeout=1)

# Lista de mensajes a enviar
mensajes = ["¿Cuál es tu estado?\n", "¿Cuál es la temperatura?\n",
            "¿Cómo está la batería?\n", "¿Hay algún error?\n"]

for i in range(4):
    mensaje = mensajes[i]
    print(f"Enviando pregunta {i+1}: {mensaje.strip()}")
    ser.write(mensaje.encode())  # Enviar mensaje

   #  Esperar a que AUX pase a HIGH antes de recibir
    start_time = time.time()
    while GPIO.input(AUX) == 0:
       if time.time() - start_time > 3:  # Si AUX no cambia en 3 segundos, salir
        print("Error: AUX no respondió en 3 segundos. Saliendo...")
        GPIO.cleanup()
       exit()
    print("aux en high, sigo con el codigo")

    # Esperar respuesta con timeout de 3 segundos
    respuesta_recibida = False
    start_time = time.time()
    while not respuesta_recibida:
        if ser.in_waiting > 0:
            respuesta = ser.readline().decode().strip()
            if respuesta:
                print(f"Respuesta recibida: {respuesta}")
                respuesta_recibida = True

            time.sleep(0.5)
        if time.time() - start_time > 3:  # Si no hay respuesta en 3 segundos, sa>
            print("Error: No se recibió respuesta en 3 segundos. Saliendo...")
            GPIO.cleanup()
            exit()
