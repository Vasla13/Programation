import multiprocessing
import time

# Fonction pour le processus 1
def process_1():
    for _ in range(5):
        print("Je suis le processus 1")
        time.sleep(0.1)

# Fonction pour le processus 2
def process_2():
    for _ in range(5):
        print("Je suis le processus 2")
        time.sleep(0.1)

if __name__ == "__main__":
    start_time = time.time()
    
    # Création des deux processus
    p1 = multiprocessing.Process(target=process_1)
    p2 = multiprocessing.Process(target=process_2)
    
    # Démarrage des processus
    p1.start()
    p2.start()
    
    # Attendre que les processus se terminent
    p1.join()
    p2.join()
    
    end_time = time.time()
    print(f"Temps d'exécution (processus) : {end_time - start_time:.4f} secondes")
