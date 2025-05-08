import paho.mqtt.client as mqtt
import json
import psycopg2

# Configuración de conexión MQTT
MQTT_BROKER = "mqtt-broker"
MQTT_PORT = 1883
MQTT_TOPIC = "sensores/datos"

# Configuración de PostgreSQL
DB_HOST = "postgres-db"
DB_NAME = "health_data"
DB_USER = "iotuser"
DB_PASSWORD = "iotpass"

# Conexión a la base de datos
conn = psycopg2.connect(
    host=DB_HOST,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)
cursor = conn.cursor()

# Inserta un registro en la tabla lecturas
def insertar_dato(nombre_sensor, fecha_registro, tipo_dato, valor):
    cursor.execute("""
        INSERT INTO lecturas (nombre_sensor, fecha_registro, tipo_dato, valor, fecha_registro)
        VALUES (%s, %s, %s, %s)
    """, (nombre_sensor, fecha_registro, tipo_dato, valor))
    conn.commit()

# Al conectarse al broker MQTT
def on_connect(client, userdata, flags, rc):
    print("Conectado a MQTT con código de resultado", rc)
    client.subscribe(MQTT_TOPIC)

# Al recibir un mensaje MQTT
def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        data = json.loads(payload)

        nombre = data.get("nombre_sensor")
        tipo = data.get("tipo_dato")
        valor = data.get("valor")

        if nombre and tipo and valor is not None:
            print(f"[✓] Dato recibido de {nombre} ({tipo}): {valor}")
            insertar_dato(nombre, tipo, valor)
        else:
            print(f"[!] JSON incompleto: {data}")
    except Exception as e:
        print(f"[✗] Error al procesar mensaje: {e}")

# Inicializar cliente MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()
