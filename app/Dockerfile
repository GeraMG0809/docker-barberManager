# Usamos una imagen base de Python
FROM python:3.9-slim

# Definimos el directorio de trabajo
WORKDIR /app

# Copiamos los archivos necesarios
COPY . /app

# Instalamos las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponemos el puerto
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "main.py"]
