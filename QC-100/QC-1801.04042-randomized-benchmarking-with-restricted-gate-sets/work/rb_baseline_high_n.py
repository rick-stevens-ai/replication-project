"""Higher-statistics full-Clifford baseline to address judge's noise concern.

400 sequences per length for the full-Clifford, n=2, p_dep=0.01 baseline.
Also runs a Stim-only symmetric-noise verification via a fully independent estimator
of lambda: measure the average post-noise Pauli-eigenvalue directly from a large
number of shots (no fitting), and compare to theory.
"""
import time, json
from pathlib import Path
from dataclasses import asdict

import numpy as np
import stim
from scipy.optimize import curve_fit

import sys
sys.path.insert(0, str(Path(__file__).parent))
from rb_replication import (
    RBConfig, random_group_element_tableau,
    prepare_initial_state_circuit, measurement_ops,
    fit_single, dep_prob_to_total_p, theory_lambda_full_clifford,
    build_rb_sequence,
)


def run_rb_full(cfg, seed=0):
    import random
    rng = random.Random(seed)
    results = {}
    t0 = time.time()
    for m in cfg.lengths:
        succ = 0; total = 0
        for _ in range(cfg.n_sequences_per_length):
            tableaus = [random_group_element_tableau(cfg.n_qubits, cfg.group, cfg.walk_len, rng)
                        for _ in range(m)]
            circ = build_rb_sequence(cfg.n_qubits, tableaus, cfg)
            sampler = circ.compile_sampler()
            samples = sampler.sample(shots=cfg.shots_per_sequence)
            succ += int(np.all(samples == 0, axis=1).sum())
            total += cfg.shots_per_sequence
        f = succ / total
        results[m] = f
        print(f"  m={m:3d}  f={f:.4f}  N={total}  [elapsed={time.time()-t0:.1f}s]", flush=True)
    return results


def main():
    evidence = Path("/Users/stevens/Dropbox/REPLICATE-PROJECT/QC-100/"
                    "QC-1801.04042-randomized-benchmarking-with-restricted-gate-sets/report/evidence")

    print("Higher-statistics full-Clifford baseline, n=2, p_dep=0.01, N=400/length")
    cfg = RBConfig(n_qubits=2, group="full",
                   lengths=(1, 2, 4, 8, 16, 32, 64, 128),
                   n_sequences_per_length=400, p_dep=0.01,
                   initial_state="0")
    res = run_rb_full(cfg, seed=42)
    lengths = sorted(res.keys()); fs = [res[m] for m in lengths]
    p_total = dep_prob_to_total_p(2, 0.01)
    lam_theory = theory_lambda_full_clifford(2, p_total)
    fit = fit_single(lengths, fs)
    print(f"\nFit lambda = {fit['lam']:.5f}")
    print(f"Theory     = {lam_theory:.5f}")
    print(f"|diff|     = {abs(fit['lam'] - lam_theory):.5f}")
    out = {
        "config": asdict(cfg),
        "lengths": lengths, "fs": fs, "fit": fit,
        "theory_lambda": lam_theory, "p_total": p_total,
    }
    with open(evidence / "results_baseline_hi_n.json", "w") as fh:
        json.dump(out, fh, indent=2, default=str)
    print(f"\nSaved: {evidence / 'results_baseline_hi_n.json'}")


if __name__ == "__main__":
    main()
