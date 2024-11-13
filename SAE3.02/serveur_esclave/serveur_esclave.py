import socket
import threading
import subprocess
import os
import sys

HOST = '0.0.0.0'
PORT = 65433

def handle_master(conn, addr):
    with conn:
        print(f"Tâche reçue du serveur maître {addr}")
        program = b''
        while True:
            data = conn.recv(1024)
            if not data:
                break
            program += data

        # Exécution du programme
        result = execute_program(program)

        # Renvoi du résultat au serveur maître
        conn.sendall(result.encode('utf-8'))

def execute_program(program):
    try:
        process = subprocess.run([sys.executable, '-c', program.decode('utf-8')], capture_output=True, text=True, timeout=10)
        return process.stdout + process.stderr
    except subprocess.TimeoutExpired:
        return "Erreur : Temps d'exécution dépassé."
    except Exception as e:
        return f"Erreur d'exécution : {e}"

def start_slave_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Serveur esclave en écoute sur {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_master, args=(conn, addr)).start()

if __name__ == '__main__':
    start_slave_server()
