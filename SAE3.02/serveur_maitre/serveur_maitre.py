import socket
import threading
import subprocess

HOST = '0.0.0.0'  # Écoute sur toutes les interfaces réseau
PORT = 65432      # Port par défaut
MAX_TASKS = 5     # Nombre maximum de programmes en cours d'exécution

# Liste des serveurs esclaves
SLAVE_SERVERS = [('127.0.0.1', 65433)]  # À ajuster selon votre configuration

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
        current_tasks = threading.active_count() - 2  # Exclure les threads principaux
        print(f"Tâches en cours : {current_tasks}")

        if current_tasks > MAX_TASKS:
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
        process = subprocess.run(['python', '-c', program.decode('utf-8')], capture_output=True, text=True, timeout=10)
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
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Serveur maître en écoute sur {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == '__main__':
    start_server()
