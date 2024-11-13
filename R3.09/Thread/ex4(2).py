import multiprocessing
import time

# Fonction pour le processus 1 avec un compte à rebours de 5
def countdown_process1():
    count = 5
    while count > 0:
        print(f"processus 1 : {count}")
        count -= 1
        time.sleep(0.1)

# Fonction pour le processus 2 avec un compte à rebours de 3
def countdown_process2():
    count = 3
    while count > 0:
        print(f"processus 2 : {count}")
        count -= 1
        time.sleep(0.1)

if __name__ == "__main__":
    start_time = time.time()
    
    # Création des deux processus
    p1 = multiprocessing.Process(target=countdown_process1)
    p2 = multiprocessing.Process(target=countdown_process2)
    
    # Démarrage des processus
    p1.start()
    p2.start()
    
    # Attendre que les processus se terminent
    p1.join()
    p2.join()
    
    end_time = time.time()
    print(f"Temps d'exécution (processus) : {end_time - start_time:.4f} secondes")
