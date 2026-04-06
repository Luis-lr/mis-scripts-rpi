import serial
import time
import RPi.GPIO as GPIO

# Pines del E44
M0 = 17
M1 = 27
AUX = 22

# Configuración de pines
GPIO.setmode(GPIO.BCM)
GPIO.setup(M0, GPIO.OUT)
GPIO.setup(M1, GPIO.OUT)
GPIO.setup(AUX, GPIO.IN)

# Serial
ser = serial.Serial('/dev/serial0', 57600, timeout=2)

def set_mode(m0, m1):
    GPIO.output(M0, m0)
    GPIO.output(M1, m1)
    time.sleep(0.1)

def esperar_respuesta(mensaje_esperado, timeout=3):
    ser.flushInput()
    start = time.time()
    buffer = ""
    while time.time() - start < timeout:
        if ser.in_waiting:
            byte = ser.read().decode(errors='ignore')
            buffer += byte
            if mensaje_esperado in buffer:
                return True
    return False

def intentar_despertar(intentos=3, espera_entre_intentos=2):
    print("Cambiando a modo 1 (wake-up necesario)...")
    set_mode(GPIO.HIGH, GPIO.LOW)  # Modo 1

    for intento in range(1, intentos + 1):
        print(f"Intento {intento}: Enviando WAKE#")
        ser.write(b'WAKE#')

        if esperar_respuesta("READY#"):
            print("✓ Arduino respondió con READY#")
            return True
        else:
            print("✗ No hubo respuesta.")
            if intento < intentos:
                print(f"Esperando {espera_entre_intentos} segundos antes del próximo intento...")
                time.sleep(espera_entre_intentos)

    print("✗ Todos los intentos fallaron. No se pudo despertar al Arduino.")
    return False

try:
    if intentar_despertar():
        print("¡Arduino despierto! Puedes continuar con la comunicación.")
    else:
        print("No se logró establecer comunicación con el Arduino.")

except KeyboardInterrupt:
    print("Cancelado por el usuario.")

finally:
    ser.close()
    GPIO.cleanup()

