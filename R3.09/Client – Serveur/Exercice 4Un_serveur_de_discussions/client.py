import socket
import threading

# Définir l'adresse du serveur et le port
host = '127.0.0.1'
port = 12345

# Fonction pour recevoir des messages du serveur
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                print(f"\n{message}")
            else:
                break
        except:
            break

# Initialiser la connexion client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))
print("Connecté au serveur.")

# Démarrer un thread pour recevoir des messages du serveur
threading.Thread(target=receive_messages, args=(client_socket,)).start()

# Boucle pour envoyer des messages au serveur
while True:
    message = input("Client: ")
    client_socket.send(message.encode())

    # Traiter les commandes de protocole
    if message.lower() == 'bye':
        print("Déconnexion du client.")
        client_socket.close()
        break
    elif message.lower() == 'arret':
        print("Arrêt du client et du serveur.")
        client_socket.close()
        break
