from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import openai
import google.generativeai as genai
import anthropic
import requests
import os
from dotenv import load_dotenv, find_dotenv
import json
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

load_dotenv(find_dotenv())

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Configurar APIs
openai.api_key = os.getenv("OPENAI_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
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
        models["openai"] = [model.id for model in openai.Model.list().data if "gpt" in model.id.lower()]
    except Exception as e:
        print(f"Error al obtener modelos de OpenAI: {e}")
    
    # Google (Gemini)
    try:
        models["google"] = [model.name for model in genai.list_models() if "gemini" in model.name.lower()]
    except Exception as e:
        print(f"Error al obtener modelos de Google: {e}")
    
    # Anthropic
    try:
        models["anthropic"] = [model.name for model in anthropic.Client(api_key=anthropic_api_key).models.list().models if "claude" in model.name.lower()]
    except Exception as e:
        print(f"Error al obtener modelos de Anthropic: {e}")
    
    # Groq
    models["groq"] = ["llama3-70b-8192", "llama3-8b-8192", "mixtral-8x7b-32768", "gemma2-9b-it", "gemma-7b-it"]
    
    # Filtrar proveedores sin modelos
    models = {k: v for k, v in models.items() if v}
    
    return models

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Usuario o contraseña incorrectos')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user:
            return render_template('register.html', error='El usuario ya existe')
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# ... (Código para obtener modelos disponibles, como en el ejemplo anterior) ...

@app.route('/get_models')
def get_models():
    models = get_available_models()
    return jsonify(models)

@app.route('/chat', methods=['POST'])
@login_required
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
            # Asegúrate de que la respuesta sea un string antes de agregarla
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
@login_required
def clear_history():
    session.pop('chat_history', None)
    return jsonify({"message": "Historial borrado"})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)