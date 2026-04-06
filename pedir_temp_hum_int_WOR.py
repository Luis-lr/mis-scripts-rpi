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
time.sleep(0.1)  # Pequeña espera para estabilizar

print("E32 listo después del retardo")

# Configurar puerto serie
ser = serial.Serial('/dev/serial0', 57600, timeout=1)

def esperar_aux_high(tiempo_limite=3):
    """Espera a que AUX pase a HIGH dentro del tiempo límite."""
    start_time = time.time()
    while GPIO.input(AUX) == 0:
        if time.time() - start_time > tiempo_limite:
            print("Error: AUX no pasó a HIGH en tiempo límite. Saliendo...")
            GPIO.cleanup()
            exit()
    print("AUX pasó a HIGH.")

# Intentos máximos para obtener respuesta
MAX_INTENTOS = 3
intentos = 0

while intentos < MAX_INTENTOS:
    intentos += 1
    print(f"Intento {intentos} de {MAX_INTENTOS}")

    # 1. Verificar que AUX pase de LOW a HIGH antes de comenzar
    print("Esperando que AUX esté en HIGH antes de iniciar...")
    esperar_aux_high()

    # 2. Esperar 3 ms antes de enviar el mensaje
    time.sleep(0.003)

    # 3. Enviar el mensaje "humedad" al Arduino
    mensaje = "3\n"
    ser.write(mensaje.encode())
    print(f"Enviado: {mensaje.strip()}")

    # 4. Esperar que AUX pase de LOW a HIGH antes de recibir respuesta
    print("Esperando que AUX esté en HIGH antes de recibir respuesta...")
    esperar_aux_high()

    # 5. Esperar y recibir la respuesta con timeout de 3 segundos
    print("Esperando respuesta del Arduino...")
    start_time = time.time()
    respuesta = ""

    while True:
        if ser.in_waiting > 0:
            respuesta = ser.readline().decode().strip()
            break  # Salir del bucle si hay respuesta
        
        if time.time() - start_time > 3:  # Timeout de 3 segundos
            print("Error: No se recibió respuesta en 3 segundos.")
            break  # Salir del bucle e intentar de nuevo

    if respuesta:
        print(f"Respuesta del Arduino: {respuesta}")
        print(f"✅ Respuesta obtenida en el intento {intentos} ✅")
        print("Finalizando aplicación con éxito.")
        GPIO.cleanup()
        exit()

print("Error: No se obtuvo respuesta después de 3 intentos. Saliendo...")
GPIO.cleanup()
exit()


