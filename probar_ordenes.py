import minimalmodbus
import struct

def read_raw_registers(instr, start_register):
    regs = instr.read_registers(start_register, 2, functioncode=4)
    return regs[0], regs[1]

def decode_float(reg1, reg2, byte_order):
    # Modbus devuelve dos registros de 16 bits: reg1 (alta), reg2 (baja)
    if byte_order == 'ABCD':  # Big endian
        raw = struct.pack('>HH', reg1, reg2)
    elif byte_order == 'CDAB':  # Little endian
        raw = struct.pack('<HH', reg1, reg2)
    elif byte_order == 'BADC':  # Swapped bytes
        raw = struct.pack('>HH', ((reg1 & 0x00FF) << 8 | (reg1 >> 8)), ((reg2 & 0x00FF) << 8 | (reg2 >> 8)))
    elif byte_order == 'DCBA':  # Word + byte swapped
        raw = struct.pack('<HH', ((reg1 & 0x00FF) << 8 | (reg1 >> 8)), ((reg2 & 0x00FF) << 8 | (reg2 >> 8)))
    else:
        return None
    return struct.unpack('>f', raw)[0]

# Configurar el instrumento
instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 1)
instrument.serial.baudrate = 9600
instrument.serial.bytesize = 8
instrument.serial.parity = minimalmodbus.serial.PARITY_NONE
instrument.serial.stopbits = 1
instrument.serial.timeout = 1
instrument.mode = minimalmodbus.MODE_RTU
instrument.clear_buffers_before_each_transaction = True

try:
    r1, r2 = read_raw_registers(instrument, 0)
    print(f"Registros crudos: {r1}, {r2}")

    for order in ['ABCD', 'CDAB', 'BADC', 'DCBA']:
        try:
            voltage = decode_float(r1, r2, order)
            print(f"Orden {order}: {voltage:.2f} V")
        except Exception as e:
            print(f"Error con orden {order}: {e}")

except Exception as e:
    print(f"Error al leer registros: {e}")
