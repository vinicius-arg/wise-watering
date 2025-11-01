#include <stdint.h>

#define SENSOR_PIN A5
#define LED_PIN 13
#define INTERVALO 1000

const char SOF[] = "\xAA\xBB";

struct Comando {
  uint8_t type;
  uint8_t data;
  uint8_t ack;
} __attribute__((packed));

struct LeituraSensor {
  uint32_t umidade;
} __attribute__((packed));

LeituraSensor pacote;
Comando comando;

/* Função para leitura de umidade do solo */
uint32_t lerDadosSensor() {
  //int dados = analogRead(SENSOR_PIN);
  uint32_t dados = (uint32_t)random(60, 121);
  return dados;
}

/* Função de execução de comportamento do atuador */
void irrigar() {
  digitalWrite(LED_PIN, HIGH);
  delay(1000);
  digitalWrite(LED_PIN, LOW);
}

/* Função auxiliar, provê sincronia ao fluxo de dados */
bool encontradoSOF() {
  if (Serial.read() == SOF[0]) {
    if (Serial.read() == SOF[1])
      return true;
  }
  return false;
}

/* Funções para controle de comunicação */
void processarComando(const Comando& cmd) {
  if (cmd.type == 1)  { // Pacote de ação
    if (cmd.data == 1) // Match (opcode de irrigar é '1')
      irrigar();
  }
}

void ouvirSolicitacoesBroker() {
  int tentativa = 0;
  bool esperando = true;

  // TODO: Corrigir não detecção do SOF
  while(esperando && tentativa < 3) {
    // if (encontradoSOF()) {
      esperando = false;

      // Necessário alterar esse trecho caso os códigos
      // de comunicação ultrapassem 1 nibble!
      comando.type = Serial.read();
      comando.data = Serial.read();
      comando.ack = Serial.read();

      processarComando(comando);
    // }

    // tentativa++;
    delay(INTERVALO);
  }
}

void enviarParaBroker(const LeituraSensor& pacote) {
  Serial.write(SOF[0]);
  Serial.write(SOF[1]);
  Serial.write((const uint8_t*)&pacote, sizeof(pacote));
}

/* Funções padrão */
void setup() {
  Serial.begin(9600);
  pinMode(SENSOR_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);
  randomSeed(analogRead(A0));
}

void loop() {
  uint32_t umidade = lerDadosSensor();
  pacote.umidade = umidade;
  enviarParaBroker(pacote);

  ouvirSolicitacoesBroker();
}
