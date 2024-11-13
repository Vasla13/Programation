import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QLabel, QMessageBox, QVBoxLayout, QWidget

# Classe principale héritant de QMainWindow
class SimpleWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Configuration de la fenêtre
        self.setWindowTitle("Une première fenêtre")
        self.setGeometry(200, 200, 300, 200)

        # Création du widget central
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Création des éléments de l'interface
        self.label = QLabel("Saisir votre nom", self)
        self.input_field = QLineEdit(self)
        self.ok_button = QPushButton("Ok", self)
        self.quit_button = QPushButton("Quitter", self)

        # Disposition verticale
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.input_field)
        layout.addWidget(self.ok_button)
        layout.addWidget(self.quit_button)
        central_widget.setLayout(layout)

        # Connexion des boutons à leurs fonctions
        self.ok_button.clicked.connect(self.on_click)
        self.quit_button.clicked.connect(self.close)

    # Méthode appelée lorsqu'on clique sur le bouton "OK"
    def on_click(self):
        user_input = self.input_field.text()
        if user_input:
            QMessageBox.information(self, "Salut", f"Bonjour {user_input} !")
        else:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer un nom.")

# Fonction principale pour exécuter l'application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimpleWindow()
    window.show()
    sys.exit(app.exec_())
