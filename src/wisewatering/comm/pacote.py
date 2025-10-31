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
        ("type", ctypes.c_uint16),
        ("data", ctypes.c_char * TAM_CARGA)
    ]