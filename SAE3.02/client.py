import socket
import tkinter as tk
from tkinter import filedialog, messagebox
import threading

class ClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Client")
        
        tk.Label(root, text="Server IP:").grid(row=0, column=0)
        self.server_ip = tk.Entry(root)
        self.server_ip.grid(row=0, column=1)
        
        tk.Label(root, text="Port:").grid(row=1, column=0)
        self.port = tk.Entry(root)
        self.port.grid(row=1, column=1)
        
        self.upload_button = tk.Button(root, text="Upload Program", command=self.upload_program)
        self.upload_button.grid(row=2, column=0, columnspan=2)

        self.output_text = tk.Text(root, height=20, width=50)
        self.output_text.grid(row=3, column=0, columnspan=2)

    def upload_program(self):
        filename = filedialog.askopenfilename()
        if not filename:
            return

        server_ip = self.server_ip.get()
        port = int(self.port.get())
        
        threading.Thread(target=self.send_program, args=(server_ip, port, filename)).start()

    def send_program(self, server_ip, port, filename):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((server_ip, port))
                
                # Envoyer le nom du fichier
                client_socket.sendall(filename.encode())
                
                # Envoyer le contenu du fichier
                with open(filename, 'rb') as file:
                    client_socket.sendfile(file)

                # Recevoir les résultats
                result = client_socket.recv(4096).decode()
                self.output_text.insert(tk.END, result + '\n')
                
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = ClientApp(root)
    root.mainloop()
