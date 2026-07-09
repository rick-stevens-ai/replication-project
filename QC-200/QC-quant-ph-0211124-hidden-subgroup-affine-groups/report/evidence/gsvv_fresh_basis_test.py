#!/usr/bin/env python3
"""
GSVV-STYLE PURE TEST: fresh Haar-random basis per trial, decoder is unaware of U.

This matches the theoretical model in Grigni-Schulman-Vazirani-Vazirani (cited by
Moore-Rockmore-Russell-Schulman): if the measurement basis is drawn independently
and randomly for each trial, then the outcome distribution -- integrated over the
basis -- becomes independent of the hidden subgroup label b.

Concretely:
  For each trial:
    - Fresh Haar-random unitary U ~ CUE(d) is drawn.
    - We measure column k, then apply U on the row wire, measure ell in {0..d-1}.
    - Decoder sees ONLY (k, ell) -- NOT U.
    - Best decoder is uniform guessing at 1/p.

We validate this by computing the total-variation distance between the induced
distribution P(k, ell | b) (over trials) for different b, and by testing
best-decoder accuracy.
"""

import json
import os
import sys
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from replicate_affine_hsp import (
    build_affine_group, hidden_subgroup_Hb, coset_state,
    fourier_component_rho, measure_random_basis, measure_paper_basis,
    decode_b_from_ell,
)
from qiskit.quantum_info import random_unitary


def collect_dist(p, n_trials_per_b, seed, basis_mode):
    """Collect empirical distribution P(k, ell | b), aggregating over fresh U's."""
    rng = np.random.default_rng(seed)
    elems, idx = build_affine_group(p)
    d = p - 1
    dist = np.zeros((p, d, d))  # b, k_idx, ell
    for b in range(p):
        H = hidden_subgroup_Hb(p, b)
        amps = coset_state(p, elems, idx, subgroup=H)
        Fhat = fourier_component_rho(amps, elems, p)
        for _ in range(n_trials_per_b):
            if basis_mode == "paper":
                kk, ell = measure_paper_basis(Fhat, p, rng)
            elif basis_mode == "fresh_random":
                # DRAW A FRESH U EACH TRIAL -- decoder never sees U
                U = np.array(random_unitary(d).data)
                kk, ell = measure_random_basis(Fhat, p, rng, U=U)
            else:
                raise ValueError(basis_mode)
            dist[b, kk - 1, ell] += 1
    dist = dist / dist.sum(axis=(1, 2), keepdims=True)
    return dist


def total_variation_matrix(dist):
    """Return pairwise TV distance matrix TV(b, b') = 0.5 sum |P(k,l|b) - P(k,l|b')|."""
    p = dist.shape[0]
    tv = np.zeros((p, p))
    for a in range(p):
        for b in range(p):
            tv[a, b] = 0.5 * np.abs(dist[a] - dist[b]).sum()
    return tv


def best_accuracy_given_map(dist_pilot, dist_scored, p, n_trials_per_b, seed, basis_mode):
    """Use dist_pilot as MAP decoder on independent sampled trials, aggregate accuracy."""
    rng = np.random.default_rng(seed)
    elems, idx = build_affine_group(p)
    d = p - 1
    correct = 0
    total = 0
    for b in range(p):
        H = hidden_subgroup_Hb(p, b)
        amps = coset_state(p, elems, idx, subgroup=H)
        Fhat = fourier_component_rho(amps, elems, p)
        for _ in range(n_trials_per_b):
            if basis_mode == "paper":
                kk, ell = measure_paper_basis(Fhat, p, rng)
            else:
                U = np.array(random_unitary(d).data)
                kk, ell = measure_random_basis(Fhat, p, rng, U=U)
            lik = dist_pilot[:, kk - 1, ell]
            b_hat = int(np.argmax(lik))
            if b_hat == b:
                correct += 1
            total += 1
    return correct / total


def main():
    results = {}
    for p in [5, 7]:
        print(f"\n=== p={p} : FRESH-U-per-trial random basis vs paper's basis ===")
        # collect fresh-U dist
        pilot_fresh = collect_dist(p, n_trials_per_b=4000, seed=42, basis_mode="fresh_random")
        pilot_paper = collect_dist(p, n_trials_per_b=4000, seed=43, basis_mode="paper")
        tv_fresh = total_variation_matrix(pilot_fresh)
        tv_paper = total_variation_matrix(pilot_paper)
        # mean off-diagonal TV
        off = np.array([tv_fresh[i, j] for i in range(p) for j in range(p) if i != j])
        off_paper = np.array([tv_paper[i, j] for i in range(p) for j in range(p) if i != j])
        print(f"  fresh-random-basis mean off-diagonal TV(b,b') = {off.mean():.4f}")
        print(f"  paper's-basis      mean off-diagonal TV(b,b') = {off_paper.mean():.4f}")
        print(f"  paper's Section-3 theoretical bound: TV >= 1/4 asymptotically")

        # accuracy under MAP decoders trained on same-mode pilot
        acc_fresh = best_accuracy_given_map(
            pilot_fresh, None, p, n_trials_per_b=1500, seed=100, basis_mode="fresh_random"
        )
        acc_paper = best_accuracy_given_map(
            pilot_paper, None, p, n_trials_per_b=1500, seed=101, basis_mode="paper"
        )
        print(f"  fresh-random-basis MAP-decoder accuracy = {acc_fresh:.4f}   "
              f"(uniform baseline = {1/p:.4f})")
        print(f"  paper's-basis      MAP-decoder accuracy = {acc_paper:.4f}")
        results[f"p={p}"] = {
            "fresh_random_mean_off_diag_TV": float(off.mean()),
            "paper_basis_mean_off_diag_TV": float(off_paper.mean()),
            "fresh_random_MAP_accuracy": float(acc_fresh),
            "paper_basis_MAP_accuracy": float(acc_paper),
            "uniform_baseline": 1.0 / p,
            "paper_theoretical_TV_bound_q_hedral": 0.25,
        }

    out_path = os.path.join(os.path.dirname(__file__), "gsvv_fresh_basis_test.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n[wrote] {out_path}")


if __name__ == "__main__":
    main()
