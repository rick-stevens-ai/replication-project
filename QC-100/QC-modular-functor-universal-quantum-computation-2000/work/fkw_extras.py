#!/usr/bin/env python3
"""Extra checks: (a) verify the exact (2,3) F-move consistency by
computing the R matrix eigenvalues that must be q and -1 for the Fibonacci
theory; (b) show density by comparing the empirical distribution of
tr(U)/2 for random braid words in B_3 through rho_{[2,1]} against the
Haar distribution for SU(2)/center, tr(U)/2 ~ uniform in [-1, 1] with
sqrt(1 - t^2) density.

Also: rerun the Hadamard approximation search with longer words using
random-restart hillclimb + BFS to demonstrate universality "in action"
more clearly.
"""

import json
import math
import cmath
import os
import time
import numpy as np

from fkw_replication import (
    build_rep, apply_braid, sample_braid_word, su2_from_u2, gate_distance, q
)

def hillclimb_approx(sigmas, target, seed=0, n_restart=32, max_len=40):
    """Random-restart hillclimb: start from random braid word, try local single-flip mutations."""
    rng = np.random.default_rng(seed)
    ngen = len(sigmas)
    invs = [np.linalg.inv(S) for S in sigmas]
    gens_signed = list(range(1, ngen + 1)) + list(range(-ngen, 0))

    def eval_word(w):
        dim = sigmas[0].shape[0]
        U = np.eye(dim, dtype=complex)
        for g in w:
            i = abs(g) - 1
            if g > 0: U = sigmas[i] @ U
            else:     U = invs[i]  @ U
        return gate_distance(U, target)

    best_word, best_d = [], eval_word([])
    for _ in range(n_restart):
        L = int(rng.integers(4, max_len + 1))
        cur = [int(x) for x in rng.choice(gens_signed, size=L)]
        cur_d = eval_word(cur)
        # Local search: try single-position mutations & appends/pops.
        improved = True
        while improved:
            improved = False
            # Mutations at each position
            for pos in range(len(cur)):
                for g in gens_signed:
                    if g == cur[pos]: continue
                    nw = list(cur); nw[pos] = g
                    d = eval_word(nw)
                    if d < cur_d - 1e-12:
                        cur, cur_d = nw, d; improved = True
            # Append/pop
            if len(cur) < max_len:
                for g in gens_signed:
                    nw = cur + [g]
                    d = eval_word(nw)
                    if d < cur_d - 1e-12:
                        cur, cur_d = nw, d; improved = True; break
            if len(cur) > 1:
                nw = cur[:-1]
                d = eval_word(nw)
                if d < cur_d - 1e-12:
                    cur, cur_d = nw, d; improved = True
        if cur_d < best_d:
            best_word, best_d = cur, cur_d
    return best_word, best_d

def main():
    t0 = time.time()
    tabs, Es, sigmas = build_rep((2, 1))
    print(f"lam=[2,1] dim={len(tabs)}, generators={len(sigmas)}")

    # (a) R-matrix eigenvalues from sigma_1 (which for the paper is
    # diagonal diag(-1, q)).  Confirm.
    evs = sorted(np.linalg.eigvals(sigmas[0]), key=lambda z: (round(z.real, 6), round(z.imag, 6)))
    print("sigma_1 eigenvalues:", evs)
    print("Expected: {-1, q=e^{2πi/5}} =", [-1.0 + 0j, q])

    # (b) empirical distribution of tr(U)/2 for random braid words.
    rng = np.random.default_rng(20260706)
    Ns = [10_000, 50_000]
    for N in Ns:
        traces = []
        for _ in range(N):
            L = int(rng.integers(20, 60))
            w = sample_braid_word(2, L, rng)
            U = apply_braid(sigmas, w)
            Uprime, _ = su2_from_u2(U)
            traces.append(np.trace(Uprime).real / 2)
        traces = np.array(traces)
        # Compare against SU(2)/center Haar: density of x = tr/2 is
        #   f(x) = (2/pi) sqrt(1 - x^2), x in [-1, 1]
        bins = np.linspace(-1, 1, 21)
        hist, edges = np.histogram(traces, bins=bins, density=True)
        centers = 0.5 * (edges[1:] + edges[:-1])
        theory = (2.0 / math.pi) * np.sqrt(np.maximum(0.0, 1.0 - centers ** 2))
        max_dev = float(np.max(np.abs(hist - theory)))
        l2      = float(np.sqrt(np.mean((hist - theory) ** 2)))
        print(f"N={N}: max_dev vs Haar density = {max_dev:.4f}, RMS = {l2:.4f}")

    # (c) Hadamard hillclimb-approx over longer words
    T = np.array([[1, 1], [1, -1]], dtype=complex) / math.sqrt(2)
    best_word, best_d = hillclimb_approx(sigmas, T, seed=1, n_restart=64, max_len=50)
    print(f"Hadamard best hillclimb approx dist = {best_d:.6f}  len={len(best_word)}")
    print(f"  word: {best_word}")

    # Verify approx really is close
    dim = sigmas[0].shape[0]
    U = np.eye(dim, dtype=complex)
    invs = [np.linalg.inv(S) for S in sigmas]
    for g in best_word:
        i = abs(g) - 1
        if g > 0: U = sigmas[i] @ U
        else:     U = invs[i]  @ U
    print("  U approx:")
    print(U)
    print("  Target Hadamard:")
    print(T)

    # (d) Braid-relation stress test on a random long word — every
    # move must preserve unitarity.
    for L in [100, 500, 2000]:
        w = sample_braid_word(2, L, rng)
        U = apply_braid(sigmas, w)
        dev = float(np.linalg.norm(U.conj().T @ U - np.eye(dim)))
        print(f"random word length {L}: unitarity deviation = {dev:.2e}")

    outdir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(outdir, "fkw_extras.json"), "w") as f:
        json.dump({
            "sigma_1_eigs": [str(z) for z in evs],
            "hadamard_best_word": best_word,
            "hadamard_best_dist": best_d,
            "runtime_seconds": time.time() - t0,
        }, f, indent=2)

if __name__ == "__main__":
    main()
