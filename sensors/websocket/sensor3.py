import asyncio
import websockets
import json
import os
import random
from datetime import datetime, timezone

INTERVALO = int(os.getenv("INTERVALO_SEGUNDOS", 60))
GATEWAY_URL = os.getenv("WS_URL", "ws://iot-gateway:5002")

async def enviar_datos():
    async with websockets.connect(GATEWAY_URL) as websocket:
        while True:
            data = {
                "nombre_sensor": "sensor-ws-1",
                "fecha_registro": datetime.now(timezone.utc).isoformat(),
                "tipo_dato": "temperatura (°C)",
                "valor": round(random.uniform(36.0, 39.0), 2)
            }
            await websocket.send(json.dumps(data))
            print(f"Enviado: {data}")
            await asyncio.sleep(INTERVALO)

asyncio.run(enviar_datos())
