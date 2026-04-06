
instrument.serial.baudrate = 9600
instrument.serial.bytesize = 8
instrument.serial.parity = minimalmodbus.serial.PARITY_NONE
instrument.serial.stopbits = 1
instrument.serial.timeout = 1
instrument.mode = minimalmodbus.MODE_RTU

print("Escaneando con función 0x03 (Holding Registers)...")

for addr in range(0, 100, 2):
    try:
       voltaje_fase_a = instrument.read_register(0, 2)  # Lee el registro con CHINT order 0 (ajusta el número de decimales)

print(f"Voltaje fase A: {voltaje_fase_a} V")

    except Exception as e:
        print(f"⚠️  Error en reg {addr}: {e}")


voltaje_fase_a = instrument.read_register(0, 2)  # Lee el registro con CHINT order 0 (ajusta el número de decimales)

print(f"Voltaje fase A: {voltaje_fase_a} V")
