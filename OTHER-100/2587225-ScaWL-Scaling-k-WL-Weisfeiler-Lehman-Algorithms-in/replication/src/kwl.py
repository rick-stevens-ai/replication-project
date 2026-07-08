"""
Independent implementation of k-dimensional Weisfeiler-Lehman (k-WL) color
refinement, inspired by the ScaWL paper (Soss et al., OSTI 2587225).

This is a from-scratch Python/NumPy implementation (no ScaWL source consulted).
We implement 2-WL (Folklore / set-based variant): for each ordered pair (u,v)
the color is refined by the multiset over w of (c(w,v), c(u,w)).

Parallelism: Python multiprocessing on chunks of the |V|^2 tuple space.
This mirrors the ScaWL strategy of partitioning tuples across workers;
in our case a single-node shared-memory analogue of their MPI+OpenMP design.

Author: Ollie (OpenClaw) for Rick Stevens, 2026-04-23.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import multiprocessing as mp
import os
import time
from typing import Dict, List, Tuple

import networkx as nx
import numpy as np


# ---------------------------------------------------------------------------
# Initial coloring
# ---------------------------------------------------------------------------

def initial_pair_colors(A: np.ndarray) -> np.ndarray:
    """Initial 2-WL color for each ordered pair (i,j).

    Encoding follows the standard k-WL atomic type: (i==j, A[i,j], A[j,i]).
    For simple undirected graphs A is symmetric, so this collapses to
    {diagonal, edge, non-edge}.
    """
    n = A.shape[0]
    diag = np.eye(n, dtype=np.int64) * 1          # 1 on diagonal
    # 2 for edge, 3 for non-edge (off-diagonal)
    offd = np.where(A == 1, 2, 3)
    C = np.where(diag == 1, 0, offd).astype(np.int64)
    return C


# ---------------------------------------------------------------------------
# Serial 2-WL refinement step
# ---------------------------------------------------------------------------

def _refine_chunk_2wl(args):
    """Compute new signatures for a contiguous row range of the tuple matrix.

    Returns list of (i, j, signature_bytes) in row-major order so the parent
    can build a global hash -> int mapping deterministically.
    """
    i0, i1, C_flat, n = args
    C = np.frombuffer(C_flat, dtype=np.int64).reshape(n, n)
    sigs: List[bytes] = []
    # Precompute column stacking helpers
    for i in range(i0, i1):
        for j in range(n):
            prev = C[i, j]
            # neighborhood multiset: (C[w,j], C[i,w]) for each w
            # Sort to make multiset canonical, then hash.
            col = C[:, j]       # c(w, j)
            row = C[i, :]       # c(i, w)
            # Combine into a single int64 key per w: col * (maxC+1) + row
            # But maxC can grow each round; use pairs and sort
            pairs = np.empty((n, 2), dtype=np.int64)
            pairs[:, 0] = col
            pairs[:, 1] = row
            # Sort lexicographically
            idx = np.lexsort((pairs[:, 1], pairs[:, 0]))
            pairs = pairs[idx]
            h = hashlib.blake2b(digest_size=16)
            h.update(np.int64(prev).tobytes())
            h.update(pairs.tobytes())
            sigs.append(h.digest())
    return i0, sigs


def refine_2wl_once(C: np.ndarray, pool=None, chunk: int | None = None) -> Tuple[np.ndarray, int]:
    """One iteration of 2-WL refinement. Returns new color matrix and #colors."""
    n = C.shape[0]
    C_flat = C.tobytes()
    if pool is None:
        chunks = [(0, n, C_flat, n)]
    else:
        nproc = pool._processes  # type: ignore[attr-defined]
        if chunk is None:
            chunk = max(1, (n + nproc - 1) // nproc)
        chunks = [(i, min(i + chunk, n), C_flat, n) for i in range(0, n, chunk)]

    if pool is None:
        results = [_refine_chunk_2wl(c) for c in chunks]
    else:
        results = pool.map(_refine_chunk_2wl, chunks)

    results.sort(key=lambda x: x[0])
    all_sigs: List[bytes] = []
    for _, sigs in results:
        all_sigs.extend(sigs)

    # Canonicalize: map unique signatures to small ints by first-appearance order
    mapping: Dict[bytes, int] = {}
    new_colors = np.empty(n * n, dtype=np.int64)
    for idx, s in enumerate(all_sigs):
        c = mapping.get(s)
        if c is None:
            c = len(mapping)
            mapping[s] = c
        new_colors[idx] = c
    return new_colors.reshape(n, n), len(mapping)


def run_2wl(G: nx.Graph, pool=None, max_iter: int = 50, verbose: bool = False) -> Tuple[np.ndarray, int, int]:
    A = nx.to_numpy_array(G, dtype=np.int64)
    C = initial_pair_colors(A)
    # Canonicalize initial colors to 0..k-1 so convergence counts are comparable.
    _, C_flat = np.unique(C, return_inverse=True)
    C = C_flat.reshape(C.shape).astype(np.int64)
    prev_count = int(C.max()) + 1
    for it in range(1, max_iter + 1):
        C, count = refine_2wl_once(C, pool=pool)
        if verbose:
            print(f"  iter {it}: {count} colors")
        if count == prev_count:
            return C, count, it
        prev_count = count
    return C, prev_count, max_iter


# ---------------------------------------------------------------------------
# Canonical color histogram -> graph invariant
# ---------------------------------------------------------------------------

def color_histogram(C: np.ndarray) -> Tuple[Tuple[int, int], ...]:
    vals, counts = np.unique(C, return_counts=True)
    order = np.argsort(counts)[::-1]
    return tuple((int(counts[i]), int(vals[i])) for i in order)


def canonical_invariant(C: np.ndarray) -> str:
    """Sorted multiset of colors -> hash. Value-agnostic (uses counts only)."""
    _, counts = np.unique(C, return_counts=True)
    counts_sorted = tuple(sorted(counts.tolist(), reverse=True))
    h = hashlib.blake2b(digest_size=16)
    h.update(str(counts_sorted).encode())
    return h.hexdigest()


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=120)
    ap.add_argument("--d", type=int, default=4, help="regular degree")
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--procs", type=int, default=1)
    ap.add_argument("--out", type=str, default=None)
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    G = nx.random_regular_graph(args.d, args.n, seed=args.seed)
    perm = list(range(args.n))[::-1]  # reversed labels, like the paper
    mapping = dict(zip(G.nodes(), perm))
    H = nx.relabel_nodes(G, mapping)

    if args.procs > 1:
        pool = mp.Pool(args.procs)
    else:
        pool = None

    t0 = time.perf_counter()
    Cg, ncg, iters_g = run_2wl(G, pool=pool, verbose=args.verbose)
    t_g = time.perf_counter() - t0

    t0 = time.perf_counter()
    Ch, nch, iters_h = run_2wl(H, pool=pool, verbose=args.verbose)
    t_h = time.perf_counter() - t0

    if pool is not None:
        pool.close(); pool.join()

    inv_g = canonical_invariant(Cg)
    inv_h = canonical_invariant(Ch)

    result = {
        "n": args.n, "d": args.d, "procs": args.procs, "seed": args.seed,
        "time_G": t_g, "time_H": t_h, "time_total": t_g + t_h,
        "iters_G": iters_g, "iters_H": iters_h,
        "colors_G": ncg, "colors_H": nch,
        "invariant_G": inv_g, "invariant_H": inv_h,
        "isomorphic_match": inv_g == inv_h,
    }
    line = json.dumps(result)
    print(line)
    if args.out:
        with open(args.out, "a") as f:
            f.write(line + "\n")


if __name__ == "__main__":
    main()
