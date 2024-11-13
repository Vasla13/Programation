# Nom du fichier à lire
nom_fichier = "test.txt"

try:
    # Ouverture du fichier avec le gestionnaire de contexte 'with'
    with open(nom_fichier, 'r') as f:
        # Lecture et affichage des lignes du fichier
        for ligne in f:
            # Utilisation de rstrip pour enlever les retours à la ligne
            ligne = ligne.rstrip("\n\r")
            print(ligne)

# Gestion des exceptions
except FileNotFoundError:
    print("Erreur : Le fichier spécifié n'a pas été trouvé.")
except PermissionError:
    print("Erreur : Vous n'avez pas les permissions nécessaires pour accéder à ce fichier.")
except IOError:
    print("Erreur : Une erreur d'entrée/sortie est survenue lors de l'accès au fichier.")
except FileExistsError:
    print("Erreur : Un fichier avec ce nom existe déjà (cela se produit surtout lors de la création).")
except Exception as e:
    print(f"Erreur inattendue : {e}")

finally:
    # Bloc finally pour indiquer la fin du programme
    print("Fin du programme.")
