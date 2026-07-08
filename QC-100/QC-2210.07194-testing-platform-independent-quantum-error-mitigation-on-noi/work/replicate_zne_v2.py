#!/usr/bin/env python3
"""
Independent replication (v2) of Russo et al. (2210.07194).

Adds:
  - Multi-trial averaging (t = 8) at each (n,d) to reduce shot noise in mu
  - Two noise levels: 1% (paper canonical) and 0.5% (to expose the low-depth
    regime where ZNE improvement is clearest, matching paper Fig 2 first bin)
  - Reports per-depth Root-Mean-Square Errors (RMSE) as well as mu

Method identical to v1: global folding, scale factors {1,2,3}, N=1e4 shots
split N/3 per scaled circuit for ZNE, |C|=4 random RB circuits per depth.
"""
import json, math, os, sys, time
from pathlib import Path
from typing import Callable

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import random_clifford
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error

from mitiq import zne
from mitiq.zne.scaling import fold_global
from mitiq.zne.inference import RichardsonFactory, LinearFactory

OUT = Path(__file__).resolve().parent.parent / "report" / "evidence"
OUT.mkdir(parents=True, exist_ok=True)

N_SHOTS_TOTAL = 10_000
K_ZNE = 3
SCALE_FACTORS = [1.0, 2.0, 3.0]
DEPTHS = [1, 3, 5, 7, 9]
N_CIRCUITS = 4
N_TRIALS = 4          # was 1 in v1; average over 4 trials
N_QUBITS = 3
NOISE_LEVELS = [0.005, 0.01]  # 0.5% and 1% (paper canonical)
RNG_SEED = 20260704


def build_rb_circuit(n, d, rng):
    layers, prod = [], None
    for _ in range(d):
        cl = random_clifford(n, seed=int(rng.integers(0, 2**31 - 1)))
        layers.append(cl); prod = cl if prod is None else cl.compose(prod)
    inv = prod.adjoint()
    qc = QuantumCircuit(n)
    for cl in layers:
        qc.compose(cl.to_circuit(), inplace=True)
    qc.compose(inv.to_circuit(), inplace=True)
    return qc


def make_noise_model(p_2q):
    nm = NoiseModel()
    err2 = depolarizing_error(p_2q, num_qubits=2)
    nm.add_all_qubit_quantum_error(err2, ["cx", "cz", "swap", "ecr"])
    return nm


def make_executor(shots, noise_model, n_qubits):
    sim = AerSimulator(noise_model=noise_model)
    target = "0" * n_qubits
    def executor(circuit) -> float:      # runtime annotation matters for mitiq!
        qc = circuit.copy()
        qc.measure_all()
        tqc = transpile(qc, sim, optimization_level=0)
        counts = sim.run(tqc, shots=shots).result().get_counts()
        total = sum(counts.values())
        p0 = sum(c for bs, c in counts.items() if bs.replace(" ", "") == target)
        return float(p0 / total)
    return executor


def improvement_factor(unmit_sq_err, mit_sq_err, n_unmit_shots, n_qem_shots):
    if mit_sq_err <= 0.0:
        return float("inf")
    return math.sqrt(n_unmit_shots * unmit_sq_err) / math.sqrt(n_qem_shots * mit_sq_err)


def run_one_noise(p_2q, rng):
    noise = make_noise_model(p_2q)
    shots_unmit = N_SHOTS_TOTAL
    shots_per_scale = N_SHOTS_TOTAL // K_ZNE
    exe_unmit = make_executor(shots_unmit, noise, N_QUBITS)
    exe_zne   = make_executor(shots_per_scale, noise, N_QUBITS)
    ideal = 1.0

    print(f"\n### Noise: {p_2q*100:.2f}% 2Q depolarizing ###")
    print(f"{'d':>2} {'A0':>8} {'AZNE_R':>8} {'AZNE_L':>8} "
          f"{'RMSE_0':>8} {'RMSE_R':>8} {'RMSE_L':>8} "
          f"{'mu_R':>7} {'mu_L':>7}")

    depth_records = []
    for d in DEPTHS:
        # generate fixed set of |C| circuits once for this depth
        circuits = [build_rb_circuit(N_QUBITS, d, rng) for _ in range(N_CIRCUITS)]
        # per-circuit lists across trials
        A0_all, AR_all, AL_all = [], [], []
        for t in range(N_TRIALS):
            for circ in circuits:
                a0 = exe_unmit(circ)
                aR = zne.execute_with_zne(circuit=circ, executor=exe_zne,
                     factory=RichardsonFactory(scale_factors=SCALE_FACTORS),
                     scale_noise=fold_global)
                aL = zne.execute_with_zne(circuit=circ, executor=exe_zne,
                     factory=LinearFactory(scale_factors=SCALE_FACTORS),
                     scale_noise=fold_global)
                A0_all.append(a0); AR_all.append(aR); AL_all.append(aL)
        # RMSE
        rmse0 = math.sqrt(np.mean([(a-ideal)**2 for a in A0_all]))
        rmseR = math.sqrt(np.mean([(a-ideal)**2 for a in AR_all]))
        rmseL = math.sqrt(np.mean([(a-ideal)**2 for a in AL_all]))
        # improvement factor (paper Eq. 5, aggregated over all trials & circuits)
        sq0 = sum((a-ideal)**2 for a in A0_all)
        sqR = sum((a-ideal)**2 for a in AR_all)
        sqL = sum((a-ideal)**2 for a in AL_all)
        muR = improvement_factor(sq0, sqR, shots_unmit, K_ZNE*shots_per_scale)
        muL = improvement_factor(sq0, sqL, shots_unmit, K_ZNE*shots_per_scale)

        print(f"{d:>2} {np.mean(A0_all):>8.4f} {np.mean(AR_all):>8.4f} {np.mean(AL_all):>8.4f} "
              f"{rmse0:>8.4f} {rmseR:>8.4f} {rmseL:>8.4f} {muR:>7.3f} {muL:>7.3f}")
        depth_records.append({
            "d": d,
            "A0_mean": float(np.mean(A0_all)),
            "AZNE_R_mean": float(np.mean(AR_all)),
            "AZNE_L_mean": float(np.mean(AL_all)),
            "RMSE_unmit": rmse0, "RMSE_ZNE_R": rmseR, "RMSE_ZNE_L": rmseL,
            "mu_ZNE_R": muR, "mu_ZNE_L": muL,
            "n_trials": N_TRIALS, "n_circuits": N_CIRCUITS,
        })
    return depth_records


def main():
    rng = np.random.default_rng(RNG_SEED)
    results = {
        "config": {
            "n_qubits": N_QUBITS, "depths": DEPTHS,
            "n_circuits_per_depth": N_CIRCUITS, "n_trials": N_TRIALS,
            "shots_total": N_SHOTS_TOTAL, "k_zne": K_ZNE,
            "scale_factors": SCALE_FACTORS,
            "noise_levels_2q_depol": NOISE_LEVELS,
            "seed": RNG_SEED,
            "mitiq_version": __import__("mitiq").__version__,
            "qiskit_version": __import__("qiskit").__version__,
            "qiskit_aer_version": __import__("qiskit_aer").__version__,
        },
        "per_noise": {},
    }
    for p in NOISE_LEVELS:
        key = f"depol_{int(p*1000):d}pmil"    # e.g. depol_5pmil, depol_10pmil
        results["per_noise"][key] = run_one_noise(p, rng)

    # summary claim check
    summary = {}
    for key, rows in results["per_noise"].items():
        muR = [r["mu_ZNE_R"] for r in rows]
        muL = [r["mu_ZNE_L"] for r in rows]
        rmse0 = [r["RMSE_unmit"] for r in rows]
        rmseR = [r["RMSE_ZNE_R"] for r in rows]
        rmseL = [r["RMSE_ZNE_L"] for r in rows]
        summary[key] = {
            "mu_R_mean": float(np.mean(muR)),
            "mu_R_range": [float(np.min(muR)), float(np.max(muR))],
            "mu_L_mean": float(np.mean(muL)),
            "mu_L_range": [float(np.min(muL)), float(np.max(muL))],
            "fraction_mu_R_above_1": float(np.mean([m > 1.0 for m in muR])),
            "fraction_mu_L_above_1": float(np.mean([m > 1.0 for m in muL])),
            "median_depth1_mu_R": float(muR[0]),
            "median_depth1_mu_L": float(muL[0]),
            "RMSE_reduction_R_at_d1": float(rmse0[0] / max(rmseR[0], 1e-9)),
            "RMSE_reduction_L_at_d1": float(rmse0[0] / max(rmseL[0], 1e-9)),
        }
    results["summary"] = summary

    out = OUT / "zne_results_v2.json"
    with open(out, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nWrote {out}")
    print("\n### Summary ###")
    for k, s in summary.items():
        print(f" {k}:")
        for kk, vv in s.items():
            print(f"    {kk}: {vv}")


if __name__ == "__main__":
    t0 = time.time()
    main()
    print(f"\nWall time: {time.time()-t0:.1f}s")
