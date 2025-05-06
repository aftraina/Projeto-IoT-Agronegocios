**Configuração de Envio de Dados e Aplicativo de Controle**

` `1. Configuração do Envio de Dados para ThingSpeak

Para enviar os dados de temperatura e umidade para o ThingSpeak, podemos modificar o código do ESP32 para incluir esta funcionalidade:

\```cpp

#include <WiFi.h>

#include <DHT.h>

#include <ThingSpeak.h>

#define DHTPIN 4

#define DHTTYPE DHT22

DHT dht(DHTPIN, DHTTYPE);

WiFiClient client;

const char\* ssid = "SUA\_REDE\_WIFI";

const char\* password = "SENHA\_WIFI";

unsigned long myChannelNumber = 12345; // Substitua pelo seu canal

const char\* myWriteAPIKey = "SUA\_CHAVE\_API"; // Sua chave API do ThingSpeak

void setup() {

`  `Serial.begin(115200);

`  `dht.begin();

`  `WiFi.begin(ssid, password);



`  `while (WiFi.status() != WL\_CONNECTED) {

`    `delay(500);

`    `Serial.print(".");

`  `}



`  `ThingSpeak.begin(client);

}

void loop() {

`  `float humidity = dht.readHumidity();

`  `float temperature = dht.readTemperature();



`  `if (isnan(humidity) || isnan(temperature)) {

`    `Serial.println("Falha ao ler o sensor DHT22!");

`    `return;

`  `}



`  `ThingSpeak.setField(1, temperature);

`  `ThingSpeak.setField(2, humidity);



`  `int httpCode = ThingSpeak.writeFields(myChannelNumber, myWriteAPIKey);



`  `if (httpCode == 200) {

`    `Serial.println("Dados enviados para ThingSpeak!");

`  `} else {

`    `Serial.println("Erro no envio para ThingSpeak. HTTP error code " + String(httpCode));

`  `}



`  `delay(300000); // Aguarda 5 minutos antes da próxima leitura

}

\```

` `**2. Configuração do Envio via Bluetooth**

Para adicionar comunicação Bluetooth, podemos usar o Bluetooth Classic do ESP32:

\```cpp

#include <BluetoothSerial.h>

#include <DHT.h>

#define DHTPIN 4

#define DHTTYPE DHT22

DHT dht(DHTPIN, DHTTYPE);

BluetoothSerial SerialBT;

void setup() {

`  `Serial.begin(115200);

`  `dht.begin();

`  `SerialBT.begin("ESP32\_Irrigacao"); // Nome do dispositivo Bluetooth

}

void loop() {

`  `float humidity = dht.readHumidity();

`  `float temperature = dht.readTemperature();



`  `if (isnan(humidity) || isnan(temperature)) {

`    `Serial.println("Falha ao ler o sensor DHT22!");

`    `return;

`  `}



`  `// Envia dados via Bluetooth

`  `SerialBT.print("Temperatura: ");

`  `SerialBT.print(temperature);

`  `SerialBT.print("°C, Umidade: ");

`  `SerialBT.print(humidity);

`  `SerialBT.println("%");



`  `delay(5000); // Aguarda 5 segundos antes da próxima leitura

}

\```

` `**3. Desenvolvimento do Aplicativo**

Para o aplicativo móvel, recomendo usar o MIT App Inventor (para uma solução rápida) ou desenvolver um app nativo (Android/iOS) com as seguintes funcionalidades:

Funcionalidades do App:

1\. Leitura de dados em tempo real:

`   `- Exibir temperatura e umidade atualizadas

2\. Controle remoto:

`   `- Botão para ligar/desligar a bomba d'água

`   `- Configuração de limites para irrigação automática

3\. Sistema de alertas:

`   `- Notificações quando a temperatura estiver fora da faixa ideal

`   `- Alertas visuais (mudança de cor) conforme a situação

4\. Configurações:

`   `- Definir parâmetros ideais de temperatura e umidade

`   `- Configurar intervalos de verificação

Código para comunicação Bluetooth no app (Android Studio - Java):

\```java

// Conexão Bluetooth

private BluetoothAdapter bluetoothAdapter;

private BluetoothSocket bluetoothSocket;

private ConnectedThread connectedThread;

private void connectToDevice(BluetoothDevice device) {

`    `try {

`        `bluetoothSocket = device.createRfcommSocketToServiceRecord(MY\_UUID);

`        `bluetoothSocket.connect();

`        `connectedThread = new ConnectedThread(bluetoothSocket);

`        `connectedThread.start();

`    `} catch (IOException e) {

`        `e.printStackTrace();

`    `}

}

private class ConnectedThread extends Thread {

`    `private final InputStream mmInStream;



`    `public ConnectedThread(BluetoothSocket socket) {

`        `InputStream tmpIn = null;

`        `try {

`            `tmpIn = socket.getInputStream();

`        `} catch (IOException e) { }

`        `mmInStream = tmpIn;

`    `}



`    `public void run() {

`        `byte[] buffer = new byte[1024];

`        `int bytes;



`        `while (true) {

`            `try {

`                `bytes = mmInStream.read(buffer);

`                `String data = new String(buffer, 0, bytes);

`                `// Processar dados recebidos (temperatura e umidade)

`                `updateUI(data);

`            `} catch (IOException e) {

`                `break;

`            `}

`        `}

`    `}

}

private void updateUI(String data) {

`    `runOnUiThread(() -> {

`        `// Atualizar a interface com os novos dados

`        `textViewTemperature.setText(extrairTemperatura(data));

`        `textViewHumidity.setText(extrairUmidade(data));



`        `// Verificar alertas

`        `checkAlerts(extrairTemperatura(data), extrairUmidade(data));

`    `});

}

private void checkAlerts(float temp, float humidity) {

`    `if (temp > 30 || temp < 15) { // Valores exemplos

`        `showAlert("Temperatura fora da faixa ideal: " + temp + "°C");

`    `}

`    `// Verificar outros parâmetros...

}

\```

` `**4. Teste de Automação**

Para testar a automação de ações baseadas nos dados, podemos implementar a seguinte lógica no ESP32:

\```cpp

void checkAndAct(float temperature, float humidity) {

`  `// Verifica temperatura crítica

`  `if (temperature > 30.0) { // Limite superior de temperatura

`    `sendAlert("Temperatura crítica: " + String(temperature) + "°C");

`  `}



`  `// Verifica umidade do solo (simulado)

`  `int soilMoisture = analogRead(34);

`  `if (soilMoisture < 500) { // Valor exemplo para solo seco

`    `activateWaterPump();

`  `}

}

void activateWaterPump() {

`  `digitalWrite(22, HIGH); // Liga a bomba

`  `delay(10000); // Mantém ligada por 10 segundos

`  `digitalWrite(22, LOW); // Desliga a bomba

}

void sendAlert(String message) {

`  `// Envia alerta via Bluetooth

`  `SerialBT.println("ALERTA: " + message);



`  `// Envia alerta para ThingSpeak

`  `ThingSpeak.setField(3, 1); // Campo de alerta

`  `ThingSpeak.writeFields(myChannelNumber, myWriteAPIKey);

}

\```

` `**5. Implementação do Dashboard no ThingSpeak**

No ThingSpeak, configure:

1\. Um canal com dois campos para temperatura e umidade

2\. Um terceiro campo para alertas (1 = alerta, 0 = normal)

3\. Widgets para visualização dos dados:

`   `- Gráfico de linha para temperatura e umidade

`   `- Display numérico para valores atuais

`   `- Indicador visual para status de alerta

` `**Considerações Finais**

Esta solução integra:

\- Envio de dados para nuvem (ThingSpeak)

\- Comunicação Bluetooth com aplicativo móvel

\- Controle remoto da bomba d'água

\- Sistema de alertas baseado em limiares

\- Automação de ações conforme os dados dos sensores
