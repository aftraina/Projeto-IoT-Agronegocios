// Conexão Bluetooth
private BluetoothAdapter bluetoothAdapter;
private BluetoothSocket bluetoothSocket;
private ConnectedThread connectedThread;

private void connectToDevice(BluetoothDevice device) {
    try {
        bluetoothSocket = device.createRfcommSocketToServiceRecord(MY_UUID);
        bluetoothSocket.connect();
        connectedThread = new ConnectedThread(bluetoothSocket);
        connectedThread.start();
    } catch (IOException e) {
        e.printStackTrace();
    }
}

private class ConnectedThread extends Thread {
    private final InputStream mmInStream;
    
    public ConnectedThread(BluetoothSocket socket) {
        InputStream tmpIn = null;
        try {
            tmpIn = socket.getInputStream();
        } catch (IOException e) { }
        mmInStream = tmpIn;
    }
    
    public void run() {
        byte[] buffer = new byte[1024];
        int bytes;
        
        while (true) {
            try {
                bytes = mmInStream.read(buffer);
                String data = new String(buffer, 0, bytes);
                // Processar dados recebidos (temperatura e umidade)
                updateUI(data);
            } catch (IOException e) {
                break;
            }
        }
    }
}

private void updateUI(String data) {
    runOnUiThread(() -> {
        // Atualizar a interface com os novos dados
        textViewTemperature.setText(extrairTemperatura(data));
        textViewHumidity.setText(extrairUmidade(data));
        
        // Verificar alertas
        checkAlerts(extrairTemperatura(data), extrairUmidade(data));
    });
}

private void checkAlerts(float temp, float humidity) {
    if (temp > 30 || temp < 15) { // Valores exemplos
        showAlert("Temperatura fora da faixa ideal: " + temp + "°C");
    }
    // Verificar outros parâmetros...
}