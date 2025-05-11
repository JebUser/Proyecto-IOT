"""
Subscriber MQTT para el sistema de monitoreo de salud.

Este módulo implementa un subscriber MQTT que:
1. Se suscribe al tópico de datos de salud
2. Procesa los mensajes recibidos
3. Almacena los datos en PostgreSQL

Los datos son almacenados en la tabla 'sensor_readings' con timestamp automático.
"""

import paho.mqtt.client as mqtt
import psycopg2
import json
import os
import time
import re

# Configuración de la base de datos
DB_HOST = os.getenv("POSTGRES_HOST", "postgres")
DB_USER = os.getenv("POSTGRES_USER", "admin")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "admin")
DB_NAME = os.getenv("POSTGRES_DB", "healthcare")

# Mapeo de nombres normalizados de sensor a IDs
SENSOR_NAME_MAP = {
    "body_temperature": 1,  # Temperatura Corporal
    "cardiac_rhythm": 2,    # Ritmo Cardíaco
    "arterial_pressure": 3  # Presión Arterial
}

# Prefijo general para tópicos MQTT
MQTT_PREFIX = os.getenv("MQTT_PREFIX", "data/healthcare")
MQTT_TOPIC_PATTERN = f"{MQTT_PREFIX}/patients/+/sensors/+"

def get_db_connection():
    """
    Establece y retorna una conexión a la base de datos PostgreSQL.
    
    Returns:
        psycopg2.connection: Objeto de conexión a PostgreSQL
        
    Raises:
        psycopg2.Error: Si hay un error en la conexión
    """
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn

def on_message(client, userdata, msg):
    """
    Callback que se ejecuta cuando se recibe un mensaje MQTT.
    
    Procesa el mensaje y almacena los datos en PostgreSQL.
    
    Args:
        client: Cliente MQTT
        userdata: Datos de usuario (no utilizados)
        msg: Mensaje MQTT recibido
    """
    print(f"Message received on topic {msg.topic}: {msg.payload.decode()}")
    
    # Extraer patient_id y sensor_name del tópico
    topic_pattern = re.compile(f"{MQTT_PREFIX}/patients/(\d+)/sensors/(\w+)")
    match = topic_pattern.match(msg.topic)
    
    if not match:
        print(f"Error: formato de tópico incorrecto: {msg.topic}")
        return
        
    patient_id = match.group(1)
    sensor_name = match.group(2)
    sensor_id = SENSOR_NAME_MAP.get(sensor_name)
    
    if not sensor_id:
        print(f"Error: sensor desconocido {sensor_name}")
        return
    
    conn = None
    cur = None
    try:
        data = json.loads(msg.payload.decode())
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Insertar datos usando sensor_id extraído del tópico
        cur.execute(
            "INSERT INTO sensor_readings (patient_id, sensor_id, value) VALUES (%s, %s, %s)",
            (patient_id, sensor_id, str(data['value']))
        )
        
        conn.commit()
        print("Data saved to PostgreSQL")
    except Exception as e:
        print(f"Error processing message: {e}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

# Configuración MQTT
MQTT_BROKER = os.getenv("MQTT_BROKER", "mqtt-broker")
MQTT_PORT = 1883

# Configurar cliente MQTT
client = mqtt.Client()
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT)
client.subscribe(MQTT_TOPIC_PATTERN)

print(f"Subscriber started. Waiting for messages on topic {MQTT_TOPIC_PATTERN}...")
client.loop_forever()