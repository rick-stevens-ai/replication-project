#!/usr/bin/env python3
"""
Independent replication of Russo et al. (2210.07194)
"Testing platform-independent quantum error mitigation on noisy quantum computers"

Reproduces the core paper claim:
  On randomized-benchmarking-style circuits under 1% two-qubit depolarizing
  noise, zero-noise extrapolation (ZNE) with global unitary folding and
  Richardson / linear extrapolation should produce a shot-normalized
  improvement factor mu > 1 (paper reports mu ranging from ~1 to ~7).

Paper-faithful settings we replicate:
  - Global unitary folding at scale factors {1, 2, 3}   (paper Sec II.B.1)
  - Total shots N = 10_000 (10^4), split N/k_ZNE per scaled circuit
  - Observable A = |z><z|  where z is the ideal-noiseless bitstring (0^n for RB)
  - Depths d in {1, 3, 5, 7, 9}; |C| = 4 random circuit instances per depth
  - Improvement factor from paper Eq. (5), shot-normalized RMSE ratio
  - Baseline noise model: 1% two-qubit depolarizing noise (Sec II.D.5)

Because we do not have access to real IBM/IonQ/Rigetti hardware, we focus on
the simulator baseline. This is the exact setup where the paper says the
largest improvement factors are expected.

Uses: mitiq (ZNE), qiskit + qiskit-aer (RB circuits + noisy simulator).
"""
# NOTE: intentionally NOT using `from __future__ import annotations` because
# mitiq inspects the *runtime* return-type annotation of the executor
# (via inspect.getfullargspec) to dispatch expectation-value handling.
# With PEP 563 postponed annotations, `-> float` becomes the string 'float'
# and mitiq's `_executor_return_type in FloatLike` check fails.
import json, math, os, sys, time, random
from pathlib import Path
from typing import Callable

import numpy as np

# --- Qiskit / Aer imports (Qiskit 2.x) -------------------------------------
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import random_clifford
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error

# --- Mitiq imports ---------------------------------------------------------
from mitiq import zne, Executor
from mitiq.zne.scaling import fold_global
from mitiq.zne.inference import RichardsonFactory, LinearFactory

OUT = Path(__file__).resolve().parent.parent / "report" / "evidence"
OUT.mkdir(parents=True, exist_ok=True)

# ------------------------------------------------------------------
# Paper params
# ------------------------------------------------------------------
N_SHOTS_TOTAL = 10_000   # paper: N = 10^4
K_ZNE = 3                # paper: k_ZNE = 3 (scale factors {1,2,3})
SCALE_FACTORS = [1.0, 2.0, 3.0]
DEPTHS = [1, 3, 5, 7, 9]  # paper: d in {1,3,5,7,9}
N_CIRCUITS = 4           # paper: |C| = 4 random instances per (n,d)
N_QUBITS = 3             # paper does n=3 and n=5 on this simulator; we do n=3 (Fig. 3 focus)
DEPOL_P = 0.01           # 1% depolarizing after each 2-qubit gate
RNG_SEED = 20260704


# ------------------------------------------------------------------
# Circuit builder: RB-style circuit that ideally returns |0..0>.
#
# Following paper Sec II.C.1 / Eq. (11):
#   C = U_inv * U_d * U_{d-1} * ... * U_1
# with U_i random Cliffords and U_inv the classically computed inverse,
# so the ideal noiseless state is |0..0>. Observable is |0><0|^n, i.e. the
# probability of measuring the all-zero bitstring. The paper applies
# 2-qubit RB sequences to each neighbouring qubit pair on a line; for a
# clean, single-observable benchmark on n=3 we use one length-d Clifford
# sequence on all 3 qubits (this gives the same "expectation = 1 in the
# noiseless limit" structure that Eq. (5) requires).
# ------------------------------------------------------------------
def build_rb_circuit(n: int, d: int, rng: np.random.Generator) -> QuantumCircuit:
    layers = []
    prod = None
    for _ in range(d):
        seed = int(rng.integers(0, 2**31 - 1))
        cl = random_clifford(n, seed=seed)
        layers.append(cl)
        prod = cl if prod is None else cl.compose(prod)
    inv = prod.adjoint()

    qc = QuantumCircuit(n)
    for cl in layers:
        qc.compose(cl.to_circuit(), inplace=True)
    qc.compose(inv.to_circuit(), inplace=True)
    return qc


# ------------------------------------------------------------------
# Noisy simulator: 1% two-qubit depolarizing after each two-qubit gate.
# (Matches paper Sec II.D.5 "simple noise model" -- Eq. (10) with p_2Q = 0.01.)
# ------------------------------------------------------------------
def make_noise_model(p_2q: float = DEPOL_P) -> NoiseModel:
    nm = NoiseModel()
    err2 = depolarizing_error(p_2q, num_qubits=2)
    # apply to common 2q gates that random Clifford compilation produces
    nm.add_all_qubit_quantum_error(err2, ["cx", "cz", "swap", "ecr"])
    return nm


# ------------------------------------------------------------------
# Executor: run one circuit on the noisy simulator, return
# probability of measuring all-zero bitstring (= <Â> for this benchmark).
# ------------------------------------------------------------------
def make_executor(shots: int, noise_model: NoiseModel, n_qubits: int) -> Callable:
    sim = AerSimulator(noise_model=noise_model)
    target_bitstr = "0" * n_qubits

    def executor(circuit: QuantumCircuit) -> float:
        # add measurements
        qc = circuit.copy()
        qc.measure_all()
        tqc = transpile(qc, sim, optimization_level=0)
        result = sim.run(tqc, shots=shots).result()
        counts = result.get_counts()
        # qiskit returns bitstrings possibly with a space (classical reg) - normalise
        total = sum(counts.values())
        p0 = 0
        for bs, c in counts.items():
            bs_clean = bs.replace(" ", "")
            # qiskit orders classical bits little-endian; all zeros is invariant
            if bs_clean == target_bitstr:
                p0 += c
        return float(p0 / total)

    return executor


# ------------------------------------------------------------------
# Ideal expectation value: for RB with inverse appended, <A>=1 exactly.
# ------------------------------------------------------------------
def ideal_expectation() -> float:
    return 1.0


# ------------------------------------------------------------------
# Improvement factor (paper Eq. 5), simplified to a single trial t=1
# per circuit (paper: t=1 per (n,d) for main figures). We average over
# |C|=4 circuits at each depth by pooling their squared errors.
#
# mu = sqrt( N_unmit  * sum_C (A0_C - A)^2 ) /
#      sqrt( N_QEM   * sum_C (AQEM_C - A)^2 )
# ------------------------------------------------------------------
def improvement_factor(unmit_vals: list[float],
                       mit_vals:   list[float],
                       ideal: float,
                       n_unmit_shots: int,
                       n_qem_shots: int) -> float:
    err0_sq_sum = sum((a - ideal)**2 for a in unmit_vals)
    errQ_sq_sum = sum((a - ideal)**2 for a in mit_vals)
    if errQ_sq_sum <= 0.0:
        return float("inf")
    num = math.sqrt(n_unmit_shots * err0_sq_sum)
    den = math.sqrt(n_qem_shots   * errQ_sq_sum)
    return num / den


# ------------------------------------------------------------------
# Main experiment.
# ------------------------------------------------------------------
def run():
    rng = np.random.default_rng(RNG_SEED)
    noise = make_noise_model(DEPOL_P)

    # For unmitigated baseline we use all N_SHOTS_TOTAL shots on the depth-d circuit.
    # For ZNE we split N_SHOTS_TOTAL across K_ZNE noise-scaled circuits (paper).
    shots_unmit = N_SHOTS_TOTAL
    shots_per_scale = N_SHOTS_TOTAL // K_ZNE

    exe_unmit = make_executor(shots_unmit, noise, N_QUBITS)
    exe_zne   = make_executor(shots_per_scale, noise, N_QUBITS)

    fac_richardson = RichardsonFactory(scale_factors=SCALE_FACTORS)
    fac_linear     = LinearFactory(scale_factors=SCALE_FACTORS)

    ideal = ideal_expectation()
    results = {
        "config": {
            "n_qubits": N_QUBITS,
            "depths": DEPTHS,
            "n_circuits_per_depth": N_CIRCUITS,
            "shots_total": N_SHOTS_TOTAL,
            "k_zne": K_ZNE,
            "scale_factors": SCALE_FACTORS,
            "shots_unmit": shots_unmit,
            "shots_per_scaled_circuit": shots_per_scale,
            "depolarizing_p_2q": DEPOL_P,
            "seed": RNG_SEED,
            "mitiq_version": __import__("mitiq").__version__,
            "qiskit_version": __import__("qiskit").__version__,
            "qiskit_aer_version": __import__("qiskit_aer").__version__,
        },
        "per_depth": [],
    }

    print(f"# n={N_QUBITS} qubits, depol p={DEPOL_P}, shots={N_SHOTS_TOTAL}, "
          f"scales={SCALE_FACTORS}")
    print(f"{'d':>2} {'ideal':>6} {'A0_mean':>8} {'AZNE_R':>8} {'AZNE_L':>8} "
          f"{'mu_ZNE_R':>9} {'mu_ZNE_L':>9}")

    for d in DEPTHS:
        unmit_vals = []
        zneR_vals  = []
        zneL_vals  = []
        per_circ = []
        for ic in range(N_CIRCUITS):
            circ = build_rb_circuit(N_QUBITS, d, rng)
            # unmitigated
            a0 = exe_unmit(circ)
            # ZNE Richardson (mitiq wraps the raw executor internally)
            aZ_R = zne.execute_with_zne(
                circuit=circ,
                executor=exe_zne,
                factory=RichardsonFactory(scale_factors=SCALE_FACTORS),
                scale_noise=fold_global,
            )
            # ZNE Linear
            aZ_L = zne.execute_with_zne(
                circuit=circ,
                executor=exe_zne,
                factory=LinearFactory(scale_factors=SCALE_FACTORS),
                scale_noise=fold_global,
            )
            unmit_vals.append(a0)
            zneR_vals.append(aZ_R)
            zneL_vals.append(aZ_L)
            per_circ.append({"circuit": ic, "A0": a0, "AZNE_R": aZ_R, "AZNE_L": aZ_L})

        mu_R = improvement_factor(unmit_vals, zneR_vals, ideal,
                                  shots_unmit, K_ZNE * shots_per_scale)
        mu_L = improvement_factor(unmit_vals, zneL_vals, ideal,
                                  shots_unmit, K_ZNE * shots_per_scale)

        print(f"{d:>2} {ideal:>6.3f} {np.mean(unmit_vals):>8.4f} "
              f"{np.mean(zneR_vals):>8.4f} {np.mean(zneL_vals):>8.4f} "
              f"{mu_R:>9.3f} {mu_L:>9.3f}")

        results["per_depth"].append({
            "d": d,
            "ideal": ideal,
            "A0_mean": float(np.mean(unmit_vals)),
            "A0_std":  float(np.std(unmit_vals)),
            "AZNE_R_mean": float(np.mean(zneR_vals)),
            "AZNE_L_mean": float(np.mean(zneL_vals)),
            "mu_ZNE_R": mu_R,
            "mu_ZNE_L": mu_L,
            "per_circuit": per_circ,
        })

    # aggregate improvement factors across depths (arithmetic mean)
    mu_R_vals = [r["mu_ZNE_R"] for r in results["per_depth"]]
    mu_L_vals = [r["mu_ZNE_L"] for r in results["per_depth"]]
    results["aggregate"] = {
        "mu_ZNE_R_mean": float(np.mean(mu_R_vals)),
        "mu_ZNE_R_min":  float(np.min(mu_R_vals)),
        "mu_ZNE_R_max":  float(np.max(mu_R_vals)),
        "mu_ZNE_L_mean": float(np.mean(mu_L_vals)),
        "mu_ZNE_L_min":  float(np.min(mu_L_vals)),
        "mu_ZNE_L_max":  float(np.max(mu_L_vals)),
        "fraction_mu_R_above_1": float(np.mean([m > 1.0 for m in mu_R_vals])),
        "fraction_mu_L_above_1": float(np.mean([m > 1.0 for m in mu_L_vals])),
    }

    out = OUT / "zne_results.json"
    with open(out, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nWrote {out}")
    print(f"Aggregate mu_ZNE_R: mean={results['aggregate']['mu_ZNE_R_mean']:.3f} "
          f"(range {results['aggregate']['mu_ZNE_R_min']:.3f}..{results['aggregate']['mu_ZNE_R_max']:.3f})")
    print(f"Aggregate mu_ZNE_L: mean={results['aggregate']['mu_ZNE_L_mean']:.3f} "
          f"(range {results['aggregate']['mu_ZNE_L_min']:.3f}..{results['aggregate']['mu_ZNE_L_max']:.3f})")


if __name__ == "__main__":
    t0 = time.time()
    run()
    print(f"\nWall time: {time.time()-t0:.1f}s")
