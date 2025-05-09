FROM python:3.9-slim

WORKDIR /app

# Instalar dependencias primero
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar archivos fuente
COPY . .

# Generar archivos gRPC durante el build
RUN pip install grpcio-tools && \
    python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. healthcare.proto

CMD ["python", "app.py"]