import serial
import time
import RPi.GPIO as GPIO

# Configuración de pines GPIO para M0 y M1
M0 = 5  # GPIO 5 (Pin 29 en Raspberry Pi)
M1 = 6  # GPIO 6 (Pin 31 en Raspberry Pi)

GPIO.setmode(GPIO.BCM)
GPIO.setup(M0, GPIO.OUT)
GPIO.setup(M1, GPIO.OUT)

# Configurar E32 en modo transparente (M0 = 0, M1 = 0)
GPIO.output(M0, GPIO.LOW)
GPIO.output(M1, GPIO.LOW)
time.sleep(0.1)

# Configurar el puerto UART de la Raspberry Pi
try:
    serial_port = serial.Serial("/dev/serial0", baudrate=57600, timeout=1)
    print("✅ UART conectado correctamente. Esperando datos del Arduino...")
except Exception as e:
    print(f"❌ Error al conectar UART: {e}")
    exit()

# Leer datos entrantes del E32
while True:
    if serial_port.in_waiting > 0:
        data = serial_port.readline().decode(errors="replace").strip()
        if "SENSOR=" in data:
            print("📊 Datos recibidos:", data)
