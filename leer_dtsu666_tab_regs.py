#import minimalmodbus


#instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 1)  # Ajusta puerto y dirección

#instrument.serial.baudrate = 9600  # Configura según tu dispositivo

# Leer registro 2006 (CHINT) - Voltaje Fase A

#voltage_a = instrument.read_register(8198, number_of_decimals=1)  # Divide entre 10 si el valor está escalado

#print(f"Voltaje Fase A (CHINT): {voltage_a} V")

import minimalmodbus

# Configuración del dispositivo
instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 1)  # Puerto y dirección MODBUS
instrument.serial.baudrate = 9600    # Ajusta según tu medidor (9600 o 38400 común)
instrument.serial.parity = 'N'       # Sin paridad
instrument.serial.timeout = 0.5      # Timeout en segundos

# Lista de registros DEC (según tu tabla)
registros = [
    8192, 8194, 8196,  # Voltajes línea-línea (A-B, B-C, C-A)
    8198, 8200, 8202,  # Voltajes fase-neutro (A, B, C)
    8204, 8206, 8208,  # Corrientes (A, B, C)
    8210, 8212, 8214, 8216,  # Potencias activas (Total, A, B, C)
    8218, 8220, 8222, 8224   # Potencias reactivas (Total, A, B, C)
]

# Nombres descriptivos para cada registro (opcional)
nombres = [
    "Voltaje A-B (V)", "Voltaje B-C (V)", "Voltaje C-A (V)",
    "Voltaje Fase A (V)", "Voltaje Fase B (V)", "Voltaje Fase C (V)",
    "Corriente Fase A (A)", "Corriente Fase B (A)", "Corriente Fase C (A)",
    "Potencia Activa Total (kW)", "Potencia Activa Fase A (kW)", "Potencia Activa Fase B (kW)", "Potencia Activa Fase C (kW)",
    "Potencia Reactiva Total (kVAr)", "Potencia Reactiva Fase A (kVAr)", "Potencia Reactiva Fase B (kVAr)", "Potencia Reactiva Fase C (kVAr)"
]

# Leer todos los registros
for i in range(len(registros)):
    try:
        valor = instrument.read_register(registros[i], number_of_decimals=1)  # Ajusta decimals según el escalado
        print(f"{nombres[i]}: {valor}")
    except Exception as e:
        print(f"Error al leer registro {registros[i]}: {str(e)}")
