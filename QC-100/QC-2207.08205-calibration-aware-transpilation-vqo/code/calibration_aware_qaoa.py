"""
Independent replication of arXiv:2207.08205
"Calibration-Aware Transpilation for Variational Quantum Optimization" (Ji et al., 2022)

Reproducible core: QAOA MAX-CUT on a small graph run on a mock IBM-style heavy-hex-ish
device with per-qubit / per-edge calibration data.

Compare two placement strategies:
  (a) STANDARD:   Qiskit transpiler with random (arbitrary) qubit selection
  (b) CAL-AWARE:  Pick the sub-graph of qubits with the LOWEST cumulative error
                  (matches paper's NAM = Noise-Aware Matching step).

Measure approximation ratio (AR) of the sampled solutions under a realistic noise
model built from the calibration data. Expect CA-placement > standard-placement.

Uses qiskit + qiskit-aer (real Aer simulator, no fabricated results).
"""

import json
import time
from pathlib import Path
from itertools import combinations

import numpy as np
import networkx as nx

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import (
    NoiseModel, depolarizing_error, ReadoutError,
)


# ---------------------------------------------------------------------------
# Reproducibility
# ---------------------------------------------------------------------------
SEED = 20260703
np.random.seed(SEED)
rng = np.random.default_rng(SEED)


# ---------------------------------------------------------------------------
# 1. Problem: MAX-CUT on a small graph (n = 6)
# ---------------------------------------------------------------------------
def build_problem(n=6, seed=SEED):
    """A small MAX-CUT instance. n=6 is well within CPU-Aer capacity."""
    g = nx.Graph()
    g.add_nodes_from(range(n))
    # Simple 3-regular-ish ring + chords (deterministic, small, easy to verify)
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0),  # ring
             (0, 3), (1, 4), (2, 5)]                          # chords => 3-regular
    for (u, v) in edges:
        g.add_edge(u, v, weight=1.0)
    return g


def maxcut_value(bitstring, g: nx.Graph):
    """Number of cut edges for a given bitstring assignment (bit i = node i)."""
    v = 0
    for (u, w, d) in g.edges(data=True):
        if bitstring[u] != bitstring[w]:
            v += d.get("weight", 1.0)
    return v


def brute_force_maxcut(g: nx.Graph):
    """Return the optimal cut value by enumeration (fine for n<=20)."""
    n = g.number_of_nodes()
    best = 0
    for k in range(2 ** n):
        bits = [(k >> i) & 1 for i in range(n)]
        v = maxcut_value(bits, g)
        if v > best:
            best = v
    return best


# ---------------------------------------------------------------------------
# 2. QAOA circuit (p=1) for MAX-CUT
# ---------------------------------------------------------------------------
def qaoa_maxcut_circuit(g: nx.Graph, gamma: float, beta: float) -> QuantumCircuit:
    n = g.number_of_nodes()
    qc = QuantumCircuit(n, n)
    # Initial |+>^n
    for q in range(n):
        qc.h(q)
    # Cost unitary exp(-i gamma sum_{(u,v)} (I - Z_u Z_v)/2)
    for (u, v) in g.edges():
        qc.cx(u, v)
        qc.rz(2 * gamma, v)
        qc.cx(u, v)
    # Mixer exp(-i beta sum_i X_i)
    for q in range(n):
        qc.rx(2 * beta, q)
    qc.measure(range(n), range(n))
    return qc


# ---------------------------------------------------------------------------
# 3. Mock hardware: heavy-hex-ish 20-qubit coupling map + calibration table
# ---------------------------------------------------------------------------
def build_mock_device(seed=SEED):
    """
    Build a mock IBM-style device.
    Coupling map: 20 physical qubits arranged in a heavy-hex-like graph.
    Calibration: per-qubit single-gate error, per-edge cx error, per-qubit readout error.
    We deliberately make some regions LOW-error and others HIGH-error, mimicking
    real ibmq_ehningen snapshots the paper shows in Fig. 1-2.
    """
    n_phys = 20
    # Heavy-hex-ish coupling: two rows of 10 qubits with vertical connectors
    coupling = []
    # Row A: 0..9  Row B: 10..19
    for i in range(9):
        coupling.append((i, i + 1))
        coupling.append((10 + i, 11 + i))
    # Vertical connectors every 2
    for i in range(0, 10, 2):
        coupling.append((i, 10 + i))
    # Symmetric edges
    edges = set()
    for (u, v) in coupling:
        edges.add((min(u, v), max(u, v)))
    coupling = sorted(edges)

    r = np.random.default_rng(seed)

    # Per-qubit single-gate error
    # Baseline 5e-4, but qubits 8, 9, 15, 16, 17 are BAD (higher)
    bad_qubits = {8, 9, 15, 16, 17}
    sq_err = {}
    for q in range(n_phys):
        base = r.uniform(3e-4, 8e-4)
        if q in bad_qubits:
            base *= 6.0
        sq_err[q] = float(base)

    # Per-edge cx error
    # Baseline 8e-3, but edges touching bad qubits are much worse
    cx_err = {}
    for (u, v) in coupling:
        base = r.uniform(5e-3, 1.5e-2)
        if u in bad_qubits or v in bad_qubits:
            base *= 5.0
        # One specific very bad edge (mirrors the paper's "cx between 8-9" outlier)
        if (u, v) == (8, 9):
            base = 0.12
        cx_err[(u, v)] = float(base)

    # Per-qubit readout error
    ro_err = {}
    for q in range(n_phys):
        base = r.uniform(0.01, 0.03)
        if q in bad_qubits:
            base *= 3.0
        ro_err[q] = float(base)

    return {
        "n_phys": n_phys,
        "coupling": coupling,
        "sq_err": sq_err,
        "cx_err": cx_err,
        "ro_err": ro_err,
    }


def coupling_subgraph(device, qubits):
    """Return the sub-list of coupling edges induced by given physical qubits."""
    qset = set(qubits)
    return [(u, v) for (u, v) in device["coupling"] if u in qset and v in qset]


def is_connected_subgraph(device, qubits, needed_edges=None):
    """Check that the induced subgraph on qubits is connected (has a spanning tree)."""
    sub_edges = coupling_subgraph(device, qubits)
    if not sub_edges:
        return len(qubits) <= 1
    gg = nx.Graph()
    gg.add_nodes_from(qubits)
    gg.add_edges_from(sub_edges)
    return nx.is_connected(gg)


# ---------------------------------------------------------------------------
# 4. Effective fidelity per paper Eq. (3): product of gate fidelities.
# ---------------------------------------------------------------------------
def effective_fidelity(qubits, device, n_cx_estimate):
    """
    Simplified fidelity estimate used to RANK sub-graphs (Alg. 2 in the paper):
      F = prod(f_single) * prod(f_cx over used edges) * prod(f_readout)
    We approximate: each qubit contributes its single-gate fidelity ^ (typical count),
    the induced-edge cx fidelities enter once each (times the ratio of cx-per-edge),
    and readout enters once per qubit.
    """
    f = 1.0
    for q in qubits:
        # single-qubit gates (~a few per qubit for p=1 QAOA on 6 qubits)
        f *= (1.0 - device["sq_err"][q]) ** 3
        # readout
        f *= (1.0 - device["ro_err"][q])
    sub_edges = coupling_subgraph(device, qubits)
    if not sub_edges:
        return 0.0
    # per-edge cx contribution: distribute total cx count across available edges
    per_edge_cx = max(1, n_cx_estimate // max(1, len(sub_edges)))
    for e in sub_edges:
        f *= (1.0 - device["cx_err"][e]) ** per_edge_cx
    return f


# ---------------------------------------------------------------------------
# 5. Placement strategies
# ---------------------------------------------------------------------------
def random_placement(device, k, seed):
    """
    "Standard" placement: pick k physical qubits at random, subject to the induced
    subgraph being CONNECTED (otherwise transpiler swap insertion explodes).
    """
    r = np.random.default_rng(seed)
    for _ in range(500):
        picks = tuple(sorted(r.choice(device["n_phys"], size=k, replace=False)))
        if is_connected_subgraph(device, picks):
            return picks
    # Fallback: just take first k connected qubits along row A
    return tuple(range(k))


def calibration_aware_placement(device, k, n_cx_estimate, n_trials=200, seed=SEED):
    """
    Paper's NAM (Alg. 2): try many candidate sub-graphs, pick highest effective fidelity.
    We enumerate/sample candidate connected k-subsets and rank by effective_fidelity.
    """
    r = np.random.default_rng(seed + 7)
    best = None
    best_f = -1.0
    tried = 0
    seen = set()

    # First enumerate all connected subsets of size k up to a cap
    max_enum = 5000
    all_qubits = list(range(device["n_phys"]))
    for combo in combinations(all_qubits, k):
        if tried >= max_enum:
            break
        if is_connected_subgraph(device, combo):
            key = tuple(sorted(combo))
            if key in seen:
                continue
            seen.add(key)
            f = effective_fidelity(combo, device, n_cx_estimate)
            if f > best_f:
                best_f = f
                best = key
            tried += 1

    if best is None:
        # Fallback random search
        for _ in range(n_trials):
            picks = tuple(sorted(r.choice(device["n_phys"], size=k, replace=False)))
            if is_connected_subgraph(device, picks):
                f = effective_fidelity(picks, device, n_cx_estimate)
                if f > best_f:
                    best_f = f
                    best = picks
    return best, best_f


# ---------------------------------------------------------------------------
# 6. Noise model from calibration data (restricted to used qubits/edges)
# ---------------------------------------------------------------------------
def build_noise_model(device, active_qubits):
    """
    Build an Aer noise model. Since we're going to relabel qubits during transpile,
    we build the noise model over the FULL device (per-qubit / per-edge) and let
    the simulator apply it to whichever physical qubits end up in the transpiled circuit.
    """
    nm = NoiseModel()

    # Single-qubit depolarizing errors
    for q, err in device["sq_err"].items():
        # applied to any single-qubit gate on that qubit
        e = depolarizing_error(err, 1)
        nm.add_quantum_error(e, ["u1", "u2", "u3", "u", "rz", "sx", "x", "h", "rx", "ry"], [q])

    # Two-qubit cx errors — symmetric on each edge
    for (u, v), err in device["cx_err"].items():
        e = depolarizing_error(err, 2)
        nm.add_quantum_error(e, ["cx"], [u, v])
        nm.add_quantum_error(e, ["cx"], [v, u])

    # Readout errors
    for q, err in device["ro_err"].items():
        p01 = err
        p10 = err
        ro = ReadoutError([[1 - p01, p01], [p10, 1 - p10]])
        nm.add_readout_error(ro, [q])

    return nm


# ---------------------------------------------------------------------------
# 7. Run one QAOA experiment with a specific placement
# ---------------------------------------------------------------------------
def run_qaoa_experiment(g, device, placement, label, shots=4096, seed=SEED):
    """Grid-search (gamma, beta) — QAOA p=1 — on given placement + noise model,
    return best AR + expectation table."""
    n = g.number_of_nodes()
    # Grid over (gamma, beta)
    n_grid = 9
    gammas = np.linspace(0, np.pi, n_grid)
    betas = np.linspace(0, np.pi / 2, n_grid)

    # Build noise model
    nm = build_noise_model(device, placement)
    sim = AerSimulator(noise_model=nm, seed_simulator=seed)

    # Optimal MAX-CUT value (for AR normalization)
    opt = brute_force_maxcut(g)

    # Coupling map for transpile (edges induced by placement)
    sub_edges = coupling_subgraph(device, placement)
    # Convert coupling to bidirectional list of pairs (physical indices)
    coupling_map = []
    for (u, v) in sub_edges:
        coupling_map.append([u, v])
        coupling_map.append([v, u])

    # Initial layout: virtual qubit i -> physical qubit placement[i]
    initial_layout = list(placement)

    best_ar = -1.0
    best_params = None
    per_point = []
    for gm in gammas:
        for bt in betas:
            qc = qaoa_maxcut_circuit(g, gm, bt)
            tqc = transpile(
                qc,
                basis_gates=["cx", "sx", "x", "rz", "id"],
                coupling_map=coupling_map,
                initial_layout=initial_layout,
                optimization_level=1,
                seed_transpiler=seed,
            )
            job = sim.run(tqc, shots=shots)
            counts = job.result().get_counts()

            # Compute expected MAX-CUT value from samples
            exp_val = 0.0
            total = 0
            for bitstring, c in counts.items():
                bits = [int(b) for b in bitstring[::-1]]  # Qiskit little-endian
                v = maxcut_value(bits, g)
                exp_val += v * c
                total += c
            exp_val /= total
            ar = exp_val / opt
            per_point.append({"gamma": float(gm), "beta": float(bt),
                              "exp": float(exp_val), "AR": float(ar)})
            if ar > best_ar:
                best_ar = ar
                best_params = (float(gm), float(bt))

    return {
        "label": label,
        "placement": list(placement),
        "n_qubits_algo": n,
        "opt_maxcut": opt,
        "best_AR": float(best_ar),
        "best_params": best_params,
        "grid": per_point,
    }


# ---------------------------------------------------------------------------
# 8. Main
# ---------------------------------------------------------------------------
def main(out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 78)
    print("QC-100 replication: arXiv:2207.08205 calibration-aware transpilation for VQO")
    print("=" * 78)

    g = build_problem(n=6)
    opt = brute_force_maxcut(g)
    print(f"Problem: MAX-CUT on n={g.number_of_nodes()} nodes, m={g.number_of_edges()} edges")
    print(f"Brute-force optimal cut value = {opt}")

    device = build_mock_device()
    print(f"Mock device: {device['n_phys']} physical qubits, "
          f"{len(device['coupling'])} coupling edges")
    print(f"  bad qubits (elevated error): 8,9,15,16,17")

    # Estimate cx count in QAOA circuit (2 per edge for p=1)
    n_cx_estimate = 2 * g.number_of_edges()  # ~18
    k = g.number_of_nodes()

    # (a) Standard: random placement
    rand_place = random_placement(device, k, seed=SEED)
    f_rand = effective_fidelity(rand_place, device, n_cx_estimate)
    print(f"\n[standard] random placement    = {rand_place}, effective F = {f_rand:.4f}")

    # (b) Calibration-aware placement
    ca_place, f_ca = calibration_aware_placement(device, k, n_cx_estimate)
    print(f"[cal-aware] best placement      = {ca_place}, effective F = {f_ca:.4f}")

    # For a fair "random" baseline, do 5 random placements and take the mean AR
    print("\nRunning QAOA on cal-aware placement...")
    t0 = time.time()
    result_ca = run_qaoa_experiment(g, device, ca_place, label="cal-aware")
    print(f"  best AR = {result_ca['best_AR']:.4f} "
          f"(gamma,beta={result_ca['best_params']})  [{time.time()-t0:.1f}s]")

    n_random_trials = 5
    random_results = []
    print(f"\nRunning QAOA on {n_random_trials} random placements...")
    for i in range(n_random_trials):
        rp = random_placement(device, k, seed=SEED + 100 * (i + 1))
        f_rp = effective_fidelity(rp, device, n_cx_estimate)
        print(f"  trial {i+1}: placement = {rp}, effective F = {f_rp:.4f}")
        t0 = time.time()
        r = run_qaoa_experiment(g, device, rp, label=f"random_{i+1}",
                                seed=SEED + 100 * (i + 1))
        r["effective_F"] = f_rp
        random_results.append(r)
        print(f"    best AR = {r['best_AR']:.4f}  [{time.time()-t0:.1f}s]")

    mean_random_AR = float(np.mean([r["best_AR"] for r in random_results]))
    std_random_AR = float(np.std([r["best_AR"] for r in random_results]))

    print("\n" + "=" * 78)
    print("SUMMARY")
    print("=" * 78)
    print(f"Standard (random) placement:  AR = {mean_random_AR:.4f} ± {std_random_AR:.4f} "
          f"(mean of {n_random_trials} trials)")
    print(f"Cal-aware placement:          AR = {result_ca['best_AR']:.4f}")
    improvement = (result_ca['best_AR'] - mean_random_AR) / mean_random_AR * 100
    print(f"Relative improvement:         {improvement:+.1f}%")

    # Ideal (no-noise) upper bound
    print("\nRunning noise-free QAOA for reference upper bound...")
    ideal_sim = AerSimulator(seed_simulator=SEED)
    n_grid = 9
    ideal_best = -1.0
    for gm in np.linspace(0, np.pi, n_grid):
        for bt in np.linspace(0, np.pi / 2, n_grid):
            qc = qaoa_maxcut_circuit(g, gm, bt)
            tqc = transpile(qc, ideal_sim, optimization_level=1, seed_transpiler=SEED)
            job = ideal_sim.run(tqc, shots=4096)
            counts = job.result().get_counts()
            exp = 0.0; tot = 0
            for bs, c in counts.items():
                bits = [int(b) for b in bs[::-1]]
                exp += maxcut_value(bits, g) * c
                tot += c
            ar = (exp / tot) / opt
            if ar > ideal_best:
                ideal_best = ar
    print(f"Noise-free QAOA (upper bound): AR = {ideal_best:.4f}")

    summary = {
        "paper": "arXiv:2207.08205",
        "problem": {
            "graph_nodes": g.number_of_nodes(),
            "graph_edges": g.number_of_edges(),
            "opt_maxcut": opt,
        },
        "device": {
            "n_phys": device["n_phys"],
            "n_coupling_edges": len(device["coupling"]),
            "bad_qubits": [8, 9, 15, 16, 17],
        },
        "cal_aware": {
            "placement": list(ca_place),
            "effective_fidelity": float(f_ca),
            "best_AR": result_ca["best_AR"],
            "best_params": result_ca["best_params"],
        },
        "random_baseline": {
            "n_trials": n_random_trials,
            "mean_AR": mean_random_AR,
            "std_AR": std_random_AR,
            "per_trial": [
                {"placement": r["placement"], "AR": r["best_AR"],
                 "effective_F": r["effective_F"]}
                for r in random_results
            ],
        },
        "improvement_percent": improvement,
        "ideal_noise_free_AR": float(ideal_best),
        "seed": SEED,
    }

    def _clean(o):
        if isinstance(o, dict):
            return {k: _clean(v) for k, v in o.items()}
        if isinstance(o, (list, tuple)):
            return [_clean(v) for v in o]
        if isinstance(o, np.integer):
            return int(o)
        if isinstance(o, np.floating):
            return float(o)
        return o
    (out_dir / "results.json").write_text(json.dumps(_clean(summary), indent=2))
    print(f"\nSaved: {out_dir / 'results.json'}")
    return summary


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "./evidence"
    main(out)
