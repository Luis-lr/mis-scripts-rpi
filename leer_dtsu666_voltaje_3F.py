import minimalmodbus
import struct

instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 1)
instrument.serial.baudrate = 9600
instrument.serial.timeout = 1
instrument.mode = minimalmodbus.MODE_RTU

# Leer UrAt del registro 7
urat = instrument.read_register(7, 0, functioncode=4, signed=True)

# Leer 6 registros desde 8198 → voltajes fase A, B, C (2 registros cada uno)
base_address = 8198
reg_count = 6
raw_data = instrument.read_registers(base_address, reg_count, functioncode=4)

# Procesar y aplicar fórmula: V = valor * urat * 0.01
voltajes = []
for i in range(0, 6, 2):
    word1, word2 = raw_data[i], raw_data[i+1]
    raw_bytes = struct.pack('>HH', word1, word2)
    valor_float = struct.unpack('>f', raw_bytes)[0]
    voltage = valor_float * urat * 0.01
    voltajes.append(voltage)

# Mostrar resultados
print(f"Tensión Fase A: {voltajes[0]:.2f} V")
print(f"Tensión Fase B: {voltajes[1]:.2f} V")
print(f"Tensión Fase C: {voltajes[2]:.2f} V")


