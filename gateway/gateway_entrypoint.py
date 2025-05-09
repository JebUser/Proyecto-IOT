import multiprocessing
import subprocess

def run_rest():
    subprocess.run(["python", "rest_server.py"])

def run_grpc():
    subprocess.run(["python", "grpc_server.py"])

def run_websocket():
    subprocess.run(["python", "websocket_server.py"])

if __name__ == "__main__":
    multiprocessing.Process(target=run_rest).start()
    multiprocessing.Process(target=run_grpc).start()
    multiprocessing.Process(target=run_websocket).start()
