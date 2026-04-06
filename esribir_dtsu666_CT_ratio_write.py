import minimalmodbus

instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 1)
instrument.serial.baudrate = 9600
instrument.serial.timeout = 1
instrument.mode = minimalmodbus.MODE_RTU

# Escribir IrAt = 30 en registro 6 usando functioncode=16 (0x10)
#instrument.write_registers(6, 30, functioncode=6)  # Sí, incluso para 1 solo registro
instrument.write_register(6, 30, functioncode=16)

# Leer para confirmar
irat = instrument.read_register(6, functioncode=4, signed=True)
print(f"Nuevo IrAt (CT ratio): {irat}")

