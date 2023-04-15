from pulp import *

nc = [
    [2, 3, 0, 0, 3, 4],
    [2, 4, 0, 0, 3, 4],
    [3, 2, 0, 1, 2, 4],
    [1, 3, 0, 1, 3, 5],
    [3, 1, 1, 1, 1, 3],
    [0, 3, 0, 1, 2, 6],
    [0, 2, 0, 0, 4, 5]
]
nc = [12, 13, 12, 13, 10, 12, 11]
nd = 7
ne = nd*max(nc)-sum(nc)


prob = LpProblem("CSRs Problem", LpMinimize)

x = LpVariable('x', lowBound=0, cat='Integer')
prob += x
ne = nd * max(nc) - sum(nc)
print(ne)
prob += nd * x + ne >= x + max(nc)
prob.solve()
print(f"Minimum number of additional CSR required: {x.value()}")
