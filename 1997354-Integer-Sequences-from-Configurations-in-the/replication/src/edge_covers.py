"""
Core formulas for edge cover counting on complete bipartite graphs
and their subgraphs (K_{m,n} minus k edges).

Based on: "Integer Sequences from Configurations in the Hausdorff Metric
Geometry via Edge Covers of Bipartite Graphs" (2021)
"""
from math import comb
from functools import lru_cache


# =============================================================================
# Level 0: Complete bipartite graph K_{m,n}
# Theorem 8: E(m,n) = Σ_{j=0}^{m} C(m,j)·(-1)^j·(2^{m-j} - 1)^n
# =============================================================================

@lru_cache(maxsize=None)
def E(m: int, n: int) -> int:
    """
    Number of edge covers of the complete bipartite graph K_{m,n}.
    
    Equivalently: number of {0,1} m×n matrices with no all-zero rows or columns.
    
    OEIS A048291 for the n×n case.
    """
    if m < 0 or n < 0:
        return 0
    if m == 0 or n == 0:
        # K_{0,n} or K_{m,0} has no edges → no edge cover possible
        # unless both are 0 (empty graph has 1 edge cover: the empty set)
        return 1 if m == 0 and n == 0 else 0
    
    total = 0
    for j in range(m + 1):
        total += comb(m, j) * ((-1) ** j) * ((2 ** (m - j) - 1) ** n)
    return total


# =============================================================================
# Level 1: K_{m,n} minus 1 edge — Theorem 10
# E₁(m,n) = ½[E(m,n) - E(m-1,n) - E(m,n-1) - E(m-1,n-1)]
# =============================================================================

@lru_cache(maxsize=None)
def E1(m: int, n: int) -> int:
    """
    Number of edge covers of K_{m,n} minus one edge.
    
    Uses Proposition 9 (edge addition formula) applied to Theorem 10.
    """
    if m < 1 or n < 1:
        return 0
    val = E(m, n) - E(m - 1, n) - E(m, n - 1) - E(m - 1, n - 1)
    assert val % 2 == 0, f"E1({m},{n}): odd numerator {val}"
    return val // 2


# =============================================================================
# Level 2: K_{m,n} minus 2 edges — Theorem 11 (3 cases)
# =============================================================================

@lru_cache(maxsize=None)
def E2_1(m: int, n: int) -> int:
    """
    Case 1: Two removed edges share a vertex in V₁, different vertices in V₂.
    
    E_{2_1}(m,n) = ½[E₁(m,n) - E(m-1,n) - E₁(m,n-1) - E(m-1,n-1)]
    """
    if m < 1 or n < 2:
        return 0
    val = E1(m, n) - E(m - 1, n) - E1(m, n - 1) - E(m - 1, n - 1)
    assert val % 2 == 0, f"E2_1({m},{n}): odd numerator {val}"
    return val // 2


@lru_cache(maxsize=None)
def E2_2(m: int, n: int) -> int:
    """
    Case 2: Two removed edges share a vertex in V₂, different vertices in V₁.
    
    E_{2_2}(m,n) = ½[E₁(m,n) - E₁(m-1,n) - E(m,n-1) - E(m-1,n-1)]
    """
    if m < 2 or n < 1:
        return 0
    val = E1(m, n) - E1(m - 1, n) - E(m, n - 1) - E(m - 1, n - 1)
    assert val % 2 == 0, f"E2_2({m},{n}): odd numerator {val}"
    return val // 2


@lru_cache(maxsize=None)
def E2_3(m: int, n: int) -> int:
    """
    Case 3: Two removed edges have no shared vertices (4 distinct endpoints).
    
    E_{2_3}(m,n) = ½[E₁(m,n) - E₁(m-1,n) - E₁(m,n-1) - E₁(m-1,n-1)]
    """
    if m < 2 or n < 2:
        return 0
    val = E1(m, n) - E1(m - 1, n) - E1(m, n - 1) - E1(m - 1, n - 1)
    assert val % 2 == 0, f"E2_3({m},{n}): odd numerator {val}"
    return val // 2


# =============================================================================
# Level 3: K_{m,n} minus 3 edges — Theorem 12 (6 cases)
# =============================================================================

@lru_cache(maxsize=None)
def E3_1(m: int, n: int) -> int:
    """
    Case 1: All 3 edges share same vertex in V₁, different vertices in V₂.
    
    E_{3_1}(m,n) = ½[E_{2_1}(m,n) - E(m-1,n) - E_{2_1}(m,n-1) - E(m-1,n-1)]
    """
    if m < 1 or n < 3:
        return 0
    val = E2_1(m, n) - E(m - 1, n) - E2_1(m, n - 1) - E(m - 1, n - 1)
    assert val % 2 == 0, f"E3_1({m},{n}): odd numerator {val}"
    return val // 2


@lru_cache(maxsize=None)
def E3_2(m: int, n: int) -> int:
    """
    Case 2: All 3 edges have different vertices in V₁, no shared vertices in V₂.
    (Forms a matching of size 3)
    
    E_{3_2}(m,n) = ½[E_{2_3}(m,n) - E_{2_3}(m-1,n) - E_{2_3}(m,n-1) - E_{2_3}(m-1,n-1)]
    """
    if m < 3 or n < 3:
        return 0
    val = E2_3(m, n) - E2_3(m - 1, n) - E2_3(m, n - 1) - E2_3(m - 1, n - 1)
    assert val % 2 == 0, f"E3_2({m},{n}): odd numerator {val}"
    return val // 2


@lru_cache(maxsize=None)
def E3_3(m: int, n: int) -> int:
    """
    Case 3: All 3 edges share same vertex in V₂, different vertices in V₁.
    
    E_{3_3}(m,n) = ½[E_{2_2}(m,n) - E_{2_2}(m-1,n) - E(m,n-1) - E(m-1,n-1)]
    """
    if m < 3 or n < 1:
        return 0
    val = E2_2(m, n) - E2_2(m - 1, n) - E(m, n - 1) - E(m - 1, n - 1)
    assert val % 2 == 0, f"E3_3({m},{n}): odd numerator {val}"
    return val // 2


@lru_cache(maxsize=None)
def E3_4(m: int, n: int) -> int:
    """
    Case 4: Exactly 2 edges share a vertex in V₁, no shared vertices in V₂.
    
    E_{3_4}(m,n) = ½[E_{2_3}(m,n) - E₁(m-1,n) - E_{2_3}(m,n-1) - E₁(m-1,n-1)]
    """
    if m < 2 or n < 3:
        return 0
    val = E2_3(m, n) - E1(m - 1, n) - E2_3(m, n - 1) - E1(m - 1, n - 1)
    assert val % 2 == 0, f"E3_4({m},{n}): odd numerator {val}"
    return val // 2


@lru_cache(maxsize=None)
def E3_5(m: int, n: int) -> int:
    """
    Case 5: All 3 edges have different vertices in V₁, exactly 2 share vertex in V₂.
    
    E_{3_5}(m,n) = ½[E_{2_3}(m,n) - E_{2_3}(m-1,n) - E₁(m,n-1) - E₁(m-1,n-1)]
    """
    if m < 3 or n < 2:
        return 0
    val = E2_3(m, n) - E2_3(m - 1, n) - E1(m, n - 1) - E1(m - 1, n - 1)
    assert val % 2 == 0, f"E3_5({m},{n}): odd numerator {val}"
    return val // 2


@lru_cache(maxsize=None)
def E3_6(m: int, n: int) -> int:
    """
    Case 6: Exactly 2 edges share a vertex in V₁, exactly 2 share a vertex in V₂.
    
    E_{3_6}(m,n) = ½[E_{2_3}(m,n) - E₁(m-1,n) - E₁(m,n-1) - E(m-1,n-1)]
    """
    if m < 2 or n < 2:
        return 0
    val = E2_3(m, n) - E1(m - 1, n) - E1(m, n - 1) - E(m - 1, n - 1)
    assert val % 2 == 0, f"E3_6({m},{n}): odd numerator {val}"
    return val // 2


# =============================================================================
# Closed-form expressions from Tables 1-3
# =============================================================================

def E1_closed(m: int, n: int) -> int:
    """Closed-form expressions for E₁(m,n) from Table 1."""
    if m == 2:
        return 3**(n - 1) - 1
    elif m == 3:
        return 3 * 7**(n - 1) - 5 * 3**(n - 1) + 2
    elif m == 4:
        return 7 * 15**(n - 1) - 16 * 7**(n - 1) + 4 * 3**n - 3
    elif m == 5:
        return 15 * 31**(n - 1) - 43 * 15**(n - 1) + 46 * 7**(n - 1) - 22 * 3**(n - 1) + 4
    elif m == 6:
        return 31 * 63**(n - 1) - 106 * 31**(n - 1) + 145 * 15**(n - 1) - 100 * 7**(n - 1) + 35 * 3**(n - 1) - 5
    else:
        raise ValueError(f"No closed form for E1({m},n)")


def E2_1_closed(m: int, n: int) -> int:
    """Closed-form for E_{2_1}(m,n) from Table 2."""
    if m == 2:
        return 3**(n - 2) - 1
    elif m == 3:
        return 9 * 7**(n - 2) - 11 * 3**(n - 2) + 2
    elif m == 4:
        return 49 * 15**(n - 2) - 76 * 7**(n - 2) + 10 * 3**(n - 1) - 3
    elif m == 5:
        return 225 * 31**(n - 2) - 421 * 15**(n - 2) + 250 * 7**(n - 2) - 58 * 3**(n - 2) + 4
    elif m == 6:
        return 961 * 63**(n - 2) - 2086 * 31**(n - 2) + 1615 * 15**(n - 2) - 580 * 7**(n - 2) + 95 * 3**(n - 2) - 5
    else:
        raise ValueError(f"No closed form for E2_1({m},n)")


def E2_2_closed(m: int, n: int) -> int:
    """Closed-form for E_{2_2}(m,n) from Table 2."""
    if m == 3:
        return 7**(n - 1) - 2 * 3**(n - 1) + 1
    elif m == 4:
        return 3 * 15**(n - 1) - 8 * 7**(n - 1) + 7 * 3**(n - 1) - 2
    elif m == 5:
        return 7 * 31**(n - 1) - 23 * 15**(n - 1) + 4 * 7**n - 5 * 3**n + 3
    elif m == 6:
        return 15 * 63**(n - 1) - 58 * 31**(n - 1) + 89 * 15**(n - 1) - 68 * 7**(n - 1) + 26 * 3**(n - 1) - 4
    else:
        raise ValueError(f"No closed form for E2_2({m},n)")


def E2_3_closed(m: int, n: int) -> int:
    """Closed-form for E_{2_3}(m,n) from Table 2."""
    if m == 2:
        return 3**(n - 2)
    elif m == 3:
        return 9 * 7**(n - 2) - 7 * 3**(n - 2) + 1
    elif m == 4:
        return 49 * 15**(n - 2) - 60 * 7**(n - 2) + 22 * 3**(n - 2) - 2
    elif m == 5:
        return 225 * 31**(n - 2) - 357 * 15**(n - 2) + 202 * 7**(n - 2) - 46 * 3**(n - 2) + 3
    elif m == 6:
        return 961 * 63**(n - 2) - 1830 * 31**(n - 2) + 1359 * 15**(n - 2) - 484 * 7**(n - 2) + 79 * 3**(n - 2) - 4
    else:
        raise ValueError(f"No closed form for E2_3({m},n)")


# =============================================================================
# Utility: generate sequence terms
# =============================================================================

def sequence(func, m: int, n_start: int, n_end: int) -> list:
    """Generate terms func(m, n) for n in [n_start, n_end]."""
    return [func(m, n) for n in range(n_start, n_end + 1)]


if __name__ == "__main__":
    print("=== E(m,n) — Complete bipartite K_{m,n} edge covers ===")
    for m in range(1, 7):
        terms = sequence(E, m, 1, 10)
        print(f"  E({m},n): {terms}")
    
    print("\n=== E₁(m,n) — K_{m,n} minus 1 edge ===")
    for m in range(2, 7):
        terms = sequence(E1, m, m, m + 9)
        print(f"  E1({m},n): {terms}")
    
    print("\n=== E_{2_1}(m,n) ===")
    for m in range(2, 7):
        terms = sequence(E2_1, m, m, m + 9)
        print(f"  E2_1({m},n): {terms}")
    
    print("\n=== E_{2_2}(m,n) ===")
    for m in range(3, 7):
        terms = sequence(E2_2, m, m, m + 9)
        print(f"  E2_2({m},n): {terms}")
    
    print("\n=== E_{2_3}(m,n) ===")
    for m in range(2, 7):
        terms = sequence(E2_3, m, m, m + 9)
        print(f"  E2_3({m},n): {terms}")
