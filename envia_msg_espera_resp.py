import serial
import time

# Configura el puerto serial (ajusta según el puerto que estés usando en DietPi)
ser = serial.Serial('/dev/ttyS0',57600, timeout=3)  # Usamos 9600 baudios para la comunicación con el Arduino

# Tiempo máximo de espera para recibir un mensaje
timeout = 5 
start_time = time.time()

print("Esperando mensaje...")

while True:
   
 # Enviar mensaje al Arduino
    mensaje = "APAGAR"  # O cualquier otro mensaje que quieras enviar
    ser.write((mensaje + '\n').encode())  # Envía el mensaje al Arduino

    print(f"Mensaje enviado: {mensaje}")

    # Esperar una respuesta del Arduino
    response = ser.readline().decode('utf-8').strip()  # Leer la respuesta del Arduino

    if response:
        print(f"Respuesta del Arduino: {response}")
    else:
        print("No se recibió respuesta del Arduino.")

    time.sleep(2)  # Espera 2 segundos antes de enviar otro mensaje

    # Ahora leer el mensaje desde el Arduino si se recibe
    if ser.in_waiting > 0:
        # Lee los datos recibidos
        data = ser.readline()  # Lee la línea completa
        try:
            # Intentamos decodificar los datos recibidos
            mensaje_recibido = data.decode('utf-8').strip()
            print(f"Mensaje recibido del Arduino: {mensaje_recibido}")
            start_time = time.time()  # Reinicia el temporizador cada vez que recibimos un mensaje
       #     time.sleep(2)  # Espera 2 segundos antes de enviar otro mensaje
        except UnicodeDecodeError:
            # Si no se puede decodificar, imprime los datos crudos (bytes)
            print(f"Error de decodificación. Datos crudos: {data}")
            start_time = time.time()  # Reinicia el temporizador

      #  time.sleep(2)  # Espera 2 segundos antes de enviar otro mensaje

    elif time.time() - start_time > timeout:
        print("No se ha recibido ningún mensaje en los últimos 3 segundos. Saliendo...")

        break  # Sale del script si han pasado 3 segundos sin mensaje


ser.close()  # Cierra el puerto serial
