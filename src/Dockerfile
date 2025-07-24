# Imagen base de Python
FROM python:3.10-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos al contenedor
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expone el puerto por donde saldrá la API
EXPOSE 8000

# Comando para arrancar la API
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
