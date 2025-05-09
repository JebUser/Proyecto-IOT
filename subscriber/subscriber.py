import paho.mqtt.client as mqtt
import psycopg2
import json
import os
import time

# Configuración de la base de datos
DB_HOST = os.getenv("POSTGRES_HOST", "postgres")
DB_USER = os.getenv("POSTGRES_USER", "admin")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "admin")
DB_NAME = os.getenv("POSTGRES_DB", "healthcare")

# Conexión a PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn

# Callback cuando se recibe un mensaje MQTT
def on_message(client, userdata, msg):
    print(f"Message received on topic {msg.topic}: {msg.payload.decode()}")
    
    conn = None
    cur = None
    try:
        data = json.loads(msg.payload.decode())
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Insertar datos (value ya viene en formato string desde los sensores)
        cur.execute(
            "INSERT INTO sensor_readings (patient_id, sensor_type, value, unit) VALUES (%s, %s, %s, %s)",
            (data['patient_id'], data['sensor_type'], str(data['value']), data.get('unit', ''))
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
MQTT_TOPIC = "healthcare/sensor_data"

# Configurar cliente MQTT
client = mqtt.Client()
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT)
client.subscribe(MQTT_TOPIC)

print("Subscriber started. Waiting for messages...")
client.loop_forever()