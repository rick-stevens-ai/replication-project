#!/usr/bin/env python3
"""
Classical-simulator replication of Shor's factoring algorithm (Shor 1997).

Implements the quantum order-finding subroutine via *exact statevector simulation*
of the algorithm described in §5 of the paper:

  1. Prepare |a>|0> in uniform superposition over 0 <= a < q, with q = 2^L the
     smallest power of 2 with N^2 <= q < 2*N^2.
  2. Compute |a>|x^a mod N> in the second register (modular exponentiation,
     done classically/coherently here since the second register acts only as
     "entanglement collapse" -- we do not need to simulate the reversible gate
     network; the resulting joint amplitude distribution is identical).
  3. Apply the quantum Fourier transform (QFT) to the first register --
     implemented as the exact unitary DFT matrix-vector product on the
     reduced amplitudes (equivalent to the §4 Coppersmith QFT exactly).
  4. Sample c from |first-register amplitudes|^2.
  5. Classical post-processing: continued-fraction expansion of c/q to recover
     denominator r' < N; try r' and small multiples; test x^r == 1 mod N.
  6. Recover factors of N via gcd(x^{r/2} - 1, N) and gcd(x^{r/2} + 1, N).

This is the *exact* probability distribution Shor's algorithm produces; we are
not subsampling or approximating. The only "substitution" is that we collapse
the second register implicitly (which is mathematically equivalent: tracing out
the second register and then sampling the first is the same joint distribution
as sampling both jointly and discarding the second).

Run:  python3 replicate.py
"""

from __future__ import annotations

import math
import random
import sys
import time
from dataclasses import dataclass, field
from fractions import Fraction
from math import gcd
from typing import Optional

import numpy as np


# ----------------------------------------------------------------------------
# Helper: classical bits
# ----------------------------------------------------------------------------

def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


def is_prime_power(n: int) -> Optional[tuple[int, int]]:
    """Return (p, k) if n = p^k for some prime p and k>=1, else None."""
    for p in range(2, int(n ** 0.5) + 2):
        if n % p != 0:
            continue
        if not is_prime(p):
            continue
        k = 0
        m = n
        while m % p == 0:
            m //= p
            k += 1
        if m == 1:
            return (p, k)
    if is_prime(n):
        return (n, 1)
    return None


def classical_order(x: int, N: int) -> int:
    """Brute-force the true multiplicative order of x mod N (small N only)."""
    assert gcd(x, N) == 1
    r = 1
    y = x % N
    while y != 1:
        y = (y * x) % N
        r += 1
    return r


# ----------------------------------------------------------------------------
# Quantum order-finding via exact statevector simulation
# ----------------------------------------------------------------------------

@dataclass
class ShorRun:
    N: int
    x: int
    q: int
    L: int  # log2(q), number of qubits in first register
    c: int
    candidate_r: Optional[int]
    true_r: int
    found_r: bool
    factor: Optional[int]


def choose_q(N: int) -> tuple[int, int]:
    """Choose q = 2^L with N^2 <= q < 2 N^2, per Shor §5."""
    target = N * N
    L = math.ceil(math.log2(target))
    q = 1 << L
    assert N * N <= q < 2 * N * N
    return q, L


def order_finding_distribution(x: int, N: int, q: int) -> np.ndarray:
    """
    Return P(c) for c in 0..q-1 produced by Shor's order-finding circuit
    on input x, N with first-register size q.

    Computed *exactly* by:
      - building f(a) = x^a mod N for a in 0..q-1
      - for each output residue y in image(f), the post-second-register-measurement
        state of register 1 is uniform over {a : f(a)=y}, with weight w_y = |{a}|/q
      - applying the QFT to that state gives amplitudes
          A_y(c) = (1/sqrt(|{a}|)) * sum_{a: f(a)=y} exp(2 pi i a c / q) / sqrt(q)
        Actually: the joint state before QFT is (1/sqrt(q)) sum_a |a>|f(a)>.
        After QFT on first register: (1/q) sum_a sum_c exp(2 pi i a c/q) |c>|f(a)>.
        P(c) = sum over distinct y of  | (1/q) sum_{a: f(a)=y} exp(2 pi i a c / q) |^2
      - this is a direct |DFT|^2 of the indicator vectors of preimages, summed
        over output classes. We compute it via per-class FFTs.
    """
    # f(a) for a in 0..q-1
    powers = np.empty(q, dtype=np.int64)
    val = 1
    for a in range(q):
        powers[a] = val
        val = (val * x) % N

    # Bucket indices by residue value
    buckets: dict[int, list[int]] = {}
    for a, y in enumerate(powers):
        buckets.setdefault(int(y), []).append(a)

    P = np.zeros(q, dtype=np.float64)
    for y, indices in buckets.items():
        # indicator vector over a's, length q, scale 1/sqrt(q)
        # FFT it. We exploit that for an arithmetic progression (which buckets
        # always are, with step r), we can compute via direct FFT.
        ind = np.zeros(q, dtype=np.complex128)
        ind[indices] = 1.0
        # The QFT mapping in the paper is |a> -> (1/sqrt q) sum_c exp(+2 pi i a c/q) |c>
        # so the amplitude at c is (1/q) * sum_{a in indices} exp(+2 pi i a c / q)
        # numpy.fft.ifft uses +2 pi i, and returns (1/N) sum, exactly what we want.
        amps = np.fft.ifft(ind)  # length q, with the 1/q normalization
        P += np.abs(amps) ** 2

    # sanity: probabilities sum to 1
    s = P.sum()
    if not (0.999 < s < 1.001):
        raise RuntimeError(f"Probability sum off: {s}")
    P /= s
    return P


def sample_c(P: np.ndarray, rng: random.Random) -> int:
    """Sample c from discrete distribution P."""
    r = rng.random()
    cum = 0.0
    for c, p in enumerate(P):
        cum += p
        if r <= cum:
            return c
    return len(P) - 1


def continued_fraction_candidates(c: int, q: int, N: int) -> list[int]:
    """
    Use continued-fraction expansion of c/q to find candidate denominators r' < N.
    Return list of candidate r's (denominators of convergents that are < N),
    plus small multiples (the paper's third trick).
    """
    if c == 0:
        return []
    frac = Fraction(c, q)
    # build convergents
    a, b = frac.numerator, frac.denominator
    convergents: list[Fraction] = []
    h_prev, h_curr = 0, 1
    k_prev, k_curr = 1, 0
    while b:
        qi = a // b
        a, b = b, a - qi * b
        h_next = qi * h_curr + h_prev
        k_next = qi * k_curr + k_prev
        h_prev, h_curr = h_curr, h_next
        k_prev, k_curr = k_curr, k_next
        convergents.append(Fraction(h_curr, k_curr))

    cands: list[int] = []
    seen: set[int] = set()
    for f in convergents:
        r = f.denominator
        if r < N and r > 0 and r not in seen:
            cands.append(r)
            seen.add(r)
    # plus small multiples of best candidate (Knill trick)
    extra: list[int] = []
    for r in cands:
        for k in (2, 3, 4, 5):
            kr = k * r
            if kr < N and kr not in seen:
                extra.append(kr)
                seen.add(kr)
    return cands + extra


def try_recover_factor(N: int, x: int, r: int) -> Optional[int]:
    """Given candidate r (true order), try x^{r/2} +- 1 to extract factor."""
    if r % 2 != 0:
        return None
    half = pow(x, r // 2, N)
    if half == N - 1:  # i.e., -1 mod N
        return None
    for cand in (gcd(half - 1, N), gcd(half + 1, N)):
        if 1 < cand < N:
            return cand
    return None


def shor_single_trial(N: int, x: int, rng: random.Random, P_cache: Optional[np.ndarray] = None) -> ShorRun:
    """One full run: prepare circuit, sample c, classical post-process."""
    q, L = choose_q(N)
    if P_cache is None:
        P = order_finding_distribution(x, N, q)
    else:
        P = P_cache
    c = sample_c(P, rng)
    true_r = classical_order(x, N)
    cands = continued_fraction_candidates(c, q, N)
    # accept r' iff x^{r'} == 1 mod N
    found_r: Optional[int] = None
    for r in cands:
        if pow(x, r, N) == 1:
            found_r = r
            break
    factor = None
    if found_r is not None:
        factor = try_recover_factor(N, x, found_r)
    return ShorRun(
        N=N, x=x, q=q, L=L, c=c,
        candidate_r=found_r, true_r=true_r,
        found_r=(found_r == true_r),
        factor=factor,
    )


# ----------------------------------------------------------------------------
# Full factoring routine
# ----------------------------------------------------------------------------

def factor_with_shor(N: int, trials: int = 20, seed: int = 0, verbose: bool = True) -> dict:
    """
    Run Shor's algorithm to factor N. For each random valid x, do one quantum
    order-finding trial, then post-process. Return summary stats.
    """
    rng = random.Random(seed)
    if N % 2 == 0:
        return {"N": N, "trivial": True, "factor": 2}
    pk = is_prime_power(N)
    if pk is not None:
        return {"N": N, "trivial": True, "prime_power": pk}

    q, L = choose_q(N)
    if verbose:
        print(f"\n=== Factoring N={N}  (q=2^{L}={q}, statevector dim = {q}) ===")
    results: list[ShorRun] = []
    factors_found = set()
    for t in range(trials):
        # pick random x coprime to N
        while True:
            x = rng.randrange(2, N)
            g = gcd(x, N)
            if g == 1:
                break
            # lucky strike
            if verbose:
                print(f"  trial {t}: lucky gcd hit, x={x}, gcd={g} -> factor {g}")
            factors_found.add(g)
            results.append(ShorRun(N=N, x=x, q=q, L=L, c=-1,
                                   candidate_r=None, true_r=0,
                                   found_r=False, factor=g))
            break
        else:
            continue
        if results and results[-1].factor and results[-1].c == -1:
            # lucky hit, continue to next trial
            continue
        run = shor_single_trial(N, x, rng)
        results.append(run)
        if run.factor:
            factors_found.add(run.factor)
            factors_found.add(N // run.factor)
        if verbose:
            print(f"  trial {t:2d}: x={x:3d}  c={run.c:6d}  cand_r={run.candidate_r}  true_r={run.true_r}  found_r={run.found_r}  factor={run.factor}")
    # compute success rates
    n_ran_quantum = sum(1 for r in results if r.c != -1)
    n_recovered_r = sum(1 for r in results if r.found_r)
    n_factor = sum(1 for r in results if r.factor and r.c != -1)
    return {
        "N": N,
        "q": q,
        "L": L,
        "trials": trials,
        "n_quantum_runs": n_ran_quantum,
        "n_recovered_r": n_recovered_r,
        "n_factor_extracted": n_factor,
        "factors_found": sorted(factors_found),
        "p_recover_r": n_recovered_r / max(n_ran_quantum, 1),
        "p_factor": n_factor / max(n_ran_quantum, 1),
        "results": results,
    }


# ----------------------------------------------------------------------------
# Theoretical comparison: lower bound on success probability per quantum run
# ----------------------------------------------------------------------------

def theoretical_lower_bound(N: int, x: int) -> float:
    """
    Shor's analytic lower bound: prob of finding r in one quantum run is at least
    phi(r) / (3r), where phi is Euler totient. We compute phi(r) exactly here.
    """
    r = classical_order(x, N)
    # Euler's phi(r):
    phi = r
    m = r
    p = 2
    while p * p <= m:
        if m % p == 0:
            while m % p == 0:
                m //= p
            phi -= phi // p
        p += 1
    if m > 1:
        phi -= phi // m
    return phi / (3 * r)


def measured_success_for_all_x(N: int, verbose: bool = True) -> list[dict]:
    """
    For every valid x in (1..N-1) coprime to N, compute the *exact* probability
    that one quantum order-finding run + continued-fraction post-processing
    recovers the true order r.

    This is the gold-standard test: we don't sample, we sum P(c) over all c
    for which the CF expansion yields the true r (or a small multiple of it
    that we accept).
    """
    q, L = choose_q(N)
    rows = []
    xs = [x for x in range(2, N) if gcd(x, N) == 1]
    for x in xs:
        true_r = classical_order(x, N)
        P = order_finding_distribution(x, N, q)
        # for every c, check whether CF post-processing recovers true_r
        good_mass = 0.0
        for c in range(q):
            if P[c] < 1e-15:
                continue
            cands = continued_fraction_candidates(c, q, N)
            ok = any(pow(x, r, N) == 1 and r == true_r for r in cands)
            if ok:
                good_mass += P[c]
        lb = theoretical_lower_bound(N, x)
        rows.append({
            "x": x, "true_r": true_r,
            "P_recover_r": good_mass,
            "shor_lb_phi_r_over_3r": lb,
        })
        if verbose:
            print(f"  x={x:3d}  r={true_r:3d}  P(recover r)={good_mass:.4f}  Shor LB phi(r)/3r={lb:.4f}  ratio={good_mass/max(lb,1e-9):.2f}x")
    return rows


# ----------------------------------------------------------------------------
# Discrete log spot-check (optional, very small prime)
# ----------------------------------------------------------------------------

def shor_discrete_log_brute(p: int, g: int, y: int) -> int:
    """
    Toy discrete-log finder using the same QFT structure, but for a tiny
    prime p so we can exact-simulate. We use the simpler approach: run
    order-finding to find r = order(g), then check Shor's two-register
    DL construction is just a higher-dim DFT. For 'feasibility evidence',
    we just verify y == g^k mod p classically and report k (since DL with
    Shor is conceptually the same QFT trick on (a,b) -> g^a y^{-b} mod p).
    """
    r = classical_order(g, p)
    for k in range(r):
        if pow(g, k, p) == y:
            return k
    raise ValueError("y not a power of g")


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------

def main():
    print("Shor 1997 -- classical statevector replication")
    print("=" * 70)

    targets = [15, 21, 35]   # 15 = 3*5, 21 = 3*7, 35 = 5*7
    summary = []

    for N in targets:
        t0 = time.time()
        out = factor_with_shor(N, trials=20, seed=42 + N, verbose=True)
        dt = time.time() - t0
        out["wall_s"] = dt
        summary.append(out)
        print(f"  -> factors found: {out['factors_found']}  "
              f"  P(recover r)={out['p_recover_r']:.2f}  "
              f"  P(get factor)={out['p_factor']:.2f}  ({dt:.2f}s)")

    print()
    print("=" * 70)
    print("EXACT per-x success probabilities (sum over all c in dist, no sampling)")
    print("=" * 70)

    exact_tables = {}
    for N in targets:
        print(f"\n--- N={N} ---")
        rows = measured_success_for_all_x(N, verbose=True)
        # aggregate
        mean_p = float(np.mean([r["P_recover_r"] for r in rows]))
        min_p = float(np.min([r["P_recover_r"] for r in rows]))
        mean_lb = float(np.mean([r["shor_lb_phi_r_over_3r"] for r in rows]))
        print(f"  AGG N={N}: mean P(recover r) over x = {mean_p:.4f}, "
              f"min = {min_p:.4f}, mean Shor LB = {mean_lb:.4f}")
        exact_tables[N] = {"rows": rows, "mean_p": mean_p, "min_p": min_p, "mean_lb": mean_lb}

    # discrete log conceptual spot-check
    print()
    print("=" * 70)
    print("Discrete-log conceptual spot-check (small group)")
    print("=" * 70)
    p, g, y = 7, 3, 5  # 3^k mod 7: 3,2,6,4,5,1 -> 3^5 = 5
    k = shor_discrete_log_brute(p, g, y)
    print(f"  group (Z/{p}Z)*, generator g={g}, target y={y}")
    print(f"  classical brute-force recovers k={k}; verify g^k mod p = {pow(g,k,p)} == y={y}: {pow(g,k,p)==y}")
    print(f"  Shor's DL circuit would use a 2-register QFT on a~q1, b~q2 to extract")
    print(f"  the slope k from the joint distribution; we did not implement the full")
    print(f"  2-register sim, but the order-finding sim above demonstrates the same")
    print(f"  QFT-period-extraction mechanism that powers it.")

    print()
    print("=" * 70)
    print("FINAL SUMMARY")
    print("=" * 70)
    for s in summary:
        print(f"  N={s['N']:2d}  trials={s['trials']}  factors={s['factors_found']}  "
              f"P(recover r)={s['p_recover_r']:.2f}  P(factor)={s['p_factor']:.2f}  q={s['q']}")
    for N, t in exact_tables.items():
        print(f"  EXACT N={N:2d}: mean P(recover r)={t['mean_p']:.4f}, "
              f"min={t['min_p']:.4f}, mean Shor LB={t['mean_lb']:.4f}")


if __name__ == "__main__":
    main()
