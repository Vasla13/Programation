import socket
import threading
import subprocess
import psutil
import time
from tasks_queue import TaskQueue
from monitoring import start_monitoring_server

HOST = '0.0.0.0'  # Écoute sur toutes les interfaces réseau
PORT = 65432      # Port par défaut
MAX_TASKS = 5     # Nombre maximum de programmes en cours d'exécution

# Liste des serveurs esclaves
SLAVE_SERVERS = [('127.0.0.1', 65433)]  # À ajuster selon votre configuration

# File d'attente des tâches
task_queue = TaskQueue()

def handle_client(conn, addr):
    with conn:
        print(f"Connecté par {addr}")
        program = b''
        while True:
            data = conn.recv(1024)
            if not data:
                break
            program += data

        # Ajouter la tâche à la file d'attente
        task_queue.add_task(conn, program)

def execute_task(conn, program):
    try:
        # Exécution sécurisée du programme
        process = subprocess.run(['python', '-c', program.decode('utf-8')], capture_output=True, text=True, timeout=10)
        result = process.stdout + process.stderr
    except subprocess.TimeoutExpired:
        result = "Erreur : Temps d'exécution dépassé."
    except Exception as e:
        result = f"Erreur d'exécution : {e}"
    
    try:
        conn.sendall(result.encode('utf-8'))
    except:
        print("Erreur lors de l'envoi du résultat au client.")

def delegate_task(conn, program):
    for slave_host, slave_port in SLAVE_SERVERS:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((slave_host, slave_port))
                s.sendall(program)
                result = s.recv(4096).decode('utf-8')
                conn.sendall(result.encode('utf-8'))
                return
        except Exception as e:
            print(f"Erreur avec le serveur esclave {slave_host}:{slave_port} - {e}")
            continue
    # Si aucun esclave disponible, exécuter localement
    execute_task(conn, program)

def task_worker():
    while True:
        if task_queue.has_tasks():
            conn, program = task_queue.get_task()
            # Vérifier la charge du système
            cpu_usage = psutil.cpu_percent(interval=1)
            memory_usage = psutil.virtual_memory().percent
            current_tasks = threading.active_count() - 2  # Exclure les threads principaux

            print(f"CPU Usage: {cpu_usage}%, Memory Usage: {memory_usage}%, Current Tasks: {current_tasks}")

            if cpu_usage > 80 or current_tasks > MAX_TASKS:
                print("Délégation de la tâche à un serveur esclave.")
                delegate_task(conn, program)
            else:
                print("Exécution locale de la tâche.")
                execute_task(conn, program)
        else:
            time.sleep(1)

def start_server():
    # Démarrer le serveur de monitoring dans un thread séparé
    monitoring_thread = threading.Thread(target=start_monitoring_server, daemon=True)
    monitoring_thread.start()

    # Démarrer le worker des tâches
    worker_thread = threading.Thread(target=task_worker, daemon=True)
    worker_thread.start()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Serveur maître en écoute sur {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == '__main__':
    start_server()
