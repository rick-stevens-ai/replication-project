"""
Brute-force edge cover enumeration for verification.

An edge cover of a graph G = (V, E) is a subset E' ⊆ E such that
every vertex in V is incident to at least one edge in E'.
"""
from itertools import combinations
from typing import List, Tuple, Set


def enumerate_edge_covers(edges: List[Tuple[int, int]], vertices: Set[int]) -> int:
    """
    Count all edge covers of a graph by exhaustive enumeration.
    
    Args:
        edges: List of (u, v) tuples
        vertices: Set of all vertices
    
    Returns:
        Number of edge covers
    """
    n_edges = len(edges)
    count = 0
    
    # An edge cover must use at least ceil(|V|/2) edges
    # and at most |E| edges
    for k in range(1, n_edges + 1):
        for subset in combinations(range(n_edges), k):
            # Check if this subset covers all vertices
            covered = set()
            for idx in subset:
                u, v = edges[idx]
                covered.add(u)
                covered.add(v)
            if covered == vertices:
                count += 1
    
    return count


def make_complete_bipartite(m: int, n: int) -> Tuple[List[Tuple[int, int]], Set[int]]:
    """Create K_{m,n} as edge list + vertex set."""
    # V₁ = {0, 1, ..., m-1}, V₂ = {m, m+1, ..., m+n-1}
    vertices = set(range(m + n))
    edges = []
    for i in range(m):
        for j in range(m, m + n):
            edges.append((i, j))
    return edges, vertices


def make_Kmn_minus_edges(m: int, n: int, 
                          removed: List[Tuple[int, int]]) -> Tuple[List[Tuple[int, int]], Set[int]]:
    """
    Create K_{m,n} with specific edges removed.
    
    removed: list of (i, j) pairs where i ∈ [0,m-1], j ∈ [0,n-1]
             (j is 0-indexed within V₂, will be shifted to m+j)
    """
    vertices = set(range(m + n))
    removed_set = {(i, m + j) for i, j in removed}
    edges = []
    for i in range(m):
        for j in range(m, m + n):
            if (i, j) not in removed_set:
                edges.append((i, j))
    return edges, vertices


def E_brute(m: int, n: int) -> int:
    """Brute-force E(m,n) — edge covers of K_{m,n}."""
    if m <= 0 or n <= 0:
        return 0
    edges, vertices = make_complete_bipartite(m, n)
    return enumerate_edge_covers(edges, vertices)


def E1_brute(m: int, n: int) -> int:
    """Brute-force E₁(m,n) — edge covers of K_{m,n} minus edge (0, m)."""
    if m < 1 or n < 1:
        return 0
    edges, vertices = make_Kmn_minus_edges(m, n, [(0, 0)])
    return enumerate_edge_covers(edges, vertices)


def E2_1_brute(m: int, n: int) -> int:
    """
    Brute-force E_{2_1}(m,n) — K_{m,n} minus 2 edges sharing vertex in V₁.
    Remove edges (0,m) and (0,m+1).
    """
    edges, vertices = make_Kmn_minus_edges(m, n, [(0, 0), (0, 1)])
    return enumerate_edge_covers(edges, vertices)


def E2_2_brute(m: int, n: int) -> int:
    """
    Brute-force E_{2_2}(m,n) — K_{m,n} minus 2 edges sharing vertex in V₂.
    Remove edges (0,m) and (1,m).
    """
    edges, vertices = make_Kmn_minus_edges(m, n, [(0, 0), (1, 0)])
    return enumerate_edge_covers(edges, vertices)


def E2_3_brute(m: int, n: int) -> int:
    """
    Brute-force E_{2_3}(m,n) — K_{m,n} minus 2 edges, no shared vertices.
    Remove edges (0,m) and (1,m+1).
    """
    edges, vertices = make_Kmn_minus_edges(m, n, [(0, 0), (1, 1)])
    return enumerate_edge_covers(edges, vertices)


def E3_1_brute(m: int, n: int) -> int:
    """
    Brute-force E_{3_1}(m,n) — all 3 edges share vertex in V₁.
    Remove (0,m), (0,m+1), (0,m+2).
    """
    edges, vertices = make_Kmn_minus_edges(m, n, [(0, 0), (0, 1), (0, 2)])
    return enumerate_edge_covers(edges, vertices)


def E3_2_brute(m: int, n: int) -> int:
    """
    Brute-force E_{3_2}(m,n) — perfect matching of 3 removed edges.
    Remove (0,m), (1,m+1), (2,m+2).
    """
    edges, vertices = make_Kmn_minus_edges(m, n, [(0, 0), (1, 1), (2, 2)])
    return enumerate_edge_covers(edges, vertices)


def E3_3_brute(m: int, n: int) -> int:
    """
    Brute-force E_{3_3}(m,n) — all 3 edges share vertex in V₂.
    Remove (0,m), (1,m), (2,m).
    """
    edges, vertices = make_Kmn_minus_edges(m, n, [(0, 0), (1, 0), (2, 0)])
    return enumerate_edge_covers(edges, vertices)


def E3_4_brute(m: int, n: int) -> int:
    """
    Brute-force E_{3_4}(m,n) — 2 edges share vertex in V₁, none share in V₂.
    Remove (0,m), (0,m+1), (1,m+2).
    """
    edges, vertices = make_Kmn_minus_edges(m, n, [(0, 0), (0, 1), (1, 2)])
    return enumerate_edge_covers(edges, vertices)


def E3_5_brute(m: int, n: int) -> int:
    """
    Brute-force E_{3_5}(m,n) — all different V₁, 2 share vertex in V₂.
    Remove (0,m), (1,m), (2,m+1).
    """
    edges, vertices = make_Kmn_minus_edges(m, n, [(0, 0), (1, 0), (2, 1)])
    return enumerate_edge_covers(edges, vertices)


def E3_6_brute(m: int, n: int) -> int:
    """
    Brute-force E_{3_6}(m,n) — 2 share V₁, 2 share V₂.
    Remove (0,m), (0,m+1), (1,m+1).
    """
    edges, vertices = make_Kmn_minus_edges(m, n, [(0, 0), (0, 1), (1, 1)])
    return enumerate_edge_covers(edges, vertices)


if __name__ == "__main__":
    print("=== Brute-force verification (small cases) ===")
    
    print("\nE(m,n) brute-force:")
    for m in range(1, 5):
        terms = [E_brute(m, n) for n in range(1, 6)]
        print(f"  E({m},n): {terms}")
    
    print("\nE1(m,n) brute-force:")
    for m in range(2, 5):
        terms = [E1_brute(m, n) for n in range(m, m + 4)]
        print(f"  E1({m},n): {terms}")
    
    print("\nE2_1(m,n) brute-force:")
    for m in range(2, 5):
        terms = [E2_1_brute(m, n) for n in range(m, m + 3)]
        print(f"  E2_1({m},n): {terms}")
