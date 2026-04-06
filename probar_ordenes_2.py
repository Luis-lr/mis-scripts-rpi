import minimalmodbus

instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 1)  # Ajusta puerto y dirección esclavo
instrument.serial.baudrate = 9600
instrument.serial.bytesize = 8
instrument.serial.parity = minimalmodbus.serial.PARITY_NONE
instrument.serial.stopbits = 1
instrument.serial.timeout = 1
instrument.mode = minimalmodbus.MODE_RTU

# Leer voltaje Ua (float32 en registros 0 y 1)
voltaje = instrument.read_float(1, functioncode=4, number_of_registers=2)
print(f"Ua: {voltaje:.2f} V")

raw = instrument.read_registers(1, 2, functioncode=4)
print("Registros crudos:", raw)
