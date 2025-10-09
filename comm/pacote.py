import ctypes

class Pacote(ctypes.LittleEndianStructure):
    _pack_ = 1 
    _fields_ = [
        ("number", ctypes.c_int),
        ("data", ctypes.c_float)
    ]