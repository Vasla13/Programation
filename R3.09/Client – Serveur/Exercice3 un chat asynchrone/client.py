import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                print(f"\n{message}")
        except:
            print("[ERREUR] Connexion au serveur perdue.")
            client_socket.close()
            break

def send_messages(client_socket):
    while True:
        message = input()
        client_socket.send(message.encode())
        if message.lower() == "bye":
            print("[INFO] Déconnexion...")
            client_socket.close()
            break
        elif message.lower() == "arret":
            print("[INFO] Fermeture du chat...")
            client_socket.close()
            break

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("localhost", 5555))
    
    print("[CONNECTÉ] Connecté au serveur.")
    
    # Thread pour recevoir des messages
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    # Thread pour envoyer des messages
    send_thread = threading.Thread(target=send_messages, args=(client_socket,))
    send_thread.start()

if __name__ == "__main__":
    start_client()
