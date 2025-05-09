import asyncio
import websockets
import random
import json
import time
import os

GATEWAY_WS_URL = os.getenv("GATEWAY_WS_URL", "ws://localhost:5002/bloodpressure")
PATIENT_ID = os.getenv("PATIENT_ID", "3")

def generate_blood_pressure():
    systolic = random.randint(90, 140)
    diastolic = random.randint(60, 90)
    return systolic, diastolic

async def send_blood_pressure():
    while True:
        systolic, diastolic = generate_blood_pressure()
        data = {
            "patient_id": PATIENT_ID,
            "sensor_type": "blood_pressure",
            "value": f"{systolic}/{diastolic}",
            "unit": "mmHg"
        }
        
        try:
            async with websockets.connect(GATEWAY_WS_URL) as websocket:
                await websocket.send(json.dumps(data))
                print(f"Sent blood pressure: {systolic}/{diastolic}mmHg")
        except Exception as e:
            print(f"Error sending blood pressure: {e}")
        
        await asyncio.sleep(15)  # Enviar cada 15 segundos

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(send_blood_pressure())