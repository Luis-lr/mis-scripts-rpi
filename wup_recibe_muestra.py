import serial
import time
import RPi.GPIO as GPIO

# Configuración de pines para M0 y M1
M0 = 5  # GPIO 5 (Pin 29 en Raspberry Pi)
M1 = 6  # GPIO 6 (Pin 31 en Raspberry Pi)

GPIO.setmode(GPIO.BCM)
GPIO.setup(M0, GPIO.OUT)
GPIO.setup(M1, GPIO.OUT)

# Configurar E32 en modo transparente (M0 = 0, M1 = 0)
GPIO.output(M0, GPIO.LOW)
GPIO.output(M1, GPIO.LOW)
time.sleep(0.1)

# Configurar UART en Raspberry Pi
try:
    serial_port = serial.Serial("/dev/serial0", baudrate=57600, timeout=3)
    print("✅ UART conectado correctamente. Listo para despertar Arduino...")
except Exception as e:
    print(f"❌ Error al conectar UART: {e}")
    exit()

def solicitar_datos():
    try:
        print("📡 Enviando solicitud de activación...")
        serial_port.write(b"WAKEUP\n")  # ⬅️ Enviar señal para despertar Arduino
        serial_port.flush()
        time.sleep(2)  # Esperar respuesta

        respuesta = ""
        tiempo_inicio = time.time()

        # Esperar datos hasta 5 segundos
        while (time.time() - tiempo_inicio) < 5:
            if serial_port.in_waiting > 0:
                respuesta = serial_port.readline().decode(errors="replace").strip()
                break  # Salir en cuanto haya respuesta
        
        if respuesta:
            print("📊 Respuesta del Arduino:", respuesta)
        else:
            print("⚠️ No se recibió respuesta del Arduino.")

    except Exception as e:
        print(f"❌ Error en la comunicación: {e}")

# Ejecutar cada 10 segundos para probar
while True:
    solicitar_datos()
    time.sleep(3)
