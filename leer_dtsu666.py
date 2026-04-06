import minimalmodbus

# Configura el instrumento
instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 1)  # Puerto y dirección Modbus
instrument.serial.baudrate = 9600
instrument.serial.bytesize = 8
instrument.serial.parity = minimalmodbus.serial.PARITY_NONE
instrument.serial.stopbits = 1
instrument.serial.timeout = 1  # segundos
instrument.mode = minimalmodbus.MODE_RTU

# Leer potencia activa total (registro 0x000C, 2 registros)
try:
#    power = instrument.read_float(0x000C, functioncode=4, number_of_registers=2)
 #   print(f"Potencia activa total: {power} W")
#    voltage = instrument.read_float(0, functioncode=4, number_of_registers=2)
 #   print(f"Voltaje Fase A (Ua): {voltage:.2f} V")
#    voltage_raw = instrument.read_long(0, functioncode=4)
#    print(f"Voltaje (raw): {voltage_raw}")
#    print(f"Voltaje Fase A (Ua): {voltage_raw / 100.0:.2f} V")

    voltaje_fase_a = instrument.read_register(2, 2)  # Lee el registro con CHINT order 0 (ajusta el número de decimales)

    print(f"Voltaje fase A: {voltaje_fase_a} V")

except Exception as e:
    print(f"Error al leer: {e}")
