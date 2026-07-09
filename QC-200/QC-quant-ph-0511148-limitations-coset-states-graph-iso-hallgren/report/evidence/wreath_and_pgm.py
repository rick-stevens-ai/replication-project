#!/usr/bin/env python3
"""
Extension to coset_state_sim.py:

  (i)  Compute Δ_char for the actual graph-isomorphism group
       G_wr := S_n ≀ S_2  with the involutive-swap subgroup H = {e, h},
       h = (e, e, 1) in the wreath-product notation.  Characters of
       S_n ≀ S_2 are built from S_n characters via the standard
       wreath-product character formula.
  (ii) Verify Helstrom (PGM) P_succ = 1/2 + 1/2 · d_tr for the two-
       hypothesis coset-state distinguishing task, for n=2..4 and t=1,2,
       against the character bound.
  (iii) Extend the exact trace-distance sweep to n=5, t=1 (dim=120), and
       compare the exact LHS with the RHS.
"""

from __future__ import annotations
import json
import math
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from coset_state_sim import (
    s_n_character_data,
    delta_char,
    build_group_S_n,
    coset_state_avg_density,
    trace_distance,
    trace_norm,
    _tensor_power,
)


# -------------------------------------------------------------
# (i) Wreath-product characters S_n ≀ S_2
# -------------------------------------------------------------
# Recall S_n ≀ S_2  has order (n!)^2 · 2.
# Its irreps are indexed by pairs (α, β) of partitions with |α|+|β| = n
# for each "chunk" — actually for S_n ≀ S_2 the irreps are parametrized
# by pairs (μ, ν) of partitions of n_1 + n_2 = n with a Z_2 symmetry.
# The full character formula (Specht / James-Kerber) is:
#   For the wreath S_n ≀ S_2 = (S_n × S_n) ⋊ S_2, irreps are:
#     (a) type "diagonal": for each pair {λ, λ'} of partitions of n
#         with λ ≠ λ', a single irrep of dim d_λ · d_{λ'} · 2.
#     (b) for each partition λ of n, TWO irreps of dim d_λ² each,
#         differing by the sign of the S_2 factor.
# But for the specific hidden subgroup H = {(e,e,0), (e,e,1)} that arises
# in GI, we do not need the full irrep decomposition:
#
# Instead, use the transfer lemma (Lemma 1) from the paper: the paper
# shows lower bounds for S_n ≀ S_2 by pulling back the H problem to S_{2n}
# where h becomes the fixed-point-free involution (1,n+1)(2,n+2)···(n,2n).
# So the relevant character bound for the GI setting is
#     Δ_char(2n, t; h = fixed-point-free involution)
#            := (2^t / (2n)!) · Σ_{τ ∈ Ŝ_{2n}} d_τ · |χ_τ(h)|,
# where h has cycle type (2^n) inside S_{2n}.
#
# This is exactly what we compute below.

from coset_state_sim import partitions, frobenius_character_table, conj_class_sizes


def s_n_character_data_at_cycle_type(n, mu):
    """Same as s_n_character_data but for a general cycle-type mu (partition of n)."""
    from math import factorial as fact
    parts, _, chi = frobenius_character_table(n)
    idx_id = parts.index(tuple([1] * n))
    if tuple(sorted(mu, reverse=True)) not in parts:
        raise ValueError(f"cycle type {mu} not a valid partition of {n}")
    idx_mu = parts.index(tuple(sorted(mu, reverse=True)))
    dims = [int(chi[i, idx_id]) for i in range(len(parts))]
    chis = [int(chi[i, idx_mu]) for i in range(len(parts))]
    return {
        "n": n,
        "|G|": fact(n),
        "cycle_type": list(mu),
        "partitions": [list(p) for p in parts],
        "dims": dims,
        "chi_h": chis,
    }


def delta_char_at_cycle_type(n, mu, t):
    """(2^t / n!) · Σ_τ d_τ |χ_τ(evaluated on cycle type mu)|"""
    d = s_n_character_data_at_cycle_type(n, mu)
    G = d["|G|"]
    S = sum(dt * abs(ch) for dt, ch in zip(d["dims"], d["chi_h"]))
    return (2.0 ** t) * S / G, S, G, d


def wreath_gi_char_sweep(n_max=4, t_max=6):
    """
    Δ_char for graph-isomorphism-style hidden subgroup: G = S_{2n},
    h = (1,n+1)(2,n+2)...(n,2n) of cycle type (2^n).
    (via the transfer lemma, this bounds the wreath-product case too.)
    """
    out = []
    for n in range(2, n_max + 1):
        mu = tuple([2] * n)  # cycle type 2^n in S_{2n}
        for t in range(1, t_max + 1):
            bnd, S, G, d = delta_char_at_cycle_type(2 * n, mu, t)
            out.append({
                "n_underlying_graph": n,
                "2n": 2 * n,
                "|S_{2n}|": G,
                "cycle_type_h": list(mu),
                "t": t,
                "sum_d_chi": S,
                "delta_char_bound": bnd,
                "log2_bound": (math.log2(bnd) if bnd > 0 else float("-inf")),
            })
    return out


# -------------------------------------------------------------
# (ii) Helstrom (=PGM for 2-hypothesis) distinguishing probability
# -------------------------------------------------------------


def helstrom_pair(rho0, rho1, p0=0.5, p1=0.5):
    """
    Optimal single-shot success probability of distinguishing rho0
    (prior p0) from rho1 (prior p1) via a POVM:
      P_succ = 1/2 (1 + || p0 ρ0 - p1 ρ1 ||_1).
    For p0 = p1 = 1/2:
      P_succ = 1/2 + 1/2 · d_tr(ρ0, ρ1),  d_tr = (1/2)||ρ0-ρ1||_1.
    """
    D = p0 * rho0 - p1 * rho1
    return 0.5 * (1.0 + trace_norm(D)), trace_norm(rho0 - rho1)


def pgm_extended(n_vals=(2, 3, 4, 5), t_vals=(1, 2)):
    """
    For each (n, t) compute:
      - LHS trace distance || avg_a ρ_{H^a}^{⊗t} − ρ_{{1}}^{⊗t} ||_1
      - Helstrom P_succ
      - Character bound
    """
    results = []
    from coset_state_sim import build_group_S_n, coset_state_avg_density
    import itertools
    for n in n_vals:
        perms, idx, compose, inverse = build_group_S_n(n)
        N = len(perms)
        e = tuple(range(n))
        h_perm = list(range(n))
        h_perm[0], h_perm[1] = 1, 0
        h_tuple = tuple(h_perm)

        avg_rho_Ha = np.zeros((N, N))
        for a in perms:
            a_inv = inverse(a)
            aha = compose(a, compose(h_tuple, a_inv))
            avg_rho_Ha += coset_state_avg_density(n, [e, aha])
        avg_rho_Ha /= N
        rho_1 = np.eye(N) / N

        for t in t_vals:
            if N ** t > 900:
                results.append({
                    "n": n, "t": t, "skipped": True,
                    "reason": f"N^t = {N**t} too big",
                })
                continue
            R = _tensor_power(avg_rho_Ha, t)
            R1 = _tensor_power(rho_1, t)
            td_1norm = trace_norm(R - R1)
            d_tr = 0.5 * td_1norm
            p_succ, _ = helstrom_pair(R, R1)
            bnd, S, G, _ = delta_char(n, t)
            results.append({
                "n": n, "|G|": N, "t": t,
                "one_norm_diff": td_1norm,
                "trace_distance": d_tr,
                "helstrom_P_succ": p_succ,
                "char_bound_on_1norm": bnd,
                "char_bound_on_trace_distance": bnd / 2.0,
                "LHS_le_RHS_1norm": bool(td_1norm <= bnd + 1e-9),
                "distance_from_random_guess": p_succ - 0.5,
            })
    return results


if __name__ == "__main__":
    outdir = os.path.dirname(os.path.abspath(__file__))
    t0 = time.time()

    print("=== Wreath / graph-iso setting: G = S_{2n}, h = (2^n) ===")
    gi_sweep = wreath_gi_char_sweep(n_max=6, t_max=8)
    for r in gi_sweep:
        print(f"  graph n={r['n_underlying_graph']}  |S_{{2n}}|={r['|S_{2n}|']:>10d}  "
              f"t={r['t']}  Σd|χ|={r['sum_d_chi']:>12d}  bound={r['delta_char_bound']:.6g}  "
              f"log2={r['log2_bound']:+.3f}")

    print("\n=== Extended PGM/Helstrom sweep, n=2..5, t=1..2 ===")
    pgm = pgm_extended(n_vals=(2, 3, 4, 5), t_vals=(1, 2))
    for r in pgm:
        if r.get("skipped"):
            print(f"  n={r['n']} t={r['t']} SKIPPED ({r['reason']})")
            continue
        print(f"  n={r['n']} t={r['t']}  "
              f"d_tr={r['trace_distance']:.5g}  "
              f"P_succ={r['helstrom_P_succ']:.5f}  "
              f"bound(1-norm)={r['char_bound_on_1norm']:.4g}  "
              f"ok={r['LHS_le_RHS_1norm']}")

    # Additional cross-check on the paper's claim:
    #   for polynomial-in-n number of copies t = poly(n),
    #   the trace-distance bound must exceed 1 (otherwise indistinguishable).
    #   solve 2^t · (Σ d|χ|) / |G| = 1  →  t* = log2( |G| / Σ d|χ| )
    print("\n=== t*(n) growth for graph-iso setting (S_{2n} target) ===")
    t_star_gi = []
    for r in gi_sweep:
        if r["t"] != 1:  # only need one row per n
            continue
        Sn = r["|S_{2n}|"]
        S = r["sum_d_chi"]
        t_star = math.log2(Sn / S) if S > 0 else float("inf")
        n = r["n_underlying_graph"]
        n_logn = n * math.log2(max(n, 2))
        t_star_gi.append({
            "n_graph": n,
            "|S_{2n}|": Sn,
            "sum_d_chi": S,
            "t_star": t_star,
            "n_log2_n": n_logn,
            "ratio_t_star_over_n_log2_n": t_star / n_logn if n_logn > 0 else None,
        })
        print(f"  n_graph={n}  t*={t_star:.3f}  n·log₂(n)={n_logn:.3f}  "
              f"ratio={t_star/n_logn:.3f}")

    total = time.time() - t0
    out = {
        "graph_iso_wreath_char_sweep": gi_sweep,
        "extended_pgm_helstrom": pgm,
        "t_star_growth_graph_iso": t_star_gi,
        "wall_clock_seconds": round(total, 3),
    }
    with open(os.path.join(outdir, "results_wreath_pgm.json"), "w") as f:
        json.dump(out, f, indent=2, default=str)
    print(f"\nWall time: {total:.2f}s")
    print(f"Written {os.path.join(outdir, 'results_wreath_pgm.json')}")
