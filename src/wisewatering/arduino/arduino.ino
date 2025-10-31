#include <stdint.h>

#define SENSOR_PIN A5
#define INTERVALO 1000
#define TAM_CARGA 16

const char SOF[] = "\xAA\xBB";

struct Comando {
  uint16_t type;
  char data[TAM_CARGA];
} __attribute__((packed));

struct LeituraSensor {
  uint32_t umidade;
} __attribute__((packed));

LeituraSensor pacote;

void setup() {
  Serial.begin(9600);
  pinMode(SENSOR_PIN, INPUT);
  randomSeed(analogRead(A0));
}

uint32_t lerDadosSensor() {
  //int dados = analogRead(SENSOR_PIN);
  uint32_t dados = (uint32_t)random(60, 121);
  return dados;
}

void ouvirSolicitacoesBroker() {

}

void enviarParaBroker(const LeituraSensor& pacote) {
  Serial.write(SOF[0]);
  Serial.write(SOF[1]);
  Serial.write((const uint8_t*)&pacote, sizeof(pacote));
}

void loop() {
  delay(INTERVALO);
  uint32_t umidade = lerDadosSensor();
  pacote.umidade = umidade;

  enviarParaBroker(pacote);

  ouvirSolicitacoesBroker();
}
