import csv

# =============================================================================
# 1. STRUCTURE DE L'ARBRE (BST) NOMMÉE 'Bide'
# =============================================================================

class Node:
    def __init__(self, price, player):
        self.price = price
        self.players = [player]  # Liste pour gérer les ex-æquo
        self.left = None
        self.right = None

class Bide:
    def __init__(self):
        self.root = None

    def insert(self, price, player):
        """Insère une mise dans l'arbre."""
        if self.root is None:
            self.root = Node(price, player)
        else:
            self._insert_recursive(self.root, price, player)

    def _insert_recursive(self, current, price, player):
        if price == current.price:
            current.players.append(player)
        elif price < current.price:
            if current.left is None:
                current.left = Node(price, player)
            else:
                self._insert_recursive(current.left, price, player)
        else:
            if current.right is None:
                current.right = Node(price, player)
            else:
                self._insert_recursive(current.right, price, player)

    def get_sorted_nodes(self):
        """Parcours infixe pour récupérer les nœuds triés par prix."""
        nodes = []
        self._inorder_traversal(self.root, nodes)
        return nodes

    def _inorder_traversal(self, node, nodes):
        if node:
            self._inorder_traversal(node.left, nodes)
            nodes.append(node)
            self._inorder_traversal(node.right, nodes)

# =============================================================================
# 2. FONCTION POUR TROUVER LE GAGNANT
# =============================================================================

def find_winner(tree_object):
    """
    Prend l'objet 'Bide' en paramètre et cherche le prix 
    le plus bas avec un seul joueur.
    """
    # On utilise la méthode de l'objet Bide pour avoir les prix triés
    sorted_nodes = tree_object.get_sorted_nodes()
    
    for node in sorted_nodes:
        # La règle : le prix le plus bas proposé par EXACTEMENT une personne
        if len(node.players) == 1:
            return node.price, node.players[0]
            
    return None, None # Aucun gagnant unique trouvé

# =============================================================================
# 3. CHARGEMENT ET EXÉCUTION
# =============================================================================

def load_data(filename, tree_object, target_manche="1"):
    """Charge le CSV et remplit l'arbre 'Bide'."""
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            count = 0
            for row in reader:
                # IMPORTANT: row["manche"] est une chaîne de caractères ("1")
                if row["manche"] == str(target_manche):
                    tree_object.insert(int(row['prix']), row['joueur'])
                    count += 1
        print(f"Succès : {count} entrées chargées pour la manche {target_manche}.")
    except FileNotFoundError:
        print("Erreur : Fichier introuvable.")
    except KeyError as e:
        print(f"Erreur : Colonne manquante dans le CSV : {e}")

def show_complete_list(tree_object):
    print("\n--- LISTE DES PARTICIPANTS (TRIÉE PAR PRIX) ---")
    print(f"{'PRIX':<10} | {'JOUEURS'}")
    print("-" * 40)
    
    all_nodes = tree_object.get_sorted_nodes()
    for node in all_nodes:
        player_list = ", ".join(node.players)
        print(f"{node.price:<10} | {player_list}")
    print("-" * 40)

# --- MAIN ---
my_bid = Bide()

# Chargement du fichier
load_data("lowbid_multi_manches_500x40.csv", my_bid, target_manche="1")

# Affichage des résultats
if my_bid.root:
    show_complete_list(my_bid)
    price, winner = find_winner(my_bid)
    
    print("\n" + "="*30)
    if winner:
        print(f"RESULT : {winner} wins!")
        print(f"Unique lowest price : {price}€")
    else:
        print("RESULT : No unique winner.")
    print("="*30)
else:
    print("L'arbre est vide. Vérifiez le numéro de la manche ou le fichier CSV.")