from flask import Blueprint, render_template

# Crear un blueprint
my_bp = Blueprint('my_bp', __name__, template_folder='../templates')

# Definir la ruta para "Hola Mundo"
@my_bp.route('/')
def hello():
    return render_template('hello.html')