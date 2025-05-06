import grpc
import time
import random
from datetime import datetime
import sensor_pb2
import sensor_pb2_grpc

GATEWAY_HOST = "iot-gateway:5001"

def generar_dato():
    return sensor_pb2.SensorData(
        nombre_sensor="sensor-grpc-1",
        timestamp=datetime.utcnow().isoformat(),
        valor=round(random.uniform(36.0, 39.0), 2)
    )

def run():
    with grpc.insecure_channel(GATEWAY_HOST) as channel:
        stub = sensor_pb2_grpc.SensorServiceStub(channel)
        while True:
            data = generar_dato()
            response = stub.SendData(data)
            print(f"Enviado {data} -> {response.status}")
            time.sleep(3)

if __name__ == '__main__':
    run()
