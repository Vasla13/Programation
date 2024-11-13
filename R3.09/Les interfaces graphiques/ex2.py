import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QComboBox, QMessageBox

class TemperatureConverter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        # Configuration de la fenêtre
        self.setWindowTitle("Conversion Celsius ↔ Kelvin")
        self.setGeometry(200, 200, 400, 200)
        
        # Création du widget central
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        
        # Création des éléments de l'interface
        self.label_input = QLabel("Entrez la température :", self)
        self.input_field = QLineEdit(self)
        self.unit_combo = QComboBox(self)
        self.unit_combo.addItems(["Celsius", "Kelvin"])
        self.convert_button = QPushButton("Convertir", self)
        self.result_label = QLabel("", self)
        
        # Disposition verticale
        layout = QVBoxLayout()
        layout.addWidget(self.label_input)
        layout.addWidget(self.input_field)
        layout.addWidget(self.unit_combo)
        layout.addWidget(self.convert_button)
        layout.addWidget(self.result_label)
        central_widget.setLayout(layout)
        
        # Connexion des événements
        self.convert_button.clicked.connect(self.convert_temperature)
        self.unit_combo.currentIndexChanged.connect(self.clear_result)
    
    def convert_temperature(self):
        """Méthode pour convertir la température."""
        try:
            # Récupérer la température entrée par l'utilisateur
            temperature = float(self.input_field.text())
            
            # Vérifier la conversion en fonction de l'unité sélectionnée
            unit = self.unit_combo.currentText()
            
            if unit == "Celsius":
                if temperature < -273.15:
                    raise ValueError("La température ne peut pas être inférieure au zéro absolu (-273,15 °C).")
                kelvin = temperature + 273.15
                self.result_label.setText(f"{temperature} °C = {kelvin:.2f} K")
            
            elif unit == "Kelvin":
                if temperature < 0:
                    raise ValueError("La température ne peut pas être inférieure à 0 K.")
                celsius = temperature - 273.15
                self.result_label.setText(f"{temperature} K = {celsius:.2f} °C")
        
        except ValueError as e:
            # Gestion des erreurs si l'utilisateur saisit une valeur incorrecte
            QMessageBox.warning(self, "Erreur de saisie", str(e))
        except Exception:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer un nombre valide.")
    
    def clear_result(self):
        """Réinitialiser le label du résultat lorsque l'unité change."""
        self.result_label.setText("")

# Fonction principale pour exécuter l'application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TemperatureConverter()
    window.show()
    sys.exit(app.exec_())
