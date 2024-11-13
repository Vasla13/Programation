import socket

# Définir l'adresse du serveur et le port
host = '127.0.0.1'
port = 12345

while True:
    # Créer une socket pour le client
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
    except ConnectionRefusedError:
        print("Impossible de se connecter au serveur.")
        break

    print("Connecté au serveur.")
    
    while True:
        # Envoyer un message au serveur
        message = input("Client: ")
        client_socket.send(message.encode())

        # Traiter les messages de protocole
        if message.lower() in ['bye', 'arret']:
            break

        # Recevoir la réponse du serveur
        data = client_socket.recv(1024).decode()
        print(f"Serveur: {data}")

    client_socket.close()
    print("Client déconnecté.")
    
    # Arrêter le client si la commande 'arret' est envoyée
    if message.lower() == 'arret':
        print("Arrêt du client.")
        break
