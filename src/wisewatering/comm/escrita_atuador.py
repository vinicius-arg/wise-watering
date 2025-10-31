import requests
import ctypes

from .pacote import Pacote
from .pacote import Comando

SOF = b'\xAA\xBB'

class Escrita:
    @staticmethod
    def checar_acoes_pendentes():
        url = "http://127.0.0.1:3000/api/acoes"
        resposta = requests.get(url)
        status = resposta.status_code
        
        if status == 200:
            pacote = resposta.json()
            return Escrita.json_to_bytes(pacote)

        return {}

    @staticmethod
    def json_to_bytes(pacote):
        carga = pacote["data"].encode("ascii")
        
        comando_struct = Comando()
        comando_struct.type = 1 # Código para type "action"
        ctypes.memmove(comando_struct.carga, carga, len(carga))

        return bytes(comando_struct)


    @staticmethod
    def enviar_pro_atuador(serial, pacote):
        serial.write(SOF)
        serial.write(pacote)