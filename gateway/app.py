from flask import Flask, request, jsonify
import threading
import paho.mqtt.client as mqtt
import grpc
from concurrent import futures
import websockets
import asyncio
import json

app = Flask(__name__)

# Configuración MQTT
MQTT_BROKER = "mqtt-broker"
MQTT_PORT = 1883
MQTT_TOPIC = "healthcare/sensor_data"

# Cliente MQTT
mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_BROKER, MQTT_PORT)

# REST Endpoint para temperatura
@app.route('/temperature', methods=['POST'])
def handle_temperature():
    data = request.json
    print(f"Received temperature data: {data}")
    
    # Publicar en MQTT
    mqtt_client.publish(MQTT_TOPIC, json.dumps(data))
    
    return jsonify({"status": "success"}), 200

# gRPC Service
import healthcare_pb2
import healthcare_pb2_grpc

class HealthcareService(healthcare_pb2_grpc.HealthcareServicer):
    def SendHeartRate(self, request, context):
        print(f"Received heart rate data: {request}")
        
        # Publicar en MQTT
        data = {
            "patient_id": request.patient_id,
            "sensor_type": "heart_rate",
            "value": request.heart_rate,
            "unit": "bpm"
        }
        mqtt_client.publish(MQTT_TOPIC, json.dumps(data))
        
        return healthcare_pb2.HealthResponse(status="success")

def serve_grpc():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    healthcare_pb2_grpc.add_HealthcareServicer_to_server(HealthcareService(), server)
    server.add_insecure_port('[::]:5001')
    server.start()
    server.wait_for_termination()

# WebSocket para presión arterial
async def handle_bloodpressure(websocket, path):
    async for message in websocket:
        data = json.loads(message)
        print(f"Received blood pressure data: {data}")
        
        # Publicar en MQTT
        mqtt_client.publish(MQTT_TOPIC, json.dumps(data))

def start_websocket():
    asyncio.set_event_loop(asyncio.new_event_loop())
    server = websockets.serve(handle_bloodpressure, "0.0.0.0", 5002)
    asyncio.get_event_loop().run_until_complete(server)
    asyncio.get_event_loop().run_forever()

if __name__ == '__main__':
    # Iniciar servidor gRPC en un hilo separado
    grpc_thread = threading.Thread(target=serve_grpc)
    grpc_thread.start()
    
    # Iniciar WebSocket en un hilo separado
    ws_thread = threading.Thread(target=start_websocket)
    ws_thread.start()
    
    # Iniciar servidor REST Flask
    app.run(host='0.0.0.0', port=5000)