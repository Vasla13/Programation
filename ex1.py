def divEntier(x: int, y: int) -> int:
    if y == 0:
        raise ZeroDivisionError("Erreur: Division par zéro n'est pas possible.")
    if x < 0 or y < 0:
        raise ValueError("Erreur: Les valeurs négatives ne sont pas autorisées pour x ou y.")
    
    if x < y:
        return 0
    else:
        x = x - y
        return divEntier(x, y) + 1

def main():
    try:
        # Demander à l’utilisateur de saisir les valeurs
        x = int(input("Entrez un entier positif pour x: "))
        y = int(input("Entrez un entier positif pour y: "))
        
        # Effectuer la division entière en utilisant divEntier
        result = divEntier(x, y)
        print(f"Le résultat de la division entière de {x} par {y} est: {result}")
    
    except ValueError as ve:
        print(f"Erreur de valeur: {ve}")
    
    except ZeroDivisionError as zde:
        print(f"Erreur de division: {zde}")

# Exécuter la fonction principale
if __name__ == "__main__":
    main()
