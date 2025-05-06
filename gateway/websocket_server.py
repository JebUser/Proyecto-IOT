import asyncio
import websockets
import json
from mqtt_client import publicar_en_mqtt

async def manejar_cliente(websocket, path):
    async for mensaje in websocket:
        try:
            data = json.loads(mensaje)
            publicar_en_mqtt(data)
        except Exception as e:
            print(f"Error procesando mensaje: {e}")

start_server = websockets.serve(manejar_cliente, "0.0.0.0", 5002)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
