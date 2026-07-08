"""
Asymmetric-noise stress test for the CNOT+Pauli subgroup RB (Brown & Eastin 2018).

Motivation: when we inject symmetric per-qubit depolarizing noise, every non-identity
Pauli error is equally likely, so each block's per-Pauli mass is identical and all
block eigenvalues degenerate to a single lambda. This is consistent with the paper
but does not exercise the multi-exponential structure. To confirm the paper's
per-block formulas we inject *dephasing-heavy* noise -- pure Z error on each qubit.

Under pure Z noise on 2 qubits:
  Pauli support: {I, Z_1, Z_2, Z_1 Z_2}. All non-identity Paulis are in block B1
  (Z-only). Blocks B2, B3, B4 have zero mass.

  So p1 = p (all error weight), p2 = p3 = p4 = 0.

  For |00> init (measures lambda1):
    lambda1 = 1 - (p2 + p3 + p4) * 2^n / (2^n - 1) = 1 (NO decay from |00>)
  For |++> init (measures lambda2):
    lambda2 = 1 - (p1 + p3 + p4) * 2^n / (2^n - 1) = 1 - p1 * 4/3

Prediction: |00> RB shows flat/near-flat fidelity (only measurement error decays),
            |++> RB shows single-exponential decay with lambda2 = 1 - p*(4/3).

This exercises the block structure and tests the paper's asymmetric-noise formula.
"""

import time
import json
from pathlib import Path
from dataclasses import asdict

import numpy as np
import stim
from scipy.optimize import curve_fit

import sys
sys.path.insert(0, str(Path(__file__).parent))
from rb_replication import (
    RBConfig, random_group_element_tableau,
    prepare_initial_state_circuit, measurement_ops, fit_single,
    dep_prob_to_total_p, theory_lambda_cnot_pauli_symmetric,
)


def build_rb_sequence_zerror(n, tableaus, cfg, p_z):
    """Build RB sequence with per-qubit Z_ERROR(p_z) noise instead of depolarizing."""
    circ = prepare_initial_state_circuit(n, cfg.initial_state)
    product = stim.Tableau(n)
    for T in tableaus:
        subc = T.to_circuit(method="elimination")
        circ += subc
        for q in range(n):
            circ.append("Z_ERROR", [q], p_z)
        product = product.then(T)
    inv = product.inverse()
    circ += inv.to_circuit(method="elimination")
    for q in range(n):
        circ.append("Z_ERROR", [q], p_z)
    circ += measurement_ops(n, cfg.initial_state)
    return circ


def run_rb_zerror(cfg, p_z, seed=0, verbose=True):
    import random
    rng = random.Random(seed)
    results = {}
    t0 = time.time()
    for m in cfg.lengths:
        succ = 0; total = 0
        for _ in range(cfg.n_sequences_per_length):
            tableaus = [random_group_element_tableau(cfg.n_qubits, cfg.group, cfg.walk_len, rng)
                        for _ in range(m)]
            circ = build_rb_sequence_zerror(cfg.n_qubits, tableaus, cfg, p_z)
            sampler = circ.compile_sampler()
            samples = sampler.sample(shots=cfg.shots_per_sequence)
            succ += int(np.all(samples == 0, axis=1).sum())
            total += cfg.shots_per_sequence
        f = succ / total
        results[m] = f
        if verbose:
            print(f"  m={m:3d}  f={f:.4f}  [elapsed={time.time()-t0:.1f}s]", flush=True)
    return results


def dep_z_to_total_p(n, p_z):
    """For Z_ERROR(p_z) on n qubits independently, total P(non-identity) = 1 - (1-p_z)^n."""
    return 1 - (1 - p_z) ** n


def main():
    outdir = Path("/Users/stevens/Dropbox/REPLICATE-PROJECT/QC-100/"
                  "QC-1801.04042-randomized-benchmarking-with-restricted-gate-sets/report/evidence")
    outdir.mkdir(parents=True, exist_ok=True)

    n = 2
    p_z = 0.02   # per-qubit Z-error probability per group element
    p_total = dep_z_to_total_p(n, p_z)

    # Under pure Z noise, only p1 (Z-block) is nonzero.
    # p1 = p_total, p2 = p3 = p4 = 0.
    # From paper eigenvalue formulas (CNOT+Pauli, block eigenvalues):
    #   lambda1 = 1 - 0 (no decay from |00>)
    #   lambda2 = 1 - p1 * 2^n/(2^n - 1)  = 1 - p_total * 4/3
    lam1_theory = 1.0
    lam2_theory = 1 - p_total * (2 ** n) / (2 ** n - 1)
    print(f"n={n}  p_z={p_z}  p_total={p_total:.5f}")
    print(f"Theory (pure Z noise): lambda1={lam1_theory:.5f}  lambda2={lam2_theory:.5f}")

    all_results = {}

    # (A) |00> - should be ~flat (no decay)
    print("\n--- CNOT+Pauli, |00>, pure Z noise ---")
    cfg = RBConfig(n_qubits=n, group="cnot_pauli",
                   lengths=(1, 2, 4, 8, 16, 32, 64, 128),
                   n_sequences_per_length=60, p_dep=0.0,
                   initial_state="0", walk_len=60)
    res_00 = run_rb_zerror(cfg, p_z=p_z, seed=101)
    lengths = sorted(res_00.keys()); fs = [res_00[m] for m in lengths]
    fit_00 = fit_single(lengths, fs)
    print(f"Fit lambda (|00>) = {fit_00['lam']:.4f}  (theory {lam1_theory:.4f})")
    all_results["zerror_00"] = dict(config=asdict(cfg), lengths=lengths, fs=fs,
                                     fit=fit_00, lam_theory=lam1_theory, p_total=p_total)

    # (B) |++> - single exp with lambda2
    print("\n--- CNOT+Pauli, |++>, pure Z noise ---")
    cfg = RBConfig(n_qubits=n, group="cnot_pauli",
                   lengths=(1, 2, 4, 8, 16, 32, 64, 128),
                   n_sequences_per_length=60, p_dep=0.0,
                   initial_state="+", walk_len=60)
    res_pp = run_rb_zerror(cfg, p_z=p_z, seed=102)
    lengths = sorted(res_pp.keys()); fs = [res_pp[m] for m in lengths]
    fit_pp = fit_single(lengths, fs)
    print(f"Fit lambda (|++>) = {fit_pp['lam']:.4f}  (theory {lam2_theory:.4f})")
    all_results["zerror_pp"] = dict(config=asdict(cfg), lengths=lengths, fs=fs,
                                     fit=fit_pp, lam_theory=lam2_theory, p_total=p_total)

    outfile = outdir / "results_asym.json"
    with open(outfile, "w") as fh:
        json.dump(all_results, fh, indent=2, default=str)
    print(f"\nSaved: {outfile}")

    print("\n" + "=" * 70)
    print("ASYMMETRIC (pure-Z) SUMMARY")
    print("=" * 70)
    print(f"{'Init state':10s} {'lambda_fit':>12s} {'lambda_theory':>14s} {'|diff|':>10s}")
    print(f"{'|00>':10s} {fit_00['lam']:12.4f} {lam1_theory:14.4f} {abs(fit_00['lam']-lam1_theory):10.4f}")
    print(f"{'|++>':10s} {fit_pp['lam']:12.4f} {lam2_theory:14.4f} {abs(fit_pp['lam']-lam2_theory):10.4f}")


if __name__ == "__main__":
    main()
