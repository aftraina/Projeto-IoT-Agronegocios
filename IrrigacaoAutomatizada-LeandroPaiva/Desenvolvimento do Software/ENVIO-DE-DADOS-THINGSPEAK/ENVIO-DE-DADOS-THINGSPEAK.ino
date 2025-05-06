#include <WiFi.h>
#include <DHT.h>
#include <ThingSpeak.h>

#define DHTPIN 4
#define DHTTYPE DHT22

DHT dht(DHTPIN, DHTTYPE);
WiFiClient client;

const char* ssid = "SUA_REDE_WIFI";
const char* password = "SENHA_WIFI";
unsigned long myChannelNumber = 12345; // Substitua pelo seu canal
const char* myWriteAPIKey = "SUA_CHAVE_API"; // Sua chave API do ThingSpeak

void setup() {
  Serial.begin(115200);
  dht.begin();
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  ThingSpeak.begin(client);
}

void loop() {
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();
  
  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("Falha ao ler o sensor DHT22!");
    return;
  }
  
  ThingSpeak.setField(1, temperature);
  ThingSpeak.setField(2, humidity);
  
  int httpCode = ThingSpeak.writeFields(myChannelNumber, myWriteAPIKey);
  
  if (httpCode == 200) {
    Serial.println("Dados enviados para ThingSpeak!");
  } else {
    Serial.println("Erro no envio para ThingSpeak. HTTP error code " + String(httpCode));
  }
  
  delay(300000); // Aguarda 5 minutos antes da próxima leitura
}