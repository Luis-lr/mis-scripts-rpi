import minimalmodbus
import struct

instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 1)  # Ajusta según tu configuración
instrument.serial.baudrate = 9600
instrument.serial.timeout = 1
instrument.mode = minimalmodbus.MODE_RTU

# Dirección del registro (0x2044 = 8260)
register_address = 8198
raw_data = instrument.read_registers(register_address, 2, functioncode=4)

# Interpretar como float en orden AB CD
raw_bytes = struct.pack('>HH', raw_data[0], raw_data[1])
raw_volt = struct.unpack('>f', raw_bytes)[0]

# Dirección del registro 0x0007 = 7 decimal
register_address = 7
urat = instrument.read_register(register_address, 0, functioncode=4, signed=True)

# Aplicar factor de conversión del manual
voltage = raw_volt * urat * 0.01

print(f"Voltage: {voltage:.2f} V")
