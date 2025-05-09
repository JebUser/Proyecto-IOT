FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY sensor.proto .
RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. sensor.proto

COPY sensor2.py .

CMD ["python", "sensor2.py"]
