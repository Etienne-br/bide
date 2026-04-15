import csv
import random

class Node:
    def __init__(self, price, player):
        self.price = price
        self.players = [player]
        self.left = None
        self.right = None

class Bide:
    def __init__(self):
        self.root = None

    def insert(self, price, player):
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
        nodes = []
        self._inorder_traversal(self.root, nodes)
        return nodes

    def _inorder_traversal(self, node, nodes):
        if node:
            self._inorder_traversal(node.left, nodes)
            nodes.append(node)
            self._inorder_traversal(node.right, nodes)

def calculate_bid_cost(price, base_cost, alpha):
    """Compute cost depending on alpha and base cost."""
    return base_cost + (alpha / (price + 1))

def find_winner(tree_object):
    sorted_nodes = tree_object.get_sorted_nodes()
    for node in sorted_nodes:
        if len(node.players) == 1:
            return node.price, node.players[0]
    return None, None

alpha_choose = int(input('Choose alpha value:'))
base_cost_choose = int(input('Choose base value:'))

def run_simulation(base_cost = base_cost_choose, alpha = alpha_choose, num_rounds=500):
    stats = {
        "Aggressive": {"wins": 0, "total_spent": 0},
        "Cautious": {"wins": 0, "total_spent": 0}
    }
    total_seller_revenue = 0

    for _ in range(num_rounds):
        sim_bide = Bide()
        # 40 joueurs par round
        for i in range(40):
            if i % 2 == 0:
                strat = "Aggressive"
                price = random.randint(0, 10)
            else:
                strat = "Cautious"
                price = random.randint(11, 40)
            
            sim_bide.insert(price, f"P{i}_{strat}")
            
            # Calcul financier
            cost = calculate_bid_cost(price, base_cost, alpha)
            stats[strat]["total_spent"] += cost
            total_seller_revenue += cost

        # Détermination du gagnant
        p, w = find_winner(sim_bide)
        if w:
            strat_winner = w.split('_')[1]
            stats[strat_winner]["wins"] += 1

    print("\n" + "="*50)
    print(f"SIMULATION RESULTS ({num_rounds} ROUNDS)")
    print("="*50)
    print(f"{'STRATEGY':<12} | {'VICTORIES':<10} | {'AVERAGE COST':<10}")
    print("-" * 50)
    for s, data in stats.items():
        avg_cost = data["total_spent"] / (20 * num_rounds)
        print(f"{s:<12} | {data['wins']:<10} | {avg_cost:.2f}€")
    print("-" * 50)
    print(f"TOTAL REVENUES : {total_seller_revenue:.2f}€")
    print("="*50)

def load_data(filename, tree_object, target_round="1"):
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            count = 0
            for row in reader:
                if row["round"] == str(target_round):
                    tree_object.insert(int(row['prix']), row['bidder'])
                    count += 1
        print(f"Success : {count} price for round: {target_round}.")
    except Exception as e:
        print(f"Error: {e}")

def show_complete_list(tree_object):
    print("\nBIDDERS LIST (SORTED BY PRICE)")
    print(f"{'PRIX':<10} | {'BIDDERS'}")
    print("-" * 40)
    all_nodes = tree_object.get_sorted_nodes()
    for node in all_nodes:
        player_list = ", ".join(node.players)
        print(f"{node.price:<10} | {player_list}")
    print("-" * 40)

if __name__ == "__main__":
    # 1. Utilisation classique (Chargement CSV)
    my_bid = Bide()
    load_data("lowbid_multi_manches_500x40.csv", my_bid, target_round="1")
    
    if my_bid.root:
        show_complete_list(my_bid)
        p, w = find_winner(my_bid)
        print(f"\nWINNER ROUND : {w} ({p}€)")

    run_simulation(500)
