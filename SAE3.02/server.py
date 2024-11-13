import socket
import subprocess
import threading
import os

HOST = '0.0.0.0'
current_process = None

def handle_client(client_socket):
    global current_process
    if current_process is not None and current_process.poll() is None:
        client_socket.sendall(b"Server busy. Try another server.")
        client_socket.close()
        return

    try:
        # Recevoir le nom du fichier
        filename = client_socket.recv(1024).decode()
        if not filename:
            client_socket.close()
            return

        # Recevoir le contenu du fichier
        with open(filename, 'wb') as file:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                file.write(data)
        
        # Compiler le programme si nécessaire
        if filename.endswith('.c'):
            compile_process = subprocess.run(['gcc', filename, '-o', 'program'], capture_output=True, text=True)
            if compile_process.returncode != 0:
                client_socket.sendall(f"Compilation failed:\n{compile_process.stderr}".encode())
                os.remove(filename)
                return
            executable = './program'
        else:
            executable = f'python3 {filename}'

        # Exécuter le programme
        current_process = subprocess.Popen(executable, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = current_process.communicate()
        
        # Envoyer les résultats au client
        if stdout:
            client_socket.sendall(stdout)
        if stderr:
            client_socket.sendall(stderr)

    finally:
        current_process = None
        client_socket.close()
        os.remove(filename)
        if os.path.exists('program'):
            os.remove('program')

def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, port))
    server_socket.listen()
    print(f"Server started on port {port}")

    while True:
        client_socket, _ = server_socket.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python server.py <port>")
        sys.exit(1)
    start_server(int(sys.argv[1]))
