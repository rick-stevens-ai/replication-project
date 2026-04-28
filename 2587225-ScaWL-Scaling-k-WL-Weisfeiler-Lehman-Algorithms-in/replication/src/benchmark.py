"""Strong-scaling benchmark for 2-WL, mirroring Soss et al. (ScaWL).

We fix a graph and sweep the number of worker processes p ∈ {1,2,4,8,16,...}.
For each p we measure wall-clock runtime of a full 2-WL refinement on the
G/H pair (isomorphic pair produced by reversed node labels, as in the paper).
Reports T(p), speedup S(p)=T(1)/T(p), and efficiency E(p)=S(p)/p.
"""
from __future__ import annotations

import json
import multiprocessing as mp
import os
import time
from pathlib import Path

import networkx as nx
import numpy as np

from kwl import run_2wl, canonical_invariant


def make_pair(n: int, d: int, seed: int = 7):
    G = nx.random_regular_graph(d, n, seed=seed)
    mapping = {v: n - 1 - v for v in G.nodes()}
    H = nx.relabel_nodes(G, mapping)
    return G, H


def bench_one(G, H, procs: int, repeats: int = 3):
    best = None
    # Create pool once per (procs) setting so startup cost doesn't pollute timing.
    if procs > 1:
        pool = mp.Pool(procs)
        # warm-up: submit a no-op chunk so workers import numpy, etc.
        pool.map(lambda x: x, [0] * procs) if False else None
    else:
        pool = None
    try:
        # Warm-up run (not timed)
        _ = run_2wl(G, pool=pool)
        for _ in range(repeats):
            t0 = time.perf_counter()
            Cg, ncg, ig = run_2wl(G, pool=pool)
            Ch, nch, ih = run_2wl(H, pool=pool)
            t = time.perf_counter() - t0
            best = t if best is None else min(best, t)
            inv_match = canonical_invariant(Cg) == canonical_invariant(Ch)
    finally:
        if pool is not None:
            pool.close(); pool.join()
    return best, ncg, nch, ig, ih, inv_match


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=150)
    ap.add_argument("--d", type=int, default=4)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--procs", type=str, default="1,2,4,8")
    ap.add_argument("--repeats", type=int, default=3)
    ap.add_argument("--out", type=str, required=True)
    args = ap.parse_args()

    procs_list = [int(x) for x in args.procs.split(",")]
    G, H = make_pair(args.n, args.d, args.seed)
    print(f"Graph: n={args.n}, d={args.d}, |E|={G.number_of_edges()}")

    results = []
    T1 = None
    for p in procs_list:
        t, ncg, nch, ig, ih, match = bench_one(G, H, p, args.repeats)
        if T1 is None:
            T1 = t
        speedup = T1 / t
        eff = speedup / p
        rec = dict(n=args.n, d=args.d, procs=p, time_s=t,
                   speedup=speedup, efficiency=eff,
                   colors_G=ncg, colors_H=nch,
                   iters_G=ig, iters_H=ih, invariant_match=match)
        print(f"  p={p:3d}: t={t:7.3f}s  speedup={speedup:5.2f}  eff={eff:5.2f}  colors={ncg}/{nch}  iters={ig}/{ih}  match={match}")
        results.append(rec)

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(dict(config=vars(args), results=results), f, indent=2)
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
