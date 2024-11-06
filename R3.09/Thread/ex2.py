import threading
import time

def compte_a_rebours(nom, depart):
    for i in range(depart, 0, -1):
        print(f"{nom} : {i}")
        time.sleep(0.1)  # Petit délai entre chaque affichage

# Création des threads avec des valeurs de départ différentes
thread1 = threading.Thread(target=compte_a_rebours, args=("thread 1", 5))
thread2 = threading.Thread(target=compte_a_rebours, args=("thread 2", 3))

# Démarrage des threads
thread1.start()
thread2.start()

# Attente de la fin des threads
thread1.join()
thread2.join()
