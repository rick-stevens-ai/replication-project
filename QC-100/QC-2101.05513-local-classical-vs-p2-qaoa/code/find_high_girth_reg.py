#!/usr/bin/env python
"""
Try to build a 4-regular graph with girth >= 6.

Strategy: sample random 4-regular graphs on large N and pick one with high girth.
"""
import networkx as nx
import random

random.seed(0)
best_n = None
best_gth = 0
best_seed = None
for n in [20, 24, 26, 28, 30, 40, 50, 60]:
    if n % 2 != 0:
        continue
    for seed in range(200):
        try:
            g = nx.random_regular_graph(4, n, seed=seed)
        except Exception:
            continue
        gth = nx.girth(g)
        if gth > best_gth:
            best_gth = gth
            best_n = n
            best_seed = seed
            print(f"n={n} seed={seed} girth={gth} m={g.number_of_edges()}")
        if gth >= 6:
            print(f"  FOUND girth>=6! n={n} seed={seed}")
            break
    if best_gth >= 6:
        break

print(f"\nBest: n={best_n} seed={best_seed} girth={best_gth}")
