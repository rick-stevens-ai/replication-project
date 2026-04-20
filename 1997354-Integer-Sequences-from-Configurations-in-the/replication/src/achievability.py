"""
Determine which integers are achievable as #([A,B]) — the number of
"between sets" for a configuration in Hausdorff metric geometry.

By the paper's key result, this equals finding which integers appear
as edge cover counts of bipartite graphs.
"""
from itertools import combinations
from typing import Set, Dict, List, Tuple
from brute_force import enumerate_edge_covers


def all_bipartite_graphs(m: int, n: int):
    """
    Generate all bipartite graphs on vertex sets V₁={0..m-1}, V₂={m..m+n-1}.
    
    Yields (edges, vertices) for each graph (including the empty edge set,
    which has 0 edge covers).
    """
    vertices = set(range(m + n))
    all_possible_edges = [(i, j) for i in range(m) for j in range(m, m + n)]
    
    for k in range(len(all_possible_edges) + 1):
        for edge_subset in combinations(all_possible_edges, k):
            yield list(edge_subset), vertices


def achievable_values(max_m: int = 6, max_n: int = 6) -> Set[int]:
    """
    Find all integers achievable as edge cover counts of bipartite graphs
    with |V₁| ≤ max_m, |V₂| ≤ max_n.
    """
    achieved = set()
    
    for m in range(1, max_m + 1):
        for n in range(m, max_n + 1):  # n ≥ m by symmetry
            print(f"  Checking bipartite graphs on ({m},{n})...")
            for edges, vertices in all_bipartite_graphs(m, n):
                if len(edges) == 0:
                    continue  # No edge cover possible
                count = enumerate_edge_covers(edges, vertices)
                if count > 0:
                    achieved.add(count)
    
    return achieved


def find_gaps(achieved: Set[int], up_to: int = 100) -> List[int]:
    """Find integers in [1, up_to] not achieved."""
    return [i for i in range(1, up_to + 1) if i not in achieved]


def verify_known_gaps(achieved: Set[int]):
    """Check the paper's claims about non-achievable integers."""
    known_gaps = {
        19: "Blackburn et al.",
        37: "Honigs",
        41: "Ovsyannikov",
        59: "Ovsyannikov",
        67: "Ovsyannikov",
    }
    
    print("\n=== Known gap verification ===")
    for val, source in sorted(known_gaps.items()):
        if val in achieved:
            print(f"  ❌ {val} IS achieved (paper says it shouldn't be! - {source})")
        else:
            print(f"  ✅ {val} not achieved (confirmed - {source})")


def verify_fibonacci_achievable(achieved: Set[int]):
    """Verify that all Fibonacci numbers are achievable."""
    fibs = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
    print("\n=== Fibonacci achievability ===")
    for f in fibs:
        status = "✅" if f in achieved else "❌"
        print(f"  {status} F = {f}")


def verify_lucas_achievable(achieved: Set[int]):
    """Verify that even-indexed Lucas numbers are achievable."""
    # Lucas: 2, 1, 3, 4, 7, 11, 18, 29, 47, 76, 123, ...
    # Even-indexed: L_0=2, L_2=3, L_4=7, L_6=18, L_8=47, L_10=123, ...
    even_lucas = [2, 3, 7, 18, 47, 123]
    print("\n=== Even-indexed Lucas number achievability ===")
    for l in even_lucas:
        status = "✅" if l in achieved else "❌ (may need larger graphs)"
        print(f"  {status} L = {l}")


if __name__ == "__main__":
    print("=== Achievability Analysis ===")
    print("(This may take a while for larger graphs...)\n")
    
    # Start small
    achieved = achievable_values(max_m=4, max_n=6)
    
    print(f"\nAchieved values (up to max found): {sorted(achieved)[:50]}...")
    print(f"Total distinct values: {len(achieved)}")
    
    gaps = find_gaps(achieved, up_to=max(achieved) if achieved else 0)
    print(f"Gaps in [1, {max(achieved) if achieved else 0}]: {gaps[:20]}...")
    
    verify_known_gaps(achieved)
    verify_fibonacci_achievable(achieved)
    verify_lucas_achievable(achieved)
