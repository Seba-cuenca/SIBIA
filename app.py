from flask import Flask, request, jsonify
import openai
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message', '')
    if not user_input:
        return jsonify({'reply': 'No se recibió ningún mensaje.'})
    
    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {'role': 'system', 'content': 'Sos un asistente amigable que ayuda a empresarios con soluciones inteligentes.'},
                {'role': 'user', 'content': user_input}
            ]
        )
        reply = response['choices'][0]['message']['content']
        return jsonify({'reply': reply})
    except Exception as e:
        return jsonify({'reply': f'Error al conectar con ChatGPT: {str(e)}'})
        
@app.route('/')
def home():
    return 'SIBIA chatbot backend funcionando.'

if __name__ == '__main__':
    app.run(debug=True)