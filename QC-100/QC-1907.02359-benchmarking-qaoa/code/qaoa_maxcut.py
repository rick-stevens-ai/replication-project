#!/usr/bin/env python3
"""
QAOA MAX-CUT benchmark reproducing the framework of
Willsch et al. 2019 (arXiv:1907.02359) "Benchmarking QAOA".

Uses Qiskit + Aer statevector simulator for exact E_p(gamma, beta).
Instances: n = 6, 8, 10 vertices; random 3-regular graphs and
Erdős–Rényi G(n, 0.5) graphs. QAOA layers p = 1, 2, 3.
Classical optimizer: COBYLA (SciPy).

Reports per instance:
  - Emin, Emax (exact classical MAX-CUT extremes)
  - E_p(gamma*, beta*)  optimized expectation
  - r = (E_p - Emax) / (Emin - Emax)     [Eq. (16) of the paper]
  - approximation ratio alpha = <cut>/C_max
      where <cut> = (Emax - E_p)/(Emax - Emin) * C_max + ...  see below
  - success probability P(ground state)
"""
from __future__ import annotations
import itertools, json, math, os, sys, time
from pathlib import Path
import numpy as np
import networkx as nx
from scipy.optimize import minimize

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

# ---------- Classical MAX-CUT (exact by brute force, n<=16) ----------

def cut_value(G: nx.Graph, bits: np.ndarray) -> int:
    """Number of cut edges given bit assignment (0/1 per vertex)."""
    c = 0
    for u, v in G.edges():
        if bits[u] != bits[v]:
            c += 1
    return c

def exact_extremes(G: nx.Graph):
    """Return (Cmax, Cmin_over_bits, Emin, Emax) using HC convention below.

    We use HC = sum_{(i,j) in E} (1/2)(Z_i Z_j - 1)  (see Eq. 4 of the paper).
    Eigenvalue on bitstring z: sum_{(i,j)} (1/2)((-1)^{z_i+z_j} - 1)
                             = -(# cut edges).
    So <z|HC|z> = -cut(z).  Emin = -Cmax, Emax = 0 (uncut config).
    Approx ratio alpha = cut(z) / Cmax = <-HC>/Cmax.
    Paper's r = (E_p - Emax)/(Emin - Emax) = E_p / Emin = E_p / (-Cmax).
    """
    n = G.number_of_nodes()
    best_cut = -1
    worst_cut = 10**9
    best_bits = None
    for x in range(2**n):
        bits = np.array([(x >> i) & 1 for i in range(n)], dtype=int)
        c = cut_value(G, bits)
        if c > best_cut:
            best_cut = c
            best_bits = bits.copy()
        if c < worst_cut:
            worst_cut = c
    Cmax = best_cut
    Cmin = worst_cut
    Emin = -Cmax          # smallest eigenvalue of HC
    Emax = -Cmin          # largest eigenvalue of HC (usually 0 if graph is bipartite-like; else -Cmin)
    return Cmax, Cmin, Emin, Emax, best_bits

# ---------- QAOA circuit ----------

def qaoa_circuit(G: nx.Graph, gammas, betas) -> QuantumCircuit:
    n = G.number_of_nodes()
    p = len(gammas)
    qc = QuantumCircuit(n)
    # initial |+>^n
    for q in range(n):
        qc.h(q)
    for layer in range(p):
        gamma = gammas[layer]
        beta = betas[layer]
        # Cost unitary  exp(-i gamma HC), HC = sum (1/2)(Z_i Z_j - 1)
        # The constant term is a global phase and can be dropped.
        # Per edge:  exp(-i gamma * (1/2) Z_i Z_j) = Rzz(gamma * 1)  in qiskit
        # Qiskit's Rzz(theta) = exp(-i theta/2 Z Z).  So we need theta = gamma.
        for (u, v) in G.edges():
            qc.rzz(gamma, u, v)
        # Mixer unitary  exp(-i beta HB), HB = sum X_i
        # per qubit: Rx(2 beta)
        for q in range(n):
            qc.rx(2 * beta, q)
    return qc

def _eig_table(G: nx.Graph) -> np.ndarray:
    n = G.number_of_nodes()
    eigs = np.empty(2**n)
    edges = list(G.edges())
    for x in range(2**n):
        c = 0
        for (u, v) in edges:
            if ((x >> u) & 1) != ((x >> v) & 1):
                c += 1
        eigs[x] = -c
    return eigs

def qaoa_expectation_and_probs(G: nx.Graph, params: np.ndarray, p: int, eigs: np.ndarray | None = None):
    gammas = params[:p]
    betas = params[p:]
    qc = qaoa_circuit(G, gammas, betas)
    sv = Statevector.from_instruction(qc)
    probs = np.abs(sv.data) ** 2
    if eigs is None:
        eigs = _eig_table(G)
    Ep = float(np.dot(probs, eigs))
    return Ep, probs, eigs

# ---------- Optimization loop ----------

def optimize_qaoa(G: nx.Graph, p: int, restarts: int = 4, seed: int = 0, maxiter: int = 200):
    rng = np.random.default_rng(seed)
    eigs = _eig_table(G)
    best = None
    for r in range(restarts):
        x0 = rng.uniform(0, math.pi, size=2 * p)
        def cost(x, _eigs=eigs):
            Ep, _, _ = qaoa_expectation_and_probs(G, x, p, eigs=_eigs)
            return Ep
        res = minimize(cost, x0, method="COBYLA",
                       options={"maxiter": maxiter, "rhobeg": 0.3, "disp": False})
        if best is None or res.fun < best.fun:
            best = res
    Ep, probs, eigs = qaoa_expectation_and_probs(G, best.x, p, eigs=eigs)
    Emin = eigs.min()
    P_ground = float(probs[np.isclose(eigs, Emin)].sum())
    return best.x, Ep, P_ground

# ---------- Benchmark ----------

def make_graphs():
    graphs = []
    rng_seeds = [11, 23, 37]
    # Random 3-regular, n=6,8,10
    for n, s in zip([6, 8, 10], rng_seeds):
        G = nx.random_regular_graph(3, n, seed=s)
        graphs.append((f"3reg_n{n}_s{s}", G))
    # Erdős–Rényi G(n, 0.5), n=6,8,10
    er_seeds = [101, 202, 303]
    for n, s in zip([6, 8, 10], er_seeds):
        G = nx.erdos_renyi_graph(n, 0.5, seed=s)
        # ensure connected/non-trivial
        while G.number_of_edges() == 0:
            s += 1
            G = nx.erdos_renyi_graph(n, 0.5, seed=s)
        graphs.append((f"er_n{n}_s{s}", G))
    return graphs

def main():
    out_dir = Path(__file__).resolve().parent.parent / "report" / "evidence"
    out_dir.mkdir(parents=True, exist_ok=True)
    results = []
    graphs = make_graphs()
    t_start = time.time()
    for label, G in graphs:
        n = G.number_of_nodes()
        m = G.number_of_edges()
        Cmax, Cmin, Emin, Emax, gs_bits = exact_extremes(G)
        print(f"\n=== {label}: n={n}, m={m}, Cmax={Cmax}, Cmin={Cmin} ===", flush=True)
        for p in (1, 2, 3):
            t0 = time.time()
            restarts = 4 if n <= 8 else 3
            maxiter = 200 if p == 1 else (250 if p == 2 else 300)
            params, Ep, Psucc = optimize_qaoa(G, p, restarts=restarts, seed=100 + p, maxiter=maxiter)
            # r as in Eq. (16)
            r = (Ep - Emax) / (Emin - Emax) if (Emin != Emax) else float("nan")
            # approximation ratio alpha = <cut>/Cmax = -Ep / Cmax
            alpha = (-Ep) / Cmax if Cmax > 0 else float("nan")
            dt = time.time() - t0
            print(f"  p={p}: Ep={Ep:+.4f}  r={r:.4f}  alpha={alpha:.4f}  P_gs={Psucc:.4f}  "
                  f"[t={dt:.1f}s, params={np.round(params,3).tolist()}]", flush=True)
            results.append({
                "graph": label, "n": n, "m": m,
                "Cmax": Cmax, "Cmin": Cmin, "Emin": Emin, "Emax": Emax,
                "p": p, "Ep": Ep, "r": r, "alpha": alpha, "P_ground": Psucc,
                "opt_params": np.round(params, 6).tolist(),
                "wallclock_s": dt,
            })
    dt_all = time.time() - t_start
    print(f"\nTotal wallclock: {dt_all:.1f}s")

    with open(out_dir / "qaoa_results.json", "w") as f:
        json.dump({"results": results, "total_wallclock_s": dt_all}, f, indent=2)
    # CSV
    import csv
    with open(out_dir / "qaoa_results.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["graph","n","m","Cmax","Cmin","Emin","Emax","p","Ep","r","alpha","P_ground","wallclock_s"])
        for r_ in results:
            w.writerow([r_["graph"], r_["n"], r_["m"], r_["Cmax"], r_["Cmin"],
                        r_["Emin"], r_["Emax"], r_["p"],
                        f'{r_["Ep"]:.6f}', f'{r_["r"]:.6f}',
                        f'{r_["alpha"]:.6f}', f'{r_["P_ground"]:.6f}',
                        f'{r_["wallclock_s"]:.2f}'])

    # Aggregates for the headline claim: mean alpha at each p per family
    def mean_by(family_prefix, p_val):
        vals = [x["alpha"] for x in results if x["graph"].startswith(family_prefix) and x["p"] == p_val]
        return float(np.mean(vals)), vals
    agg = {}
    for fam in ("3reg", "er"):
        for p_val in (1, 2, 3):
            m_a, vs = mean_by(fam, p_val)
            agg[f"{fam}_p{p_val}"] = {"mean_alpha": m_a, "values": vs}
    with open(out_dir / "qaoa_aggregate.json", "w") as f:
        json.dump(agg, f, indent=2)
    print("\nAggregate mean approx ratio:")
    for k, v in agg.items():
        print(f"  {k}: mean alpha = {v['mean_alpha']:.4f}   individual: {[round(x,4) for x in v['values']]}")

if __name__ == "__main__":
    main()
