import socket

# Définir l'adresse du serveur et le port
host = '127.0.0.1'  # localhost
port = 12345

# Créer une socket pour le client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Se connecter au serveur
client_socket.connect((host, port))

# Envoyer un message au serveur
message = "Bonjour, serveur !"
client_socket.send(message.encode())
print("Message envoyé au serveur.")

# Recevoir la réponse du serveur
data = client_socket.recv(1024).decode()
print(f"Réponse du serveur : {data}")

# Fermer la connexion
client_socket.close()
print("Connexion fermée.")
