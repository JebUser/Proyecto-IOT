import paho.mqtt.client as mqtt
import json
import psycopg2
from datetime import datetime

# Configuración MQTT
MQTT_BROKER = "mosquitto"
MQTT_PORT = 1883
MQTT_TOPIC = "sensores/datos"

# Configuración PostgreSQL
DB_HOST = "postgres"
DB_NAME = "sensores"
DB_USER = "user"
DB_PASSWORD = "pass"

# Conexión inicial a PostgreSQL
conn = psycopg2.connect(
    host=DB_HOST,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)
cursor = conn.cursor()

def insertar_dato(nombre_sensor, timestamp, valor):
    cursor.execute("""
        INSERT INTO lecturas (nombre_sensor, timestamp, valor)
        VALUES (%s, %s, %s)
    """, (nombre_sensor, timestamp, valor))
    conn.commit()

def on_connect(client, userdata, flags, rc):
    print("Conectado a MQTT con código", rc)
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        nombre = data.get("nombre_sensor")
        timestamp = data.get("timestamp") or datetime.utcnow().isoformat()
        valor = data.get("valor")
        print(f"Recibido: {data}")
        insertar_dato(nombre, timestamp, valor)
    except Exception as e:
        print(f"Error procesando mensaje: {e}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()
