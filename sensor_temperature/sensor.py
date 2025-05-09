import requests
import random
import time
import os
import json

GATEWAY_URL = os.getenv("GATEWAY_URL", "http://localhost:5000/temperature")
PATIENT_ID = os.getenv("PATIENT_ID", "1")

def generate_temperature():
    return round(random.uniform(36.0, 39.5), 1)

def send_temperature():
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