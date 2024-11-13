import tkinter as tk
from tkinter import filedialog, messagebox
import socket
import threading
import ssl

def send_program():
    ip = ip_entry.get()
    port = int(port_entry.get())
    program = program_text.get("1.0", tk.END)

    def send():
        try:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            with socket.create_connection((ip, port)) as sock:
                with context.wrap_socket(sock, server_hostname=ip) as ssock:
                    ssock.sendall(program.encode('utf-8'))
                    result = ssock.recv(4096).decode('utf-8')
                    output_text.delete("1.0", tk.END)
                    output_text.insert(tk.END, result)
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    threading.Thread(target=send).start()

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
    if file_path:
        with open(file_path, 'r') as file:
            program = file.read()
            program_text.delete("1.0", tk.END)
            program_text.insert(tk.END, program)

app = tk.Tk()
app.title("Client")

# Adresse IP
tk.Label(app, text="Adresse IP du serveur :").pack()
ip_entry = tk.Entry(app)
ip_entry.insert(0, "127.0.0.1")
ip_entry.pack()

# Port
tk.Label(app, text="Port :").pack()
port_entry = tk.Entry(app)
port_entry.insert(0, "65432")
port_entry.pack()

# Zone de texte pour le programme
tk.Label(app, text="Programme Python :").pack()
program_text = tk.Text(app, height=15)
program_text.pack()

# Boutons
tk.Button(app, text="Ouvrir un fichier", command=open_file).pack()
tk.Button(app, text="Envoyer", command=send_program).pack()

# Zone de texte pour le résultat
tk.Label(app, text="Résultat :").pack()
output_text = tk.Text(app, height=10)
output_text.pack()

app.mainloop()
