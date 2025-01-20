import hashlib
import redis
import os
from flask import Flask, request, render_template_string
import requests
import json

app = Flask(__name__)

# Conectar con Redis
cache = redis.StrictRedis(host='redis', port=6379, db=0, decode_responses=True)

# Dirección base de dnmonster
DNMONSTER_URL = "http://dnmonster:5000/monster/"  # nombre del servicio en docker-compose

# Página de inicio
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        if not name:
            return render_template_string(FORM_HTML, message="Por favor ingresa un nombre.")
        
        # Generar un hash del nombre
        name_hash = hashlib.md5(name.encode()).hexdigest()

        # Verificar si la imagen ya está en caché
        cached_image = cache.get(name_hash)
        if cached_image:
            return render_template_string(FORM_HTML, message="Imagen obtenida de caché.", image=cached_image)
        
        # Si no está en caché, generamos la imagen
        response = requests.get(f"{DNMONSTER_URL}{name_hash}")
        
        if response.status_code == 200:
            # Guardamos la imagen en caché
            cache.set(name_hash, response.text)
            return render_template_string(FORM_HTML, message="Imagen generada.", image=response.text)
        else:
            return render_template_string(FORM_HTML, message="Error al generar la imagen.")
    
    return render_template_string(FORM_HTML)

# HTML del formulario
FORM_HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Generador de Imagenes</title>
</head>
<body>
    <h1>Generador de Imágenes</h1>
    <form method="POST">
        <label for="name">Ingresa tu nombre:</label>
        <input type="text" name="name" id="name" required>
        <button type="submit">Generar Imagen</button>
    </form>
    <br>
    {% if message %}
        <p>{{ message }}</p>
    {% endif %}
    {% if image %}
        <h2>Imagen Generada:</h2>
        <pre>{{ image }}</pre>
    {% endif %}
</body>
</html>
"""

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
