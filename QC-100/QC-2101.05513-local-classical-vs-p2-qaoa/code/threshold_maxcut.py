#!/usr/bin/env python
"""
2-step threshold algorithm from Marwaha 2021 (arXiv:2101.05513) Section 3.

Algorithm (Section 3, generalized from HRSS14):
  Given a graph G and thresholds tau_1, tau_2:
    1. Randomly assign each vertex a spin +/-1 with equal probability.
    2. For each vertex v, if the number of neighbors with the SAME spin
       is >= tau_1, flip v.  (All flips computed on step-1 state, applied together.)
    3. Repeat with tau_2 (using the current state).
    4. Output the cut induced by the final spins.

We estimate the expected cut fraction by Monte Carlo over the initial random
spin assignment.  Compare to the paper's Table 1 values.

For a D-regular graph of girth > 5, cut fraction = 0.5 + improvement/sqrt(...);
Table 1 reports the "improvement over random" (i.e. E[cut fraction] - 0.5).

Numbers from Table 1 (Threshold_2 with (tau_1, tau_2), improvement over random):
  D=2: 0.3125 (2, 2)
  D=3: 0.2461 (2, 3)
  D=4: 0.2128 (3, 4)  -- outperforms QAOA2 (0.1693)
  D=5: 0.1851 (4, 4)  -- outperforms QAOA2 (0.1907)?  NO, 0.1851 < 0.1907
                         Look: 0.1851 (4,4) OR 0.1832 (4,5)? Both < 0.1907.
                         Only Modified Threshold_2 beats QAOA2 at D=5.
  D=6: 0.1607 (5, 5)  outperforms QAOA2 (0.1726)? NO. So threshold2 only
                        beats QAOA2 starting D=4 in this simple form.
Actually re-read paper carefully:
  * Threshold2(tau_1, tau_2) starts to outperform QAOA2 for 5 < D < 500 (line 76).
  * For D in {2,3,4,5}, need Modified Threshold_2 (Hastings framework).
So the clean D that Threshold2 wins is D=6 onward.  Let's verify D=6, D=7, ...

Actually wait: Table 1 shows Threshold2(τ1,τ2) for D=4 = 0.2128, and QAOA2 for D=4 = 0.1693.
0.2128 > 0.1693, so Threshold2 DOES beat QAOA2 at D=4.
Also D=5: Threshold2 = 0.1832 (4,5); QAOA2 = 0.1907.  1832 < 1907 → threshold LOSES at D=5.
D=6: Threshold2 = 0.1607 (5,5); QAOA2 = 0.1726.  threshold LOSES at D=6.
D=7: Threshold2 = 0.1599 (5,6); QAOA2 = 0.1589.  threshold WINS narrowly.

Hmm actually paper says "5 < D < 50" for Threshold2 to outperform QAOA2, meaning D=6..49.
But numerically at D=6, Threshold2 (5,5) = 0.1607 < QAOA2 = 0.1726.  Something inconsistent.
Let me re-read... Line 76: "The optimal 2-step threshold algorithm outperforms QAOA2 for all
5 < D < 50."  But Table 1 at D=6 shows 0.1607 < 0.1726.  Perhaps Table 1 lists the specific
(τ1, τ2) trialled, not the true optimum.  Or perhaps the paper's "5 < D < 50" statement is
about optimization more broadly.

Empirically: Threshold2 beats QAOA2 at D=4 per Table 1.  Focus there.

For the replication, we'll:
 1. Verify Threshold_1 matches Table 1 on Heawood (D=3, tau=3): expect 0.5 + 0.1875 = 0.6875.
 2. Verify Threshold_2 matches Table 1 on a D=4 girth>5 graph (tau1=3, tau2=4):
    expect 0.5 + 0.2128 = 0.7128.
 3. Compare to QAOA2 on the same D=4 graph.

D=4 girth>5 graph: the smallest such is the "4-regular Robertson graph"? Actually the smallest
4-regular graph of girth 6 is (4,6)-cage = 26 vertices (too big for QAOA statevector).
Alternative: use a random 4-regular high-girth-ish graph or use the LOCAL analysis
(the algorithm is 2-local on tree neighborhoods, so on ANY tree-like local structure
the expectation matches).  For a large enough random 4-regular graph, most edges have
girth-6 local neighborhoods, and the empirical estimate converges.

We'll estimate empirically on:
  (a) Heawood graph (D=3, n=14, girth=6): compare Threshold_1(τ=3), Threshold_2(τ1=2,τ2=3)
      to Table 1.
  (b) A large random 4-regular graph (n=200) with sampled girth-6+ subgraphs.
      Compare Threshold_2 optimal to Table 1 for D=4.
"""

import argparse
import json
import time
from pathlib import Path

import numpy as np
import networkx as nx


def one_step_threshold(spins, adj_list, tau):
    """Apply one step of the threshold algorithm.
    spins: 1D int array of +/-1 (length n).
    adj_list: list of neighbor index arrays.
    tau: integer threshold.
    Flip vertex v if number-of-same-spin-neighbors >= tau.
    All flips computed before any applied.
    Returns new spins.
    """
    n = len(spins)
    flip = np.zeros(n, dtype=bool)
    for v in range(n):
        nb = adj_list[v]
        if len(nb) == 0:
            continue
        same = int(np.sum(spins[nb] == spins[v]))
        if same >= tau:
            flip[v] = True
    new = spins.copy()
    new[flip] = -new[flip]
    return new


def threshold_algorithm(graph, taus, n_trials=2000, seed=0):
    """Run the (len(taus))-step threshold algorithm on `graph` and return
    the empirical mean cut fraction.
    """
    rng = np.random.default_rng(seed)
    n = graph.number_of_nodes()
    nodes = list(graph.nodes())
    idx = {v: i for i, v in enumerate(nodes)}
    adj_list = [np.array([idx[u] for u in graph.neighbors(v)], dtype=int)
                for v in nodes]
    edges = np.array([(idx[u], idx[v]) for u, v in graph.edges()], dtype=int)
    m = len(edges)

    cuts = np.zeros(n_trials, dtype=float)
    for t in range(n_trials):
        # random initial spins
        spins = rng.choice([-1, 1], size=n).astype(np.int8)
        for tau in taus:
            spins = one_step_threshold(spins, adj_list, tau)
        # count cut edges: spin[u] != spin[v]
        cut = int(np.sum(spins[edges[:, 0]] != spins[edges[:, 1]]))
        cuts[t] = cut / m
    return {
        "mean": float(np.mean(cuts)),
        "std": float(np.std(cuts)),
        "sem": float(np.std(cuts) / np.sqrt(n_trials)),
        "n_trials": n_trials,
        "n_vertices": n,
        "n_edges": m,
    }


def sweep_threshold2(graph, tau_range, n_trials=1000, seed=0):
    """Sweep over (tau1, tau2) pairs and record the mean cut fraction.
    """
    results = {}
    for t1 in tau_range:
        for t2 in tau_range:
            r = threshold_algorithm(graph, [t1, t2], n_trials=n_trials, seed=seed + t1 * 100 + t2)
            results[f"({t1},{t2})"] = r
    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--graph", default="heawood",
                    choices=["heawood", "mobius_kantor", "random_4reg",
                             "random_3reg_large", "random_5reg"])
    ap.add_argument("--n", type=int, default=200, help="n for random graphs")
    ap.add_argument("--trials", type=int, default=5000)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--tau_max", type=int, default=6)
    ap.add_argument("--out", default="report/evidence/threshold_result.json")
    args = ap.parse_args()

    if args.graph == "heawood":
        G = nx.heawood_graph()
        D = 3
    elif args.graph == "mobius_kantor":
        G = nx.moebius_kantor_graph()
        D = 3
    elif args.graph == "random_4reg":
        G = nx.random_regular_graph(4, args.n, seed=args.seed)
        D = 4
    elif args.graph == "random_5reg":
        G = nx.random_regular_graph(5, args.n, seed=args.seed)
        D = 5
    elif args.graph == "random_3reg_large":
        G = nx.random_regular_graph(3, args.n, seed=args.seed)
        D = 3

    n = G.number_of_nodes()
    m = G.number_of_edges()
    try:
        girth = nx.girth(G)
    except Exception:
        # fallback
        girth = -1
    print(f"[thresh] graph={args.graph} n={n} m={m} D={D} girth={girth}")

    # Table 1 targets (improvement over random, so cut fraction = 0.5 + value)
    table1_thr1 = {2: 0.2500, 3: 0.1875, 4: 0.1406, 5: 0.1562, 6: 0.1221}
    table1_thr1_tau = {2: 2, 3: 3, 4: 3, 5: 4, 6: 5}
    table1_thr2 = {2: 0.3125, 3: 0.2461, 4: 0.2128, 5: 0.1851, 6: 0.1607}
    table1_thr2_taus = {2: (2, 2), 3: (2, 3), 4: (3, 4), 5: (4, 4), 6: (5, 5)}

    t0 = time.time()
    # Threshold_1 at paper's best tau for this D
    tau1_paper = table1_thr1_tau.get(D)
    if tau1_paper is not None:
        r_thr1 = threshold_algorithm(G, [tau1_paper], n_trials=args.trials, seed=args.seed)
        thr1_paper_target = 0.5 + table1_thr1[D]
    else:
        r_thr1, thr1_paper_target = None, None

    # Threshold_2 at paper's best (tau1, tau2) for this D
    taus2_paper = table1_thr2_taus.get(D)
    if taus2_paper is not None:
        r_thr2 = threshold_algorithm(G, list(taus2_paper), n_trials=args.trials,
                                      seed=args.seed)
        thr2_paper_target = 0.5 + table1_thr2[D]
    else:
        r_thr2, thr2_paper_target = None, None

    # Sweep over (tau1, tau2) to find empirical optimum
    tau_range = list(range(1, args.tau_max + 1))
    sweep = sweep_threshold2(G, tau_range, n_trials=max(500, args.trials // 4),
                             seed=args.seed)
    best_key = max(sweep, key=lambda k: sweep[k]["mean"])
    best = sweep[best_key]

    elapsed = time.time() - t0
    out = {
        "graph": args.graph,
        "n_vertices": n,
        "n_edges": m,
        "D": D,
        "girth": int(girth),
        "n_trials": args.trials,
        "thr1_at_paper_tau": r_thr1,
        "thr1_paper_target_cut_fraction": thr1_paper_target,
        "thr1_paper_tau": tau1_paper,
        "thr2_at_paper_taus": r_thr2,
        "thr2_paper_target_cut_fraction": thr2_paper_target,
        "thr2_paper_taus": taus2_paper,
        "sweep_tau_range": tau_range,
        "sweep_results": sweep,
        "empirical_best_key": best_key,
        "empirical_best_cut_fraction": best["mean"],
        "elapsed_sec": elapsed,
    }
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(out, f, indent=2)

    if r_thr1:
        print(f"[thresh] Threshold_1 (tau={tau1_paper}) cut fraction = "
              f"{r_thr1['mean']:.4f} +/- {r_thr1['sem']:.4f}  "
              f"(paper: {thr1_paper_target:.4f})")
    if r_thr2:
        print(f"[thresh] Threshold_2 (taus={taus2_paper}) cut fraction = "
              f"{r_thr2['mean']:.4f} +/- {r_thr2['sem']:.4f}  "
              f"(paper: {thr2_paper_target:.4f})")
    print(f"[thresh] Empirical best over sweep: {best_key} -> "
          f"{best['mean']:.4f} +/- {best['sem']:.4f}")
    print(f"[thresh] elapsed = {elapsed:.1f} s -> {args.out}")


if __name__ == "__main__":
    main()
