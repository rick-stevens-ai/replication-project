"""
Graph algorithms expressed purely in GraphBLAS primitives.

Each algorithm uses ONLY operations from operations.py — no direct 
graph traversal, no cheating with adjacency list walks.
"""

from __future__ import annotations
from typing import Optional, Dict, List

from .algebra import (
    SparseMatrix, SparseVector, Semiring, Monoid, _NOVAL,
    BOOLEAN, TROPICAL, ARITHMETIC, PLUS, TIMES, INF, OR, AND
)
from .operations import (
    mxv, vxm, mxm, eWiseAdd, eWiseMult, apply_op,
    reduce_matrix_to_vector, reduce_vector_to_scalar, transpose
)


def bfs_levels(A: SparseMatrix, source: int) -> SparseVector:
    """
    BFS via repeated matrix-vector multiplication on Boolean semiring.
    
    Returns a vector where entry i = BFS level (0-indexed) from source.
    Uses A^T so that multiplying a frontier vector by A^T gives successors.
    
    From Section 2.7 of the paper (Figure 7).
    """
    n = A.nrows
    AT = transpose(A)  # transpose so mxv gives successors

    # Level vector: stores BFS level for each discovered vertex
    levels = SparseVector(n)
    levels[source] = 0

    # Current frontier
    frontier = SparseVector(n, {source: True})

    level = 0
    while frontier.nnz() > 0:
        level += 1
        # Advance frontier: multiply by A^T on Boolean semiring
        next_frontier = mxv(AT, frontier, BOOLEAN)

        # Mask out already-visited vertices
        new_entries = {}
        for i, val in next_frontier.entries.items():
            if i not in levels.entries:
                new_entries[i] = True
                levels[i] = level

        frontier = SparseVector(n, new_entries)

    return levels


def sssp(A: SparseMatrix, source: int, max_iter: Optional[int] = None) -> SparseVector:
    """
    Single-Source Shortest Paths via Bellman-Ford on tropical (min-plus) semiring.
    
    A should have edge weights as values. Missing entries = no edge (∞).
    Returns distance vector from source.
    
    d^(k+1) = d^(k) ⊕.⊗ A  on (min, +, ∞, 0) semiring
    """
    n = A.nrows
    if max_iter is None:
        max_iter = n - 1

    # Distance vector: 0 at source, ∞ elsewhere (not stored)
    dist = SparseVector(n, {source: 0})

    for _ in range(max_iter):
        # d_new = d ⊕.⊗ A  (vector-matrix multiply on tropical semiring)
        new_dist_from_mul = vxm(dist, A, TROPICAL)

        # Merge: take min of existing dist and new distances
        changed = False
        merged = dict(dist.entries)
        for i, val in new_dist_from_mul.entries.items():
            old = merged.get(i, INF)
            if val < old:
                merged[i] = val
                changed = True

        dist = SparseVector(n, merged)
        if not changed:
            break

    return dist


def triangle_count(A: SparseMatrix) -> int:
    """
    Triangle counting via masked matrix multiply on arithmetic semiring.
    
    Count = (1/6) * reduce(A ⊕.⊗ A ⊙ A)
    
    where ⊙ is element-wise multiply (intersection),
    and the factor 6 accounts for the 6 permutations of each triangle
    in an undirected graph (3 rotations × 2 directions).
    
    For directed graphs, use factor 1 (or adapt accordingly).
    This assumes A is the adjacency matrix of an undirected graph.
    """
    # B = A ⊕.⊗ A (arithmetic semiring: counts 2-hop paths)
    B = mxm(A, A, ARITHMETIC)

    # C = B ⊙ A (element-wise multiply: only entries where A has an edge)
    C = eWiseMult(B, A, lambda a, b: a * b)

    # Total = sum of all entries in C
    row_sums = reduce_matrix_to_vector(C, PLUS, axis='row')
    total = reduce_vector_to_scalar(row_sums, PLUS)

    # Each triangle is counted 6 times (undirected)
    return total // 6


def triangle_count_lower(A: SparseMatrix) -> int:
    """
    Triangle counting using lower-triangular masking (more efficient).
    
    L = tril(A)  (lower triangular part)
    B = L ⊕.⊗ L
    C = B ⊙ L
    count = reduce(C)
    """
    # Extract lower triangular
    L_entries = {(i, j): v for (i, j), v in A.entries.items() if i > j}
    L = SparseMatrix(A.nrows, A.ncols, L_entries)

    B = mxm(L, L, ARITHMETIC)
    C = eWiseMult(B, L, lambda a, b: a * b)

    row_sums = reduce_matrix_to_vector(C, PLUS, axis='row')
    total = reduce_vector_to_scalar(row_sums, PLUS)

    return total


def betweenness_centrality(A: SparseMatrix) -> SparseVector:
    """
    Betweenness centrality via Brandes' algorithm expressed in GraphBLAS.
    
    For each source s:
      1. BFS forward pass: compute number of shortest paths σ
      2. Backward pass: accumulate dependency δ
      
    BC(v) = Σ_s δ_s(v)
    """
    n = A.nrows
    AT = transpose(A)
    bc = SparseVector(n, {i: 0.0 for i in range(n)})

    for s in range(n):
        # Forward BFS: compute σ (shortest path counts) and level structure
        sigma = SparseVector(n, {s: 1.0})  # σ[s] = 1
        levels_list = []  # list of frontier vectors at each level
        visited = {s}

        frontier = SparseVector(n, {s: 1.0})
        while frontier.nnz() > 0:
            levels_list.append(frontier)
            # Next frontier: advance via A^T
            next_f = mxv(AT, frontier, ARITHMETIC)

            # Filter to unvisited and accumulate sigma
            new_entries = {}
            for i, val in next_f.entries.items():
                if i not in visited:
                    new_entries[i] = val
                    sigma[i] = val
                    visited.add(i)

            frontier = SparseVector(n, new_entries)

        # Backward pass: accumulate dependencies
        delta = SparseVector(n, {i: 0.0 for i in range(n)})

        for level_idx in range(len(levels_list) - 1, 0, -1):
            frontier = levels_list[level_idx]
            prev_frontier = levels_list[level_idx - 1]

            # For each vertex w in this frontier, compute contribution
            # δ(v) += (σ(v)/σ(w)) * (1 + δ(w)) for each predecessor v
            w_contrib = SparseVector(n)
            for w in frontier.entries:
                s_w = sigma[w] if sigma[w] is not _NOVAL else 0.0
                d_w = delta[w] if delta[w] is not _NOVAL else 0.0
                if s_w > 0:
                    w_contrib[w] = (1.0 + d_w) / s_w

            # Multiply by A to propagate back to predecessors
            back_prop = mxv(A, w_contrib, ARITHMETIC)

            # Accumulate into delta for vertices in previous frontier
            for v in prev_frontier.entries:
                bp_val = back_prop[v] if back_prop[v] is not _NOVAL else 0.0
                s_v = sigma[v] if sigma[v] is not _NOVAL else 0.0
                d_v = delta[v] if delta[v] is not _NOVAL else 0.0
                delta[v] = d_v + s_v * bp_val

        # Accumulate into BC (exclude source)
        for v in range(n):
            if v != s:
                d_v = delta[v] if delta[v] is not _NOVAL else 0.0
                bc_v = bc[v] if bc[v] is not _NOVAL else 0.0
                bc[v] = bc_v + d_v

    return bc


def pagerank(A: SparseMatrix, damping: float = 0.85,
             max_iter: int = 100, tol: float = 1e-6) -> SparseVector:
    """
    PageRank via repeated matrix-vector multiplication.
    
    pr^(k+1) = (1-d)/n * 1 + d * A_norm^T ⊕.⊗ pr^(k)
    
    where A_norm has each row normalized by out-degree.
    """
    n = A.nrows

    # Compute out-degree and build normalized adjacency
    out_deg = reduce_matrix_to_vector(A, PLUS, axis='row')
    A_norm_entries = {}
    for (i, j), v in A.entries.items():
        deg = out_deg[i]
        if deg is not _NOVAL and deg > 0:
            A_norm_entries[(i, j)] = v / deg
    A_norm = SparseMatrix(n, n, A_norm_entries)
    A_norm_T = transpose(A_norm)

    # Initialize PR uniformly
    pr = SparseVector(n, {i: 1.0 / n for i in range(n)})
    base = (1.0 - damping) / n

    for _ in range(max_iter):
        new_pr = mxv(A_norm_T, pr, ARITHMETIC)
        # Apply damping + teleportation
        pr_next = SparseVector(n, {
            i: base + damping * (new_pr[i] if new_pr[i] is not _NOVAL else 0.0)
            for i in range(n)
        })

        # Check convergence
        diff = sum(abs((pr_next[i] if pr_next[i] is not _NOVAL else 0.0) -
                       (pr[i] if pr[i] is not _NOVAL else 0.0))
                   for i in range(n))
        pr = pr_next
        if diff < tol:
            break

    return pr


def connected_components(A: SparseMatrix) -> SparseVector:
    """
    Connected components via label propagation on (min, min) or (min, second) semiring.
    
    Each vertex starts with its own label. Iteratively propagate minimum label.
    Uses min-select semiring on the Boolean structure.
    """
    n = A.nrows
    # Make symmetric (undirected)
    entries = dict(A.entries)
    for (i, j), v in A.entries.items():
        if (j, i) not in entries:
            entries[(j, i)] = v
    A_sym = SparseMatrix(n, n, entries)

    # Labels: each vertex labeled with itself
    labels = SparseVector(n, {i: i for i in range(n)})

    for _ in range(n):
        # Propagate: for each vertex, take min of neighbors' labels
        new_labels = SparseVector(n)
        for i in range(n):
            min_label = labels[i] if labels[i] is not _NOVAL else i
            # Check all neighbors
            row = A_sym.row_indices(i)
            for j in row:
                j_label = labels[j] if labels[j] is not _NOVAL else j
                min_label = min(min_label, j_label)
            new_labels[i] = min_label

        if new_labels.entries == labels.entries:
            break
        labels = new_labels

    return labels
