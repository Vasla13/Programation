import threading
from multiprocessing import Process
import time

def tache_thread():
    total = 0
    for _ in range(10000000):
        total += 1

def tache_processus():
    total = 0
    for _ in range(10000000):
        total += 1

if __name__ == '__main__':
    # Mesure du temps pour les threads
    debut_thread = time.time()
    threads = []
    for _ in range(2):
        thread = threading.Thread(target=tache_thread)
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    fin_thread = time.time()
    print(f"Temps d'exécution avec threads : {fin_thread - debut_thread} secondes")

    # Mesure du temps pour les processus
    debut_processus = time.time()
    processus = []
    for _ in range(2):
        process = Process(target=tache_processus)
        processus.append(process)
        process.start()
    for process in processus:
        process.join()
    fin_processus = time.time()
    print(f"Temps d'exécution avec processus : {fin_processus - debut_processus} secondes")
