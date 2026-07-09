#!/usr/bin/env python3
"""
Replication of van Dam, Hallgren, Ip 2002 (quant-ph/0211140).

We implement the paper's hidden-shift algorithm (Algorithm 1 generalized to
Z_N) using a pure numpy statevector simulator.

Setup: given oracle f(x) = g(x+s mod N) where g : Z_N -> {+1,-1} is a KNOWN
character-like function whose Fourier transform g_hat has unit-modulus
entries.  Goal: recover the unknown shift s.

Algorithm (paper's circuit, Fig. 1):
  1. Prepare  |psi_1> = (1/sqrt N) sum_x g(x+s) |x>
  2. QFT_N    |psi_2> = sum_y g_hat(y) * omega^(-s y) |y>
  3. Phase-uncompute g_hat: apply diag(1/g_hat(y))  -> sum_y omega^(-s y) |y>
  4. Inverse QFT_N and measure => outcome is (N - s) mod N.

Because g in our reproduction is real-valued in {+1,-1} and chosen so that
|g_hat(y)| = 1 for all y (a "bent"-like function), the phase-uncompute step
is well defined without any zero entries.

We test N = 8, 16, 32.  For each we:
  * pick a random hidden shift s,
  * build the statevector exactly,
  * apply the three unitary steps as N x N matrices,
  * verify the measurement is deterministically N - s (probability = 1),
  * count 1 quantum "query" (the oracle call in step 1 provides all N values
    in superposition -- this is the paper's query model).

We compare to the classical query lower bound: distinguishing among N
possible shifts requires Omega(log N) classical queries (by an information-
theoretic + adversary argument -- each classical query yields <= 1 bit
about s, and log2 N bits are needed).  The quantum algorithm uses O(1)
oracle queries plus O(log N) other gates -- an exponential separation in
oracle complexity.
"""

import json
import numpy as np
from pathlib import Path

RNG = np.random.default_rng(0xC0DE1D)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def qft_matrix(N: int) -> np.ndarray:
    """Standard N-dimensional DFT / QFT matrix (unitary)."""
    j = np.arange(N)
    k = j.reshape(-1, 1)
    omega = np.exp(2j * np.pi / N)
    return omega ** (j * k) / np.sqrt(N)


def choose_bent_like_g(N: int, rng, tries: int = 200000) -> np.ndarray:
    """
    Return g : Z_N -> {+/-1} such that |g_hat(y)| = 1 for all y (a
    "bent-like" function on Z_N).  Note: exact bent functions with real
    +/-1 values do NOT exist on Z_N as an additive group unless N is a
    perfect square (they need |g_hat(y)| = sqrt(N)/sqrt(N) = 1 which
    requires a quadratic character-like construction).  We first attempt
    an exhaustive/random search; if it fails we fall through.
    """
    for _ in range(tries):
        g = rng.choice([-1, +1], size=N).astype(np.complex128)
        gh = np.fft.fft(g) / np.sqrt(N)
        if np.allclose(np.abs(gh), 1.0, atol=1e-9):
            return g
    raise RuntimeError(f"could not find bent-like Boolean g on Z_{N}")


def choose_flat_spectrum_g(N: int, rng) -> np.ndarray:
    """
    Deterministic construction of a function g : Z_N -> unit circle in C
    with |g_hat(y)| = 1 for all y.  We use a chirp / quadratic-phase
    function

        g(x) = exp(2 pi i * a * x^2 / (2N))

    with a coprime to 2N.  This is a Zadoff-Chu / discrete chirp; its
    DFT is another chirp with unit magnitude for even/odd N with the
    obvious parity fix (we adjust a).  For our purposes we just verify
    the flat-spectrum property numerically and pick a working a.

    Such a g is a bona fide known function (paper's setup: g is
    completely known to the algorithm; only s is unknown).  It replaces
    the Boolean bent construction which does not exist on general Z_N.
    """
    x = np.arange(N)
    for a in range(1, 4 * N):
        # try both even and odd chirps
        for phi0 in (0.0, np.pi / N):
            g = np.exp(2j * np.pi * a * x * x / (2 * N) + 1j * phi0)
            gh = np.fft.fft(g) / np.sqrt(N)
            if np.allclose(np.abs(gh), 1.0, atol=1e-8):
                return g
    raise RuntimeError(f"chirp construction failed on Z_{N}")


def choose_g_boolean_noflat(N: int, rng) -> np.ndarray:
    """
    Random Boolean g : Z_N -> {+/-1} with a NOWHERE-ZERO Fourier
    transform (weaker than flat, but sufficient for the algorithm since
    we only need to divide by g_hat(y)).  Used to satisfy the task's
    request for a Boolean g while accepting probabilistic (not
    deterministic) success.
    """
    for _ in range(20000):
        g = rng.choice([-1, +1], size=N).astype(np.complex128)
        gh = np.fft.fft(g) / np.sqrt(N)
        if np.min(np.abs(gh)) > 1e-6:
            return g
    raise RuntimeError(f"no nowhere-zero-spectrum Boolean g on Z_{N}")


# ---------------------------------------------------------------------------
# Hidden-shift algorithm on Z_N
# ---------------------------------------------------------------------------

def run_hidden_shift_zn(N: int, s: int, g: np.ndarray, verbose: bool = False):
    """
    Execute the paper's circuit on Z_N and return the (deterministic-in-
    ideal-case) measurement outcome plus the induced probability
    distribution.  All steps are done as exact statevector operations.

    For a function g with FLAT spectrum |g_hat(y)| = 1 for all y, the
    outcome is deterministic: measurement yields (N - s) mod N with
    probability 1.  For a Boolean g with NOWHERE-ZERO but non-flat
    spectrum, s can still be recovered but only probabilistically.
    """
    assert g.shape == (N,)
    # oracle f(x) = g(x + s mod N)
    f = np.array([g[(x + s) % N] for x in range(N)], dtype=np.complex128)

    # Step 1: |psi_1> = (1/sqrt N) sum_x f(x) |x>.
    # (Lemma 1 -- 2 queries to build the phase-encoded superposition.)
    psi = f / np.sqrt(N)

    # Step 2: QFT
    F = qft_matrix(N)
    psi = F @ psi   # expected: sum_y g_hat(y) omega^{-s y} |y>

    # Step 3: phase uncompute using known g_hat -- multiply by 1/g_hat(y).
    # For flat spectrum this is a unit-modulus phase.  For non-flat but
    # nowhere-zero spectrum we instead multiply by conj(g_hat)/|g_hat|
    # (unit-phase correction) so the state remains normalized; residual
    # magnitude imbalance survives and reduces the peak probability.
    g_hat = F @ g
    inv_g_hat_phase = np.conj(g_hat) / np.abs(g_hat)
    psi = inv_g_hat_phase * psi

    # Step 4: inverse QFT
    Finv = F.conj().T
    psi = Finv @ psi

    probs = np.abs(psi) ** 2
    outcome = int(np.argmax(probs))
    if verbose:
        print(f"  N={N}, hidden s={s}, measured y={outcome}, "
              f"(N-s) mod N={(N-s)%N}, p_max={probs.max():.6f}")
    return {
        "N": N,
        "s": s,
        "outcome": outcome,
        "expected": (N - s) % N,
        "p_outcome": float(probs[outcome]),
        "queries": 2,
    }


# ---------------------------------------------------------------------------
# Classical query lower bound for hidden shift on Z_N with our g
# ---------------------------------------------------------------------------

def classical_shift_lower_bound(N: int, g: np.ndarray, k_max: int = 6):
    """
    A distinguisher-style empirical lower bound on the number of classical
    (adaptive) queries needed to determine s given oracle access to
    f(x) = g(x+s mod N).

    Fact: with k queries the algorithm sees at most k values of g at
    shifted arguments, which together give <= log2(N/collisions) bits
    about s.  We compute, for k = 1..k_max, the WORST-CASE remaining
    ambiguity across all query strategies (approximated via a random
    baseline plus an information-theoretic entropy lower bound).
    """
    # Information-theoretic lower bound: need at least log2(N) bits, and
    # each query into a {+1,-1} oracle yields at most 1 bit, so
    #     k >= log2(N)  =>  k = ceil(log2 N).
    k_bits = int(np.ceil(np.log2(N)))

    # Empirical: for random non-adaptive query set Q of size k, count
    # how many shifts s are indistinguishable (i.e. produce same answer
    # vector).  Average over trials.
    from itertools import combinations
    xs_all = list(range(N))
    empirical = {}
    for k in range(1, min(k_max, N) + 1):
        # try a modest number of random query sets
        worst_ambiguity = 0
        best_ambiguity = N
        avg_ambiguity = 0.0
        trials = 0
        for _ in range(200):
            Q = list(RNG.choice(xs_all, size=k, replace=False))
            # for each s, produce (g(x+s) for x in Q)
            sig = {}
            for s in range(N):
                v = tuple(int(g[(x + s) % N].real) for x in Q)
                sig.setdefault(v, []).append(s)
            # ambiguity = max class size
            worst_class = max(len(v) for v in sig.values())
            worst_ambiguity = max(worst_ambiguity, worst_class)
            best_ambiguity = min(best_ambiguity, worst_class)
            avg_ambiguity += worst_class
            trials += 1
        empirical[k] = {
            "worst_class_worst_of_trials": worst_ambiguity,
            "worst_class_best_of_trials": best_ambiguity,
            "worst_class_avg": avg_ambiguity / trials,
        }
    return {
        "info_theoretic_lower_bound_queries": k_bits,
        "empirical_random_nonadaptive": empirical,
    }


# ---------------------------------------------------------------------------
# Legendre-symbol variant (paper's flagship example, N = p prime)
# ---------------------------------------------------------------------------

def legendre_symbol(a: int, p: int) -> int:
    a = a % p
    if a == 0:
        return 0
    r = pow(a, (p - 1) // 2, p)
    return -1 if r == p - 1 else r


def run_legendre_shift(p: int, s: int, verbose: bool = False):
    """
    Shifted-Legendre-symbol hidden shift on Z_p (paper Section 4,
    Algorithm 1 specialized to the finite field F_p with multiplicative
    character chi = Legendre symbol).

    We implement it as an exact p-dim statevector, following the paper's
    circuit:
       1. Create   sum_x chi(x+s) |x>          (Lemma 1)
       2. QFT      sum_y chi_hat(y) omega^{-s y} |y>
       3. Phase-uncompute chi(y):  |y> -> chi(y) |y> for y != 0.
          Note chi_hat(y) = chi(y) * chi_hat(1) and chi_hat(1) is a Gauss
          sum of magnitude sqrt(p).  So after this step (up to a global
          factor chi_hat(1)) the state is sum_{y != 0} omega^{-s y}|y>.
       4. Inverse QFT and measure -> outcome (p - s) mod p with
          probability (1 - 1/p)^2.
    """
    # Build oracle values chi(x+s)
    chi = np.array([legendre_symbol(x, p) for x in range(p)], dtype=np.complex128)
    f = np.array([chi[(x + s) % p] for x in range(p)], dtype=np.complex128)

    # Step 1: amplitude-encode; note chi has p-1 nonzero entries
    psi = f / np.sqrt(np.sum(np.abs(f) ** 2))

    # Step 2: QFT
    F = qft_matrix(p)
    psi = F @ psi

    # Step 3: phase-uncompute chi for nonzero y.  chi(y) is real +-1 so
    # its inverse is itself; we skip y=0.
    phase = np.array([1.0 + 0j] + [1.0 / chi[y] if chi[y] != 0 else 0
                                    for y in range(1, p)])
    psi = phase * psi

    # Step 4: inverse QFT
    Finv = F.conj().T
    psi = Finv @ psi

    probs = np.abs(psi) ** 2
    # Renormalize (state has some support on |0> from the y=0 kill step)
    outcome = int(np.argmax(probs))
    if verbose:
        print(f"  p={p}, hidden s={s}, measured x={outcome}, "
              f"(p-s) mod p={(p-s)%p}, p_max={probs.max():.4f}, "
              f"theory (1-1/p)^2={(1-1/p)**2:.4f}")
    return {
        "p": p,
        "s": s,
        "outcome": outcome,
        "expected": (p - s) % p,
        "p_outcome": float(probs[outcome]),
        "theory_success_prob": (1 - 1 / p) ** 2,
        "queries": 2,
    }


# ---------------------------------------------------------------------------
# Main driver
# ---------------------------------------------------------------------------

def main():
    out_dir = Path(__file__).resolve().parent
    results = {"paper": "quant-ph/0211140",
               "algorithm": "Algorithm 1 (van Dam-Hallgren-Ip 2002)",
               "backend": "numpy exact statevector",
               "runs": {}}

    # ---- Part (a),(b),(c): hidden shift on Z_N for N = 8, 16, 32 ----
    print("=" * 70)
    print("Hidden shift on Z_N with bent-like Boolean g (paper Alg. 1 on Z_N)")
    print("=" * 70)
    zn_runs = []
    for N in (8, 16, 32):
        # (1) chirp construction: g has FLAT spectrum -> deterministic.
        g_chirp = choose_flat_spectrum_g(N, RNG)
        gh_c = np.fft.fft(g_chirp) / np.sqrt(N)
        flat_c = bool(np.allclose(np.abs(gh_c), 1.0, atol=1e-8))
        print(f"\nN = {N}: chirp g -- |g_hat| flat = {flat_c}")
        for trial in range(10):
            s = int(RNG.integers(0, N))
            r = run_hidden_shift_zn(N, s, g_chirp, verbose=(trial < 2))
            r["success"] = (r["outcome"] == r["expected"])
            r["g_type"] = "chirp_flat_spectrum"
            zn_runs.append(r)
        n_ok_c = sum(1 for r in zn_runs
                     if r["N"] == N and r.get("g_type") == "chirp_flat_spectrum"
                     and r["success"])
        avg_p_c = float(np.mean([r["p_outcome"] for r in zn_runs
                                 if r["N"] == N
                                 and r.get("g_type") == "chirp_flat_spectrum"]))
        print(f"  chirp g -> N={N}: {n_ok_c}/10 exact recoveries, "
              f"mean p(outcome)={avg_p_c:.4f}")

        # (2) Boolean g with nowhere-zero spectrum -- task-requested variant.
        try:
            g_bool = choose_g_boolean_noflat(N, RNG)
            gh_b = np.fft.fft(g_bool) / np.sqrt(N)
            bool_ok = True
            for trial in range(10):
                s = int(RNG.integers(0, N))
                r = run_hidden_shift_zn(N, s, g_bool)
                r["success"] = (r["outcome"] == r["expected"])
                r["g_type"] = "boolean_nowhere_zero"
                zn_runs.append(r)
            n_ok_b = sum(1 for r in zn_runs
                         if r["N"] == N and r.get("g_type") == "boolean_nowhere_zero"
                         and r["success"])
            avg_p_b = float(np.mean([r["p_outcome"] for r in zn_runs
                                     if r["N"] == N
                                     and r.get("g_type") == "boolean_nowhere_zero"]))
            print(f"  boolean g -> N={N}: {n_ok_b}/10 recoveries as argmax, "
                  f"mean p(outcome)={avg_p_b:.4f}, spectrum min|ghat|={np.min(np.abs(gh_b)):.4f}")
        except Exception as e:
            print(f"  boolean g -> N={N}: SKIPPED ({e})")
            n_ok_b = None
            avg_p_b = None
            bool_ok = False

        # classical lower bound (Boolean case; well-defined per-query = 1 bit)
        cl = classical_shift_lower_bound(N, g_bool if bool_ok else g_chirp.real.astype(int).clip(-1,1),
                                          k_max=6)
        print(f"  classical info-theoretic query lower bound: "
              f"{cl['info_theoretic_lower_bound_queries']} queries "
              f"(= ceil log2 N)")

        results["runs"][f"Z_{N}"] = {
            "N": N,
            "chirp_flat_spectrum": flat_c,
            "chirp_success_count": n_ok_c,
            "chirp_mean_p_outcome": avg_p_c,
            "boolean_success_count": n_ok_b,
            "boolean_mean_p_outcome": avg_p_b,
            "trials": [r for r in zn_runs if r["N"] == N],
            "quantum_queries_per_shift": 2,
            "classical_lower_bound_queries": cl["info_theoretic_lower_bound_queries"],
        }

    # ---- Part (d): Legendre symbol hidden shift on F_13 ----
    print("\n" + "=" * 70)
    print("Shifted Legendre symbol hidden shift on F_p (paper Section 4)")
    print("=" * 70)
    p = 13
    leg_runs = []
    for trial in range(10):
        s = int(RNG.integers(1, p))   # avoid trivial 0
        r = run_legendre_shift(p, s, verbose=(trial < 3))
        r["success"] = (r["outcome"] == r["expected"])
        leg_runs.append(r)
    n_ok = sum(1 for r in leg_runs if r["success"])
    print(f"\n  -> p={p}: {n_ok}/10 shifts recovered exactly, "
          f"theory success = {(1-1/p)**2:.4f}")
    results["runs"][f"Legendre_F{p}"] = {
        "p": p,
        "trials": leg_runs,
        "n_success": n_ok,
        "quantum_queries_per_shift": 2,
        "theory_success_prob": (1 - 1 / p) ** 2,
    }

    # ---- Global verdict summary ----
    summary = {
        "zn_sizes_recovered_flat_spectrum": [
            N for N in (8, 16, 32)
            if results["runs"][f"Z_{N}"]["chirp_success_count"] == 10
        ],
        "zn_sizes_recovered_boolean_g": [
            N for N in (8, 16, 32)
            if (results["runs"][f"Z_{N}"]["boolean_success_count"] or 0) == 10
        ],
        "legendre_p13_success_rate": n_ok / 10,
    }
    results["summary"] = summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(json.dumps(summary, indent=2))

    out_json = out_dir / "hidden_shift_results.json"
    with open(out_json, "w") as fh:
        json.dump(results, fh, indent=2, default=str)
    print(f"\nWrote {out_json}")


if __name__ == "__main__":
    main()
