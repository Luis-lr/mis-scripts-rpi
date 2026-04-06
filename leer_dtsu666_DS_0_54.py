

import minimalmodbus
import logging

# Configuración básica de logging (para debug)
logging.basicConfig(level=logging.DEBUG)

# Configuración del instrumento MODBUS
instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 1)  # Puerto y dirección del dispositivo
instrument.serial.baudrate = 9600     # Ajusta según tu medidor (9600 o 38400 común)
instrument.serial.parity = 'N'        # Sin paridad
instrument.serial.timeout = 0.5       # Timeout en segundos

# Función para leer registros
def scan_registers(start_reg, end_reg, decimals=1, functioncode=4):
    for reg in range(start_reg, end_reg + 1):
        try:
            value = instrument.read_register(reg, number_of_decimals=decimals, functioncode=functioncode)
            #value = instrument.read_register(reg, number_of_decimals=1, byteorder=minimalmodbus.BYTEORDER_BIG)
            print(f"Registro {reg}: {value}")
        except Exception as e:
            print(f"Error al leer registro {reg}: {e}")

# Escanea registros del 0 al 54
print("=== Escaneando registros (0 a 54) ===")
scan_registers(0,55 )

# Opcional: Leer como float si los datos están en ese formato
# print("=== Intentando leer como float ===")
#for reg in range(0, 55):
 #   try:
  #      value = instrument.read_float(reg, functioncode=4)
   #     print(f"Registro {reg} (float): {value}")
   # except Exception as e:
    #    print(f"Error al leer registro {reg} como float: {e}")
