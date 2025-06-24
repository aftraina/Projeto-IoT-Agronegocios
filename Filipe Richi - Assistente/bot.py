from flask import Flask, request
import requests
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# --- Configurações do Twilio ---
ACCOUNT_SID = 'AC872050c93433012b9fea4cc0fc7da82f'
AUTH_TOKEN = '08ef50d65fb8cd95973cb8b74e6ba738'
TWILIO_WHATSAPP_NUMBER = '+14155238886'
client = Client(ACCOUNT_SID, AUTH_TOKEN)

# --- Chaves de API ---
OPENWEATHER_KEY = '33d50505355ba6f3aa1fc7bba6881a83'
BCB_API = 'https://economia.awesomeapi.com.br/json/last/USD-BRL'
ROBOFLOW_API_KEY = 'SUA_API_KEY_AQUI'
ROBOFLOW_ENDPOINT = 'https://detect.roboflow.com/NOME_DO_MODELO/1'  # ex: plant-disease-detector/1

# --- Funções de apoio ---
def get_weather(city):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_KEY}&lang=pt_br&units=metric'
    resp = requests.get(url)
    if resp.status_code != 200:
        return "Cidade não encontrada."
    data = resp.json()
    try:
        clima = data['weather'][0]['description']
        temp = data['main']['temp']
        return f"Clima em {city.title()}: {clima}, {temp}°C"
    except:
        return "Erro ao processar os dados da previsão."

def get_dollar():
    try:
        resp = requests.get(BCB_API)
        data = resp.json()
        valor = data['USDBRL']['bid']
        return f"Dólar hoje: R$ {valor}"
    except:
        return "Erro ao obter cotação do dólar."

def detectar_praga(imagem_path):
    try:
        with open(imagem_path, 'rb') as img_file:
            response = requests.post(
                f"{ROBOFLOW_ENDPOINT}?api_key={ROBOFLOW_API_KEY}",
                files={"file": img_file}
            )
        if response.status_code == 200:
            result = response.json()
            if result.get('predictions'):
                pred = result['predictions'][0]
                nome = pred.get('class', 'Doença desconhecida')
                confianca = pred.get('confidence', 0)
                return f"⚠️ Detecção: {nome} com {confianca*100:.1f}% de confiança."
            else:
                return "✅ Nenhuma praga ou doença foi detectada na imagem."
        else:
            return "Erro ao analisar a imagem com Roboflow."
    except Exception as e:
        return f"Erro ao processar imagem: {e}"

# --- Webhook do Twilio ---
@app.route('/webhook', methods=['POST'])
def webhook():
    incoming_msg = request.values.get('Body', '').lower()
    sender = request.values.get('From', '')
    num_media = int(request.values.get("NumMedia", 0))
    
    resp = MessagingResponse()

    if num_media > 0:
        media_url = request.values.get("MediaUrl0")
        content_type = request.values.get("MediaContentType0")
        
        if "image" in content_type:
            imagem = requests.get(media_url)
            nome_arquivo = "imagem_recebida.jpg"
            with open(nome_arquivo, 'wb') as f:
                f.write(imagem.content)

            resposta = detectar_praga(nome_arquivo)
        else:
            resposta = "Por favor, envie apenas imagens para análise."

    elif 'tempo' in incoming_msg:
        partes = incoming_msg.split()
        cidade = ' '.join(partes[1:]) if len(partes) > 1 else 'Ribeirão Preto'
        resposta = get_weather(cidade)

    elif 'dólar' in incoming_msg or 'dolar' in incoming_msg:
        resposta = get_dollar()

    else:
        resposta = (
            "👋 Olá! Eu sou seu assistente agrícola no WhatsApp:\n\n"
            "📍 Envie *tempo Ribeirão Preto* para previsão\n"
            "💵 Envie *dólar* para saber a cotação\n"
            "🌿 Envie uma *foto de planta ou folha* para detectar pragas ou doenças!"
        )

    resp.message(resposta)
    return str(resp)

if __name__ == '__main__':
    app.run(debug=True, port=5000)