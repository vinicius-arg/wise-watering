import time
import ctypes

from threading import Thread
from serial import Serial, SerialException

from .pacote import Pacote
from .sensor import Sensor
from .leitura_sensor import Leitura
from .escrita_atuador import Escrita

SOF = b'\xAA\xBB'
INTERVALO_LEITURA = 0.1
TAMANHO_PACOTE = ctypes.sizeof(Pacote)

class ManipuladorSerial(Thread):
    """Thread para ler continuamente a porta serial.
    """
    def __init__(self, porta, baudrate):
        super().__init__()
        self.porta = porta
        self.baudrate = baudrate
        self.sensor = Sensor()
  
        self.executando = False


    def __checar_sof(self):
        if self.serial.read(1) == SOF[0:1]:
            if self.serial.read(1) == SOF[1:2]:
                return True

        return False
    

    def __checar_acoes_pendentes(self):
        return Escrita.checar_acoes_pendentes()


    def __enviar_pro_servidor(self, pacote):
        Leitura.enviar_pro_servidor(pacote)


    def __enviar_pro_atuador(self, pacote):
        Escrita.enviar_pro_atuador(self.serial, pacote)


    def run(self):
        """Executado quando self.start() é chamado.
        """
        self.conectar(self.porta, self.baudrate)

        while self.executando:
            time.sleep(INTERVALO_LEITURA)
            try:
                if self.__checar_sof():
                    leitura = self.serial.read(TAMANHO_PACOTE)
                    self.sensor.atualizar_dados(leitura)
                    pacote = { "carga": self.sensor.obter_ultimo_pacote() }
                    self.__enviar_pro_servidor(pacote)

                    # TODO sincronização por eventos

                    pendente = self.__checar_acoes_pendentes()
                    
                    if pendente:
                        self.__enviar_pro_atuador(pendente)

            except SerialException as e:
                print(e)
                self.desconectar()


    def conectar(self, porta, baudrate=9600):
        """Realiza a conexão com a porta serial passada como argumento.
        """
        try:
            self.serial = Serial(porta, baudrate=int(baudrate), timeout=2)
            self.executando = True
            time.sleep(2)
        
        except SerialException as e:
            print(e)
            self.desconectar()
        
                
    def desconectar(self):
        """Para a thread e fecha a conexão.
        """
        self.serial.close()
        self.stop_event.set()
        self.executando = False
        self.join()

