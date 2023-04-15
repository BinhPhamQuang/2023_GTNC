from pulp import *
import math
days = [[6, 9, 9, 8, 3, 3, 7, 8, 8, 5, 3, 3, 2],  # Monday
        [6, 10, 7, 7, 3, 4, 7, 5, 9, 5, 3, 4, 3],  # Tuesday
        [7, 9, 9, 6, 3, 4, 6, 8, 7, 4, 3, 3, 3],  # Wednesday
        [6, 9, 8, 6, 4, 4, 5, 8, 7, 5, 4, 3, 4],  # Thursday
        [6, 7, 8, 7, 3, 5, 6, 7, 6, 5, 3, 3, 3],  # Friday
        [6, 9, 9, 4, 3, 3, 4, 5, 5, 5, 3, 3, 2],  # Saturday
        [5, 7, 6, 5, 4, 3, 4, 5, 6, 5, 3, 3, 3]]  # Sunday
# S_kt
shifts = [[1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0],  # C1
          [0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0],  # C2
          [0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0],  # C3
          [0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0],  # C4
          [0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1],  # C5
          [1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1]]  # C6


nc = [
    [2, 3, 0, 0, 3, 4],
    [2, 4, 0, 0, 3, 4],
    [3, 2, 0, 1, 2, 4],
    [1, 3, 0, 1, 3, 5],
    [3, 1, 1, 1, 1, 3],
    [0, 3, 0, 1, 2, 6],
    [0, 2, 0, 0, 4, 5]
]
nck = [11, 18, 1, 4, 18, 31]
ncc = 14
nd = 7

I = range(ncc)  # CSRs
J = range(len(days))  # days
K = range(len(shifts))  # shift

problem = LpProblem("CSRs Problem", LpMinimize)

x = pulp.LpVariable.dicts('x', ((i, j, k)
                          for i in I for j in J for k in K), cat='Binary')

problem += pulp.lpSum([x[i, j, k] for i in I for j in J for k in K])

for i in I:
  for j in J:
    problem += pulp.lpSum(x[i, j, k] for k in K) <= 0


for i in I:
  problem += pulp.lpSum(x[i, j, k] for j in J for k in K) <= (nd - 1)


for j in J:
  for t in range(len(shifts[0])):
    djt = days[j][t]
    problem += pulp.lpSum(shifts[k][t] * x[i, j, k]
                          for i in I for k in K) >= sum([days[j][t]])


for k in K:
  for i in I:
    problem += pulp.lpSum([x[i, j, k] for j in J]) <= math.ceil(nck[k]/ncc)
    problem += pulp.lpSum([x[i, j, k] for j in J]) >= math.floor(nck[k]/ncc)


problem.solve()
for a in x.values():
  if a.valueOrDefault() == 1.0:
    print(a)
