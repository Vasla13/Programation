from concurrent.futures import ThreadPoolExecutor
import time

def tache(nom):
    for i in range(3):
        print(f"{nom} exécute l'itération {i}")
        time.sleep(0.1)

# Liste des noms de threads
noms = ['Thread 1', 'Thread 2', 'Thread 3']

# Création d'un pool de threads
with ThreadPoolExecutor(max_workers=2) as executor:
    executor.map(tache, noms)
