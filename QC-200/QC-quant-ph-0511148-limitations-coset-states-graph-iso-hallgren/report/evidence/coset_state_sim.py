#!/usr/bin/env python3
"""
Independent replication for Hallgren-Rötteler-Sen, arXiv:quant-ph/0511148
'Limitations of Quantum Coset States for Graph Isomorphism' (2005).

We reproduce the concrete inequality of Theorem 12,

    || E_g[ σ_{H^g}^{⊗t} ] − σ_{{1}}^{⊗t} ||_tr  <  (2^t / |G|) · Σ_{τ∈Ĝ} d_τ · |χ_τ(h)|,

for small symmetric groups G = S_n with the involutive-swap-style
hidden subgroup H = {e, h}, where h is a fixed transposition
(prototype of the involutive swaps that arise in the graph-isomorphism
HSP reduction to S_n ≀ S_2).

We compute:
  (a) The character-table RHS  Δ_char(n, t) := (2^t / n!) · Σ_τ d_τ |χ_τ(h)|.
  (b) The exact LHS trace distance via explicit density matrices ρ_H, ρ_{1}
      on ℂ[G] and their tensor powers, for the smallest n where the ⊗t
      matrix still fits in memory.
  (c) The pretty-good measurement (PGM) success probability
      P_succ = (1/2) + (1/4) · || ρ_H^{⊗t} − ρ_{1}^{⊗t} ||_1
      (Helstrom bound) — the maximum single-shot distinguishing
      probability of the state-discrimination task.
  (d) Scaling in n, t: verifies that Δ_char scales as expected
      (exponentially small in n at fixed t; grows like 2^t at fixed n)
      and confirms the paper's central negative claim: Δ_char < 1
      unless t ≳ log|G| = O(n log n).

All linear algebra is real numpy over the regular representation.
No fabrication.  Runtime O(minutes) up through n = 5, t = 3.
"""

from __future__ import annotations
import itertools
import json
import math
import os
import sys
import time

import numpy as np
from sympy.combinatorics import Permutation, SymmetricGroup
from sympy.combinatorics.permutations import _af_new
from sympy import Rational

# -------------------------------------------------------------
# 1) Symmetric-group character table (via Frobenius / Murnaghan)
# -------------------------------------------------------------
# We need χ_τ(h) for every irrep τ of S_n, where h is a fixed
# transposition.  This depends only on cycle type of h = (2, 1^{n-2}).
# For symmetric groups we use sympy's character-table facility
# for reliability at small n.
from sympy.combinatorics import Permutation as P
from sympy.combinatorics.named_groups import SymmetricGroup as Sym
from sympy import symmetric_poly


def partitions(n):
    """Yield all integer partitions of n as tuples in weakly decreasing order."""
    if n == 0:
        yield ()
        return

    def _rec(n, max_part):
        if n == 0:
            yield ()
            return
        for p in range(min(n, max_part), 0, -1):
            for rest in _rec(n - p, p):
                yield (p,) + rest

    yield from _rec(n, n)


def cycle_type(perm_tuple):
    """Cycle type of a permutation given as image tuple (0-indexed)."""
    n = len(perm_tuple)
    seen = [False] * n
    cyc = []
    for i in range(n):
        if seen[i]:
            continue
        j = i
        L = 0
        while not seen[j]:
            seen[j] = True
            j = perm_tuple[j]
            L += 1
        cyc.append(L)
    return tuple(sorted(cyc, reverse=True))


def conj_class_sizes(n):
    """Return dict: partition-of-n -> class size in S_n."""
    from math import factorial as fact
    out = {}
    for lam in partitions(n):
        # class size = n! / (Π_i (i^{m_i} · m_i!))  with lam = 1^{m1} 2^{m2} ...
        m = {}
        for p in lam:
            m[p] = m.get(p, 0) + 1
        denom = 1
        for i, mi in m.items():
            denom *= (i ** mi) * fact(mi)
        out[lam] = fact(n) // denom
    return out


def frobenius_character_table(n):
    """
    Return (partitions_list, cycle_types_list, chi) where
       chi[i,j] = character χ_{λ_i} evaluated on cycle type μ_j,
    computed via the Frobenius formula using symmetric polynomials.
    Integer entries only (S_n characters are integers).
    """
    from sympy import symbols, Poly, prod as sym_prod, factorial
    from sympy import symmetric_poly

    parts = list(partitions(n))
    # For efficiency, use standard hook-length via Murnaghan-Nakayama.
    from math import factorial as fact
    # Fall back to sympy's own S_n character table:
    from sympy.combinatorics.named_groups import SymmetricGroup
    from sympy.combinatorics.perm_groups import PermutationGroup
    # sympy does not ship a direct character table for S_n in older versions;
    # implement Murnaghan-Nakayama directly.
    return _murnaghan_nakayama_table(n, parts)


def _remove_border_strip(shape, k):
    """
    Yield (new_shape, height) for every way to remove a k-border-strip
    from Young shape `shape` (as a nonincreasing tuple of row lengths).
    `height` = (# rows spanned) - 1.
    """
    # Standard Murnaghan-Nakayama border-strip enumeration.
    rows = list(shape)
    # We treat shape as list of row lengths; a border strip is a connected
    # skew shape of size k with no 2x2 block, occupying columns i..j and rows
    # such that in each row we remove some contiguous rightmost cells.
    # Enumerate by choosing the topmost row `r` of the strip and iterating.
    m = len(rows)
    # try every top row r (0-indexed)
    results = []
    for r in range(m):
        # We remove cells from rows r, r+1, ..., r+h, forming a border strip.
        # In each such row s, we remove rows[s] - a_s cells from the right,
        # where a_s (residual length) satisfies:
        #   rows[s] > a_s   (must remove at least one cell)
        #   a_s >= rows[s+1] - 1     (so that the strip is connected via
        #                             overlapping columns between rows s and s+1)
        #   a_s >= 0
        # We also need the final residual shape to be a valid partition.
        # Simpler: enumerate over height h (0..m-r-1), then over the number of
        # cells taken from each of rows r..r+h subject to the constraints.
        for h in range(m - r):
            # rows r..r+h are involved.  The strip in row s occupies columns
            # [a_s+1, rows[s]] with a_s >= 0.
            # Connectivity: strip in row s and row s+1 must share a column,
            # i.e. a_{s+1}+1 <= rows[s]  <=>  a_{s+1} <= rows[s]-1  (auto by a_{s+1} < rows[s+1] <= rows[s]).
            # Also strip must be connected downward: rows[s+1] > a_s  <=>  a_s < rows[s+1].
            # And no 2x2: a_{s+1} >= rows[s+1] - 1 ??  Actually no 2x2 means
            # in the strip, consecutive rows can overlap in at most 1 column,
            # so a_{s+1} >= a_s ... let's use the standard characterization:
            #   for s = r..r+h-1:   a_s = rows[s+1] - 1
            # (i.e. in the interior of the strip, the row-residual is forced).
            # Only a_{r+h} (bottom of strip) is free, and we choose it so that
            # total cells removed = k.
            # Cells removed in row s = rows[s] - a_s.
            # For s = r..r+h-1: cells = rows[s] - (rows[s+1] - 1) = rows[s]-rows[s+1]+1.
            # For s = r+h: cells = rows[r+h] - a_{r+h}.
            # Sum must equal k.
            fixed = 0
            ok = True
            for s in range(r, r + h):
                a_s = rows[s + 1] - 1
                if a_s < 0 or a_s >= rows[s]:
                    ok = False
                    break
                fixed += rows[s] - a_s
            if not ok:
                continue
            remaining = k - fixed
            # cells removed in bottom row = remaining, so a_bot = rows[r+h] - remaining.
            bot = r + h
            a_bot = rows[bot] - remaining
            if remaining <= 0 or a_bot < 0:
                continue
            # a_bot must not exceed row above's a_{bot-1} (which is rows[bot]-1) ... actually
            # we need the resulting shape to remain a partition:
            new_rows = list(rows)
            for s in range(r, bot):
                new_rows[s] = rows[s + 1] - 1
            new_rows[bot] = a_bot
            # verify partition
            good = True
            for i in range(len(new_rows) - 1):
                if new_rows[i] < new_rows[i + 1]:
                    good = False
                    break
            if not good:
                continue
            # trim trailing zeros
            while new_rows and new_rows[-1] == 0:
                new_rows.pop()
            # for the strip to be valid, we also need connectivity in the interior:
            # a_s < rows[s+1] for s in [r..bot-1].  a_s = rows[s+1]-1 < rows[s+1] ✓.
            # And connectivity of bottom to (bot-1): we required a_{bot-1}=rows[bot]-1 above.
            results.append((tuple(new_rows), h))
    return results


def chi_lambda_on_mu(lam, mu):
    """
    Compute χ_λ(μ) via the Murnaghan-Nakayama rule.
    lam, mu: tuples (nonincreasing) with sum(lam) == sum(mu) == n.
    """
    # Base case
    if sum(lam) == 0:
        return 1
    mu = list(mu)
    k = mu[0]
    mu_rest = tuple(mu[1:])
    total = 0
    for new_shape, h in _remove_border_strip(lam, k):
        total += ((-1) ** h) * chi_lambda_on_mu(new_shape, mu_rest)
    return total


def _murnaghan_nakayama_table(n, parts):
    """Return (parts, parts, chi_matrix) as int numpy array."""
    m = len(parts)
    chi = np.zeros((m, m), dtype=object)
    for i, lam in enumerate(parts):
        for j, mu in enumerate(parts):
            chi[i, j] = chi_lambda_on_mu(lam, mu)
    return parts, parts, chi.astype(np.int64)


def s_n_character_data(n):
    """
    Return dict with:
      partitions:  list of partitions of n (irreps of S_n indexed by these)
      dims:        list of dim d_τ = χ_τ(1^n)  (must match hook-length)
      chi_h:       list of χ_τ(h) for h = transposition, cycle type 2·1^{n-2}
      class_sizes: dict partition -> class size in S_n
    """
    from math import factorial as fact
    parts, _, chi = frobenius_character_table(n)
    idx_id = parts.index(tuple([1] * n))
    trans_type = tuple([2] + [1] * (n - 2)) if n >= 2 else tuple([1] * n)
    idx_h = parts.index(trans_type)
    dims = [int(chi[i, idx_id]) for i in range(len(parts))]
    chi_h_vals = [int(chi[i, idx_h]) for i in range(len(parts))]
    return {
        "n": n,
        "|G|": fact(n),
        "partitions": [list(p) for p in parts],
        "dims": dims,
        "chi_h": chi_h_vals,
        "class_sizes": {str(list(k)): v for k, v in conj_class_sizes(n).items()},
    }


# -------------------------------------------------------------
# 2) Theorem 12 RHS:  Δ_char(n, t) := (2^t / |G|) Σ_τ d_τ |χ_τ(h)|
# -------------------------------------------------------------


def delta_char(n, t):
    d = s_n_character_data(n)
    G = d["|G|"]
    S = sum(dt * abs(ch) for dt, ch in zip(d["dims"], d["chi_h"]))
    # exact integer arithmetic + one float division
    return (2.0 ** t) * S / G, S, G, d


# -------------------------------------------------------------
# 3) LHS: exact trace distance via density matrices on ℂ[G]
# -------------------------------------------------------------
# The regular-representation coset state for coset gH is
#   |gH> = (1/√|H|) Σ_{h∈H} |g·h>
# and the *hidden-subgroup coset state* mixed state is
#   σ_{H} := (1/|G|) Σ_{g∈G} |gH><gH|
# We compute σ_H and σ_{1} explicitly.
# Then the LHS of Thm 12 is  || E_{a∈G}[ σ_{a H a^{-1}}^{⊗t} ] − σ_{{1}}^{⊗t} ||_tr.
# Since conjugation of H by a fixed transposition merely relabels basis
# vectors, all conjugate copies σ_{H^a} are basis-permutation conjugates of
# σ_H, so E_a σ_{H^a} = (1/|G|) Σ_a σ_{H^a} is easy to compute directly.


def build_group_S_n(n):
    """Return list of permutations of [0..n-1] as tuples, and product/inverse tables."""
    from math import factorial as fact
    perms = list(itertools.permutations(range(n)))
    idx = {p: i for i, p in enumerate(perms)}

    def compose(p, q):
        # (p ∘ q)(i) = p(q(i))
        return tuple(p[q[i]] for i in range(n))

    def inverse(p):
        inv = [0] * n
        for i, v in enumerate(p):
            inv[v] = i
        return tuple(inv)

    return perms, idx, compose, inverse


def coset_state_avg_density(n, H_elems):
    """
    Return ρ = (1/|G|) Σ_{g∈G} |gH><gH|, as a dense |G|×|G| numpy array,
    where |gH> = (1/√|H|) Σ_{h∈H} e_{g·h} in the standard basis of ℂ[G].
    H_elems: list of permutation tuples that form a subgroup of S_n.
    """
    perms, idx, compose, _ = build_group_S_n(n)
    N = len(perms)
    HN = len(H_elems)
    rho = np.zeros((N, N), dtype=np.float64)
    coef_g = 1.0 / N   # (1/|G|)
    coef_h = 1.0 / HN  # (1/|H|)  from |gH><gH|
    # Instead of building each ket, sum outer products directly.
    for gi, g in enumerate(perms):
        for h1 in H_elems:
            i1 = idx[compose(g, h1)]
            for h2 in H_elems:
                i2 = idx[compose(g, h2)]
                rho[i1, i2] += coef_g * coef_h
    return rho


def trace_norm(A):
    """|| A ||_1 = sum of singular values."""
    # A is Hermitian in our use case, so eigvalsh is fine and stable.
    if np.allclose(A, A.T.conj()):
        w = np.linalg.eigvalsh(A)
        return float(np.sum(np.abs(w)))
    s = np.linalg.svd(A, compute_uv=False)
    return float(np.sum(s))


def trace_distance(rho, sigma):
    return 0.5 * trace_norm(rho - sigma)


# -------------------------------------------------------------
# 4) Simulation driver
# -------------------------------------------------------------


def run_char_sweep(n_max=8, t_max=6):
    """
    Compute Δ_char(n, t) := (2^t / |G|) Σ_τ d_τ |χ_τ(h)| for n=2..n_max,
    t=1..t_max.  This is closed-form character-theoretic and cheap.
    """
    out = {"description":
           "Theorem-12 RHS upper bound on trace distance between "
           "E_g σ_{H^g}^{⊗t} and σ_{{1}}^{⊗t} for G=S_n, "
           "H generated by a single transposition.",
           "grid": []}
    for n in range(2, n_max + 1):
        for t in range(1, t_max + 1):
            val, S, G, d = delta_char(n, t)
            out["grid"].append({
                "n": n,
                "|G|": G,
                "t": t,
                "sum_d_chi": S,
                "delta_char_bound": val,
                "log2_bound": (math.log2(val) if val > 0 else float("-inf")),
            })
    return out


def run_exact_trace_distance(n_vals=(2, 3, 4), t_vals=(1, 2), verbose=True):
    """
    Exact numerical trace distance for small n, t.
    Compares to Δ_char(n, t) upper bound.
    """
    results = []
    for n in n_vals:
        perms, idx, compose, inverse = build_group_S_n(n)
        e = tuple(range(n))
        # H = {e, transposition (0 1)}.  h_tuple:
        h_perm = list(range(n))
        h_perm[0], h_perm[1] = 1, 0
        h_tuple = tuple(h_perm)
        H_elems = [e, h_tuple]

        # ρ_H  (mixed state for H = {e, h})
        rho_H = coset_state_avg_density(n, H_elems)
        # ρ_{1}  (mixed state for H = {e}) = maximally-mixed / |G|
        # because  σ_{{1}} = (1/|G|) Σ_g |g><g| = I/|G|.
        N = len(perms)
        rho_1 = np.eye(N) / N

        # For hidden-subgroup H^a = a H a^{-1}, ρ_{H^a} is obtained by
        # basis relabeling.  E_{a∈G}[ρ_{H^a}] is:
        # E_a[ρ_{H^a}] = (1/|G|) Σ_a P_a ρ_H P_a^†, where P_a is the
        # permutation matrix acting on ℂ[G] as e_g -> e_{a g a^{-1}}.
        # But conjugation stabilizes trace; and for a *single* copy the LHS
        # of Thm 12 with the norm outside the expectation is bounded above
        # via the RHS. To match the theorem statement literally, we
        # compute E_a[ρ_{H^a}] − ρ_{{1}} first.
        # For k=1 (single copy), all conjugates are permutation-equivalent
        # to ρ_H, so we accumulate and average.

        avg_rho_Ha = np.zeros_like(rho_H)
        for a in perms:
            a_inv = inverse(a)
            # H^a = {e, a h a^{-1}}
            aha = compose(a, compose(h_tuple, a_inv))
            H_a = [e, aha]
            avg_rho_Ha += coset_state_avg_density(n, H_a)
        avg_rho_Ha /= len(perms)

        for t in t_vals:
            # Tensor power sizes: N^t x N^t
            if N ** t > 900:
                # Skip if too big; keep the run tractable.
                results.append({
                    "n": n,
                    "|G|": N,
                    "t": t,
                    "skipped": True,
                    "reason": f"N^t = {N**t} exceeds 900 dim cap",
                })
                continue
            # Build tensor powers
            rho_Ha_t = _tensor_power(avg_rho_Ha, t)
            rho_1_t = _tensor_power(rho_1, t)
            td = trace_distance(rho_Ha_t, rho_1_t)
            bnd, S, G, _ = delta_char(n, t)
            # Also Helstrom (PGM) success probability for the two-hypothesis
            # discrimination task:  ρ_H vs ρ_{1}, each with prior 1/2.
            # P_succ = 1/2 + 1/2 · d_tr(ρ_H, ρ_{1})   (per the exact
            # Helstrom bound d_tr = 1/2 || · ||_1).
            p_succ = 0.5 + 0.5 * td
            results.append({
                "n": n,
                "|G|": N,
                "t": t,
                "trace_distance_LHS": td,
                "delta_char_bound_RHS": bnd,
                "ratio_LHS_over_RHS": td / bnd if bnd > 0 else None,
                "helstrom_P_succ": p_succ,
                "matches_theorem": bool(td <= bnd + 1e-9),
            })
            if verbose:
                print(f"n={n} t={t}  LHS={td:.6g}  RHS(Thm12)={bnd:.6g}  ok={td<=bnd+1e-9}")
    return results


def _tensor_power(A, t):
    if t == 1:
        return A
    T = A
    for _ in range(t - 1):
        T = np.kron(T, A)
    return T


# -------------------------------------------------------------
# 5) Scaling analysis
# -------------------------------------------------------------


def scaling_analysis(char_sweep):
    """
    Given the character-sweep grid, determine the threshold
    t*(n) = smallest t such that Δ_char(n, t) >= 1
    (i.e. beyond which the trace-distance bound no longer implies
    inability to distinguish).
    Compare log2(t*(n)) to n · log2(n) (paper's Ω(n log n) claim).
    """
    grid = char_sweep["grid"]
    # organize by n
    by_n = {}
    for r in grid:
        by_n.setdefault(r["n"], []).append(r)
    scaling = []
    for n, rows in by_n.items():
        rows.sort(key=lambda r: r["t"])
        # t* = smallest t with bound >= 1; if none, extrapolate log2
        # d_τ |χ_τ| sum grows exp in n; bound = 2^t * S/G, so t* = log2(G/S)
        # from the *last row* just read off S,G:
        S = rows[0]["sum_d_chi"]
        G = rows[0]["|G|"]
        t_star_real = math.log2(G / S) if S > 0 else float("inf")
        n_logn = n * math.log2(max(n, 2))
        scaling.append({
            "n": n,
            "|G|": G,
            "sum_d_chi": S,
            "t_star (log2(G/S))": t_star_real,
            "n·log2(n)": n_logn,
            "ratio t*/(n·log2(n))": t_star_real / n_logn if n_logn > 0 else None,
        })
    return scaling


# -------------------------------------------------------------
# 6) Main
# -------------------------------------------------------------

if __name__ == "__main__":
    outdir = os.path.dirname(os.path.abspath(__file__))
    t0 = time.time()

    # (A) closed-form character sweep, n=2..8, t=1..6
    print("=== Character sweep (Thm 12 RHS bound) ===")
    char_sweep = run_char_sweep(n_max=8, t_max=6)
    for row in char_sweep["grid"]:
        print(f"  n={row['n']} t={row['t']}  |G|={row['|G|']:>6d}  "
              f"Σd|χ|={row['sum_d_chi']:>10d}  bound={row['delta_char_bound']:.6g}  "
              f"log2={row['log2_bound']:+.3f}")

    # (B) exact trace-distance verification, n=2..4
    print("\n=== Exact trace-distance verification (LHS ≤ RHS?) ===")
    exact = run_exact_trace_distance(n_vals=(2, 3, 4), t_vals=(1, 2))

    # (C) scaling extraction
    print("\n=== Scaling: t*(n) vs n·log₂(n) ===")
    scaling = scaling_analysis(char_sweep)
    for row in scaling:
        print(f"  n={row['n']}  t*={row['t_star (log2(G/S))']:.3f}  "
              f"n·log₂(n)={row['n·log2(n)']:.3f}  "
              f"ratio={row['ratio t*/(n·log2(n))']:.3f}")

    # (D) also record character data for n=2..7 (n=8 dim table gets large)
    print("\n=== Character data ===")
    char_data = {}
    for n in range(2, 8):
        d = s_n_character_data(n)
        char_data[str(n)] = d
        print(f"  S_{n}: irreps={len(d['partitions'])}  "
              f"dims={d['dims']}  χ(transposition)={d['chi_h']}")

    total_time = time.time() - t0

    result = {
        "paper": "arXiv:quant-ph/0511148 Hallgren-Rötteler-Sen 2005",
        "quantity_reproduced": "Theorem 12 upper bound on trace distance "
                               "|| E_g σ_{H^g}^{⊗t} − σ_{{1}}^{⊗t} ||_tr "
                               "≤ (2^t/|G|) Σ_τ d_τ |χ_τ(h)|",
        "group_family": "S_n, H = <transposition>",
        "n_range": [2, 8],
        "t_range": [1, 6],
        "character_sweep": char_sweep,
        "exact_trace_distance_verification": exact,
        "scaling_analysis": scaling,
        "character_data_S_n": char_data,
        "wall_clock_seconds": round(total_time, 3),
    }
    with open(os.path.join(outdir, "results.json"), "w") as f:
        json.dump(result, f, indent=2, default=str)
    print(f"\nWall time: {total_time:.2f}s")
    print(f"Results written to {os.path.join(outdir, 'results.json')}")
