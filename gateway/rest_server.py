from flask import Flask, request, jsonify
from mqtt_client import publicar_en_mqtt

app = Flask(__name__)

@app.route("/data", methods=["POST"])
def recibir_dato():
    data = request.get_json()
    if data:
        publicar_en_mqtt(data)
        return jsonify({"status": "ok"}), 200
    return jsonify({"error": "No data"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
