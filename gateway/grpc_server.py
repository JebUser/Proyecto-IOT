from concurrent import futures
import grpc
import sensor_pb2
import sensor_pb2_grpc
from mqtt_client import publicar_en_mqtt

class SensorService(sensor_pb2_grpc.SensorServiceServicer):
    def SendData(self, request, context):
        data = {
            "nombre_sensor": request.nombre_sensor,
            "timestamp": request.timestamp,
            "valor": request.valor
        }
        publicar_en_mqtt(data)
        return sensor_pb2.Response(status="ok")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sensor_pb2_grpc.add_SensorServiceServicer_to_server(SensorService(), server)
    server.add_insecure_port('[::]:5001')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
