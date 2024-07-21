from flask import Flask, render_template, request, jsonify
import os
import openai
import anthropic
import requests

app = Flask(__name__)

# Configura la API de OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Configura la API de Anthropic
anthropic.api_key = os.getenv("ANTHROPIC_API_KEY")

# Configura la API de Gemini (reemplaza con tu clave real)
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Define las opciones de modelos
models = {
    "gpt-3.5-turbo": "GPT-3.5 Turbo",
    "gpt-4": "GPT-4",
    "claude-2": "Claude-2",
    "gemini-pro": "Gemini Pro",
}

@app.route("/")
def index():
    return render_template("index.html", models=models)

@app.route("/chat", methods=["POST"])
def chat():
    model_name = request.form.get("model")
    message = request.form.get("message")

    # Selecciona el modelo y realiza la solicitud a la API
    if model_name == "gpt-3.5-turbo" or model_name == "gpt-4":
        response = openai.ChatCompletion.create(
            model=model_name,
            messages=[
                {"role": "user", "content": message}
            ]
        )
        response_text = response.choices[0].message.content
    elif model_name == "claude-2":
        response = anthropic.Client().completion(
            model="claude-2",
            prompt=message,
            max_tokens=1000
        )
        response_text = response.completion
    elif model_name == "gemini-pro":
        headers = {
            "Authorization": f"Bearer {gemini_api_key}",
            "Content-Type": "application/json",
        }
        data = {
            "model": "gemini-pro",
            "messages": [
                {"role": "user", "content": message}
            ],
            "temperature": 0.7,
            "max_tokens": 1000
        }
        response = requests.post("https://api.gemini.ai/v1/chat/completions", headers=headers, json=data)
        response_text = response.json()["choices"][0]["message"]["content"]
    else:
        return jsonify({"error": "Modelo no válido"})

    return jsonify({"response": response_text})

if __name__ == "__main__":
    app.run(debug=True)