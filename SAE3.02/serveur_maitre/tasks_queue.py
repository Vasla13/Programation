import threading
from queue import Queue

class TaskQueue:
    def __init__(self):
        self.queue = Queue()
        self.lock = threading.Lock()

    def add_task(self, conn, program):
        with self.lock:
            self.queue.put((conn, program))
            print("Nouvelle tâche ajoutée à la file d'attente.")

    def get_task(self):
        with self.lock:
            return self.queue.get()

    def has_tasks(self):
        with self.lock:
            return not self.queue.empty()
