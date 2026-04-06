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

ser = serial.Serial('/dev/serial0', 57600, timeout=2)

def esperar_aux_high(tiempo_limite=3):
    start = time.time()
    while GPIO.input(AUX) == 0:
        if time.time() - start > tiempo_limite:
            raise TimeoutError("AUX no subió a HIGH.")

def esperar_respuesta(mensaje_esperado, timeout=2):
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
    for intento in range(MAX_INTENTOS):
        GPIO.output(M0, GPIO.HIGH)
        GPIO.output(M1, GPIO.LOW)
        time.sleep(0.05)

        ser.write(b'WAKE#')
        time.sleep(0.05)
        GPIO.output(M0, GPIO.LOW)
        GPIO.output(M1, GPIO.LOW)
        time.sleep(0.05)

        if esperar_respuesta("READY#", timeout=2):
            break
    else:
        return {"error": "No se recibió READY# tras 3 intentos."}

    # ENVÍO OPTIMIZADO DE COMANDOS
    comandos = ''.join(lista_comandos) + '#'
    ser.write(comandos.encode())

    esperar_aux_high()
    time.sleep(0.1)  # Pequeño retraso para asegurar que todo el paquete llegó

    struct_size = 33
    formato_struct = '<cffffffff'

    # Esperar hasta que lleguen todos los bytes (máximo 3 segundos)
    timeout = 3  # segundos
    start_time = time.time()

    while ser.in_waiting < struct_size:
        if time.time() - start_time > timeout:
            print(f"Error: Espera superada. Solo hay {ser.in_waiting} bytes disponibles.")
            return {"error": "Estructura binaria incompleta (timeout)."}
        time.sleep(0.05)  # esperar un poco para no saturar CPU

    # Ahora sí, leer los datos

    data = ser.read(struct_size)

    if len(data) != struct_size:
        print(f"Error: Estructura binaria incompleta. Bytes recibidos ({len(data)}): {data}")
        return {"error": "Estructura binaria incompleta."}

    # Si llega aquí, data está completa    
    print(f"Datos binarios recibidos (raw): {data}")
    
    valores = struct.unpack(formato_struct, data)
    print(f"Datos deserializados: {valores}")
    return {
        #"tipo": valores[0],
        "volt_analog": valores[1],
        "volt_bat": valores[2],
        "carga_bat": valores[3],
        "temp_dht": valores[4],
        "hum_dht": valores[5],
        "temp_ds18": valores[6],
        "temp_sht": valores[7],
        "hum_sht": valores[8] 
    }
