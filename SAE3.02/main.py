import subprocess
import os
import sys
import time

def run_process(script_path):
    return subprocess.Popen([sys.executable, script_path])

if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Chemins des scripts
    serveur_maitre_script = os.path.join(base_dir, 'serveur_maitre', 'serveur_maitre.py')
    serveur_esclave_script = os.path.join(base_dir, 'serveur_esclave', 'serveur_esclave.py')
    client_script = os.path.join(base_dir, 'client', 'client.py')
    
    # Lancer le serveur esclave
    esclave_proc = run_process(serveur_esclave_script)
    print("Serveur esclave lancé.")
    
    # Lancer le serveur maître
    maitre_proc = run_process(serveur_maitre_script)
    print("Serveur maître lancé.")
    
    # Attendre quelques secondes pour s'assurer que les serveurs sont prêts
    time.sleep(3)
    
    # Lancer le client
    client_proc = run_process(client_script)
    print("Client lancé.")
    
    # Attendre que le client se termine
    client_proc.wait()
    
    # Terminer les serveurs maître et esclave
    maitre_proc.terminate()
    esclave_proc.terminate()
    print("Serveurs terminés.")
