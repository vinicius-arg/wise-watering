import ctypes

TAM_CARGA = 16

class Pacote(ctypes.LittleEndianStructure):
    _pack_ = 1 
    _fields_ = [
        ("umidade", ctypes.c_uint32)
    ]

class Comando(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("type", ctypes.c_uint8),
        ("data", ctypes.c_uint8),
        ("ack", ctypes.c_uint8)
    ]