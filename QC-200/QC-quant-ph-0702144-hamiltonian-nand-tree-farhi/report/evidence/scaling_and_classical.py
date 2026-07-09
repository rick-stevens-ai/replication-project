#!/usr/bin/env python3
"""
Follow-on analysis for the Farhi-Goldstone-Gutmann NAND-tree replication.

(A) Runtime scaling: for n = 2,3 measure how large L needs to be to hit
    100% accuracy over all 2^N inputs. Compare to the paper's asymptotic
    L ~ sqrt(N) leading-order claim vs the finite-N requirement that
    L >> 16 sqrt(N) (from the plateau width in Sec. 1).

(B) Classical randomized-algorithm baseline: implement the standard Snir /
    Saks-Wigderson randomized alpha-beta NAND-tree evaluator and measure the
    expected number of leaf queries on random inputs, comparing to the
    N^0.753 asymptotic (Saks-Wigderson lower bound / Snir upper bound).
"""
from __future__ import annotations

import itertools
import json
import random
import time
from pathlib import Path

import numpy as np

# Reuse the quantum walk primitives
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from nand_tree_qwalk import (
    build_graph, hamiltonian, initial_state, right_runway_indices,
    evolve_and_measure, sweep, decision_check, nand_tree_value,
)


# ---------------------------------------------------------------------------
# (A) Quantum runtime scaling: how big must L be for full 100% accuracy?
# ---------------------------------------------------------------------------
def find_min_L_for_full_accuracy(n, L_candidates, verbose=True):
    trace = []
    best = dict(L=None, gap=None, accuracy=None, trace=trace)
    for L in L_candidates:
        rows = sweep(n, L)
        dec = decision_check(rows)
        trace.append(dict(L=L, accuracy=dec["accuracy"], gap=dec["gap"]))
        if verbose:
            print(f"  n={n} L={L} acc={dec['accuracy']*100:.1f}% gap={dec['gap']}", flush=True)
        if dec["accuracy"] == 1.0 and (dec["gap"] is None or dec["gap"] > 0) and best["L"] is None:
            best = dict(L=L, gap=dec["gap"], accuracy=dec["accuracy"], trace=trace)
            # Keep scanning a couple more L to record how the gap grows
            # but return early to save time if we've had 2 successes
            return best
    return best


# ---------------------------------------------------------------------------
# (B) Classical randomized NAND-tree evaluator (Snir 1985 / Saks-Wigderson 1986).
#
# Recursive rule:
#   - At an AND-of-NANDs internal node with children c1, c2:
#       shuffle order; query c1 first; if c1=0 => return 1 (NAND short-circuits).
#       else query c2; return NAND(c1, c2).
#   - At a leaf: return the input bit (counts as 1 query).
#
# For balanced binary NAND tree of depth n, expected queries is Theta(N^alpha)
# with alpha = log2((1+sqrt(33))/4) ~ 0.7538 (Saks-Wigderson).
# ---------------------------------------------------------------------------
def randomized_nand_eval(bits, n, rng):
    """Return (value, query_count)."""
    count = [0]
    def recurse(depth, offset, span):
        if depth == n:
            count[0] += 1
            return bits[offset]
        half = span // 2
        # Randomize which subtree we visit first
        order = [(offset, half), (offset + half, half)]
        rng.shuffle(order)
        (o1, s1), (o2, s2) = order
        v1 = recurse(depth + 1, o1, s1)
        if v1 == 0:
            # NAND(0, *) = 1 -- short-circuit, no need to query the sibling
            return 1
        v2 = recurse(depth + 1, o2, s2)
        return 1 - (v1 & v2)
    val = recurse(0, 0, 2 ** n)
    return val, count[0]


def classical_scaling(n, trials_per_input=200, max_exhaustive_n=3):
    """For small n (2^N = 2^{2^n} inputs tractable), average over ALL 2^N inputs.
    For larger n, average over `n_samples` uniformly-drawn random inputs."""
    rng = random.Random(0xC0FFEE ^ n)
    N = 2 ** n
    total_q = 0
    total_calls = 0
    correct = 0
    if n <= max_exhaustive_n:
        all_inputs = list(itertools.product([0, 1], repeat=N))
        for bits in all_inputs:
            truth = nand_tree_value(bits)
            for _ in range(trials_per_input):
                v, q = randomized_nand_eval(bits, n, rng)
                total_q += q
                total_calls += 1
                if v == truth:
                    correct += 1
    else:
        # Sample uniformly random inputs
        n_samples = min(2000, 2 ** N)  # cap so this stays fast
        for _ in range(n_samples):
            bits = tuple(rng.randint(0, 1) for _ in range(N))
            truth = nand_tree_value(bits)
            for _ in range(trials_per_input):
                v, q = randomized_nand_eval(bits, n, rng)
                total_q += q
                total_calls += 1
                if v == truth:
                    correct += 1
    return dict(
        n=n, N=N,
        trials=total_calls,
        avg_queries=total_q / total_calls,
        accuracy=correct / total_calls,
        asymptotic_N_alpha=N ** 0.7538,
    )


def main():
    outdir = Path(__file__).resolve().parent
    out = {}

    # (A) Scaling of the required L
    scaling = {}
    # Coarser scan to keep this fast; we already know L~sqrt(N) is the target regime
    for n in [2, 3]:
        if n == 2:
            cand = [2, 4, 6, 8, 12, 16, 24, 32]
        else:
            cand = [4, 8, 12, 16, 20, 24, 28, 32, 40, 48, 64]
        r = find_min_L_for_full_accuracy(n, cand)
        r["N"] = 2 ** n
        r["sqrt_N"] = float(np.sqrt(2 ** n))
        r["16_sqrt_N"] = 16.0 * float(np.sqrt(2 ** n))
        scaling[f"n={n}"] = r
        print(f"[quantum scaling] n={n} N={2**n}: min L for 100% acc = {r['L']} "
              f"(sqrt(N)={r['sqrt_N']:.2f}, 16*sqrt(N)={r['16_sqrt_N']:.2f}, gap={r['gap']})")
    out["quantum_scaling"] = scaling

    # (B) Classical randomized baseline
    classical = {}
    for n in [2, 3, 4, 5, 6, 7]:
        r = classical_scaling(n, trials_per_input=(200 if n <= 4 else 50))
        classical[f"n={n}"] = r
        print(f"[classical] n={n} N={r['N']}: avg queries = {r['avg_queries']:.2f} "
              f"(N^0.7538 = {r['asymptotic_N_alpha']:.2f}, N = {r['N']}), "
              f"correctness = {r['accuracy']*100:.1f}%")
    out["classical_scaling"] = classical

    # (C) Head-to-head at N=8: quantum T(=L/2) vs classical average queries
    #     -- both should be O(sqrt(N)) vs O(N^0.753)? No: the classical bound
    #     is a LOWER bound of N^0.753, but the *randomized upper bound* is
    #     also N^0.753 (Snir tight). Quantum here uses O(sqrt(N)) TIME in the
    #     Hamiltonian-oracle model, not queries -- so this is a model-vs-model
    #     comparison, not a like-with-like query comparison. We record both.
    out["notes"] = (
        "Paper's quantum result is in the Hamiltonian-oracle model: run time "
        "proportional to sqrt(N) (T = L/2, L = Theta(sqrt(N)) asymptotically, "
        "but L >> 16*sqrt(N) is needed at the small-N regime we simulate). "
        "The classical N^0.7538 is the RANDOMIZED QUERY complexity in the "
        "standard model; the two are not directly comparable numerically -- "
        "the paper proves the sqrt(N) speedup in a fair Hamiltonian-oracle "
        "sense in its lower-bound section."
    )

    with open(outdir / "scaling_and_classical_results.json", "w") as f:
        json.dump(out, f, indent=2)
    print(f"Wrote {outdir/'scaling_and_classical_results.json'}")


if __name__ == "__main__":
    main()
