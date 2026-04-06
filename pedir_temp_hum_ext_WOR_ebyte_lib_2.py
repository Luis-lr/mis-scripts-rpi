import serial
import time
import RPi.GPIO as GPIO

import struct

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
ser = serial.Serial('/dev/serial0',57600, timeout=1)

def esperar_aux_high(tiempo_limite=3):
    """Espera a que AUX pase a HIGH dentro del tiempo límite."""
    start_time = time.time()
    while GPIO.input(AUX) == 0:
        if time.time() - start_time > tiempo_limite:
            print("Error: AUX no pasó a HIGH en tiempo límite. Saliendo...")
            GPIO.cleanup()
            exit()
    print("AUX pasó a HIGH.")

# Contador para enviar múltiples mensajes
contador = 0

struct_size = 14

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
        # Llenamos la estructura con valores conocidos o simulados
        Count = contador
        Bits = 500  # valor simulado (ADC entre 0 y 1023)
        Volts = Bits * (5.0 / 1024.0)
        Amps = 1  # valor simulado
        print(f"Enviando -> Count: {Count}, Bits: {Bits}, Volts: {Volts:.2f}, Amps: {Amps:.2f}")
        # Empaquetar usando la misma estructura que Arduino
        packet = struct.pack('<Lhff', Count, Bits, Volts, Amps)
        # Enviar por el puerto serial
        ser.write(packet)
        contador += 1
        
        # 4. Esperar que AUX pase de LOW a HIGH antes de recibir respuesta
        print("Esperando que AUX esté en HIGH antes de recibir respuesta...")
        esperar_aux_high()
        time.sleep(1)
        # 5. Esperar y recibir la respuesta con timeout de 3 segundos
        print("Esperando respuesta del Arduino...")
        start_time = time.time()
        respuesta = ""


        while True:
            if ser.in_waiting >= struct_size:
                data = ser.read(struct_size)

                # Desempaquetar en el mismo orden y tipos: <Lhff
                Count, Bits, Volts, Amps = struct.unpack('<Lhff', data)

                print(f"Recibido -> Count: {Count}, Bits: {Bits}, Volts: {Volts:.2f}, Amps: {Amps:.2f}")
           
                #if ser.in_waiting > 0:
                print("saliendo de recibir") 
                break  # Salir del bucle si hay respuesta
               
                if time.time() - start_time > 3:  # Timeout de 3 segundos
                print("Error: No se recibió respuesta en 3 segundos.")
                break  # Salir del bucle e intentar de nuevo
           # else:
            #    time.sleep(0.1)
        #time.sleep(2)
        break  # Salir del bucle si hay respuesta

except KeyboardInterrupt:
    print("\nFinalizado por el usuario.")
finally:
    ser.close()
GPIO.cleanup()




