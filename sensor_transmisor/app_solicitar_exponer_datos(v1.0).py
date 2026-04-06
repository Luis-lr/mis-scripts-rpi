from flask import Flask, render_template, jsonify
import subprocess
import struct
import serial
import time
import RPi.GPIO as GPIO

app = Flask(__name__)

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
            return False
    return True

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
    intento = 0
    exito = False

    while intento < MAX_INTENTOS:
        intento += 1
        GPIO.output(M0, GPIO.HIGH)
        GPIO.output(M1, GPIO.LOW)
        time.sleep(0.05)

        ser.write(b'WAKE#')
        time.sleep(0.05)
        GPIO.output(M0, GPIO.LOW)
        GPIO.output(M1, GPIO.LOW)
        time.sleep(0.15)

        if esperar_respuesta("READY#", timeout=2):
            exito = True
            break

    if not exito:
        return {"error": "Arduino no respondió"}

    for cmd in lista_comandos:
        ser.write(cmd.encode())
        time.sleep(0.05)
    ser.write(b'#')

    if not esperar_aux_high():
        return {"error": "AUX no subió a HIGH"}

    struct_size = 28
    formato_struct = '<fffffff'
    data = ser.read(struct_size)

    if len(data) == struct_size:
        valores = struct.unpack(formato_struct, data)
        return {
            "volt_analog": round(valores[0], 2),
            "volt_bat": round(valores[1], 2),
            "temp_dht": round(valores[2], 2),
            "hum_dht": round(valores[3], 2),
            "temp_ds18": round(valores[4], 2),
            "temp_sht": round(valores[5], 2),
            "hum_sht": round(valores[6], 2)
        }
    else:
        return {"error": "Lectura incompleta"}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/leer_sensores')
def leer_sensores():
    datos = solicitar_sensores(['A', 'D'])
    return jsonify(datos)

@app.route('/cerrar')
def cerrar():
    ser.close()
    GPIO.cleanup()
    return "Recursos liberados"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
