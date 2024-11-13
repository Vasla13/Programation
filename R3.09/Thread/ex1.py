import threading
import time

# Fonction pour le thread 1
def thread_1():
    for _ in range(5):
        print("Je suis la thread 1")
        time.sleep(0.1)  # Délai pour laisser l'autre thread s'exécuter

# Fonction pour le thread 2
def thread_2():
    for _ in range(5):
        print("Je suis la thread 2")
        time.sleep(0.1)  # Délai pour laisser l'autre thread s'exécuter

# Création des deux threads
t1 = threading.Thread(target=thread_1)
t2 = threading.Thread(target=thread_2)

# Démarrage des threads
t1.start()
t2.start()

# Attendre que les threads se terminent
t1.join()
t2.join()

print("Fin du programme.")
