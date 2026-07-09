#!/usr/bin/env python3
"""
Independent replication of Ambainis & Kokainis (arXiv:1704.06774) Algorithm 1:
Quantum DAG/tree size estimation via eigenvalue estimation on R_B * R_A.

We build the exact statevector Hilbert space H = span{|e> : e in E'} where E'
is the edge set of the tree plus one auxiliary edge e_{T+1} = (v_{V+1}, v_1)
attached to the root. We then construct the diffusion-based reflection operators
R_A (over even-depth vertices) and R_B (over odd-depth vertices + the aux edge).

The paper proves (Algorithm 1, Section 3.2):
     T = 1 / ( alpha^2 * sin^2(theta_min / 2) )
where theta_min is the smallest nonzero absolute eigenphase of U = R_B * R_A,
and alpha is a free parameter satisfying alpha >= sqrt(2n).

Rather than *simulate* quantum phase estimation (which needs extra ancilla and
just estimates theta_min stochastically to precision ~1/M using M controlled-U
applications), we EXACTLY diagonalize U with numpy.linalg.eig, read off
theta_min, plug into the formula, and check that we recover the true edge
count T. This exercises the *paper's mathematical core* (the invariant
sin^2(theta_min/2) = 1/(alpha^2 T)) end to end on real trees.

We then bound the query complexity of quantum EE for theta_min against the
classical bound: reconstruct/enumerate all T edges needs Theta(T) queries;
quantum needs O( (1/C) * (1/delta_min) * ... ) = O( sqrt(n T) ) queries by
Lemma 1 + Algorithm 1, giving a quadratic speedup.
"""
from __future__ import annotations
import json
import math
import time
from pathlib import Path

import numpy as np


# ----------------------------- tree utilities --------------------------------

def make_complete_binary_tree(depth: int):
    """Return (edges, parent_of, depth_of, root) for a complete binary tree.

    Vertex 1 is the root. Vertices are numbered 1..V. Edges are directed
    (parent -> child) but the algorithm treats them as unoriented basis states.
    """
    V = 2 ** (depth + 1) - 1  # 1 + 2 + ... + 2^depth
    edges = []
    parent_of = {1: None}
    depth_of = {1: 0}
    for parent in range(1, V + 1):
        d = depth_of[parent]
        if d >= depth:
            continue
        left = 2 * parent
        right = 2 * parent + 1
        edges.append((parent, left))
        edges.append((parent, right))
        parent_of[left] = parent
        parent_of[right] = parent
        depth_of[left] = d + 1
        depth_of[right] = d + 1
    return edges, parent_of, depth_of, V


def make_unbalanced_tree(spec):
    """Build a tree from an adjacency dict {parent: [children,...]} rooted at 1."""
    edges = []
    parent_of = {1: None}
    depth_of = {1: 0}
    stack = [1]
    while stack:
        p = stack.pop()
        for c in spec.get(p, []):
            edges.append((p, c))
            parent_of[c] = p
            depth_of[c] = depth_of[p] + 1
            stack.append(c)
    V = 1 + sum(len(v) for v in spec.values())
    return edges, parent_of, depth_of, V


# ----------------------------- build R_A, R_B --------------------------------

def build_operators(edges, parent_of, depth_of, V, alpha, root=1):
    """Construct the DAG-size-estimation state space + R_A, R_B operators.

    H is spanned by |e> for e in E' = E ∪ {e_{T+1}} where e_{T+1} is the
    auxiliary edge (v_{V+1}, root). Basis-state index 0 is e_{T+1}; indices
    1..T index the real edges in `edges`.

    For each vertex v, E(v) = edges incident to v (excluding e_{T+1} unless v
    is the root -- the paper explicitly excludes e_{T+1} from E(v_1); the
    auxiliary edge lives in R_B via the extra |e_{T+1}><e_{T+1}| term).

    |s_v> :
        - v == root:   |e_{T+1}> + alpha * sum_{e in E(v)} |e>
        - otherwise:   sum_{e in E(v)} |e>

    V_A = vertices at even distance, V_B = vertices at odd distance.
    D_v acts on H_v = span{|e> : e in E(v) [∪ {|e_{T+1}>} if v==root]} as
    I - 2/||s_v||^2 * |s_v><s_v|.
    R_A = ⊕_{v in V_A} D_v.
    R_B = |e_{T+1}><e_{T+1}|   +   ⊕_{v in V_B} D_v.
    """
    T = len(edges)
    dim = T + 1  # +1 for e_{T+1}
    # Basis: 0 -> e_{T+1}; 1..T -> edges[0..T-1]
    edge_index = {e: i + 1 for i, e in enumerate(edges)}

    # Incidence lists per vertex (list of basis indices)
    inc = {v: [] for v in range(1, V + 1)}
    for e in edges:
        p, c = e
        idx = edge_index[e]
        inc[p].append(idx)
        inc[c].append(idx)

    def build_reflection(vertex_set, include_aux_projector: bool):
        R = np.eye(dim, dtype=complex)
        for v in vertex_set:
            H_v_indices = list(inc[v])
            if v == root:
                H_v_indices = [0] + H_v_indices  # e_{T+1} lives in root's neighborhood via s_v
            # s_v in the subspace basis
            s_local = np.zeros(len(H_v_indices), dtype=complex)
            for j, idx in enumerate(H_v_indices):
                if v == root and idx == 0:
                    s_local[j] = 1.0
                elif v == root:
                    s_local[j] = alpha
                else:
                    s_local[j] = 1.0
            norm2 = float(np.vdot(s_local, s_local).real)
            # D_v on H_v: I - 2/||s||^2 * s s^T
            D_local = np.eye(len(H_v_indices), dtype=complex) - (2.0 / norm2) * np.outer(s_local, s_local.conj())
            # Embed into full-dim identity operator on H
            # Replace the sub-block corresponding to H_v with D_local; but this
            # only works if the row/col support of R is disjoint per vertex.
            # For a tree, distinct-depth vertices at the same parity DO share
            # edges: each edge (p,c) is incident to *both* p and c. p and c
            # have different parities, so they belong to opposite (A, B) sets
            # and get processed in different reflections. Within V_A alone,
            # no two vertices share an edge (parent/child have opposite
            # parity), so the H_v subspaces are pairwise orthogonal. Same
            # holds for V_B. Direct sum is valid.
            idxs = np.array(H_v_indices)
            # R[np.ix_(idxs, idxs)] currently = I on that block; overwrite.
            R[np.ix_(idxs, idxs)] = D_local
        if include_aux_projector:
            # For R_B, the aux edge sits in a 1-d invariant subspace where the
            # operator is +|e_{T+1}><e_{T+1}| (i.e. the identity on that basis
            # state). Since we started with R = I, this is already the case.
            pass
        return R

    V_A = [v for v in range(1, V + 1) if depth_of[v] % 2 == 0]
    V_B = [v for v in range(1, V + 1) if depth_of[v] % 2 == 1]
    R_A = build_reflection(V_A, include_aux_projector=False)
    R_B = build_reflection(V_B, include_aux_projector=True)
    return R_A, R_B, dim


# ------------------------- Algorithm 1 numerics ------------------------------

def estimate_T_via_algorithm1(edges, parent_of, depth_of, V, n_depth, delta=0.3, root=1):
    """Return (T_hat, T_true, theta_min, alpha, U_dim).

    alpha = sqrt(2n) / delta ; the paper picks alpha = sqrt(2n) * delta^{-1}
    (the exponent 1.5 in the paper's alpha appears in the tighter step-count
    accountancy, but the identity T = 1/(alpha^2 sin^2(theta/2)) only needs
    alpha >= sqrt(2n) for Lemma 4 overlap; the identity itself is exact for
    ANY alpha).
    """
    T_true = len(edges)
    alpha = math.sqrt(2 * n_depth) / delta
    R_A, R_B, dim = build_operators(edges, parent_of, depth_of, V, alpha, root=root)
    U = R_B @ R_A
    # Diagonalize exactly. Eigenvalues on the unit circle.
    w, _ = np.linalg.eig(U)
    # Extract eigenphases; find smallest nonzero |theta|.
    thetas = np.angle(w)  # in (-pi, pi]
    # discard 1-eigenvalues (theta ≈ 0) and -1-eigenvalues (theta ≈ ±pi are ok,
    # but "closest to 1" means smallest |theta| > 0).
    abs_th = np.abs(thetas)
    tol = 1e-8
    nonzero = abs_th[abs_th > tol]
    if len(nonzero) == 0:
        return None, T_true, None, alpha, dim
    theta_min = float(np.min(nonzero))
    T_hat = 1.0 / (alpha ** 2 * math.sin(theta_min / 2) ** 2)
    return T_hat, T_true, theta_min, alpha, dim


# ----------------------------- experiments -----------------------------------

def run_experiments():
    results = []

    # 1. Complete binary trees of depths 1..5
    for depth in range(1, 6):
        edges, par, dep, V = make_complete_binary_tree(depth)
        n_bound = depth  # exact depth bound
        t0 = time.time()
        T_hat, T_true, theta, alpha, D = estimate_T_via_algorithm1(edges, par, dep, V, n_bound, delta=0.3)
        dt = time.time() - t0
        rel_err = abs(T_hat - T_true) / T_true if T_hat is not None else None
        results.append({
            "instance": f"complete_binary_depth_{depth}",
            "V_vertices": V,
            "T_edges": T_true,
            "n_depth": n_bound,
            "dim_H": D,
            "alpha": alpha,
            "theta_min": theta,
            "T_hat": T_hat,
            "rel_error": rel_err,
            "time_sec": dt,
        })

    # 2. Unbalanced tree (depth 4, T=15 nodes as brief suggests => 14 edges)
    # Construct: root -> 2 kids; each kid -> 2 grandkids; some leaves deeper.
    #
    #        1
    #       / \
    #      2   3
    #     /|   |\
    #    4 5   6 7
    #    |     |
    #    8     9
    #    |
    #    10
    #
    # V=10 vertices, T=9 edges, depth=4 (path 1-2-4-8-10)
    spec = {
        1: [2, 3],
        2: [4, 5],
        3: [6, 7],
        4: [8],
        6: [9],
        8: [10],
    }
    edges, par, dep, V = make_unbalanced_tree(spec)
    T_hat, T_true, theta, alpha, D = estimate_T_via_algorithm1(edges, par, dep, V, 4, delta=0.3)
    results.append({
        "instance": "unbalanced_depth4_V10",
        "V_vertices": V,
        "T_edges": T_true,
        "n_depth": 4,
        "dim_H": D,
        "alpha": alpha,
        "theta_min": theta,
        "T_hat": T_hat,
        "rel_error": abs(T_hat - T_true) / T_true,
        "time_sec": 0.0,
    })

    # 3. Ternary tree depth 3 (V = 1+3+9+27 = 40; T=39 edges)
    spec3 = {1: [2, 3, 4],
             2: [5, 6, 7], 3: [8, 9, 10], 4: [11, 12, 13],
             5: [14, 15, 16], 6: [17, 18, 19], 7: [20, 21, 22],
             8: [23, 24, 25], 9: [26, 27, 28], 10: [29, 30, 31],
             11: [32, 33, 34], 12: [35, 36, 37], 13: [38, 39, 40]}
    edges, par, dep, V = make_unbalanced_tree(spec3)
    T_hat, T_true, theta, alpha, D = estimate_T_via_algorithm1(edges, par, dep, V, 3, delta=0.3)
    results.append({
        "instance": "ternary_depth3_V40",
        "V_vertices": V,
        "T_edges": T_true,
        "n_depth": 3,
        "dim_H": D,
        "alpha": alpha,
        "theta_min": theta,
        "T_hat": T_hat,
        "rel_error": abs(T_hat - T_true) / T_true,
        "time_sec": 0.0,
    })

    # 4. Path (degenerate: worst case, T=n)
    spec_path = {i: [i + 1] for i in range(1, 8)}  # path of 8 vertices
    edges, par, dep, V = make_unbalanced_tree(spec_path)
    T_hat, T_true, theta, alpha, D = estimate_T_via_algorithm1(edges, par, dep, V, 7, delta=0.3)
    results.append({
        "instance": "path_depth7_V8",
        "V_vertices": V,
        "T_edges": T_true,
        "n_depth": 7,
        "dim_H": D,
        "alpha": alpha,
        "theta_min": theta,
        "T_hat": T_hat,
        "rel_error": abs(T_hat - T_true) / T_true,
        "time_sec": 0.0,
    })

    return results


def query_complexity_comparison():
    """For each instance in `run_experiments`, compute the theoretical query
    complexities:
      classical = Theta(T)      (must visit every node to count)
      quantum   = c * sqrt(n * T) / delta^{1.5}    (Theorem 2 leading order)
    """
    rows = []
    delta = 0.3
    for depth in [2, 4, 6, 8, 10, 12, 14]:
        T = 2 ** (depth + 1) - 2  # edges in complete binary tree
        classical = T
        quantum = math.sqrt(depth * T) / delta ** 1.5
        rows.append({
            "instance": f"complete_binary_depth_{depth}",
            "T_edges": T,
            "n_depth": depth,
            "classical_queries": classical,
            "quantum_queries_leading": quantum,
            "speedup_ratio": classical / quantum,
        })
    return rows


def main():
    out_dir = Path(__file__).parent
    print("=== Ambainis-Kokainis 2017 Algorithm 1: independent replication ===")
    results = run_experiments()
    for r in results:
        print(f"{r['instance']:35s}  T_true={r['T_edges']:4d}  T_hat={r['T_hat']:.6f}  "
              f"rel_err={r['rel_error']:.3e}  theta_min={r['theta_min']:.6f}  alpha={r['alpha']:.4f}")

    complexity = query_complexity_comparison()
    print("\n=== Query complexity scaling (theoretical) ===")
    for r in complexity:
        print(f"{r['instance']:35s}  T={r['T_edges']:6d}  classical={r['classical_queries']:8.1f}  "
              f"quantum={r['quantum_queries_leading']:8.2f}  speedup~{r['speedup_ratio']:6.2f}x")

    (out_dir / "results_algorithm1.json").write_text(json.dumps(results, indent=2))
    (out_dir / "results_complexity.json").write_text(json.dumps(complexity, indent=2))

    # Sanity: verdict
    max_rel = max(r["rel_error"] for r in results)
    verdict = "REPLICATED" if max_rel < 1e-6 else "PARTIAL"
    print(f"\nMax relative error across {len(results)} instances: {max_rel:.3e}")
    print(f"VERDICT: {verdict}")

    (out_dir / "verdict.txt").write_text(f"{verdict}\nmax_rel_error={max_rel}\n")


if __name__ == "__main__":
    main()
