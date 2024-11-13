import threading
import time

# Fonction pour le thread 1 avec un compte à rebours de 5
def countdown_thread1():
    count = 5
    while count > 0:
        print(f"thread 1 : {count}")
        count -= 1
        time.sleep(0.1)

# Fonction pour le thread 2 avec un compte à rebours de 3
def countdown_thread2():
    count = 3
    while count > 0:
        print(f"thread 2 : {count}")
        count -= 1
        time.sleep(0.1)

# Création des deux threads
t1 = threading.Thread(target=countdown_thread1)
t2 = threading.Thread(target=countdown_thread2)

# Démarrage des threads
t1.start()
t2.start()

# Attendre que les threads se terminent
t1.join()
t2.join()

print("Fin du programme.")
