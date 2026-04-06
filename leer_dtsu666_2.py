import minimalmodbus

instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 1)
instrument.serial.baudrate = 9600
instrument.serial.bytesize = 8
instrument.serial.parity = minimalmodbus.serial.PARITY_NONE
instrument.serial.stopbits = 1
instrument.serial.timeout = 1
instrument.mode = minimalmodbus.MODE_RTU

# Muy importante: forzar el orden correcto de palabras y bytes
instrument.clear_buffers_before_each_transaction = True
instrument.swap_bytes = True  # Intercambia bytes
instrument.debug = False      # Pon True si quieres ver los paquetes

try:
    voltage = instrument.read_float(0, functioncode=4, number_of_registers=2)
    print(f"Voltaje Fase A (Ua): {voltage:.2f} V")
except Exception as e:
    print(f"Error al leer: {e}")
