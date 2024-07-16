from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
app.config['DATABASE'] = os.path.join(app.root_path, 'cimol.db')

def get_db_connection():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    ets = conn.execute('SELECT * FROM ets').fetchall()
    conn.close()
    return render_template('index.html', ets=ets)

@app.route('/add', methods=('GET', 'POST'))
def add():
    if request.method == 'POST':
        vivienda = request.form['vivienda']
        codigopartida = request.form['codigopartida']
        descripcion = request.form['descripcion']
        detalle = request.form['detalle']
        caracteristicas = request.form['caracteristicas']

        conn = get_db_connection()
        conn.execute('INSERT INTO ets (vivienda, codigopartida, descripcion, detalle, caracteristicas) VALUES (?, ?, ?, ?, ?)',
                     (vivienda, codigopartida, descripcion, detalle, caracteristicas))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('edit.html')

@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit(id):
    conn = get_db_connection()
    ets = conn.execute('SELECT * FROM ets WHERE id = ?', (id,)).fetchone()
    conn.close()

    if request.method == 'POST':
        vivienda = request.form['vivienda']
        codigopartida = request.form['codigopartida']
        descripcion = request.form['descripcion']
        detalle = request.form['detalle']
        caracteristicas = request.form['caracteristicas']

        conn = get_db_connection()
        conn.execute('UPDATE ets SET vivienda = ?, codigopartida = ?, descripcion = ?, detalle = ?, caracteristicas = ? WHERE id = ?',
                     (vivienda, codigopartida, descripcion, detalle, caracteristicas, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('edit.html', ets=ets)

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM ets WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

def init_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    with open('schema.sql') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()

if __name__ == '__main__':
    if not os.path.exists(app.config['DATABASE']):
        init_db()
    app.run(debug=True)