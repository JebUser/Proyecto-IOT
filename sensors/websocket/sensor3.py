import asyncio
import websockets
import json
from datetime import datetime
import random

GATEWAY_URI = "ws://iot-gateway:5002"

async def enviar_datos():
    async with websockets.connect(GATEWAY_URI) as websocket:
        while True:
            data = {
                "nombre_sensor": "sensor-ws-1",
                "timestamp": datetime.utcnow().isoformat(),
                "valor": round(random.uniform(36.0, 39.0), 2)
            }
            await websocket.send(json.dumps(data))
            print(f"Enviado: {data}")
            await asyncio.sleep(3)

asyncio.run(enviar_datos())
