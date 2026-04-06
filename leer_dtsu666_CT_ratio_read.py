
import minimalmodbus

instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 1)  # Ajusta según tu sistema
instrument.serial.baudrate = 9600
instrument.serial.timeout = 1
instrument.mode = minimalmodbus.MODE_RTU

# Dirección del registro 0x0006 = 6 decimal
register_address = 6
irat = instrument.read_register(register_address, 0, functioncode=4, signed=True)

print(f"Relación del transformador de corriente (IrAt): {irat}")

