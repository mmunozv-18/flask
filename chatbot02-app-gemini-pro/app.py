from flask import Flask, render_template, request, jsonify
import os
import openai  # Asegúrate de tener instalada la librería openai: pip install openai

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Configuración inicial, puedes agregar más modelos aquí
MODELOS_DISPONIBLES = {
    "openai": {
        "nombre": "OpenAI GPT-3.5",
        "api_key": os.environ.get("OPENAI_API_KEY"),  # Obtener la clave API de las variables de entorno
    },
    # "gemini": {
    #     "nombre": "Google Gemini",
    #     "api_key": os.environ.get("GEMINI_API_KEY"),
    # },
    # # Agrega más modelos aquí (Groq, Antropic, etc.)
}

# Modelo seleccionado por defecto
modelo_seleccionado = "openai"

@app.route("/")
def index():
    """Renderiza la plantilla HTML principal."""
    return render_template(
        "index.html", modelos=MODELOS_DISPONIBLES, modelo_seleccionado=modelo_seleccionado
    )

@app.route("/obtener_respuesta", methods=["POST"])
def obtener_respuesta():
    """Procesa las solicitudes del usuario y devuelve la respuesta del modelo."""
    datos = request.get_json()
    mensaje_usuario = datos.get("mensaje")

    try:
        # Obtener el modelo seleccionado
        modelo = MODELOS_DISPONIBLES.get(modelo_seleccionado)

        if modelo is None:
            raise ValueError("Modelo no encontrado.")

        # Realizar la llamada a la API del modelo seleccionado
        if modelo_seleccionado == "openai":
            openai.api_key = modelo["api_key"]
            respuesta = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Eres un chatbot amigable."},
                    {"role": "user", "content": mensaje_usuario},
                ],
            )
            respuesta_modelo = respuesta.choices[0].message.content
        # elif modelo_seleccionado == "gemini":
        #     # Implementa la llamada a la API de Gemini aquí
        #     pass
        # # Agrega la lógica para otros modelos (Groq, Antropic, etc.)
        else:
            raise ValueError("Modelo no soportado.")

        return jsonify({"respuesta": respuesta_modelo, "error": None})
    except Exception as e:
        return jsonify({"respuesta": None, "error": str(e)})

@app.route("/cambiar_modelo", methods=["POST"])
def cambiar_modelo():
    """Cambia el modelo de lenguaje a utilizar."""
    global modelo_seleccionado
    datos = request.get_json()
    nuevo_modelo = datos.get("modelo")

    if nuevo_modelo in MODELOS_DISPONIBLES:
        modelo_seleccionado = nuevo_modelo
        return jsonify(
            {
                "mensaje": f"Modelo cambiado a: {MODELOS_DISPONIBLES[nuevo_modelo]['nombre']}"
            }
        )
    else:
        return jsonify({"error": "Modelo inválido."})

if __name__ == "__main__":
    app.run(debug=True)