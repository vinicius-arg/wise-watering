from collections import deque
import ctypes

from .pacote import Pacote

class Sensor():
    def __init__(self, tam: int = 50):
        super().__init__()
        self.ultimo_pacote = Pacote()
        self.tam_lista = tam

        self.inicializar_dados()

    def inicializar_dados(self):
        self.dados = { "umidade": deque(maxlen=self.tam_lista) }

    def obter_dados(self):
        return self.dados
    
    def definir_dados(self, novo_valor):
        self.dados.umidade.append(novo_valor)
    
    def obter_ultimo_pacote(self):
        return self.ultimo_pacote

    def atualizar_dados(self, raw_bytes: bytes):
        self.ultimo_pacote = Pacote.from_buffer_copy(raw_bytes)
        
        valor = getattr(self.ultimo_pacote, "umidade")
        self.definir_dados(valor)
