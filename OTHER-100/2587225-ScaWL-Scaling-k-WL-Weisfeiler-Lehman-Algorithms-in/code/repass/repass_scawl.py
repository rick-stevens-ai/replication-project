"""ScaWL re-pass (OSTI 2587225) — coverage-lifting CPU-only reproduction.

Runs:
  C1. Dataset grounding: load 3 paper-Table-1 UFL graphs (LFAT5, Trefethen_20,
      celegansneural) from SuiteSparse Matrix Market files; check vertex/edge
      counts match Table 1.
  C2. 2-WL convergence-iteration count is independent of #procs (correctness
      invariant from §7 Proof of Correctness; the proof says ScaWL produces
      the same equivalence classes at each iteration as classic k-WL — the
      observable consequence is that {color-count, #iters} is invariant
      under partitioning).
  C3. 2-WL expressivity probes (textbook k-WL cases that ground §7):
      - C12 vs 2xC6  : 1-WL CANNOT distinguish (both 2-regular), 2-WL CAN.
      - 4x4 rook vs Shrikhande (both SRG(16,6,2,2)): 2-WL CANNOT distinguish,
        3-WL CAN.  We verify 2-WL=same and (optionally) 3-WL=different.
      - Two non-iso 4-regular graphs: 2-WL should distinguish.
  C4. Single-node strong-scaling shape of our 2-WL impl on CherryRd CPU
      (1, 2, 4, 8 procs). Paper §6.3 average 2-WL speedups on a different
      node (2x Xeon e5-2660v3, 20 cores) were 2.38 / 4.26 / 7.64 / 13.20 / 16.06
      at 2/4/8/16/20 cores. We do not expect identical numbers on a different
      CPU + a different language (Python+multiprocessing vs C+OpenMP) — we
      check that scaling is sub-linear-but-positive and report ours honestly.
  C5. Tiny 3-WL on Shrikhande/rook (n=16) to ground the "3-WL more expressive
      than 2-WL" claim that underpins the whole motivation of pushing k up.

All outputs are written to results/repass/ as JSON; this script is the single
entry point (`python repass_scawl.py`).
"""
from __future__ import annotations

import hashlib
import itertools
import json
import multiprocessing as mp
import os
import platform
import socket
import sys
import time
from pathlib import Path

import networkx as nx
import numpy as np
import scipy.io as sio

REPO = Path(__file__).resolve().parents[2]
SRC = REPO / "replication" / "src"
sys.path.insert(0, str(SRC))
from kwl import run_2wl, canonical_invariant, color_histogram, initial_pair_colors  # noqa: E402

DATA = REPO / "data" / "ufl"
OUT = REPO / "results" / "repass"
OUT.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# Dataset loading (Table 1 grounding)
# ---------------------------------------------------------------------------

def mtx_nnz_and_kind(path: Path) -> tuple[int, str]:
    """Return (nnz, kind) from MTX header. nnz = the count printed in the
    'V V E' shape line. kind in {'symmetric','general',...}. Paper Table 1
    `Edges` column = this nnz value (verified: LFAT5 30, Trefethen_20 89,
    celegansneural 4690 = 2*2345 because 'general' = directed and they
    double-count for an undirected view)."""
    with open(path) as f:
        header = f.readline().strip().lower()
    kind = header.split()[-1]   # 'symmetric' / 'general' / etc.
    with open(path) as f:
        for line in f:
            if line.startswith('%'):
                continue
            parts = line.split()
            if len(parts) >= 3:
                return int(parts[2]), kind
    raise RuntimeError(f"no shape line in {path}")


def mtx_to_simple_graph(path: Path) -> nx.Graph:
    """Read a Matrix Market file and treat it as a simple undirected graph
    on the sparsity pattern (drop self-loops and weights, dedupe (i,j) and
    (j,i))."""
    M = sio.mmread(str(path))
    M = M.tocoo()
    G = nx.Graph()
    n = max(M.shape)
    G.add_nodes_from(range(n))
    for i, j in zip(M.row.tolist(), M.col.tolist()):
        if i == j:
            continue
        G.add_edge(int(i), int(j))
    return G


def dataset_grounding():
    """Claim C1: vertex / edge counts of paper Table 1 graphs."""
    paper_table1 = {
        # name -> (vertices, edges, min_deg, max_deg) as printed in Table 1
        "LFAT5":          (14,     30,   2,   5),
        "Trefethen_20":   (20,     89,   6,   6),
        "celegansneural": (297,  4_690,  0, 134),
    }
    rows = []
    for name, (v_p, e_p, mind_p, maxd_p) in paper_table1.items():
        mtx_path = DATA / name / f"{name}.mtx"
        if not mtx_path.exists():
            rows.append({"graph": name, "loaded": False,
                         "error": f"missing {mtx_path}"})
            continue
        nnz, kind = mtx_nnz_and_kind(mtx_path)
        # Paper's "Edges" = MTX nnz for symmetric files; = 2*nnz for general
        # (directed) files (e.g. celegansneural: 2*2345 = 4690).
        if kind == "symmetric":
            paper_e_from_nnz = nnz
        else:
            paper_e_from_nnz = 2 * nnz
        G = mtx_to_simple_graph(mtx_path)
        n = G.number_of_nodes()
        m = G.number_of_edges()
        degs = [d for _, d in G.degree()]
        rows.append({
            "graph": name,
            "loaded": True,
            "mtx_kind": kind,
            "mtx_nnz": nnz,
            "paper": {"V": v_p, "E": e_p, "minD": mind_p, "maxD": maxd_p},
            "paper_E_explained_by": ("mtx_nnz" if kind == "symmetric"
                                       else "2*mtx_nnz (directed)"),
            "paper_E_predicted_from_nnz": paper_e_from_nnz,
            "paper_E_grounded": paper_e_from_nnz == e_p,
            "ours_simple_undirected": {"V": n, "E": m,
                                        "minD": min(degs), "maxD": max(degs)},
            "V_match": n == v_p,
            "maxD_match_simple": max(degs) == maxd_p,
            "minD_match_simple": min(degs) == mind_p,
            "note": "V matches Table 1 exactly. E in Table 1 is the raw "
                    "MTX nnz (counts diagonal + both orientations for general "
                    "matrices); paper_E_grounded confirms that explanation."
        })
    return rows


# ---------------------------------------------------------------------------
# 2-WL correctness invariants (C2)
# ---------------------------------------------------------------------------

def correctness_invariant_under_partitioning():
    """Claim C2: For a fixed graph, the (#colors, #iters, color-histogram)
    output of 2-WL must be identical regardless of how we shard the
    refinement across processes. This is the operational consequence of
    Section 7's bijection F between equivalence-classes."""
    G = nx.random_regular_graph(4, 50, seed=7)
    results = {}
    for p in [1, 2, 4]:
        pool = mp.Pool(p) if p > 1 else None
        C, ncol, iters = run_2wl(G, pool=pool)
        if pool is not None:
            pool.close(); pool.join()
        results[p] = {
            "procs": p,
            "colors": int(ncol),
            "iters": int(iters),
            "invariant": canonical_invariant(C),
            "hist_top5": [list(x) for x in color_histogram(C)[:5]],
        }
    # Cross-check: all invariants and counts identical
    invs = {results[p]["invariant"] for p in results}
    cols = {results[p]["colors"] for p in results}
    its = {results[p]["iters"] for p in results}
    return {
        "graph": "random_regular(d=4,n=50,seed=7)",
        "per_procs": results,
        "invariant_stable_across_procs": len(invs) == 1,
        "color_count_stable_across_procs": len(cols) == 1,
        "iter_count_stable_across_procs": len(its) == 1,
    }


# ---------------------------------------------------------------------------
# 2-WL expressivity probes (C3)
# ---------------------------------------------------------------------------

def shrikhande_graph() -> nx.Graph:
    H = nx.Graph()
    H.add_nodes_from(range(16))
    diffs = [(1, 0), (0, 1), (1, 1), (-1, 0), (0, -1), (-1, -1)]
    for i in range(4):
        for j in range(4):
            u = i * 4 + j
            for di, dj in diffs:
                ni, nj = (i + di) % 4, (j + dj) % 4
                v = ni * 4 + nj
                if u != v:
                    H.add_edge(u, v)
    return H


def rook_4x4_graph() -> nx.Graph:
    R = nx.cartesian_product(nx.complete_graph(4), nx.complete_graph(4))
    return nx.convert_node_labels_to_integers(R)


def expressivity_2wl():
    """Claim C3: 2-WL distinguishes some pairs that 1-WL cannot, and fails
    to distinguish strongly-regular pairs with the same parameters."""
    results = []

    # (a) C12 vs 2xC6: equal degree sequence, 1-WL cannot tell, 2-WL CAN.
    G1 = nx.cycle_graph(12)
    G2 = nx.union(nx.cycle_graph(6), nx.cycle_graph(6), rename=("a", "b"))
    C1, _, _ = run_2wl(G1); C2, _, _ = run_2wl(G2)
    same = canonical_invariant(C1) == canonical_invariant(C2)
    results.append({
        "pair": "C12 vs 2xC6",
        "expected_2wl_can_distinguish": True,
        "ours_2wl_invariants_match": same,
        "ours_2wl_distinguishes": not same,
        "status": "PASS" if (not same) else "FAIL",
    })

    # (b) Rook 4x4 vs Shrikhande: same SRG(16,6,2,2), 2-WL CANNOT distinguish.
    R = rook_4x4_graph(); S = shrikhande_graph()
    Cr, _, _ = run_2wl(R); Cs, _, _ = run_2wl(S)
    same_rs = canonical_invariant(Cr) == canonical_invariant(Cs)
    results.append({
        "pair": "Rook(4x4) vs Shrikhande",
        "both_SRG_params": "(16, 6, 2, 2)",
        "rook_degree": [d for _, d in R.degree()],
        "shrikhande_degree": [d for _, d in S.degree()],
        "expected_2wl_can_distinguish": False,
        "ours_2wl_invariants_match": same_rs,
        "ours_2wl_distinguishes": not same_rs,
        # PASS = our 2-WL agrees with theory (cannot distinguish)
        "status": "PASS" if same_rs else "FAIL",
    })

    # (c) Petersen graph vs another non-iso 3-regular graph on 10 nodes:
    # 2-WL distinguishes them (Petersen is famously distinguishable from
    # other (3,5)-cage candidates by 2-WL via its girth/triangle-count
    # signature). Use canonical_invariant of color histogram + #colors.
    Pet = nx.petersen_graph()
    # Disjoint union of 2 K_{3,3,bridge}? Use 2 disjoint K4-with-an-edge-
    # removed: degree sequence (3,3,3,3,3,3,3,3,3,3) — same as Petersen.
    # Simpler: K_{3,3} + K4 has wrong degree. Use 2x K_{3,3} (cubic, 6+6=12
    # nodes, different from Petersen which has 10).  Use cubic graph on 10
    # nodes that is NOT Petersen: Desargues-style? Use 2 disjoint copies of
    # K_4 with 1 edge removed produces deg seq (3,3,2,2)*2 — not 3-regular.
    # Cleanest cubic-graph-vs-Petersen: use 5-prism (Y_5) = pentagonal prism
    # (10 nodes, all degree 3). Y_5 has girth 4 (squares), Petersen girth 5.
    Y5 = nx.circulant_graph(10, [1]); Y5.add_edges_from((i, i+5) for i in range(5))
    Y5 = nx.convert_node_labels_to_integers(Y5)
    Cp, kp, _ = run_2wl(Pet); Cq, kq, _ = run_2wl(Y5)
    same_pq = (canonical_invariant(Cp) == canonical_invariant(Cq))
    results.append({
        "pair": "Petersen vs 5-prism (Y5) — both 3-regular, 10 nodes",
        "petersen_girth": int(nx.girth(Pet)),
        "y5_girth": int(nx.girth(Y5)),
        "petersen_colors": int(kp), "y5_colors": int(kq),
        "expected_2wl_can_distinguish": True,
        "ours_2wl_invariants_match": same_pq,
        "ours_2wl_distinguishes": not same_pq,
        "status": "PASS" if (not same_pq) else "FAIL",
    })

    return results


# ---------------------------------------------------------------------------
# Single-node strong scaling (C4)
# ---------------------------------------------------------------------------

def single_node_strong_scaling():
    """Claim C4: speedup grows positively with cores (paper §6.3 average
    2-WL speedups on its hardware were 2.38/4.26/7.64/13.20/16.06 at
    2/4/8/16/20 cores). We replicate the shape on CherryRd CPU with
    Python + multiprocessing — not expected to match absolute numbers."""
    G = nx.random_regular_graph(4, 60, seed=11)  # n=60 -> n^2 = 3,600 tuples
    procs_list = [1, 2, 4, 8]
    rows = []
    base = None
    for p in procs_list:
        pool = mp.Pool(p) if p > 1 else None
        # warm
        run_2wl(G, pool=pool, max_iter=2)
        t0 = time.perf_counter()
        C, ncol, iters = run_2wl(G, pool=pool)
        dt = time.perf_counter() - t0
        if pool is not None:
            pool.close(); pool.join()
        if base is None:
            base = dt
        speedup = base / dt
        rows.append({
            "procs": p, "seconds": dt, "speedup_vs_1proc": speedup,
            "colors": int(ncol), "iters": int(iters),
            "invariant": canonical_invariant(C),
        })
    invs = {r["invariant"] for r in rows}
    return {
        "graph": "random_regular(d=4,n=60,seed=11)",
        "n_tuples": 60 * 60,
        "rows": rows,
        "all_procs_agree_on_invariant": len(invs) == 1,
        "paper_reference_avg_2wl_speedups_on_xeon": {
            "2 cores": 2.38, "4 cores": 4.26, "8 cores": 7.64,
            "16 cores": 13.20, "20 cores": 16.06,
        },
        "paper_hardware": "2x Intel Xeon e5-2660 v3 (20 cores), C+OpenMP",
        "our_hardware": platform.platform(),
        "note": "Our implementation is Python+multiprocessing; absolute "
                "speedup expected lower than paper's native C+OpenMP. "
                "We only ground the shape (monotonic-positive scaling) "
                "and the invariant-stability under #procs.",
    }


# ---------------------------------------------------------------------------
# Minimal 3-WL on n=16 (C5): does 3-WL distinguish Rook vs Shrikhande?
# ---------------------------------------------------------------------------

def init_3wl_colors(A: np.ndarray) -> np.ndarray:
    """Initial 3-WL color of triple (i,j,k) = atomic type of induced subgraph
    on the multiset {i,j,k}. Encode via (i==j, i==k, j==k, A[i,j], A[i,k],
    A[j,k]) -> integer key."""
    n = A.shape[0]
    out = np.zeros((n, n, n), dtype=np.int64)
    for i in range(n):
        for j in range(n):
            for k in range(n):
                key = (
                    int(i == j), int(i == k), int(j == k),
                    int(A[i, j]), int(A[i, k]), int(A[j, k]),
                )
                # pack into int
                code = 0
                for b in key:
                    code = code * 4 + b  # values are 0/1, but pad to base 4
                out[i, j, k] = code
    # canonicalize to 0..K-1
    _, inv = np.unique(out, return_inverse=True)
    return inv.reshape(n, n, n).astype(np.int64)


def refine_3wl_once(C: np.ndarray) -> tuple[np.ndarray, int]:
    """Folklore 3-WL: c'(i,j,k) = HASH(c(i,j,k),  multiset_w{
        (c(w,j,k), c(i,w,k), c(i,j,w))
    })."""
    n = C.shape[0]
    sigs = {}
    new_flat = np.empty(n * n * n, dtype=np.int64)
    idx = 0
    for i in range(n):
        for j in range(n):
            for k in range(n):
                prev = C[i, j, k]
                triples = []
                for w in range(n):
                    triples.append((int(C[w, j, k]),
                                    int(C[i, w, k]),
                                    int(C[i, j, w])))
                triples.sort()
                key = (int(prev), tuple(triples))
                h = sigs.get(key)
                if h is None:
                    h = len(sigs); sigs[key] = h
                new_flat[idx] = h
                idx += 1
    return new_flat.reshape(n, n, n), len(sigs)


def run_3wl_small(G: nx.Graph, max_iter: int = 8):
    A = nx.to_numpy_array(G, dtype=np.int64)
    C = init_3wl_colors(A)
    prev = int(C.max()) + 1
    for it in range(1, max_iter + 1):
        C, k = refine_3wl_once(C)
        if k == prev:
            return C, k, it
        prev = k
    return C, prev, max_iter


def canonical_3wl_inv(C: np.ndarray) -> str:
    _, counts = np.unique(C, return_counts=True)
    s = tuple(sorted(counts.tolist(), reverse=True))
    return hashlib.blake2b(str(s).encode(), digest_size=16).hexdigest()


def expressivity_3wl():
    """Claim C5: 3-WL distinguishes Rook(4x4) from Shrikhande."""
    R = rook_4x4_graph(); S = shrikhande_graph()
    t0 = time.perf_counter()
    Cr, kr, itr = run_3wl_small(R)
    Cs, ks, its = run_3wl_small(S)
    dt = time.perf_counter() - t0
    inv_r = canonical_3wl_inv(Cr); inv_s = canonical_3wl_inv(Cs)
    same = inv_r == inv_s
    return {
        "n_per_graph": 16,
        "tuples_per_graph": 16 ** 3,
        "rook":      {"colors": int(kr), "iters": int(itr), "inv": inv_r},
        "shrikhande":{"colors": int(ks), "iters": int(its), "inv": inv_s},
        "3wl_invariants_match": same,
        "3wl_distinguishes_them": not same,
        "expected_3wl_can_distinguish": True,
        "seconds": dt,
        "status": "PASS" if (not same) else "FAIL",
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    started = time.time()
    summary = {
        "host": socket.gethostname(),
        "platform": platform.platform(),
        "python": sys.version.split()[0],
        "ncpu_physical": os.cpu_count(),
        "started_unix": started,
        "claims": {},
    }

    print("[C1] Dataset grounding (paper Table 1) ...", flush=True)
    summary["claims"]["C1_dataset_grounding"] = dataset_grounding()
    (OUT / "C1_dataset_grounding.json").write_text(
        json.dumps(summary["claims"]["C1_dataset_grounding"], indent=2))

    print("[C2] Invariant stability under #procs ...", flush=True)
    summary["claims"]["C2_invariant_stability"] = \
        correctness_invariant_under_partitioning()
    (OUT / "C2_invariant_stability.json").write_text(
        json.dumps(summary["claims"]["C2_invariant_stability"], indent=2))

    print("[C3] 2-WL expressivity probes ...", flush=True)
    summary["claims"]["C3_2wl_expressivity"] = expressivity_2wl()
    (OUT / "C3_2wl_expressivity.json").write_text(
        json.dumps(summary["claims"]["C3_2wl_expressivity"], indent=2))

    print("[C4] Single-node strong-scaling shape ...", flush=True)
    summary["claims"]["C4_strong_scaling"] = single_node_strong_scaling()
    (OUT / "C4_strong_scaling.json").write_text(
        json.dumps(summary["claims"]["C4_strong_scaling"], indent=2))

    print("[C5] 3-WL distinguishes Rook(4x4) from Shrikhande ...", flush=True)
    summary["claims"]["C5_3wl_expressivity"] = expressivity_3wl()
    (OUT / "C5_3wl_expressivity.json").write_text(
        json.dumps(summary["claims"]["C5_3wl_expressivity"], indent=2))

    summary["finished_unix"] = time.time()
    summary["wallclock_seconds"] = summary["finished_unix"] - started
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2))
    print(f"\nWallclock: {summary['wallclock_seconds']:.1f}s")
    print(f"Wrote: {OUT}")


if __name__ == "__main__":
    main()
