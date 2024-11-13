import tkinter as tk
from tkinter import filedialog, messagebox
import socket
import threading

def send_program():
    ip = ip_entry.get()
    port = int(port_entry.get())
    program = program_text.get("1.0", tk.END).strip()

    def send():
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((ip, port))
                sock.sendall(program.encode('utf-8'))
                result = sock.recv(4096).decode('utf-8')
                output_text.delete("1.0", tk.END)
                output_text.insert(tk.END, result)
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    threading.Thread(target=send).start()

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
    if file_path:
        try:
            with open(file_path, 'r') as file:
                program = file.read()
                program_text.delete("1.0", tk.END)
                program_text.insert(tk.END, program)
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'ouvrir le fichier : {e}")

app = tk.Tk()
app.title("Client")

# Adresse IP
tk.Label(app, text="Adresse IP du serveur :").pack(pady=5)
ip_entry = tk.Entry(app, width=30)
ip_entry.insert(0, "127.0.0.1")
ip_entry.pack(pady=5)

# Port
tk.Label(app, text="Port :").pack(pady=5)
port_entry = tk.Entry(app, width=30)
port_entry.insert(0, "65432")
port_entry.pack(pady=5)

# Zone de texte pour le programme
tk.Label(app, text="Programme Python :").pack(pady=5)
program_text = tk.Text(app, height=15, width=60)
program_text.pack(pady=5)

# Boutons
button_frame = tk.Frame(app)
button_frame.pack(pady=5)
tk.Button(button_frame, text="Ouvrir un fichier", command=open_file).grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="Envoyer", command=send_program).grid(row=0, column=1, padx=5)

# Zone de texte pour le résultat
tk.Label(app, text="Résultat :").pack(pady=5)
output_text = tk.Text(app, height=10, width=60)
output_text.pack(pady=5)

app.mainloop()
