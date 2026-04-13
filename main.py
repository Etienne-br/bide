import csv

class Node:
    def __init__(self, price):
        self.data = price
        self.bidders = []
        self.left = None
        self.right = None

class TreeBid:
    def __init__(self, base_cost, alpha):
        self.root = None
        self.base_cost = base_cost
        self.alpha = alpha

    def bid_cost(self, price):
        return self.base_cost + self.alpha / (price + 1)

    def insert(self, name, price):
        cost = self.bid_cost(price)
        if self.root is None:
            self.root = Node(price)
            self.root.bidders.append((name, cost))
            return
        current = self.root
        while True:
            if price == current.data:
                current.bidders.append((name, cost))
                return
            elif price < current.data:
                if current.left is None:
                    current.left = Node(price)
                    current.left.bidders.append((name, cost))
                    return
                current = current.left
            else:
                if current.right is None:
                    current.right = Node(price)
                    current.right.bidders.append((name, cost))
                    return
                current = current.right

    def load_from_csv(self, filepath):
        with open(filepath, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row['joueur']
                price = int(row['prix'])
                self.insert(name, price)

    def display2(self):
        self._inorder(self.root)

    def _inorder(self, node):
        if node:
            self._inorder(node.left)
            for name, cost in node.bidders:
                print(f"  {name} bid {node.data} — bid cost: {cost:.2f}")
            self._inorder(node.right)

    def find_lowest_unique(self):
        return self._find_lowest_unique(self.root)

    def _find_lowest_unique(self, node):
        if node is None:
            return None
        left_result = self._find_lowest_unique(node.left)
        if left_result:
            return left_result
        if len(node.bidders) == 1:
            return (node.data, node.bidders[0][0])
        return self._find_lowest_unique(node.right)


# --- Setup ---
while True:
    try:
        base_cost = float(input("Enter base cost: "))
        break
    except ValueError:
        print("Please enter a valid number.")

while True:
    try:
        alpha = float(input("Enter alpha: "))
        if alpha == 0:
            print("Alpha cannot be 0.")
            continue
        break
    except ValueError:
        print("Please enter a valid number.")

# --- Load from CSV ---
bid2 = TreeBid(base_cost, alpha)
bid2.load_from_csv(r"C:\Users\gfour\OneDrive\Desktop\pbl2\bide\APP_lowbid_data (1)\lowbid_manche_demo.csv")

# --- Results ---
print("\n--- Auction state ---")
bid2.display2()

result = bid2.find_lowest_unique()
if result:
    print(f"\nWinner: {result[1]} with bid {result[0]}")
else:
    print("\nNo winner — no unique bid found.")