import minimalmodbus
import struct

# Configuración del instrumento
instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 1)  # Ajusta el puerto y la dirección del esclavo
instrument.serial.baudrate = 9600
instrument.serial.timeout = 1
instrument.mode = minimalmodbus.MODE_RTU

# Dirección del registro 0x0006 = 6 decimal
register_address = 6
irat = instrument.read_register(register_address, 0, functioncode=4, signed=True)

# Dirección del registro 0x0007 = 7 decimal
register_address = 7
urat = instrument.read_register(register_address, 0, functioncode=4, signed=True)

# Dirección del registro de energía total acumulada
register_address = 16414  # 0x401E en hexadecimal

# Lectura de los 2 registros que componen el valor float
raw_data = instrument.read_registers(register_address, 2, functioncode=4)

# Conversión de los registros a un valor float
raw_bytes = struct.pack('>HH', raw_data[0], raw_data[1])
ImpEp = struct.unpack('>f', raw_bytes)[0]


# Supongamos que ya has leído estos valores:
E = ImpEp  # Valor base de energía
UrAt = urat     # Factor de transformación de tensión
IrAt = irat     # Factor de transformación de corriente

# Cálculo de la energía real
Ep = E * UrAt * IrAt * 0.1
print(f"Energía total escalada: {Ep:.2f} kWh")


# Aplicación del factor de escala
#energy_kwh = energy_raw 

#print(f"Energía activa total acumulada: {energy_kwh:.2f} kWh")
