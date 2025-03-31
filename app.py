from flask import Flask, request, jsonify
import openai
import os
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

openai.api_key = os.getenv("OPENAI_API_KEY")

# Configuración de Twilio: las variables deben estar definidas en el entorno
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
MY_PHONE_NUMBER = os.getenv("MY_PHONE_NUMBER")

def send_sms(body):
    url = f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}/Messages.json"
    data = {
        "From": TWILIO_PHONE_NUMBER,
        "To": MY_PHONE_NUMBER,
        "Body": body
    }
    response = requests.post(url, data=data, auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN))
    return response.json()

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message', '')
    if not user_input:
        return jsonify({'reply': 'No se recibió ningún mensaje.'})
    
    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {
                    'role': 'system', 
                    'content': (
                        'Eres un asistente amigable que ayuda a empresarios con soluciones inteligentes. '
                        'Responde de manera natural y profesional. Si detectas que el usuario muestra interés en '
                        'contactarse (por ejemplo, menciona "llamar", "hablar" o "contactar"), sugiere enviar un correo '
                        'y notifica al administrador mediante SMS para que se contacte con el cliente en menos de 24 horas.'
                    )
                },
                {'role': 'user', 'content': user_input}
            ]
        )
        reply = response['choices'][0]['message']['content']
        
        # Ejemplo: si la respuesta contiene palabras clave, enviamos un SMS
        if any(word in reply.lower() for word in ["llamar", "hablar", "contactar"]):
            sms_body = f"Nuevo mensaje de cliente: {user_input}"
            send_sms(sms_body)
        
        return jsonify({'reply': reply})
    except Exception as e:
        return jsonify({'reply': f'Error al conectar con ChatGPT: {str(e)}'})

@app.route('/')
def home():
    return 'SIBIA chatbot backend funcionando.'

if __name__ == '__main__':
    app.run(debug=True)
