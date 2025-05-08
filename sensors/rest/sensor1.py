import time
import requests
import json
from datetime import datetime, timezone
import random

GATEWAY_URL = "http://iot-gateway:5000/data"

def generar_dato():
    return {
        "nombre_sensor": "sensor-rest-1",
        "fecha_registro": datetime.now(timezone.utc).isoformat(),
        "tipo_dato": "temperatura (°C)",
        "valor": round(random.uniform(36.0, 39.0), 2)
    }

while True:
    data = generar_dato()
    try:
        res = requests.post(GATEWAY_URL, json=data)
        print(f"Enviado: {data} -> status {res.status_code}")
    except Exception as e:
        print(f"Error al enviar: {e}")
    time.sleep(3)
