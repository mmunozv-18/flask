from flask import Flask

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return '<h1>Pagina de Inicio</h1>'

@app.route('/hello')
@app.route('/hello/<name>')
@app.route('/hello/<name>/<int:age>')
def hello(name = None, age = None):
    if name == None and age == None:
        return '<h2>Hola Mundo</h2>'
    elif age ==None:
        return f'<h2>Hola, {name}!</h2>'
    else:
        return f'<h2>Hola, {name} el doble de tu edad es {age * 2}</h2>'

from markupsafe import escape
@app.route('/code/<path:code>')
def code(code):
    return f'<code>{escape(code)}</code>'

