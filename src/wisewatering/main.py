from wisewatering.comm.comunicacao import ManipuladorSerial

porta, baudrate = "/dev/ttyACM0", 9600
s = ManipuladorSerial(porta, baudrate) # Instância leitor/escritor de dados

s.start() # Inicia leitura de porta