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
            return Escrita.json_para_bytes(pacote)
        else: # Montar pacote só com 'ack'
            return Escrita.apenas_ack()

    @staticmethod
    def json_para_bytes(pacote):
        comando_struct = Comando()
        carga = pacote["data"]
        
        if carga == "irrigar":
            comando_struct.data = 1 # Código de operação

        comando_struct.type = 1 # Código para type "action"
        comando_struct.ack = 1 # Confirma recebimento de leitura

        return bytes(comando_struct)


    @staticmethod
    def apenas_ack():
        comando_struct = Comando()
        comando_struct.ack = 1

        return bytes(comando_struct)


    @staticmethod
    def enviar_pro_atuador(serial, pacote):
        # serial.write(SOF)
        serial.write(pacote)
