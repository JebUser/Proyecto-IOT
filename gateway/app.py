"""
Gateway IoT multiprotocolo para el sistema de monitoreo de salud.

Este módulo implementa un gateway que soporta múltiples protocolos de comunicación:
- REST API para datos de temperatura
- gRPC para datos de ritmo cardíaco
- WebSocket para datos de presión arterial

Todos los datos recibidos son normalizados y publicados a través de MQTT.
"""

from flask import Flask, request, jsonify
import threading
import paho.mqtt.client as mqtt
import grpc
from concurrent import futures
import websockets
import asyncio
import json
import os

app = Flask(__name__)

# Configuración MQTT
MQTT_BROKER = "mqtt-broker"
MQTT_PORT = 1883

# Prefijo general para tópicos MQTT
MQTT_PREFIX = os.getenv("MQTT_PREFIX", "data/healthcare")

# Mapeo de tipos de sensor a nombres normalizados
SENSOR_TYPE_MAP = {
    "temperature": "body_temperature",
    "heart_rate": "cardiac_rhythm",
    "blood_pressure": "arterial_pressure"
}

# Cliente MQTT
mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_BROKER, MQTT_PORT)

def publish_to_mqtt(patient_id, sensor_type, value):
    """
    Publica datos en MQTT con el formato de tópico nuevo.
    
    Args:
        patient_id: ID del paciente
        sensor_type: Tipo de sensor
        value: Valor de la lectura
    """
    sensor_name = SENSOR_TYPE_MAP.get(sensor_type)
    if not sensor_name:
        print(f"Error: tipo de sensor desconocido {sensor_type}")
        return
        
    topic = f"{MQTT_PREFIX}/patients/{patient_id}/sensors/{sensor_name}"
    data = {"value": value}
    
    mqtt_client.publish(topic, json.dumps(data))
    print(f"Published to {topic}: {data}")

# REST Endpoint para temperatura
@app.route('/temperature', methods=['POST'])
def handle_temperature():
    """
    Endpoint REST que recibe datos de temperatura y los publica en MQTT.
    
    Espera un JSON con el formato:
    {
        "patient_id": str,
        "value": str
    }
    
    Returns:
        tuple: (JSON response, HTTP status code)
    """
    data = request.json
    print(f"Received temperature data: {data}")
    
    # Publicar en MQTT con el nuevo formato de tópico
    publish_to_mqtt(data["patient_id"], "temperature", data["value"])
    
    return jsonify({"status": "success"}), 200

# gRPC Service
import healthcare_pb2
import healthcare_pb2_grpc

class HealthcareService(healthcare_pb2_grpc.HealthcareServicer):
    """Implementación del servicio gRPC para datos de ritmo cardíaco."""
    
    def SendHeartRate(self, request, context):
        """
        Maneja las solicitudes gRPC de datos de ritmo cardíaco.
        
        Args:
            request: Objeto HeartRateRequest con patient_id y heart_rate
            context: Contexto gRPC
            
        Returns:
            HealthResponse: Respuesta con estado de la operación
        """
        print(f"Received heart rate data: {request}")
        
        # Publicar en MQTT con el nuevo formato de tópico
        publish_to_mqtt(str(request.patient_id), "heart_rate", str(request.heart_rate))
        
        return healthcare_pb2.HealthResponse(status="success")

def serve_grpc():
    """Inicia el servidor gRPC en el puerto 5001."""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    healthcare_pb2_grpc.add_HealthcareServicer_to_server(HealthcareService(), server)
    server.add_insecure_port('[::]:5001')
    server.start()
    server.wait_for_termination()

# WebSocket para presión arterial
async def handle_bloodpressure(websocket, path):
    """
    Maneja conexiones WebSocket para datos de presión arterial.
    
    Args:
        websocket: Objeto WebSocket para la conexión
        path: Ruta de la conexión WebSocket
    """
    async for message in websocket:
        data = json.loads(message)
        print(f"Received blood pressure data: {data}")
        
        # Publicar en MQTT con el nuevo formato de tópico
        publish_to_mqtt(data["patient_id"], "blood_pressure", data["value"])

def start_websocket():
    """Inicia el servidor WebSocket en el puerto 5002."""
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