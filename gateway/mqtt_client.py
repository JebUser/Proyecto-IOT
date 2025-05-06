import paho.mqtt.client as mqtt
import json

MQTT_BROKER = "mosquitto"
MQTT_PORT = 1883
MQTT_TOPIC = "sensores/datos"

def publicar_en_mqtt(data):
    client = mqtt.Client()
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.publish(MQTT_TOPIC, json.dumps(data))
    client.disconnect()
