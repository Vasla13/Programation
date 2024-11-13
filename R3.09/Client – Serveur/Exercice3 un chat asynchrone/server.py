import socket
import threading

clients = []

# Fonction pour gérer chaque client
def handle_client(client_socket, addr):
    print(f"[NOUVELLE CONNEXION] {addr} connecté.")
    while True:
        try:
            # Recevoir un message du client
            message = client_socket.recv(1024).decode()
            if not message:
                break

            print(f"[{addr}] {message}")

            # Gérer les commandes spéciales
            if message.lower() == "bye":
                print(f"[INFO] {addr} a quitté.")
                break
            elif message.lower() == "arret":
                print("[SERVEUR] Arrêt du serveur...")
                broadcast("Serveur arrêté", client_socket)
                client_socket.close()
                exit(0)
            
            # Diffuser le message à tous les autres clients
            broadcast(f"[{addr}] {message}", client_socket)
        except:
            break

    client_socket.close()
    clients.remove(client_socket)
    print(f"[DÉCONNEXION] {addr} déconnecté.")

# Fonction pour diffuser un message à tous les clients sauf l'envoyeur
def broadcast(message, exclude_socket=None):
    for client in clients:
        if client != exclude_socket:
            try:
                client.send(message.encode())
            except:
                client.close()
                clients.remove(client)

# Fonction pour envoyer des messages depuis le serveur
def send_server_message():
    while True:
        message = input()
        if message.lower() == "arret":
            print("[SERVEUR] Fermeture du serveur...")
            broadcast("Serveur arrêté")
            for client in clients:
                client.close()
            exit(0)
        broadcast(f"[SERVEUR] {message}")

# Fonction pour démarrer le serveur
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 5555))
    server.listen(5)
    print("[DÉMARRÉ] Le serveur écoute sur le port 5555")

    # Thread pour gérer l'envoi de messages par le serveur
    thread = threading.Thread(target=send_server_message)
    thread.start()

    while True:
        client_socket, addr = server.accept()
        clients.append(client_socket)
        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()
        print(f"[CONNEXIONS ACTIVES] {threading.active_count() - 2}")

if __name__ == "__main__":
    start_server()
