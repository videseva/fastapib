# Etapa 1: Crear la imagen de la aplicación
FROM python:3.10.12 as app-builder

WORKDIR /app

# Crea un entorno virtual
RUN python3 -m venv venv

# Instala las dependencias de la aplicación
RUN /app/venv/bin/pip install fastapi uvicorn sqlalchemy mysql-connector-python pymysql cryptography boto3 python-multipart

# Copia el código de la aplicación a la imagen
COPY . .

# Etapa 2: Crear la imagen final
FROM python:3.10.12

WORKDIR /app

# Copia el entorno virtual y el código de la etapa anterior
COPY --from=app-builder /app/venv /app/venv
COPY --from=app-builder /app /app

# Configura la base de datos MySQL
ENV DATABASE_URL=mysql+pymysql://root:12345@mysql_host/cloudtaller

# Expone el puerto en el que la aplicación FastAPI escucha (por defecto 8000)
EXPOSE 8000

# Comando para iniciar la aplicación FastAPI
CMD ["/app/venv/bin/uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
