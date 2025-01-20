# Usamos la imagen oficial de Python como base
FROM python:3.8-slim

# Establecemos el directorio de trabajo
WORKDIR /app

# Copiamos los archivos necesarios al contenedor
COPY . /app

# Instalamos las dependencias necesarias
RUN pip install --no-cache-dir -r requirements.txt

# Exponemos el puerto que utilizaremos en Flask
EXPOSE 5000

# Definimos el comando para ejecutar la aplicación
CMD ["python", "identidock.py"]
