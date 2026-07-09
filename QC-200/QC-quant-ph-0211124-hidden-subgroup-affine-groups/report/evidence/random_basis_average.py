#!/usr/bin/env python3
"""
GSVV-style stronger test: AVERAGE over Haar-random unitaries U.

Paper's contrast (Grigni-Schulman-Vazirani-Vazirani, cited): 'even the strong
standard method, in which rows and columns are measured, cannot solve [HSP]
unless there exist bases for the representations of Sn with very special
computational properties. ... Under the assumption that a random basis is
used for each representation, trivial and nontrivial subgroups are still
information-theoretically indistinguishable.'

The right way to test this is to AVERAGE the random-basis decoder's accuracy
over many independent draws of U. Under a Haar-random U (a fresh draw each
trial), the resulting outcome distribution is INDEPENDENT of b (mixing).
The best any decoder can do is uniform guessing at 1/p.

We test this here for p=5 and p=7.
"""

import json
import os
import sys
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from replicate_affine_hsp import (
    build_affine_group, hidden_subgroup_Hb, coset_state,
    fourier_component_rho, measure_random_basis, decode_b_from_ell,
)
from qiskit.quantum_info import random_unitary


def test_avg_random_basis(p, n_U=50, n_trials_per_b_per_U=200, seed=42):
    """For each draw of a Haar-random U:
       - build a MAP decoder from a pilot on that U,
       - score on independent trials from the same U,
       - average across U's.
    We use a light/agnostic decoder: guess b_hat = argmax over b of
    (empirical likelihood P(k,ell | b, U)) using a shared pilot.
    """
    rng = np.random.default_rng(seed)
    elems, idx = build_affine_group(p)
    d = p - 1

    # Also test the OMNISCIENT-per-U MAP baseline
    accs = []
    for u_idx in range(n_U):
        U = np.array(random_unitary(d, seed=seed + 10000 + u_idx).data)
        # pilot table
        pilot = np.zeros((p, d, d))
        for b in range(p):
            H = hidden_subgroup_Hb(p, b)
            amps = coset_state(p, elems, idx, subgroup=H)
            Fhat = fourier_component_rho(amps, elems, p)
            for _ in range(n_trials_per_b_per_U):
                kk, ell = measure_random_basis(Fhat, p, rng, U=U)
                pilot[b, kk - 1, ell] += 1
        # normalize per (b) -> joint P(k,ell | b, U)
        row_sums = pilot.sum(axis=(1, 2), keepdims=True)
        Pjoint = pilot / np.maximum(row_sums, 1)

        # score
        correct = 0
        total = 0
        for b in range(p):
            H = hidden_subgroup_Hb(p, b)
            amps = coset_state(p, elems, idx, subgroup=H)
            Fhat = fourier_component_rho(amps, elems, p)
            for _ in range(n_trials_per_b_per_U):
                kk, ell = measure_random_basis(Fhat, p, rng, U=U)
                # MAP decode
                lik = Pjoint[:, kk - 1, ell]
                b_hat = int(np.argmax(lik))
                if b_hat == b:
                    correct += 1
                total += 1
        acc = correct / total
        accs.append(acc)
    return {
        "p": p,
        "n_U": n_U,
        "n_trials_per_b_per_U": n_trials_per_b_per_U,
        "mean_accuracy": float(np.mean(accs)),
        "std_accuracy": float(np.std(accs)),
        "min_accuracy": float(np.min(accs)),
        "max_accuracy": float(np.max(accs)),
        "uniform_baseline": 1.0 / p,
        "per_U_accuracy": accs,
    }


def main():
    out = {}
    for p in [5, 7]:
        print(f"\n=== p={p} : averaging over random unitaries ===")
        r = test_avg_random_basis(p=p, n_U=30, n_trials_per_b_per_U=150, seed=42)
        print(f"  mean = {r['mean_accuracy']:.4f}   "
              f"std = {r['std_accuracy']:.4f}   "
              f"[min={r['min_accuracy']:.4f}, max={r['max_accuracy']:.4f}]   "
              f"uniform-baseline={r['uniform_baseline']:.4f}")
        out[f"p={p}"] = r
    out_path = os.path.join(os.path.dirname(__file__), "random_basis_average.json")
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\n[wrote] {out_path}")


if __name__ == "__main__":
    main()
