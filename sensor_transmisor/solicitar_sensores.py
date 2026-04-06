import serial
import time
import RPi.GPIO as GPIO
import struct
import json
# Pines del E44
M0 = 17
M1 = 27
AUX = 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(M0, GPIO.OUT)
GPIO.setup(M1, GPIO.OUT)
GPIO.setup(AUX, GPIO.IN)

GPIO.output(M0, GPIO.HIGH)
GPIO.output(M1, GPIO.LOW)
time.sleep(0.05)

ser = serial.Serial('/dev/serial0', 57600, timeout=2)

def esperar_aux_high(tiempo_limite=3):
    start = time.time()
    while GPIO.input(AUX) == 0:
        if time.time() - start > tiempo_limite:
            raise TimeoutError("AUX no subió a HIGH.")


def intentos_wake(duracion_ventana=6, intervalo_intento=0.1):
    """
    Envía múltiples WAKE# dentro del tiempo total de duración_ventana (1s por defecto),
    cada intervalo_intento segundos (200 ms por defecto). Tras cada WAKE#, espera 20 ms.
    """
    inicio = time.time()
    intento = 0

    while time.time() - inicio < duracion_ventana:
        intento += 1
        print(f"\nIntento {intento} (t={round((time.time() - inicio)*1000)} ms):")

        #ser.write(b'WAKE#')
        #print("WAKE# enviado.")
        mensaje = f'WAKE{intento}#'
        ser.write(mensaje.encode())
        print(f"{mensaje} enviado.")
        
        if esperar_respuesta("READY#", timeout=0.500):  # espera 200 ms tras cada intento
            print("✅ READY# recibido.")
            time.sleep(0.150)
            return

        print("❌ No se recibió READY#.")
        tiempo_restante = intervalo_intento - 0.02  # para mantener ritmo de 200 ms por intento
        if tiempo_restante > 0:
            time.sleep(tiempo_restante)

    print("⚠️ No se recibió READY# dentro del tiempo de ventana.")
    return {"error": "No se recibió READY# en el tiempo definido."}
    
def esperar_respuesta(mensaje_esperado, timeout=0.2):  # 20 ms de espera tras cada WAKE#
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


# Aquí preparas el mensaje según el modo def global
struct_size = 33
formato_struct = '<cffffffff'
detener_LC = False

def solicitar_sensores_normal(comandos):
    #modo = modo.strip().upper()
    #global detener_LC

    #print("[DEBUG] solicitando sensores modo NORMAL, retorno simple dict")
    #return {"test": "ok"}  # respuesta fija para prueba
    comando_str = ','.join(comandos) + '#' #agrega la coma a los comandos
    intentos_wake()
    GPIO.output(M0, GPIO.LOW)
    GPIO.output(M1, GPIO.LOW)
    time.sleep(0.05)
    enviar_comando_e44(comando_str)
    #print(f"[TX] Enviando comando al Arduino: {comandos}")
    datos = leer_datos_e44(timeout=3)
    print(f"[DEBUG1] Tipo de retorno en modo NORMAL: {type(datos)}")
    return datos

def solicitar_sensores_lc(comandos, frecuencia):
    global detener_LC
    detener_LC = False

    if not frecuencia or len(comandos) != 1:
        yield {'error': 'Modo LC requiere frecuencia y un solo comando'}
        return

    comando_str = f"LC,{frecuencia},{comandos[0]}"
    intentos_wake()
    enviar_comando_e44(comando_str)
    print(f"[TX] Enviando comando al Arduino: {comando_str}")

    while not detener_LC:
        timeout = int(frecuencia) + 5
        datos = leer_datos_e44(timeout=timeout)

        if isinstance(datos, dict) and 'error' in datos:
                msg = json.dumps(datos)
                yield f"data: {msg}\n\n".encode()  # en bytes
                break

        msg = json.dumps(datos)
        yield f"data: {msg}\n\n".encode()  # en bytes

        time.sleep(float(frecuencia))  # opcional: espera frecuencia para no saturar el stream
        
def detener_lectura_lc():
    global detener_LC
    detener_LC = True
    GPIO.output(M0, GPIO.LOW)
    GPIO.output(M1, GPIO.LOW)
    time.sleep(0.05)

    intentos_max  = 5
    espera_entre_intentos  = 1  # segundos
    ser.reset_input_buffer()  # Limpiar datos previos
    
    for intento in range(intentos_max):
        print(f"Enviando STOP#, intento {intento + 1}")
        ser.write(b'STOP#')

        # Esperamos un corto periodo para ver si llega respuesta
        tiempo_espera = time.time() + espera_entre_intentos
        while time.time() < tiempo_espera:
            if ser.in_waiting:
                raw = ser.read_until(b'#')
                try:
                    mensaje = raw.decode(errors='ignore').strip()
                    print(f"[RX]: {mensaje}")
                    if  "STOPPED" in mensaje:
                        print("[INFO] Confirmación de STOPPED recibida")
                        return {'status': 'Lectura continua detenida'}
                except Exception as e:
                    print(f"[WARN] Decodificación fallida: {e}")
            else:
                time.sleep(0.1)

    print("[ERROR] No se recibió STOPPED después de múltiples intentos")
    return {'status': 'Error: No se pudo detener la lectura continua'}

    #ser.write(b'STOP#')
    #print("[TX] Enviando comando STOP#")
    #return {'status': 'Lectura continua detenida'}


def enviar_comando_e44(comando_str):
    ser.reset_input_buffer()
    ser.write(comando_str.encode())
    esperar_aux_high()
    time.sleep(0.1)  # Pequeño retraso para asegurar que todo el paquete llegó
    print(f"[TX] Enviado al Arduino: {comando_str}")


    # Esperar hasta que lleguen todos los bytes (máximo 3 segundos)
def leer_datos_e44(timeout=5):
    start_time = time.time()

    while ser.in_waiting < struct_size:
        if time.time() - start_time > timeout:
            print(f"Error: Espera superada. Solo hay {ser.in_waiting} bytes disponibles.")
            return {"error": "Estructura binaria incompleta (timeout)."}
        time.sleep(0.05)

    data = ser.read(struct_size)
    if len(data) != struct_size:
        print(f"Error: Estructura incompleta. Recibidos ({len(data)}): {data}")
        return {"error": "Estructura binaria incompleta."}
        
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
    