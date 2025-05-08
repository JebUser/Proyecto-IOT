import asyncio
import websockets
import json
from datetime import datetime, timezone
import random

GATEWAY_URI = "ws://iot-gateway:5002"

async def enviar_datos():
    async with websockets.connect(GATEWAY_URI) as websocket:
        while True:
            data = {
                "nombre_sensor": "sensor-ws-1",
                "fecha_registro": datetime.now(timezone.utc).isoformat(),
                "tipo_valor": "presion arterial sistolica (mmHg)",
                "valor": round(random.uniform(100.0, 139.0), 2)
            }
            await websocket.send(json.dumps(data))
            print(f"Enviado: {data}")
            await asyncio.sleep(3)

asyncio.run(enviar_datos())
