from flask import Flask, render_template, request
import random

app = Flask(__name__)

# Lista de símbolos
symbols = [str(i) for i in range(1, 10)]

# Contador de tiros
spin_count = 0

@app.route('/')
def index():
    global spin_count  # Accede a la variable global

    # Reinicia el contador al iniciar el juego
    #if request.method == 'GET':
    #    spin_count = 0

    # Genera símbolos aleatorios para los 3 rollos
    reels = [random.choice(symbols) for _ in range(3)]

    # Verifica si hay una línea ganadora
    if reels[0] == reels[1] == reels[2]:
        winning_combo = reels[0]
        message = f"¡Ganaste! Combinación ganadora: {winning_combo} en {spin_count} tiros"
        spin_count = 0
    else:
        winning_combo = None
        message = "Sigue intentando..."

    # **Actualiza el contador de tiros antes de renderizar la plantilla**
    spin_count += 1

    return render_template('index.html', reels=reels, spin_count=spin_count, winning_combo=winning_combo, message=message)

if __name__ == '__main__':
    app.run(debug=True)
