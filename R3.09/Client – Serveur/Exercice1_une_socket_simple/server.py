import socket

# Définir l'adresse du serveur et le port
host = '127.0.0.1'  # localhost
port = 12345

# Créer une socket pour le serveur
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(1)
print("Serveur en attente de connexion...")

# Accepter une connexion du client
conn, address = server_socket.accept()
print(f"Connexion établie avec {address}")

# Recevoir le message du client
data = conn.recv(1024).decode()
print(f"Message reçu du client : {data}")

# Envoyer une réponse au client
reply = "Message reçu par le serveur"
conn.send(reply.encode())

# Fermer la connexion
conn.close()
print("Connexion fermée.")
