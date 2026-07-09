#!/usr/bin/env python3
"""
Independent replication of:
Farhi, Goldstone, Gutmann (2007), "A Quantum Algorithm for the Hamiltonian NAND Tree"
arXiv:quant-ph/0702144

Core claim tested (headline): a continuous-time quantum walk on the graph
G = runway + perfectly bifurcating tree + input-encoding leaf-pair nodes
evaluates a depth-n NAND tree (N = 2^n leaves) in time O(sqrt(N)).

Operational fact from the paper (Sec. 1, Sec. 2):
  - Initial state = right-moving packet localized on the left half of the runway
    hr|psi(0)> = (1/sqrt(L)) e^{i r pi/2} for -L+1 <= r <= 0, else 0 on the runway,
    vanishing in the tree, and packet momentum theta=pi/2 (energy E = -2 cos(pi/2)=0).
  - Evolve with H = -A(G) for time ~ L/2 (the free-transit time to move L to the right).
  - Measure the projector onto the right side of the runway (r > 0):
      * NAND=1  => transmission T(0)=1, packet appears on the right with high prob.
      * NAND=0  => transmission T(0)=0, packet is reflected, tiny weight on the right.

We implement this EXACTLY (small finite runway M, exact matrix exponential via scipy),
then sweep every one of the 2^N input assignments for N in {4, 8} and check that a
simple decision rule (right-side probability > threshold) recovers the NAND-tree value
for all 2^N inputs with the paper's promised gap between the "1" and "0" cases.
"""
from __future__ import annotations

import itertools
import json
import time
from dataclasses import dataclass, asdict
from pathlib import Path

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla


# ---------------------------------------------------------------------------
# Classical NAND-tree ground truth (balanced binary, depth n, N = 2^n leaves).
# ---------------------------------------------------------------------------
def nand_tree_value(bits):
    """Evaluate the balanced binary NAND tree bottom-up. len(bits) must be 2^n."""
    cur = list(bits)
    while len(cur) > 1:
        cur = [1 - (a & b) for a, b in zip(cur[0::2], cur[1::2])]
    return cur[0]


# ---------------------------------------------------------------------------
# Build the graph G(bits, n, M) from the paper (figs. 2-4).
# Vertices:
#   - Runway sites r = -M, -M+1, ..., -1, 0, 1, ..., M      (2M+1 sites)
#   - Tree sites of the perfect binary tree of depth n; root attaches to r=0
#       We store the tree level-by-level; level 0 = root (attached to runway r=0),
#       level k has 2^k nodes, k = 0..n; level n = the "leaves" of the tree.
#   - Input-encoding "outer" nodes: one per leaf; if bit=1 that outer node is
#     connected to its leaf, if bit=0 the outer node is present but disconnected
#     (we keep it in the Hilbert space, it just gets no edges -- equivalently we
#     can omit it; both give the same restricted dynamics).
#
# H = -A(G).
# ---------------------------------------------------------------------------
@dataclass
class Graph:
    n: int          # tree depth (N = 2^n leaves)
    M: int          # half-runway length
    bits: tuple     # input assignment, len = 2^n
    idx_runway: dict          # r -> global index
    idx_tree: list            # idx_tree[k] = list of 2^k global indices at tree level k
    idx_outer: list           # global index of the outer node connected to leaf i (len=2^n)
    edges: list               # list of (u, v) unordered edges
    size: int                 # total number of vertices


def build_graph(bits, n, M):
    N = 2 ** n
    assert len(bits) == N

    # 1. Runway indices
    idx_runway = {}
    counter = 0
    for r in range(-M, M + 1):
        idx_runway[r] = counter
        counter += 1

    # 2. Tree indices, level by level. Level 0 = root, level n = leaves.
    idx_tree = []
    for k in range(n + 1):
        level = []
        for _ in range(2 ** k):
            level.append(counter)
            counter += 1
        idx_tree.append(level)

    # 3. Outer/input-encoding node per leaf
    idx_outer = []
    for _ in range(N):
        idx_outer.append(counter)
        counter += 1

    size = counter

    edges = []
    # Runway edges
    for r in range(-M, M):
        edges.append((idx_runway[r], idx_runway[r + 1]))
    # Attach root (tree level 0, node 0) to runway r=0
    edges.append((idx_runway[0], idx_tree[0][0]))
    # Tree edges: level k node i attaches to level k+1 nodes 2i and 2i+1
    for k in range(n):
        for i in range(2 ** k):
            parent = idx_tree[k][i]
            edges.append((parent, idx_tree[k + 1][2 * i]))
            edges.append((parent, idx_tree[k + 1][2 * i + 1]))
    # Leaf <-> outer node iff bit=1
    for i, b in enumerate(bits):
        if b == 1:
            edges.append((idx_tree[n][i], idx_outer[i]))

    return Graph(
        n=n, M=M, bits=tuple(bits),
        idx_runway=idx_runway,
        idx_tree=idx_tree,
        idx_outer=idx_outer,
        edges=edges,
        size=size,
    )


def hamiltonian(G: Graph) -> sp.csr_matrix:
    """H = -A(G) as a sparse symmetric matrix."""
    rows, cols = [], []
    for u, v in G.edges:
        rows.append(u); cols.append(v)
        rows.append(v); cols.append(u)
    data = [-1.0] * len(rows)
    return sp.csr_matrix((data, (rows, cols)), shape=(G.size, G.size)).tocsc()


def initial_state(G: Graph, L: int) -> np.ndarray:
    """Right-moving packet on the runway, momentum pi/2 (energy 0)."""
    psi = np.zeros(G.size, dtype=complex)
    for r in range(-L + 1, 1):  # r = -L+1, ..., 0
        psi[G.idx_runway[r]] = np.exp(1j * r * np.pi / 2) / np.sqrt(L)
    # Normalization check: sum |psi|^2 = L * 1/L = 1
    return psi


def right_runway_indices(G: Graph):
    return [G.idx_runway[r] for r in range(1, G.M + 1)]


def evolve_and_measure(bits, n, L, extra_M_factor=2.5, verbose=False):
    """Run the algorithm end-to-end and return metadata + P(right)."""
    N = 2 ** n
    # M must be much larger than L so the packet never reaches the far right edge
    # in time L/2 (packet speed is at most 2 at momentum pi/2, group velocity =
    # dE/dtheta = 2 sin(pi/2) = 2). The far edge is at r=M, so we need M > L/2 * 2 + L
    # comfortably. We take M = extra_M_factor * L (>= 2.5 * L) which is plenty.
    M = int(np.ceil(extra_M_factor * L))
    G = build_graph(bits, n, M)
    H = hamiltonian(G)
    psi0 = initial_state(G, L)
    T = L / 2.0

    t0 = time.perf_counter()
    # scipy.sparse.linalg.expm_multiply computes exp(-i H T) psi0
    # by Krylov, exact to machine precision.
    psiT = spla.expm_multiply(-1j * H * T, psi0)
    dt = time.perf_counter() - t0

    right = right_runway_indices(G)
    p_right = float(np.sum(np.abs(psiT[right]) ** 2))
    p_left = float(np.sum(np.abs(psiT[[G.idx_runway[r] for r in range(-M, 1)]]) ** 2))
    # everything else = tree + outer nodes
    p_other = 1.0 - p_right - p_left

    truth = nand_tree_value(bits)
    if verbose:
        print(f"n={n} L={L} M={M} bits={bits} truth={truth} "
              f"P(right)={p_right:.4f} P(left)={p_left:.4f} "
              f"P(tree+outer)={p_other:.4f} evolve_time={dt:.2f}s dim={G.size}")

    return dict(
        n=n, N=N, L=L, M=M, T=T,
        bits=list(bits), truth=int(truth),
        p_right=p_right, p_left=p_left, p_other=p_other,
        wall_seconds=dt, dim=G.size,
    )


def sweep(n, L, extra_M_factor=2.5):
    N = 2 ** n
    rows = []
    for combo in itertools.product([0, 1], repeat=N):
        rows.append(evolve_and_measure(combo, n, L, extra_M_factor))
    return rows


def summarize(rows):
    ones = [r for r in rows if r["truth"] == 1]
    zeros = [r for r in rows if r["truth"] == 0]
    def stats(xs, key):
        vals = [x[key] for x in xs]
        return dict(n=len(vals), mean=float(np.mean(vals)), min=float(np.min(vals)),
                    max=float(np.max(vals)), std=float(np.std(vals)))
    return dict(
        n_total=len(rows),
        n_truth_1=len(ones),
        n_truth_0=len(zeros),
        p_right_when_1=stats(ones, "p_right") if ones else None,
        p_right_when_0=stats(zeros, "p_right") if zeros else None,
    )


def decision_check(rows, threshold=None):
    """Verify the decision rule 'P(right) > threshold => output 1' matches truth
    for every input assignment."""
    ones = [r["p_right"] for r in rows if r["truth"] == 1]
    zeros = [r["p_right"] for r in rows if r["truth"] == 0]
    if not ones or not zeros:
        # degenerate case (all inputs give the same NAND value shouldn't happen for these sizes)
        gap = None
        thr = threshold if threshold is not None else 0.5
    else:
        min_one = min(ones)
        max_zero = max(zeros)
        gap = min_one - max_zero
        if threshold is None:
            threshold = 0.5 * (min_one + max_zero)
    correct = 0
    for r in rows:
        pred = 1 if r["p_right"] > threshold else 0
        if pred == r["truth"]:
            correct += 1
    return dict(
        threshold=float(threshold),
        gap=None if gap is None else float(gap),
        min_p_right_truth1=None if not ones else float(min(ones)),
        max_p_right_truth1=None if not ones else float(max(ones)),
        min_p_right_truth0=None if not zeros else float(min(zeros)),
        max_p_right_truth0=None if not zeros else float(max(zeros)),
        correct=correct,
        total=len(rows),
        accuracy=correct / len(rows),
    )


def main():
    outdir = Path(__file__).resolve().parent
    results = {}

    # Depth 2 (N = 4 leaves): tiny, sweep all 2^4 = 16 inputs
    # L is order sqrt(N); for N=4 that's ~2 -- take a modest L that resolves the
    # transmission plateau. Empirically L=8 is comfortably in the "packet long enough"
    # regime for N=4.
    # For depth n, transmission plateau has width ~ 1/(16 sqrt(N)); packet has
    # spectral width ~ 1/L, so L must be >> 16 sqrt(N) for the sharp T(0) plateau
    # to dominate. We test both the paper's asymptotic O(sqrt(N)) scaling AND
    # larger L that resolves the plateau in these tiny-N regimes.
    for n, Ls in [(2, [4, 8, 16, 32]), (3, [8, 16, 32, 64, 96])]:
        for L in Ls:
            key = f"n={n}_L={L}"
            t0 = time.perf_counter()
            rows = sweep(n, L)
            summ = summarize(rows)
            dec = decision_check(rows)
            wall = time.perf_counter() - t0
            print(f"[{key}] N={2**n} sweep of {2**(2**n)} inputs done in {wall:.1f}s -- "
                  f"acc={dec['accuracy']*100:.1f}% gap={dec['gap']}")
            results[key] = dict(rows=rows, summary=summ, decision=dec, wall_seconds=wall)

    with open(outdir / "nand_tree_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"Wrote {outdir/'nand_tree_results.json'}")


if __name__ == "__main__":
    main()
