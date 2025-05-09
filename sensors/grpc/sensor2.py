import grpc
import time
import os
import random
from datetime import datetime, timezone
import sensor_pb2
import sensor_pb2_grpc

INTERVALO = int(os.getenv("INTERVALO_SEGUNDOS", 60))
GATEWAY_HOST = os.getenv("GRPC_HOST", "iot-gateway:5001")

def generar_dato():
    return sensor_pb2.SensorData(
        nombre_sensor="sensor-grpc-1",
        fecha_registro=datetime.now(timezone.utc).isoformat(),
        tipo_dato="presión arterial sistólica (mmHg)",
        valor=round(random.uniform(100, 140), 2)
    )

def run():
    with grpc.insecure_channel(GATEWAY_HOST) as channel:
        stub = sensor_pb2_grpc.SensorServiceStub(channel)
        while True:
            try:
                data = generar_dato()
                response = stub.SendData(data)
                print(f"[✓] Enviado: {data} → {response.status}")
            except Exception as e:
                print(f"[✗] Error gRPC: {e}")
            time.sleep(INTERVALO)

if __name__ == '__main__':
    run()
