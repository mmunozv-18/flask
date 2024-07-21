# app.py
from flask import Flask, render_template, request, jsonify, session
import openai
import google.generativeai as genai
import anthropic
import requests
import os
from dotenv import load_dotenv
import json

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Necesario para usar sesiones

# Configurar APIs
openai.api_key = os.getenv("OPENAI_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

# Función para obtener modelos disponibles de cada proveedor
def get_available_models():
    models = {
        "openai": [],
        "google": [],
        "anthropic": [],
        "groq": []
    }
    
    # OpenAI
    try:
        openai_models = openai.Model.list()
        models["openai"] = [model.id for model in openai_models.data if "gpt" in model.id.lower()]
    except Exception as e:
        print(f"Error al obtener modelos de OpenAI: {e}")
    
    # Google (Gemini)
    try:
        google_models = genai.list_models()
        models["google"] = [model.name for model in google_models if "gemini" in model.name.lower()]
    except Exception as e:
        print(f"Error al obtener modelos de Google: {e}")
    
    # Anthropic
    models["anthropic"] = ["claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-2.1", "claude-instant-1.2"]
    
    # Groq
    models["groq"] = ["llama3-70b-8192", "llama3-8b-8192", "mixtral-8x7b-32768", "gemma2-9b-it", "gemma-7b-it"]
    
    # Filtrar proveedores sin modelos
    models = {k: v for k, v in models.items() if v}
    
    return models

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_models')
def get_models():
    models = get_available_models()
    return jsonify(models)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    message = data['message']
    provider = data['provider']
    model = data['model']
    
    # Obtener el historial de la sesión o crear uno nuevo
    history = session.get('chat_history', [])
    
    # Añadir el mensaje del usuario al historial
    history.append({"role": "user", "content": message})
    
    try:
        if provider == 'openai':
            response = openai.ChatCompletion.create(
                model=model,
                messages=history
            )
            bot_response = response.choices[0].message.content
        
        elif provider == 'google':
            model = genai.GenerativeModel(model)
            chat = model.start_chat(history=history)
            response = chat.send_message(message)
            bot_response = response.text
        
        elif provider == 'anthropic':
            client = anthropic.Anthropic(api_key=anthropic_api_key)
            response = client.messages.create(
                model=model,
                max_tokens=1000,
                messages=history
            )
            bot_response = response.content[0].text
        
        elif provider == 'groq':
            headers = {
                "Authorization": f"Bearer {groq_api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": model,
                "messages": history
            }
            response = requests.post("https://api.groq.com/openai/v1/chat/completions", json=data, headers=headers)
            response.raise_for_status()
            bot_response = response.json()['choices'][0]['message']['content']
        
        # Añadir la respuesta del bot al historial
        history.append({"role": "assistant", "content": bot_response})
        
        # Guardar el historial actualizado en la sesión
        session['chat_history'] = history
        
        return jsonify({"response": bot_response, "history": history})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/clear_history', methods=['POST'])
def clear_history():
    session.pop('chat_history', None)
    return jsonify({"message": "Historial borrado"})

if __name__ == '__main__':
    app.run(debug=True)