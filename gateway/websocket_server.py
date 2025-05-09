import asyncio
import websockets
import json
from mqtt_client import publicar_en_mqtt

async def manejar_cliente(websocket, path):
    async for mensaje in websocket:
        try:
            data = json.loads(mensaje)
            publicar_en_mqtt(data)
            print(f"[✓] Dato recibido por WebSocket: {data}")
        except Exception as e:
            print(f"[✗] Error procesando mensaje: {e}")

async def main():
    async with websockets.serve(manejar_cliente, "0.0.0.0", 5002):
        print("Servidor WebSocket corriendo en puerto 5002")
        await asyncio.Future()  # espera infinita

if __name__ == '__main__':
    asyncio.run(main())
