# Nom du fichier spécifié dans une variable
filename = 'test.txt'

# Gestion des exceptions lors de l'ouverture et de la lecture du fichier avec 'with'
try:
    with open(filename, 'r') as f:
        for ligne in f:
            ligne = ligne.rstrip('\n\r')
            print(ligne)
except FileNotFoundError:
    print("Erreur : Le fichier n'a pas été trouvé.")
except IOError:
    print("Erreur : Problème d'entrée/sortie.")
except FileExistsError:
    print("Erreur : Le fichier existe déjà.")
except PermissionError:
    print("Erreur : Vous n'avez pas la permission d'accéder à ce fichier.")
finally:
    print("Fin du programme.")
