import socket
import threading
import subprocess
import psutil
import os
import sys
import multiprocessing
from flask import Flask, render_template

HOST = '0.0.0.0'
PORT = 65432
MAX_TASKS = 5
SLAVE_SERVERS = [('127.0.0.1', 65433)]

# Dossier courant pour les certificats SSL
CERT_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'certificats')
CERT_FILE = os.path.join(CERT_FOLDER, 'cert.pem')
KEY_FILE = os.path.join(CERT_FOLDER, 'key.pem')

def handle_client(conn, addr):
    with conn:
        print(f"Connecté par {addr}")
        program = b''
        while True:
            data = conn.recv(1024)
            if not data:
                break
            program += data

        # Surveillance de la charge
        cpu_usage = psutil.cpu_percent()
        num_tasks = threading.active_count()
        print(f"Utilisation CPU : {cpu_usage}%, Tâches en cours : {num_tasks}")

        if cpu_usage > 80 or num_tasks > MAX_TASKS:
            # Déléguer à un serveur esclave
            result = delegate_to_slave(program)
        else:
            # Exécuter localement
            result = execute_program(program)

        # Envoyer le résultat au client
        conn.sendall(result.encode('utf-8'))

def execute_program(program):
    try:
        # Exécution sécurisée du programme
        process = subprocess.run([sys.executable, '-c', program.decode('utf-8')], capture_output=True, text=True, timeout=10)
        return process.stdout + process.stderr
    except subprocess.TimeoutExpired:
        return "Erreur : Temps d'exécution dépassé."
    except Exception as e:
        return f"Erreur d'exécution : {e}"

def delegate_to_slave(program):
    for slave_host, slave_port in SLAVE_SERVERS:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((slave_host, slave_port))
                s.sendall(program)
                result = s.recv(4096).decode('utf-8')
                return result
        except Exception as e:
            print(f"Erreur avec le serveur esclave {slave_host}:{slave_port} - {e}")
            continue
    return "Aucun serveur esclave disponible."

def start_server():
    import ssl
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        with context.wrap_socket(s, server_side=True) as ssock:
            print(f"Serveur maître sécurisé en écoute sur {HOST}:{PORT}")
            while True:
                conn, addr = ssock.accept()
                threading.Thread(target=handle_client, args=(conn, addr)).start()

def start_monitoring():
    app = Flask(__name__, template_folder='templates')

    @app.route('/')
    def index():
        cpu_usage = psutil.cpu_percent()
        num_tasks = threading.active_count()
        return render_template('index.html', cpu_usage=cpu_usage, num_tasks=num_tasks)

    app.run(port=5000)

def main():
    # Démarrer le monitoring dans un processus séparé
    monitoring_process = multiprocessing.Process(target=start_monitoring)
    monitoring_process.start()

    start_server()

    # Arrêter le monitoring lorsque le serveur s'arrête
    monitoring_process.terminate()

if __name__ == '__main__':
    main()
