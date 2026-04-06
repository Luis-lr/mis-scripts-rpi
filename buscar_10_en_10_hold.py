import minimalmodbus

instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 1)  # Ajusta puerto e ID esclavo
instrument.serial.baudrate = 9600
instrument.serial.bytesize = 8
instrument.serial.parity = minimalmodbus.serial.PARITY_NONE
instrument.serial.stopbits = 1
instrument.serial.timeout = 1
instrument.mode = minimalmodbus.MODE_RTU

print("Escaneando con función 0x03 (Holding Registers)...")

for addr in range(0, 100, 2):
    try:
        value = instrument.read_float(addr, functioncode=3, number_of_registers=2)
        if 100.0 < value < 300.0:
            print(f"🟢 Posible voltaje en reg {addr} (f03): {value:.2f} V")
        else:
            print(f"Reg {addr}: {value:.2f}")
    except Exception as e:
        print(f"⚠️  Error en reg {addr}: {e}")
