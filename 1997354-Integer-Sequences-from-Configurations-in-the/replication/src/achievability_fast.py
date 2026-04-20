"""
Fast achievability analysis using formula-based edge cover counting
instead of brute-force enumeration of all subgraphs.

Strategy: use the inclusion-exclusion formula for edge covers directly,
and compute edge cover counts for specific graph families from the paper's
formulas, plus a faster brute-force for small graphs.
"""
from math import comb
from itertools import combinations, product
from typing import Set, List, Tuple


def count_edge_covers_fast(m: int, n: int, adj_matrix: List[List[int]]) -> int:
    """
    Count edge covers of a bipartite graph using inclusion-exclusion.
    
    For a bipartite graph with parts V1 (size m), V2 (size n) and adjacency
    matrix adj[i][j] = 1 if edge (i,j) exists:
    
    edge_covers = Σ_{S⊆V1} Σ_{T⊆V2} (-1)^{|S|+|T|} * Π_{(i,j) : i∉S, j∉T} (1 + adj[i][j])
    
    Wait, that's not quite right. Use the standard formula:
    
    edge_covers = Σ_{S⊆V1} Σ_{T⊆V2} (-1)^{m+n-|S|-|T|} * N(S,T)
    
    where N(S,T) = number of edge subsets covering at least all vertices in S∪T.
    
    Actually, the fastest general approach for small graphs is:
    For each subset of edges, check if it covers all vertices.
    But we can optimize with inclusion-exclusion over uncovered vertices.
    
    edge_covers(G) = Σ_{S⊆V} (-1)^{|S|} * 2^{|E(V\S)|}
    
    where E(V\S) = edges with both endpoints in V\S.
    """
    vertices_v1 = set(range(m))
    vertices_v2 = set(range(n))
    
    # Build edge set
    edges = []
    for i in range(m):
        for j in range(n):
            if adj_matrix[i][j]:
                edges.append((i, j))
    
    if not edges:
        return 0
    
    total_vertices = m + n
    
    # Inclusion-exclusion: iterate over subsets of vertices to EXCLUDE
    # For each excluded set S, count edge subsets where ALL edges have
    # at least one endpoint in the non-excluded set = 2^(# edges fully in complement)
    # 
    # edge_covers = Σ_{S⊆V} (-1)^{|S|} * 2^{|edges with both endpoints NOT in S|}
    
    result = 0
    
    # Iterate over subsets of V1 to exclude and subsets of V2 to exclude
    for mask1 in range(1 << m):
        excluded1 = set()
        for i in range(m):
            if mask1 & (1 << i):
                excluded1.add(i)
        
        for mask2 in range(1 << n):
            excluded2 = set()
            for j in range(n):
                if mask2 & (1 << j):
                    excluded2.add(j)
            
            # Count edges with both endpoints NOT excluded
            n_remaining = 0
            for i, j in edges:
                if i not in excluded1 and j not in excluded2:
                    n_remaining += 1
            
            sign = (-1) ** (len(excluded1) + len(excluded2))
            result += sign * (2 ** n_remaining)
    
    return result


def achievable_via_formulas() -> Set[int]:
    """
    Collect achievable values from the paper's formula families.
    """
    from edge_covers import E, E1, E2_1, E2_2, E2_3, E3_1, E3_2, E3_3, E3_4, E3_5, E3_6
    
    achieved = set()
    
    # E(m,n) for K_{m,n}
    for m in range(1, 10):
        for n in range(m, 10):
            val = E(m, n)
            if val > 0 and val <= 10000:
                achieved.add(val)
    
    # E1(m,n)
    for m in range(2, 8):
        for n in range(m, m + 15):
            val = E1(m, n)
            if val > 0 and val <= 10000:
                achieved.add(val)
    
    # E2_k
    for func in [E2_1, E2_2, E2_3]:
        for m in range(2, 8):
            for n in range(m, m + 15):
                val = func(m, n)
                if val > 0 and val <= 10000:
                    achieved.add(val)
    
    # E3_k
    for func in [E3_1, E3_2, E3_3, E3_4, E3_5, E3_6]:
        for m in range(2, 8):
            for n in range(max(m, 3), max(m, 3) + 15):
                val = func(m, n)
                if val > 0 and val <= 10000:
                    achieved.add(val)
    
    return achieved


def achievable_small_graphs(max_m: int = 3, max_n: int = 5) -> Set[int]:
    """
    Enumerate all bipartite graphs up to (max_m, max_n) and compute 
    edge cover counts using fast inclusion-exclusion.
    """
    achieved = set()
    
    for m in range(1, max_m + 1):
        for n in range(m, max_n + 1):
            n_possible = m * n
            print(f"  ({m},{n}): {2**n_possible} graphs to check...")
            
            # Iterate over all possible adjacency matrices
            for mask in range(1, 1 << n_possible):  # skip empty graph
                # Decode mask into adjacency matrix
                adj = [[0]*n for _ in range(m)]
                for bit in range(n_possible):
                    if mask & (1 << bit):
                        i = bit // n
                        j = bit % n
                        adj[i][j] = 1
                
                count = count_edge_covers_fast(m, n, adj)
                if count > 0:
                    achieved.add(count)
    
    return achieved


if __name__ == "__main__":
    print("=== Fast Achievability Analysis ===\n")
    
    # Method 1: From formulas
    print("From formula families:")
    formula_vals = achievable_via_formulas()
    print(f"  {len(formula_vals)} distinct values ≤ 10000")
    
    # Method 2: Small graph enumeration  
    print("\nFrom small graph enumeration:")
    small_vals = achievable_small_graphs(max_m=3, max_n=5)
    print(f"  {len(small_vals)} distinct values from graphs up to (3,5)")
    
    # Combine
    all_achieved = formula_vals | small_vals
    
    # Check gaps
    max_check = 100
    gaps = [i for i in range(1, max_check + 1) if i not in all_achieved]
    
    print(f"\nAchieved in [1,{max_check}]: {sorted([v for v in all_achieved if v <= max_check])}")
    print(f"Gaps in [1,{max_check}]: {gaps}")
    
    # Known gaps
    known_gaps = {19: "Blackburn", 37: "Honigs", 41: "Ovsyannikov", 59: "Ovsyannikov", 67: "Ovsyannikov"}
    print(f"\n=== Known gap verification ===")
    for val, source in sorted(known_gaps.items()):
        status = "❌ ACHIEVED (BUG!)" if val in all_achieved else "✅ confirmed gap"
        print(f"  {val}: {status} ({source})")
    
    # Fibonacci
    fibs = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
    print(f"\n=== Fibonacci achievability ===")
    for f in fibs:
        status = "✅" if f in all_achieved else "❌ (need larger graphs)"
        print(f"  F={f}: {status}")
    
    # Even-indexed Lucas
    even_lucas = [2, 3, 7, 18, 47, 123]
    print(f"\n=== Even-indexed Lucas achievability ===")
    for l in even_lucas:
        status = "✅" if l in all_achieved else "❌ (need larger graphs)"
        print(f"  L={l}: {status}")
