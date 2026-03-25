#bid_cost(price) = base_cost + α/(price+1) 
def alpha(k):
    if k==0:
        return False
    return 100/k
def bid_cost(price):
    if price==0:
        return f"error cannot put 0"
    return base_cost+alpha(k)/(price+1)
base_cost=10
k=1
print(bid_cost(10))