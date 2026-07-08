"""
Multi-seed sanity check for arXiv:2201.11792 replication.

Uses a 4-qubit GHZ preparation circuit (H on q0, then CX cascade) so the
noiseless expectation value P(|0000>) = 0.5 has a large dynamic range.
Runs the ZNE experiment for several noise seeds and reports averages ±
standard deviation, both for uncorrelated depolarizing and time-correlated
coherent noise.
"""

import json
import os
import time
import numpy as np

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error

from mitiq import zne
from mitiq.zne.scaling import fold_gates_at_random
from mitiq.zne.inference import RichardsonFactory


NUM_SHOTS = 6000
NUM_TRIALS_CORRELATED = 80
SCALE_FACTORS = [1.0, 3.0, 5.0]
DEPOL_P = 0.02
CORR_SIGMA_STEP = 0.06
NUM_SEEDS = 5


def build_ghz(n=4) -> QuantumCircuit:
    qc = QuantumCircuit(n)
    qc.h(0)
    for i in range(n - 1):
        qc.cx(i, i + 1)
    # bring back with reverse cascade so the ideal state is |0...0>
    for i in reversed(range(n - 1)):
        qc.cx(i, i + 1)
    qc.h(0)
    qc.measure_all()
    return qc


def p_all_zero(counts, n):
    total = sum(counts.values())
    if total == 0:
        return 0.0
    return counts.get("0" * n, 0) / total


def make_depol_nm(p):
    nm = NoiseModel()
    err1 = depolarizing_error(p, 1)
    err2 = depolarizing_error(min(1.0, 2 * p), 2)
    for g in ["ry", "rz", "u", "u1", "u2", "u3", "sx", "x", "h"]:
        nm.add_all_qubit_quantum_error(err1, g)
    nm.add_all_qubit_quantum_error(err2, ["cx", "cz"])
    return nm


def exec_noiseless(circ):
    sim = AerSimulator()
    tqc = transpile(circ, sim, optimization_level=0)
    r = sim.run(tqc, shots=NUM_SHOTS).result()
    return p_all_zero(r.get_counts(), circ.num_qubits)


def exec_uncorr(circ):
    sim = AerSimulator(noise_model=make_depol_nm(DEPOL_P))
    tqc = transpile(circ, sim, optimization_level=0)
    r = sim.run(tqc, shots=NUM_SHOTS, seed_simulator=int(np.random.randint(1 << 30))).result()
    return p_all_zero(r.get_counts(), tqc.num_qubits)


def inject_drift(circ, rng):
    new = QuantumCircuit(*circ.qregs, *circ.cregs)
    theta = float(rng.normal(0.0, CORR_SIGMA_STEP))
    for instr in circ.data:
        op = instr.operation
        qargs = instr.qubits
        cargs = instr.clbits
        new.append(op, qargs, cargs)
        if op.name in ("measure", "barrier", "reset"):
            continue
        theta += float(rng.normal(0.0, CORR_SIGMA_STEP))
        for q in qargs:
            new.rz(theta, q)
    return new


def exec_corr(circ):
    sim = AerSimulator()
    trials = NUM_TRIALS_CORRELATED
    shots_per_trial = max(1, NUM_SHOTS // trials)
    rng = np.random.default_rng()
    circuits = [inject_drift(circ, rng) for _ in range(trials)]
    tqcs = transpile(circuits, sim, optimization_level=0)
    r = sim.run(tqcs, shots=shots_per_trial).result()
    counts = {}
    for i in range(trials):
        for k, v in r.get_counts(i).items():
            counts[k] = counts.get(k, 0) + v
    return p_all_zero(counts, circ.num_qubits)


def run_one_seed(seed, log):
    np.random.seed(seed)
    circ = build_ghz(4)
    noiseless = exec_noiseless(circ)
    log(f"  seed={seed}  circ depth={circ.depth()} size={circ.size()} noiseless={noiseless:.4f}")

    raw_u = exec_uncorr(circ)
    fac = RichardsonFactory(scale_factors=SCALE_FACTORS)
    zne_u = zne.execute_with_zne(circ, exec_uncorr, factory=fac, scale_noise=fold_gates_at_random)

    raw_c = exec_corr(circ)
    fac2 = RichardsonFactory(scale_factors=SCALE_FACTORS)
    zne_c = zne.execute_with_zne(circ, exec_corr, factory=fac2, scale_noise=fold_gates_at_random)

    return {
        "seed": seed,
        "noiseless": noiseless,
        "raw_uncorr": raw_u,
        "zne_uncorr": zne_u,
        "raw_corr": raw_c,
        "zne_corr": zne_c,
    }


def main():
    out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "report", "evidence")
    os.makedirs(out_dir, exist_ok=True)
    log_path = os.path.join(out_dir, "run_ghz_multiseed.log")
    logf = open(log_path, "w")

    def log(m):
        print(m)
        logf.write(m + "\n")
        logf.flush()

    log(f"# GHZ multi-seed replication of arXiv:2201.11792")
    log(f"# num_seeds={NUM_SEEDS} shots={NUM_SHOTS} trials_corr={NUM_TRIALS_CORRELATED}")
    log(f"# depol_p={DEPOL_P} corr_sigma_step={CORR_SIGMA_STEP} scales={SCALE_FACTORS}")

    rows = []
    t0 = time.time()
    for s in range(1, NUM_SEEDS + 1):
        r = run_one_seed(seed=1000 + s, log=log)
        rows.append(r)
        log(f"  --> raw_u={r['raw_uncorr']:.4f} zne_u={r['zne_uncorr']:.4f}  raw_c={r['raw_corr']:.4f} zne_c={r['zne_corr']:.4f}   ({time.time()-t0:.0f}s)")

    noiseless = np.mean([r["noiseless"] for r in rows])
    def stat(key):
        arr = np.array([r[key] for r in rows])
        return float(arr.mean()), float(arr.std(ddof=1))

    m_raw_u, s_raw_u = stat("raw_uncorr")
    m_zne_u, s_zne_u = stat("zne_uncorr")
    m_raw_c, s_raw_c = stat("raw_corr")
    m_zne_c, s_zne_c = stat("zne_corr")

    bias_raw_u = m_raw_u - noiseless
    bias_zne_u = m_zne_u - noiseless
    bias_raw_c = m_raw_c - noiseless
    bias_zne_c = m_zne_c - noiseless

    zne_helps_uncorrelated = abs(bias_zne_u) < abs(bias_raw_u)
    zne_worse_under_correlation = abs(bias_zne_c) > abs(bias_zne_u)

    summary = {
        "arxiv_id": "2201.11792",
        "circuit": "GHZ prepare-and-invert (4 qubits)",
        "num_seeds": NUM_SEEDS,
        "num_shots": NUM_SHOTS,
        "num_trials_correlated": NUM_TRIALS_CORRELATED,
        "scale_factors": SCALE_FACTORS,
        "depol_p": DEPOL_P,
        "corr_sigma_step": CORR_SIGMA_STEP,
        "per_seed": rows,
        "noiseless_mean": float(noiseless),
        "uncorrelated": {
            "raw_mean": m_raw_u, "raw_std": s_raw_u,
            "zne_mean": m_zne_u, "zne_std": s_zne_u,
            "bias_raw": bias_raw_u,
            "bias_zne": bias_zne_u,
        },
        "time_correlated": {
            "raw_mean": m_raw_c, "raw_std": s_raw_c,
            "zne_mean": m_zne_c, "zne_std": s_zne_c,
            "bias_raw": bias_raw_c,
            "bias_zne": bias_zne_c,
        },
        "checks": {
            "zne_helps_uncorrelated": bool(zne_helps_uncorrelated),
            "zne_worse_under_correlation_vs_uncorrelated": bool(zne_worse_under_correlation),
            "variance_ratio_zne_corr_over_uncorr": (s_zne_c / s_zne_u) if s_zne_u > 0 else None,
        },
    }
    with open(os.path.join(out_dir, "results_ghz_multiseed.json"), "w") as f:
        json.dump(summary, f, indent=2, default=float)
    log("")
    log(f"# noiseless                = {noiseless:.4f}")
    log(f"# raw (uncorr)  = {m_raw_u:.4f} ± {s_raw_u:.4f}   bias={bias_raw_u:+.4f}")
    log(f"# ZNE (uncorr)  = {m_zne_u:.4f} ± {s_zne_u:.4f}   bias={bias_zne_u:+.4f}")
    log(f"# raw (corr)    = {m_raw_c:.4f} ± {s_raw_c:.4f}   bias={bias_raw_c:+.4f}")
    log(f"# ZNE (corr)    = {m_zne_c:.4f} ± {s_zne_c:.4f}   bias={bias_zne_c:+.4f}")
    log(f"# ZNE-helps-uncorr={zne_helps_uncorrelated}   ZNE-worse-under-corr={zne_worse_under_correlation}")
    log(f"# var(ZNE_corr)/var(ZNE_uncorr) = {(s_zne_c/s_zne_u) if s_zne_u>0 else 'nan'}")
    logf.close()


if __name__ == "__main__":
    main()
