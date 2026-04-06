import serial
import time
import RPi.GPIO as GPIO
import struct

# Pines del E44
M0 = 17
M1 = 27
AUX = 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(M0, GPIO.OUT)
GPIO.setup(M1, GPIO.OUT)
GPIO.setup(AUX, GPIO.IN)

# Configura el puerto serial
ser = serial.Serial('/dev/serial0', 57600, timeout=2)

def esperar_aux_high(tiempo_limite=3):
    """Espera a que AUX suba a HIGH"""
    start = time.time()
    while GPIO.input(AUX) == 0:
        if time.time() - start > tiempo_limite:
            print("AUX no subió a HIGH.")
            if GPIO.getmode() is not None:
                 GPIO.cleanup()
            exit()
    print("AUX pasó a HIGH.")

def esperar_respuesta(mensaje_esperado, timeout=2):
    """Espera a que llegue un mensaje específico por UART"""
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

def solicitar_sensores(lista_comandos):
    MAX_INTENTOS = 3
    intento = 0
    exito = False

    while intento < MAX_INTENTOS:
        intento += 1
        print(f"\n🔁 Intento {intento} de {MAX_INTENTOS}")

        # 1. Modo 1 (M0=HIGH, M1=LOW) para transmisión wake
        GPIO.output(M0, GPIO.HIGH)
        GPIO.output(M1, GPIO.LOW)
        time.sleep(0.05)

        # 2. Enviar "WAKE#"
        print("→ Enviando WAKE#")
        ser.write(b'WAKE#')

        # 3. Cambiar a modo 0 (M0=LOW, M1=LOW) para recepción normal
        time.sleep(0.05)  # Espera corta antes de cambiar modo
        GPIO.output(M0, GPIO.LOW)
        GPIO.output(M1, GPIO.LOW)
        time.sleep(0.15)  # Esperar más de 150 ms para dar tiempo al Arduino

        # 4. Esperar READY#
        print("⌛ Esperando READY# del Arduino...")
        if esperar_respuesta("READY#", timeout=2):
            print("✅ Arduino listo (READY# recibido)")
            exito = True
            break
        else:
            print("❌ No se recibió READY#, reintentando...")

    if not exito:
        print("❌ Falló tras 3 intentos. Abortando.")
        if GPIO.getmode() is not None:
            GPIO.cleanup()
        return

    # 5. Enviar comandos
    print(f"📤 Enviando comandos: {lista_comandos}")
    for cmd in lista_comandos:
        ser.write(cmd.encode())
        time.sleep(0.05)
    ser.write(b'#')  # Fin de comandos

    esperar_aux_high()

    # 6. Leer estructura binaria (28 bytes esperados)
    struct_size = 28
    formato_struct = '<fffffff'
    data = ser.read(struct_size)

    if len(data) == struct_size:
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

        print("📊 Lectura recibida:")
        print(f"  Voltaje analógico: {volt_analog:.2f} V")
        print(f"  Voltaje batería:   {volt_bat:.2f} V")
        print(f"  DHT11 -> Temp:     {temp_dht:.2f} °C, Humedad: {hum_dht:.2f} %")
        print(f"  DS18B20 -> Temp:   {temp_ds18:.2f} °C")
        print(f"  SHT10 -> Temp:     {temp_sht:.2f} °C, Humedad: {hum_sht:.2f} %")
    else:
        print("⚠️ Error: estructura incompleta")

try:
    print("📡 Iniciando solicitud de sensores...")
    solicitar_sensores(['A','D'])  # Puedes ajustar los comandos aquí

except KeyboardInterrupt:
    print("🛑 Cancelado por el usuario.")

finally:
    ser.close()
    if GPIO.getmode() is not None:
        GPIO.cleanup()
