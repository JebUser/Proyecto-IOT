import grpc
import healthcare_pb2
import healthcare_pb2_grpc
import random
import time
import os

GATEWAY_HOST = os.getenv("GATEWAY_HOST", "localhost")
GATEWAY_PORT = os.getenv("GATEWAY_PORT", "5001")
PATIENT_ID = int(os.getenv("PATIENT_ID", "2"))

def generate_heart_rate():
    return random.randint(60, 120)

def send_heart_rate():
    channel = grpc.insecure_channel(f"{GATEWAY_HOST}:{GATEWAY_PORT}")
    stub = healthcare_pb2_grpc.HealthcareStub(channel)
    
    while True:
        heart_rate = generate_heart_rate()
        request = healthcare_pb2.HeartRateRequest(
            patient_id=PATIENT_ID,
            heart_rate=heart_rate
        )
        
        try:
            response = stub.SendHeartRate(request)
            print(f"Sent heart rate: {heart_rate}bpm - Status: {response.status}")
        except Exception as e:
            print(f"Error sending heart rate: {e}")
        
        time.sleep(5)  # Enviar cada 5 segundos

if __name__ == '__main__':
    send_heart_rate()