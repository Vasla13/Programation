nom_fichier = "test.txt"

try:
    with open(nom_fichier, 'r') as f:
        for l in f:
            l = l.rstrip("\n\r")
            print(l)
except FileNotFoundError:
    print("Erreur : le fichier n'a pas été trouvé.")
except IOError:
    print("Erreur d'entrée/sortie lors de l'accès au fichier.")
except FileExistsError:
    print("Erreur : le fichier existe déjà.")
except PermissionError:
    print("Erreur : vous n'avez pas les permissions nécessaires pour accéder au fichier.")
finally:
    print("Fin du programme.")
