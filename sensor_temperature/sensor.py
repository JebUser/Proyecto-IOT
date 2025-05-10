"""
Sensor simulado de temperatura corporal.

Este módulo simula un sensor de temperatura que:
1. Genera lecturas aleatorias de temperatura corporal
2. Envía los datos al gateway a través de REST API
3. Opera de forma continua con intervalos de 10 segundos

Las temperaturas generadas están en el rango normal del cuerpo humano (36.0°C - 39.5°C)
"""

import requests
import random
import time
import os
import json

GATEWAY_URL = os.getenv("GATEWAY_URL", "http://localhost:5000/temperature")
PATIENT_ID = os.getenv("PATIENT_ID", "1")

def generate_temperature():
    """
    Genera una temperatura corporal aleatoria.
    
    Returns:
        float: Temperatura en grados Celsius (36.0°C - 39.5°C)
    """
    return round(random.uniform(36.0, 39.5), 1)

def send_temperature():
    """
    Función principal que genera y envía datos de temperatura continuamente.
    
    Envía datos cada 10 segundos al gateway mediante POST request.
    Los datos incluyen:
    - ID del paciente
    - Tipo de sensor (temperature)
    - Valor de temperatura
    - Unidad de medida (°C)
    """
    while True:
        temp = generate_temperature()
        data = {
            "patient_id": PATIENT_ID,
            "sensor_type": "temperature",
            "value": str(temp),
            "unit": "°C"
        }
        
        try:
            response = requests.post(GATEWAY_URL, json=data)
            print(f"Sent temperature: {temp}°C - Status: {response.status_code}")
        except Exception as e:
            print(f"Error sending temperature: {e}")
        
        time.sleep(10)  # Enviar cada 10 segundos

if __name__ == '__main__':
    send_temperature()