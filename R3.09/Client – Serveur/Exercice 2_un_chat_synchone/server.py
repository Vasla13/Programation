import socket

# Définir l'adresse et le port du serveur
host = '127.0.0.1'
port = 12345

# Créer une socket pour le serveur
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(5)  # Écouter jusqu'à 5 connexions
print("Serveur démarré et en attente de connexion...")

# Boucle principale du serveur
while True:
    conn, address = server_socket.accept()
    print(f"Connexion établie avec {address}")

    while True:
        # Recevoir le message du client
        data = conn.recv(1024).decode()
        if not data:
            break

        print(f"Client: {data}")

        # Traiter les messages de protocole
        if data.lower() == 'bye':
            conn.send("Déconnexion du client.".encode())
            break
        elif data.lower() == 'arret':
            conn.send("Arrêt du serveur.".encode())
            conn.close()
            server_socket.close()
            print("Serveur arrêté.")
            exit(0)

        # Répondre au client
        reply = input("Serveur: ")
        conn.send(reply.encode())

    conn.close()
    print("Client déconnecté, en attente d'un nouveau client...")

