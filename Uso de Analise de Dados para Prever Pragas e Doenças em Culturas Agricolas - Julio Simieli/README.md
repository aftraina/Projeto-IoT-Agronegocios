# Sistema de Previsão de Pragas e Doenças em Milho 🐛🌽

Este projeto utiliza um microcontrolador **ESP32** e sensores ambientais (temperatura, umidade do ar e umidade do solo) para coletar dados em campo.  
Em seguida, aplica **Machine Learning** em Python para prever o risco de pragas e doenças na cultura do milho.

## Estrutura dos Arquivos

```
milho_pragas_projeto/
├── ESP32/
│   └── esp32_pragas_milho.ino
├── python/
│   └── modelo_pragas_milho.py
├── data/
│   └── dados_milho_exemplo.csv
└── README.md
```

### ESP32/esp32_pragas_milho.ino
Código Arduino para o ESP32 ler sensores DHT22 (temperatura/umidade) e umidade do solo.  
Envia ou grava leituras a cada 5 min.

### python/modelo_pragas_milho.py
Script Python que:
1. Carrega `data/dados_milho_exemplo.csv`
2. Treina um RandomForestClassifier
3. Salva o modelo em `modelo_pragas_milho.pkl`
4. Faz previsão de risco para uma amostra de teste

### data/dados_milho_exemplo.csv
Amostra fictícia de 20 leituras rotuladas (`risco_praga` 0/1).

## Como Usar

1. **ESP32**  
   * Carregue o arquivo `esp32_pragas_milho.ino` no Arduino IDE.  
   * Ajuste os pinos conforme seu hardware.  
   * Conecte o DHT22 no pino 4 (GPIO4) e o sensor capacitivo de umidade do solo no GPIO34 (ADC1_6).  

2. **Python**  
   * Instale dependências:  
     ```bash
     pip install pandas scikit-learn joblib
     ```  
   * Execute:  
     ```bash
     python modelo_pragas_milho.py
     ```  
   * O script treinará o modelo e imprimirá o risco estimado.

3. **Expansões Futuras**  
   * Envio dos dados do ESP32 via Wi‑Fi (MQTT, HTTP ou Firebase).  
   * Painel em tempo real com Grafana ou Power BI.  
   * Integração com APIs meteorológicas externas.  

*Projeto gerado automaticamente em 3 de junho de 2025.*