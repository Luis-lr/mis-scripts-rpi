import minimalmodbus

instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 1)  # Ajusta el puerto y dirección del esclavo
instrument.serial.baudrate = 9600
instrument.serial.bytesize = 8
instrument.serial.parity = minimalmodbus.serial.PARITY_NONE
instrument.serial.stopbits = 1
instrument.serial.timeout = 1
instrument.mode = minimalmodbus.MODE_RTU

print("Escaneando registros en bloques de 2 (interpretados como float32)...")

for addr in range(0, 100, 2):  # Prueba cada 2 registros desde 0 hasta 98
    try:
        value = instrument.read_float(addr, functioncode=4, number_of_registers=2)
        if 100.0 < value < 300.0:  # Rango típico para voltaje
            print(f"🟢 Posible voltaje encontrado en reg {addr}: {value:.2f} V")
        else:
            print(f"Reg {addr}: {value:.2f}")
    except Exception as e:
        print(f"⚠️  Error en reg {addr}: {e}")
