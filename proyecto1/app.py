from flask import Flask
from my_blueprint.views import my_bp

# Inicializar la aplicación Flask
app = Flask(__name__)

# Registrar el blueprint
app.register_blueprint(my_bp)

if __name__ == '__main__':
    app.run(debug=True)