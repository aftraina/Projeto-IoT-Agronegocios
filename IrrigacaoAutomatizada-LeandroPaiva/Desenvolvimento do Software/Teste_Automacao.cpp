void checkAndAct(float temperature, float humidity) {
  // Verifica temperatura crítica
  if (temperature > 30.0) { // Limite superior de temperatura
    sendAlert("Temperatura crítica: " + String(temperature) + "°C");
  }
  
  // Verifica umidade do solo (simulado)
  int soilMoisture = analogRead(34);
  if (soilMoisture < 500) { // Valor exemplo para solo seco
    activateWaterPump();
  }
}

void activateWaterPump() {
  digitalWrite(22, HIGH); // Liga a bomba
  delay(10000); // Mantém ligada por 10 segundos
  digitalWrite(22, LOW); // Desliga a bomba
}

void sendAlert(String message) {
  // Envia alerta via Bluetooth
  SerialBT.println("ALERTA: " + message);
  
  // Envia alerta para ThingSpeak
  ThingSpeak.setField(3, 1); // Campo de alerta
  ThingSpeak.writeFields(myChannelNumber, myWriteAPIKey);
}