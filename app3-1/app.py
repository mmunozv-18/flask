from flask import Flask, render_template, request, jsonify
import datetime
from flask_bootstrap import Bootstrap
from datetime import date

app = Flask(__name__)
Bootstrap(app)

# Rutas de las aplicaciones
@app.route('/')
def index():
    return render_template('base.html')

@app.route('/app1')
def app1():
    return render_template('base.html', app_name="App 1")

@app.route('/app2', methods=['GET', 'POST'])
def app2():
    if request.method == 'POST':
        name = request.form['name']
        birthdate = request.form['birthdate']
        data = {'name': name, 'birthdate': birthdate}
        return jsonify(data)
    return render_template('base.html', app_name="App 2")

@app.route('/app3')
def app3():
    return render_template('base.html', app_name="App 3")

if __name__ == '__main__':
    app.run(debug=True)