import time
import ctypes
import requests

from threading import Thread, Event
from serial import Serial, SerialException

from .pacote import Pacote
from .sensor import Sensor

SOF = b'\xAA\xBB'
PACKET_SIZE = ctypes.sizeof(Pacote)

class HandshakeException(Exception):
    """Classe pra lançar exceção caso dê problema no hanshake.
    """
    pass

class LeitorDados(Thread):
    """Thread para ler continuamente a porta serial.
    """
    def __init__(self, porta, baudrate):
        super().__init__()
        self.porta = porta
        self.baudrate = baudrate
        self.sensor = Sensor()
        self.stop_event = Event()
  
        self.executando = False

    def run(self):
        """Executado quando self.start() é chamado.
        """
        self.conectar(self.porta, self.baudrate)

        while self.executando:
            try:
                if self.serial.read(1) == SOF[0:1]:
                    if self.serial.read(1) == SOF[1:2]:
                        leitura = self.serial.read(PACKET_SIZE)
                        self.sensor.atualizar_dados(leitura)
                        pacote = { "carga": self.sensor.obter_dados() }
                        self.enviar_pro_servidor(pacote)

            except SerialException as e:
                print(e)
                self.desconectar()

            time.sleep(1) # Uma leitura por segundo

    def conectar(self, porta, baudrate=9600):
        """Realiza a conexão com a porta serial passada como argumento.
        """
        try:
            self.serial = Serial(porta, baudrate=int(baudrate), timeout=2)
            time.sleep(2)
            self.handshake(self.serial)
        
        except SerialException as e:
            print(e)
            self.desconectar()
        
        except HandshakeException as e:
            print(e)
            self.desconectar()
        
    def handshake(self, ser: Serial):
        """Verifica se o dispositivo foi realmente conectado; se pode ler e transmitir dados.
        """
        ser.flush()
        ser.write(b'AT\r\n') # Comando AT (Attention). Resposta esperada: OK
        res = ser.readline()
        res_str = res.decode('utf-8').strip()
        if "OK" not in res_str:
            raise HandshakeException("HandshakeException: Serial connection not estabelished.")
        
    def enviar_pro_servidor(self, pacote):
        url = "http://127.0.0.1:3000"
        carga = pacote
        requests.post(url, data=carga)

    def desconectar(self):
        """Para a thread e fecha a conexão.
        """
        self.serial.close()
        self.stop_event.set()
        self.executando = False
        self.join()