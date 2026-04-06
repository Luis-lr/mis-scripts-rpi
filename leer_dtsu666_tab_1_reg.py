import minimalmodbus


instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 1)  # Ajusta puerto y dirección

instrument.serial.baudrate = 9600  # Configura según tu dispositivo

#Leer registro 2006 (CHINT) - Voltaje Fase A

voltage_a = instrument.read_register(8198, number_of_decimals=1)  # Divide entre 10 si el valor está escalado

print(f"Voltaje Fase A (CHINT): {voltage_a} V")
