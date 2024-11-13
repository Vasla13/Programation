import socket
import threading

# Définir l'adresse et le port du serveur
host = '127.0.0.1'
port = 12345

clients = []

# Fonction pour gérer chaque client
def handle_client(conn, address):
    print(f"Connexion établie avec {address}")
    while True:
        try:
            # Recevoir un message du client
            message = conn.recv(1024).decode()
            if not message:
                break

            print(f"[{address}] Client: {message}")

            # Traiter les commandes de protocole
            if message.lower() == 'bye':
                conn.send("Déconnexion du client.".encode())
                break
            elif message.lower() == 'arret':
                conn.send("Arrêt du serveur.".encode())
                conn.close()
                shutdown_server()
                return

            # Envoyer une réponse à tous les autres clients
            broadcast(f"[{address}] {message}", conn)
        except:
            break

    conn.close()
    print(f"Client {address} déconnecté.")
    clients.remove(conn)

# Fonction pour diffuser un message à tous les clients sauf l'expéditeur
def broadcast(message, sender_conn):
    for client in clients:
        if client != sender_conn:
            try:
                client.send(message.encode())
            except:
                client.close()
                clients.remove(client)

# Fonction pour arrêter le serveur
def shutdown_server():
    print("Arrêt du serveur...")
    for client in clients:
        client.close()
    server_socket.close()
    exit(0)

# Initialisation du serveur
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(5)
print("Serveur démarré et en attente de connexions...")

# Boucle principale pour accepter les connexions entrantes
while True:
    conn, address = server_socket.accept()
    clients.append(conn)
    threading.Thread(target=handle_client, args=(conn, address)).start()
