import subprocess
import os
import sys
import threading

def run_serveur_maitre():
    os.chdir('serveur_maitre')
    subprocess.run([sys.executable, 'serveur_maitre.py'])

def run_serveur_esclave():
    os.chdir('serveur_esclave')
    subprocess.run([sys.executable, 'serveur_esclave.py'])

def run_client():
    os.chdir('client')
    subprocess.run([sys.executable, 'client.py'])

if __name__ == '__main__':
    # Lancer le serveur esclave dans un thread séparé
    threading.Thread(target=run_serveur_esclave).start()
    
    # Lancer le serveur maître dans un thread séparé
    threading.Thread(target=run_serveur_maitre).start()
    
    # Attendre quelques secondes pour s'assurer que les serveurs sont démarrés
    import time
    time.sleep(5)
    
    # Lancer le client
    run_client()
