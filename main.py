"""
Hello!

This script is for terrafirmagreg (am i spelling this right?????) My friend wanted me to make this

Its been tested a total of 1 time so it works as far as I know.

This code uses the PuLP library to solve a linear programming problem that minimizes the number of hits required to achieve a target hit count while adhering to a specific pattern of hits.

If it doesnt work fix it and do a pr :)

ur welcome jacob :)
"""

from pulp import LpProblem, LpVariable, LpMinimize, lpSum, LpInteger, LpBinary, LpStatusOptimal
from collections import Counter

coeffs = {
    'LightHit': -3,
    'MediumHit': -6,
    'HardHit': -9,
    'Draw': -15,
    'Punch': 2,
    'Bend': 7,
    'Upset': 13,
    'Shrink': 16
}

target = int(input("Enter target hit count: "))
constant = 0

required_pattern = str(input("Enter required hit pattern (comma-separated, e.g. 'Draw,Bend,Punch'): ")).split(',')
required_pattern = [hit.strip() for hit in required_pattern]

abstract_positions = [i for i, v in enumerate(required_pattern) if v == 'Hit']
abstract_positions = [i for i, v in enumerate(required_pattern) if v == 'Hit']
concrete_positions = [v for v in required_pattern if v != 'Hit']

req_concrete_counts = Counter(concrete_positions)

prob = LpProblem("HitCountMinWithAbstractHits", LpMinimize)

counts = {v: LpVariable(v, lowBound=0, cat=LpInteger) for v in coeffs}
abstract_vars = {}
for i in abstract_positions:
    for v in ['LightHit', 'MediumHit', 'HardHit']:
        abstract_vars[(i,v)] = LpVariable(f"x_{i}_{v}", cat=LpBinary)

prob += lpSum(counts.values())

prob += constant + lpSum(coeffs[v] * counts[v] for v in coeffs) == target

for i in abstract_positions:
    prob += lpSum(abstract_vars[(i,v)] for v in ['LightHit','MediumHit','HardHit']) == 1

for v in ['LightHit','MediumHit','HardHit']:
    prob += counts[v] >= req_concrete_counts.get(v, 0) + lpSum(abstract_vars[(i,v)] for i in abstract_positions)

for v in coeffs:
    if v not in ['LightHit','MediumHit','HardHit']:
        prob += counts[v] >= req_concrete_counts.get(v,0)

status = prob.solve()

if status == LpStatusOptimal:
    print("Solution found:")
    for v in coeffs:
        print(f"{v}: {int(counts[v].varValue)}")
    total = sum(int(counts[v].varValue) for v in coeffs)
    print(f"Total hits used: {total}")

    assigned_hits = []
    for i in abstract_positions:
        assigned = None
        for v in ['LightHit','MediumHit','HardHit']:
            if abstract_vars[(i,v)].varValue > 0.5:
                assigned = v
                break
        assigned_hits.append(assigned)

    total_required_counts = Counter()
    for v in concrete_positions:
        total_required_counts[v] += 1
    for v in assigned_hits:
        total_required_counts[v] += 1

    non_required_counts = {}
    for v in coeffs:
        non_required_counts[v] = int(counts[v].varValue) - total_required_counts.get(v, 0)

    print("\nHit sequence in order:")
    for v in coeffs:
        for _ in range(non_required_counts[v]):
            print(v)

    abs_idx = 0
    for hit in required_pattern:
        if hit == 'Hit':
            print(assigned_hits[abs_idx])
            abs_idx += 1
        else:
            print(hit)
else:
    print("No solution found.")