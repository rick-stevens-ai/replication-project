#!/usr/bin/env python3
"""
Independent replication of Linden & de Wolf, arXiv:2109.10215v3
"Average-Case Verification of the Quantum Fourier Transform Enables Worst-Case
Phase Estimation" (Quantum 2022).

Replicated claims:
  C1 (Theorem 1) : Average infidelity eta = Ek[1 - <k| C(|k_hat>) |k>] can be
                   estimated up to +/- epsilon w.p. >= 1-delta using
                   r = O(log(1/delta)/epsilon^2) single-shot experiments,
                   each preparing an n-qubit product state F_N|k>, running C,
                   and measuring in the computational basis.
  C2 (Theorem 3) : n-bit theta case. With uniformly random lambda-shift
                   applied before F_N^{-1}, the probability of NOT recovering
                   theta after subtracting lambda is <= eta.
                   Hence tolerable eta is any eta < 1/2 (paper says "almost 1/2").
  C3 (Theorem 5) : General theta case. For K=2, tolerable eta <= 0.041
                   keeps the bad-outcome probability < 0.5. We evaluate
                   the exact upper bound 2|S|*eta + 2*(1 - |S|*eta)*|alpha_rho|^2.
  C4 (Section 4.1): Shor-style period finding through a noisy inverse QFT
                   still succeeds with probability >= (1 - eta) * 8/pi^2
                   at yielding a good j (i.e., |j/N - c/r| < 1/N) after the
                   worst-case-to-average-case reduction.

All numerics are real: statevector simulation with numpy (no fabrication).
Free endpoints only (no LLM calls needed for the numerics; the LLM judge is
optional and only used at the end for a verdict).
"""
from __future__ import annotations

import json
import math
import os
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, List, Tuple

import numpy as np

RNG = np.random.default_rng(20260705)

HERE = Path(__file__).resolve().parent
EVIDENCE = HERE
EVIDENCE.mkdir(parents=True, exist_ok=True)

# ------------------------------------------------------------------ QFT core

def qft_matrix(n: int) -> np.ndarray:
    """Exact 2^n x 2^n QFT unitary using the paper's convention
       |k> -> (1/sqrt(N)) sum_j omega_N^{jk} |j>, omega_N = e^{2 pi i / N}."""
    N = 1 << n
    j = np.arange(N)
    k = j.reshape(-1, 1)
    W = np.exp(2j * np.pi * (j * k) / N) / np.sqrt(N)
    return W

def iqft_matrix(n: int) -> np.ndarray:
    return qft_matrix(n).conj().T

def basis_ket(N: int, k: int) -> np.ndarray:
    v = np.zeros(N, dtype=complex)
    v[k] = 1.0
    return v

def fourier_basis_ket(n: int, k: int) -> np.ndarray:
    """|k_hat> = F_N |k>  (a product state of n qubits)."""
    N = 1 << n
    j = np.arange(N)
    return np.exp(2j * np.pi * j * k / N) / np.sqrt(N)

# ---------------------------------------------------------- Noisy channels C

def channel_perfect_iqft(n: int) -> Callable[[np.ndarray], np.ndarray]:
    U = iqft_matrix(n)
    def C(psi):
        return U @ psi
    return C

def channel_iqft_with_dephasing(n: int, p: float, rng: np.random.Generator):
    """Coherent-error channel that DOES change computational-basis measurement
       probabilities: after the ideal iQFT, apply a small unitary error
       consisting of an angle-p random RY rotation on each qubit (in the
       computational basis). This is a physically reasonable model of an
       imperfect implementation (small over/under rotation) and produces a
       real, tunable eta.

       We build the per-call 1-qubit RY on the fly and tensor into an N x N
       diagonal-plus-off-diagonal matrix on the state vector via einsum.
    """
    U = iqft_matrix(n)
    N = 1 << n
    def C(psi):
        state = (U @ psi).reshape([2] * n)
        # Apply single-qubit RY with random angle in [-p*pi, p*pi] on each qubit
        for q in range(n):
            theta = rng.uniform(-p * math.pi, p * math.pi)
            c = math.cos(theta / 2.0); s = math.sin(theta / 2.0)
            RY = np.array([[c, -s], [s, c]], dtype=complex)
            state = np.moveaxis(state, q, 0)
            shape = state.shape
            state = state.reshape(2, -1)
            state = RY @ state
            state = state.reshape(shape)
            state = np.moveaxis(state, 0, q)
        return state.reshape(N)
    return C

def channel_iqft_bitflip_before(n: int, p: float, rng: np.random.Generator):
    """Flip each input qubit independently with probability p, then apply
       perfect iQFT. Produces a noisy channel whose average infidelity we
       can tune by p."""
    U = iqft_matrix(n)
    N = 1 << n
    idx = np.arange(N)
    def C(psi):
        flip_mask = 0
        r = rng.random(n)
        for q in range(n):
            if r[q] < p:
                flip_mask |= (1 << q)
        permuted = psi[idx ^ flip_mask]
        return U @ permuted
    return C

def channel_iqft_random_output_error(n: int, p: float, rng: np.random.Generator):
    """After ideal iQFT, with probability p, replace the output state with
       a uniformly random computational basis state (a pure "worst case"
       depolarising-like corruption). Otherwise output ideal state."""
    U = iqft_matrix(n)
    N = 1 << n
    def C(psi):
        out = U @ psi
        if rng.random() < p:
            k = int(rng.integers(0, N))
            v = np.zeros(N, dtype=complex)
            v[k] = 1.0
            return v
        return out
    return C

# ------------------------------------------------------ Measurement helpers

def sample_computational(psi: np.ndarray, rng: np.random.Generator) -> int:
    probs = np.abs(psi) ** 2
    # renormalise to guard against tiny numerical drift
    probs = probs / probs.sum()
    return int(rng.choice(len(probs), p=probs))

def true_avg_infidelity(C: Callable[[np.ndarray], np.ndarray],
                        n: int,
                        n_trials_per_k: int = 200,
                        rng: np.random.Generator | None = None) -> float:
    """Estimate eta = E_k[1 - <k|C(|k_hat>)|k>] EXACTLY by evaluating for
       every Fourier basis state |k_hat>, averaging <k|C(|k_hat>)|k>
       over many stochastic runs of C. Returns 1 - avg fidelity.

       This is the ground-truth eta used as a check on the Theorem-1 estimator.
    """
    if rng is None:
        rng = np.random.default_rng(1)
    N = 1 << n
    total = 0.0
    for k in range(N):
        khat = fourier_basis_ket(n, k)
        acc = 0.0
        for _ in range(n_trials_per_k):
            out = C(khat)
            acc += float(np.abs(out[k]) ** 2)
        total += acc / n_trials_per_k
    avg_fidelity = total / N
    return 1.0 - avg_fidelity


# ================================================================= CLAIM 1

def theorem1_estimator(C: Callable[[np.ndarray], np.ndarray],
                       n: int,
                       r: int,
                       rng: np.random.Generator) -> float:
    """Implement Theorem 1 estimator exactly as stated:
       For i=1..r:
         choose k uniformly at random from {0,1}^n,
         prepare |k_hat> = F_N|k>,
         apply C, measure in comp basis obtaining k',
         emit bit  b_i = 1{ k' != k }.
       Return  hat_eta = (1/r) * sum_i b_i.
    """
    N = 1 << n
    bad = 0
    for _ in range(r):
        k = int(rng.integers(0, N))
        khat = fourier_basis_ket(n, k)
        out = C(khat)
        kp = sample_computational(out, rng)
        if kp != k:
            bad += 1
    return bad / r

def run_claim_C1() -> Dict:
    """Claim 1: The Theorem-1 estimator converges to eta at rate O(1/sqrt(r)),
       with additive error <= epsilon w.p. >= 1-delta after
       r = O(log(1/delta)/epsilon^2) runs. We fix (epsilon, delta) at several
       levels, run the estimator T times, and count the empirical failure
       probability. We compare against the ground-truth eta measured on many
       states.
    """
    results = {"description": "Theorem 1 average-infidelity estimator",
               "channels": []}
    rng = np.random.default_rng(202607051)

    channels = [
        ("perfect-iqft-n3", 3, channel_perfect_iqft(3), True),
        ("ryerr-n3-p0.10", 3, channel_iqft_with_dephasing(3, 0.10, rng), False),
        ("ryerr-n4-p0.15", 4, channel_iqft_with_dephasing(4, 0.15, rng), False),
        ("randomerr-n4-p0.05", 4, channel_iqft_random_output_error(4, 0.05, rng), False),
        ("bitflip-n5-p0.05", 5, channel_iqft_bitflip_before(5, 0.05, rng), False),
    ]
    for name, n, C, is_perfect in channels:
        print(f"  [C1] channel={name} n={n}", flush=True)
        gt_eta = true_avg_infidelity(C, n, n_trials_per_k=150,
                                     rng=np.random.default_rng(999))
        print(f"      gt_eta={gt_eta:.4f}", flush=True)
        # For several epsilons compute the number of runs prescribed and
        # measure empirical failure probability of |hat_eta - gt_eta| > epsilon
        eps_delta_grid = [
            (0.10, 0.10),
            (0.05, 0.10),
            (0.05, 0.05),
            (0.02, 0.10),
        ]
        rows = []
        for eps, delta in eps_delta_grid:
            # Chernoff with c = 3 (matches the "O" hidden constant); grow r
            # linearly in log(1/delta)/eps^2.
            r = max(1, int(math.ceil(3.0 * math.log(1.0 / delta) / (eps * eps))))
            T = 60
            print(f"      eps={eps} delta={delta} r={r} T={T}", flush=True)
            errs = []
            fails = 0
            for _ in range(T):
                hat = theorem1_estimator(C, n, r, rng)
                errs.append(hat - gt_eta)
                if abs(hat - gt_eta) > eps:
                    fails += 1
            rows.append({
                "epsilon": eps,
                "delta": delta,
                "r_used": r,
                "empirical_fail_rate": fails / T,
                "max_abs_err": float(np.max(np.abs(errs))),
                "rms_err": float(np.sqrt(np.mean(np.square(errs)))),
                "pass_delta": (fails / T) <= delta + 0.05,
            })
        results["channels"].append({
            "name": name, "n": n,
            "ground_truth_eta": gt_eta,
            "is_perfect": is_perfect,
            "rows": rows,
        })
    return results


# ================================================================= CLAIM 2

def prepare_lambda_shifted_state(n: int, theta: float, lam: float) -> np.ndarray:
    """Build the pre-C state (1/sqrt(N)) sum_j e^{2 pi i j (theta+lam)} |j>."""
    N = 1 << n
    j = np.arange(N)
    return np.exp(2j * np.pi * j * (theta + lam)) / np.sqrt(N)

def run_claim_C2() -> Dict:
    """Claim 2 (Theorem 3): For n-bit theta, worst-case-to-average-case reduction
       gives Pr[error] <= eta after lambda averaging.

       We fix a 'bad' theta, apply many random lambda shifts, run C,
       subtract lambda from measured outcome, count failures.
       Verify empirical failure prob <= gt_eta (up to Monte-Carlo noise).
    """
    rng = np.random.default_rng(202607052)
    results = {"description":
               "Theorem 3 worst-case-to-average-case reduction, n-bit theta",
               "channels": []}
    channels = [
        ("ryerr-n3-p0.20", 3, channel_iqft_with_dephasing(3, 0.20, rng)),
        ("ryerr-n4-p0.20", 4, channel_iqft_with_dephasing(4, 0.20, rng)),
        ("randomerr-n4-p0.20", 4, channel_iqft_random_output_error(4, 0.20, rng)),
        ("randomerr-n5-p0.30", 5, channel_iqft_random_output_error(5, 0.30, rng)),
    ]
    for name, n, C in channels:
        print(f"  [C2] channel={name} n={n}", flush=True)
        N = 1 << n
        gt_eta = true_avg_infidelity(C, n, n_trials_per_k=200,
                                     rng=np.random.default_rng(4001))
        print(f"      gt_eta={gt_eta:.4f}", flush=True)
        # Pick the WORST-CASE theta_star = argmax_k eta_k. Compute eta_k first.
        eta_k = []
        for k in range(N):
            khat = fourier_basis_ket(n, k)
            acc = 0.0
            for _ in range(200):
                out = C(khat)
                acc += float(np.abs(out[k]) ** 2)
            eta_k.append(1.0 - acc / 200)
        eta_k = np.array(eta_k)
        k_star = int(np.argmax(eta_k))
        theta = k_star / N  # exactly-n-bit theta

        # (A) No lambda shift (basic PE): failure probability is eta_{k_star}
        naive_trials = 500
        naive_fail = 0
        for _ in range(naive_trials):
            khat = fourier_basis_ket(n, k_star)
            out = C(khat)
            kp = sample_computational(out, rng)
            if kp != k_star:
                naive_fail += 1
        naive_fail_rate = naive_fail / naive_trials

        # (B) With uniform random lambda in {0, 1/N, ..., (N-1)/N}: failure
        # probability should drop to about gt_eta.
        shift_trials = 2000
        shift_fail = 0
        for _ in range(shift_trials):
            lam_int = int(rng.integers(0, N))
            lam = lam_int / N
            psi_in = prepare_lambda_shifted_state(n, theta, lam)
            out = C(psi_in)
            m = sample_computational(out, rng)
            # subtract lambda mod N: recovered k' = (m - lam_int) mod N
            recovered = (m - lam_int) % N
            if recovered != k_star:
                shift_fail += 1
        shift_fail_rate = shift_fail / shift_trials

        results["channels"].append({
            "name": name, "n": n,
            "ground_truth_eta": gt_eta,
            "worst_k": k_star,
            "worst_eta_k": float(eta_k[k_star]),
            "best_eta_k": float(eta_k.min()),
            "naive_fail_rate": naive_fail_rate,
            "shifted_fail_rate": shift_fail_rate,
            "theorem3_bound": gt_eta,
            "pass_theorem3": shift_fail_rate <= gt_eta + 0.05,
            "reduction_ratio": (shift_fail_rate + 1e-9) / (naive_fail_rate + 1e-9),
        })
    return results


# ================================================================= CLAIM 3

def numerical_alpha_rho_sq(n: int, K: int, samples: int = 2000,
                           rng: np.random.Generator | None = None) -> float:
    """Numerically estimate max_{theta in [0,1)} |alpha_rho|^2 where
       |alpha_rho|^2 = 1 - sum_{k in S(theta,K)} |alpha_k|^2
       and |alpha_k|^2 comes from the F_N-decomposition of
       (1/sqrt N) sum_j e^{2 pi i j theta} |j>.

       For each theta:  a_k = <k_hat| psi> = (1/N) sum_j e^{2 pi i j (theta - k/N)}
       This is a Dirichlet kernel; |a_k|^2 = (1/N^2) * sin(pi(theta-k/N) N)^2 /
       sin(pi(theta-k/N))^2  (with the delta = 0 case handled).
    """
    if rng is None:
        rng = np.random.default_rng(3)
    N = 1 << n
    thetas = rng.uniform(0, 1, size=samples)
    worst = 0.0
    for theta in thetas:
        kstar = int(np.floor(2**n * theta))
        S = set((kstar + d) % N for d in range(-K + 1, K + 1))
        prob_in_S = 0.0
        for k in S:
            delta = theta - k / N
            # handle mod 1 wraparound
            delta -= round(delta)
            if abs(delta) < 1e-12:
                p = 1.0
            else:
                num = math.sin(math.pi * delta * N) ** 2
                den = math.sin(math.pi * delta) ** 2
                p = num / (den * N * N)
            prob_in_S += p
        rho_sq = max(0.0, 1.0 - prob_in_S)
        if rho_sq > worst:
            worst = rho_sq
    return worst

def theorem5_bound(K: int, eta: float, alpha_rho_sq: float) -> float:
    S = 2 * K
    return 2 * S * eta + 2 * (1 - S * eta) * alpha_rho_sq

def run_claim_C3() -> Dict:
    """Claim 3: Theorem 5 evaluated numerically. Verify the paper's stated
       tolerable eta values.
         Paper: N=2^10, K=4 -> |alpha_rho|^2 ~ 0.05, eta <= 0.026
                              K=3 -> |alpha_rho|^2 ~ 0.067, eta <= 0.032
                              K=2 -> |alpha_rho|^2 ~ 0.099, eta <= 0.041
    """
    results = {"description":
               "Theorem 5 bound; numerical |alpha_rho|^2 for N=2^10",
               "rows": []}
    rng = np.random.default_rng(7)
    for K in [2, 3, 4]:
        arho2 = numerical_alpha_rho_sq(n=10, K=K, samples=4000, rng=rng)
        # Solve 4Kη + 2(1 - 2Kη)*arho2 < 0.5 for max eta
        # => 4Kη - 4Kη*arho2 + 2arho2 < 0.5
        # => 4Kη(1 - arho2) < 0.5 - 2 arho2
        # => eta < (0.5 - 2 arho2) / (4K(1 - arho2))
        num = 0.5 - 2 * arho2
        den = 4 * K * (1 - arho2)
        max_eta = num / den if den > 0 else 0.0
        paper_max_eta = {2: 0.041, 3: 0.032, 4: 0.026}[K]
        results["rows"].append({
            "K": K,
            "numerical_alpha_rho_sq_worst_theta_estimate": arho2,
            "paper_alpha_rho_sq_approx": {2: 0.099, 3: 0.067, 4: 0.05}[K],
            "our_max_tolerable_eta": max_eta,
            "paper_max_tolerable_eta": paper_max_eta,
            "abs_diff": abs(max_eta - paper_max_eta),
            "match": abs(max_eta - paper_max_eta) < 0.010,
        })
    # Also demo the bound for a range of eta at K=2 and K=4
    demo = {}
    for K in [2, 4]:
        row = next(r for r in results["rows"] if r["K"] == K)
        arho2 = row["paper_alpha_rho_sq_approx"]
        curve = []
        for eta in [0.005, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.08]:
            curve.append({"eta": eta, "bound": theorem5_bound(K, eta, arho2)})
        demo[f"K={K}"] = curve
    results["curves"] = demo
    return results


# ================================================================= CLAIM 4

def periodic_state(n: int, r: int, s: int) -> np.ndarray:
    N = 1 << n
    v = np.zeros(N, dtype=complex)
    idxs = [s + z * r for z in range(0, (N - s + r - 1) // r) if s + z * r < N]
    for i in idxs:
        v[i] = 1.0
    v = v / np.linalg.norm(v)
    return v

def run_claim_C4() -> Dict:
    """Claim 4 (Section 4.1): Shor-like period finding through noisy iQFT.

       For phase-estimation-based period finding of eigenvalue e^{2pi i j/N}
       of U|x> = |x+1 mod N>, on a periodic input |pi_s>, applying the ideal
       inverse QFT to |pi_s> yields FN|pi_s>  (paper reads this in reverse:
       phase estimation with U on |pi_s> outputs 'nearest cN/r' with prob >= 8/pi^2).

       Testing shortcut: we simulate the paper's PE procedure by *directly*
       applying the noisy channel C to  FN|pi_s>  (this is exactly the state
       that the ideal PE circuit produces before iQFT when U is the +1 mod N
       operator and the initial second register is |pi_s>). Then we measure.

       Good outcome := |j/N - c/r| < 1/N for some integer c in {0,...,r-1}.
       Paper's guarantee: Pr[good] >= (1 - eta) * 8/pi^2  (n-bit theta case,
       lambda shift applied).

       Since |pi_s> yields eigenphases that are exactly n-bit (j/N with j in
       {0,...,N-1}), we CAN use Theorem 3, so we apply the lambda shift here.
    """
    rng = np.random.default_rng(202607053)
    results = {"description":
               "Section 4.1: period finding via noisy inverse QFT",
               "runs": []}
    F = qft_matrix  # forward QFT

    configs = [
        {"n": 5, "r": 5, "channel": ("ryerr", 0.10)},
        {"n": 5, "r": 6, "channel": ("ryerr", 0.10)},
        {"n": 6, "r": 5, "channel": ("ryerr", 0.08)},
        {"n": 6, "r": 7, "channel": ("randomerr", 0.05)},
        {"n": 5, "r": 5, "channel": ("randomerr", 0.10)},
    ]
    
    for cfg in configs:
        n = cfg["n"]; r_period = cfg["r"]
        N = 1 << n
        ch_type, p = cfg["channel"]
        if ch_type == "ryerr":
            C = channel_iqft_with_dephasing(n, p, rng)
        else:
            C = channel_iqft_random_output_error(n, p, rng)
        gt_eta = true_avg_infidelity(C, n, n_trials_per_k=120,
                                     rng=np.random.default_rng(9001))
        print(f"      gt_eta={gt_eta:.4f}", flush=True)

        # Phase estimation on |pi_s> with U|x>=|x+1 mod N>:
        #   |pi_s> = sum_j alpha_j F_N^{-1}|j>   with alpha_j = <j|F_N|pi_s>.
        # The n-qubit first register (traced over the second register), just
        # before applying inverse QFT, is the MIXTURE
        #   rho = sum_j |alpha_j|^2  F_N|j><j|F_N^dagger .
        # So the correct Monte-Carlo per PE trial is:
        #    1) sample eigenphase index j ~ |alpha_j|^2
        #    2) prepare |j_hat> = F_N|j>
        #    3) apply C  (with optional lambda-shift phase before C)
        #    4) measure
        Fmat = F(n)
        pi_s = periodic_state(n, r_period, 0)
        alpha = Fmat @ pi_s          # coefficients in F_N^{-1}|j> basis
        p_alpha = np.abs(alpha) ** 2
        p_alpha = p_alpha / p_alpha.sum()
        # Under ideal PE (C = F_N^{-1}) the measurement outcome is j itself,
        # so the ideal PE output distribution equals p_alpha.  With noisy C
        # we sample j ~ p_alpha, prepare F_N|j>, apply C, measure.

        print(f"  [C4] n={n} r={r_period} ch={cfg['channel']}", flush=True)
        # Paper's 'good' criterion (Section 4.1): j is floor(cN/r) or
        # ceil(cN/r) for some integer c in {0,...,r-1}. This corresponds to
        # continued-fraction expansion recovering c/r from j/N.
        good_js = set()
        for c in range(r_period):
            good_js.add(int(math.floor(c * N / r_period)) % N)
            good_js.add(int(math.ceil (c * N / r_period)) % N)
        # Ideal PE success probability (with perfect iQFT)
        ideal_good = float(sum(p_alpha[j] for j in good_js))

        trials = 1500
        good_naive = 0
        good_shifted = 0
        for _ in range(trials):
            # Sample eigenphase-index j according to |alpha_j|^2 (this is what
            # the 2nd register / mixture would deliver)
            j_true = int(rng.choice(N, p=p_alpha))
            khat = fourier_basis_ket(n, j_true)
            # Naive: no lambda shift
            out = C(khat)
            j = sample_computational(out, rng)
            if j in good_js:
                good_naive += 1

            # Shifted: apply lambda shift on the eigenphase register.
            # The lambda-shift in the paper multiplies |k> by e^{2 pi i k lam_int / N}
            # BEFORE C.  Since our input F_N|j_true> is |j_true_hat>, the
            # equivalent phase-shifted input represents Fourier basis state
            # |(j_true + lam_int) mod N \hat>.
            lam_int = int(rng.integers(0, N))
            j_arr = np.arange(N)
            shift_phase = np.exp(2j * np.pi * j_arr * lam_int / N)
            out2 = C(shift_phase * khat)
            m = sample_computational(out2, rng)
            j2 = (m - lam_int) % N
            if j2 in good_js:
                good_shifted += 1

        # Paper's guarantee: with lambda-shift & noisy C,
        #   Pr[good j] >= (1 - eta) * (ideal_good_prob)
        # where ideal_good_prob is either the algorithmic 8/pi^2 lower bound
        # or the actual ideal Pr[good j] for this (n, r_period).
        paper_bound_ideal   = (1 - gt_eta) * ideal_good
        paper_bound_8pi2    = (1 - gt_eta) * 8 / (math.pi ** 2)
        results["runs"].append({
            "n": n, "r_period": r_period, "channel": cfg["channel"],
            "ground_truth_eta": gt_eta,
            "ideal_pe_good_prob": ideal_good,
            "good_naive_rate": good_naive / trials,
            "good_shifted_rate": good_shifted / trials,
            "paper_lower_bound_shifted_ideal": paper_bound_ideal,
            "paper_lower_bound_8pi2_shifted": paper_bound_8pi2,
            "pass_paper_bound_vs_ideal": (good_shifted / trials) >= paper_bound_ideal - 0.03,
            "pass_paper_bound_vs_8pi2": (good_shifted / trials) >= paper_bound_8pi2 - 0.03,
        })
    return results


# =================================================================== main

def main():
    t0 = time.time()
    all_results = {"paper": "arXiv:2109.10215v3",
                   "title": "Average-Case Verification of the QFT Enables "
                            "Worst-Case Phase Estimation",
                   "authors": ["Noah Linden", "Ronald de Wolf"],
                   "seed": 20260705,
                   "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ",
                                              time.gmtime())}
    print("Running C1 (Theorem 1 estimator) ...", flush=True)
    all_results["C1_theorem1"] = run_claim_C1()
    print("Running C2 (Theorem 3 reduction) ...", flush=True)
    all_results["C2_theorem3"] = run_claim_C2()
    print("Running C3 (Theorem 5 bound) ...", flush=True)
    all_results["C3_theorem5"] = run_claim_C3()
    print("Running C4 (period finding) ...", flush=True)
    all_results["C4_period_finding"] = run_claim_C4()
    all_results["elapsed_sec"] = round(time.time() - t0, 2)

    out = EVIDENCE / "results.json"
    with open(out, "w") as fh:
        json.dump(all_results, fh, indent=2, default=float)
    print(f"Wrote {out} in {all_results['elapsed_sec']} s")

    return all_results

if __name__ == "__main__":
    main()
