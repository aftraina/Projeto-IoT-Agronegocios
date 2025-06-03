/*
 * esp32_pragas_milho.ino
 * Código para leitura de sensores DHT22 e umidade do solo capacitivo.
 */

#include <DHT.h>

#define DHTPIN 4
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

const int soilPin = 34;  // Pino ADC para sensor de umidade do solo

void setup() {
  Serial.begin(115200);
  dht.begin();
}

void loop() {
  float temp = dht.readTemperature();
  float hum  = dht.readHumidity();

  int soilRaw = analogRead(soilPin);              // 0–4095
  float soilPct = map(soilRaw, 0, 4095, 100, 0);  // 100 % (molhado) → 0 % (seco)

  Serial.printf("Temperatura: %.2f °C\n", temp);
  Serial.printf("Umidade Ar:  %.2f %%\n", hum);
  Serial.printf("Umidade Solo: %.2f %%\n\n", soilPct);

  delay(300000);  // Aguarda 5 min
}