from flask import Flask, render_template
import psutil
import threading
import time

app = Flask(__name__, template_folder='templates')

# Variables globales pour le monitoring
cpu_usage = 0
memory_usage = 0
current_tasks = 0

def monitor_resources():
    global cpu_usage, memory_usage, current_tasks
    while True:
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_usage = psutil.virtual_memory().percent
        # current_tasks sera mis à jour par le serveur maître
        time.sleep(1)

@app.route('/')
def index():
    return render_template('index.html', cpu_usage=cpu_usage, memory_usage=memory_usage, current_tasks=current_tasks)

def start_monitoring_server():
    # Démarrer la surveillance des ressources dans un thread séparé
    monitor_thread = threading.Thread(target=monitor_resources, daemon=True)
    monitor_thread.start()

    # Démarrer le serveur Flask
    app.run(host='0.0.0.0', port=5000)
